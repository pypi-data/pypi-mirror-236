import os
import json
import uuid
from retrying import retry
import boto3

class RestartableLambda(object):
  def __init__(self, event, context, files_name_list, s3_bucket, s3_base_path, remaining_time_to_restart=None, max_number_of_execution=None):
    self.event = event
    self.context = context
    self.s3_bucket = s3_bucket
    self.s3_base_path = s3_base_path
    self.remaining_time_to_restart = int(os.getenv('remaining_time_to_restart', remaining_time_to_restart or 300000)) # 5 minutes in ms
    self.max_number_of_execution = int(os.getenv('max_number_of_execution', max_number_of_execution or 3)) # this will give the request max_number_of_execution * 15 minutes to finish
    self.s3 = boto3.resource('s3')
    self.must_restart = False
    self.max_number_of_execution_reached = False

    self.event['restart_count'] = self.event.get('restart_count', 0)
    self.event['saved_files'] = self.event.get('saved_files', {name:None for name in files_name_list})

    self.files = {}
    for name, path in self.event['saved_files'].items():
      self.files[name] = self.retrieve_file(name, path)

  def restart_if_needed(self, new_values={}):
    if self.should_restart(): self.save_before_restart(new_values)

  def restart_lambda_function(self):
    client = boto3.client('lambda', region_name='eu-west-1')

    self.event['restart_count'] += 1

    client.invoke(
      FunctionName='{}:{}'.format(self.context.function_name, self.context.function_version),
      InvocationType='Event',
      Payload=json.dumps(self.event)
    )

    print('Restarted...')

    self.must_restart = True
    raise Exception("Restarted...")

  def should_restart(self):
    can_restart = self.event['restart_count'] + 1 < self.max_number_of_execution
    has_not_enough_remaining_time = self.context.get_remaining_time_in_millis() < self.remaining_time_to_restart

    if not can_restart and has_not_enough_remaining_time:
      self.max_number_of_execution_reached = True
      raise Exception('Should restart but cannot! (max_number_of_execution reached)')

    return can_restart and has_not_enough_remaining_time

  def save_before_restart(self, new_values={}):
    for name, value in self.files.items():
      self.upload_temp_file(new_values.get(name, value), self.event['saved_files'][name])
    self.restart_lambda_function()

  @retry(wait_fixed=5000, stop_max_attempt_number=3)
  def upload_temp_file(self, json_to_upload, s3_path):
    local_path = '/tmp/{}.json'.format(str(uuid.uuid4()))
    with open(local_path, 'w+') as file:
      json.dump(json_to_upload, file)

    boto_object = self.s3.Object(self.s3_bucket, s3_path)
    boto_object.upload_file(local_path, { 'ACL': 'public-read' })

  def retrieve_file(self, name, path):
    if path:
      try:
        boto_object = self.s3.Object(self.s3_bucket, path)
        local_path = '/tmp/{}.json'.format(name)
        boto_object.download_file(local_path)

        with open(local_path, 'r') as file_json:
          return json.load(file_json)
      except Exception as e:
        print(e)
        return None
    else:
      self.event['saved_files'][name] = '{}/{}_{}.json'.format(self.s3_base_path, name, str(uuid.uuid4()))
      return None