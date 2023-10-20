# restartable_lambda
A base class containing uselful methods to monitor and restart a lambda while keeping its context, storing it on AWS

### Install
```bash
pip install restartable-lambda
```

### Usage
You can turn a class into a restartable lambda by inheriting from RestartableLambda and calling the restart_if_needed method:
```python
from restartable_lambda import RestartableLambda

class MyRestartableClass(RestartableLambda):
  def __init__(self, event, context, files_name_list, s3_bucket, s3_base_path):
    super().__init__(event, context, files_name_list, s3_bucket, s3_base_path)

  def run(self):
    self.restart_if_needed(latest_values_to_save)
```
With this, MyRestartableClass will be able to restart and transfer the event to the next execution. The files_name_list is a list of files that will be saved on S3 and reloaded on restart. The s3_bucket and s3_base_path are the bucket and path where the files will be saved.

### Deploy
If twine is not installed, run:
```bash
pip install twine
```
Then, update setup.py according to your changes, and finally run:
```bash
rm -rf build/ dist/ restartable_lambda.egg-info/ && python setup.py sdist bdist_wheel && twine upload dist/*
```
