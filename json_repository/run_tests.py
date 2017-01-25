import sys
import json

HOME_URL = 'http://127.0.0.1:5000/'
URL_FOR_STORAGE_STAT = 'http://127.0.0.1:5000/storage/stat/'
URL_MASK_FOR_UPLOAD = 'http://127.0.0.1:5000/storage/files/{0}/'

JSON_FILE = 'test_data/json_file.json'
NON_JSON_FILE = 'test_data/non_json_file.txt'

def _generate_unique_file_name():
  import uuid
  result = str(uuid.uuid4())
  return result.replace('-', '_')

def verify_is_home_page_is_running():
  print('Running home_page_test')
  import requests
  response = requests.get(HOME_URL)
  if response.status_code > 200:
    raise Exception('Home Page is not accessible. Check web_server')
  print('Test Passed')

def verify_upload_is_ok():
  print('Running upload test')
  file_name_to_upload = _generate_unique_file_name()
  files_to_upload = {file_name_to_upload: open(JSON_FILE)}
  post_response = requests.post(URL_MASK_FOR_UPLOAD.format(file_name_to_upload))
  if post_response.status_code > 200:
    raise Exception('Upload doesnt work correctly. Status Code={0}'.format(post_response.status_code))
  get_response = requests.get(URL_FOR_STORAGE_STAT)
  parsed_response = json.loads(get_response.text)
  dict_from_response = parsed_response[0]
  if not dict_from_response:
    raise Exception('Dict form Response is empty')
  tag_value = dict_from_response.get(file_name_to_upload)
  if not tag_value:
    raise Exception('Tag={0} not found'.format(file_name_to_upload))
  if tag_value[0] != file_name_to_upload:
    raise Exception('Tag Value is incorrect')

def verify_upload_is_incorrect_due_non_json_format():
  print('Running upload test with invalid json format')
  response_before_post = requests.get(URL_FOR_STORAGE_STAT)
  stat_dict_before_post = json.loads(response_before_post.text)
  files_to_upload = {'non_json_file' : open(NON_JSON_FILE)}
  post_url = URL_MASK_FOR_UPLOAD.format('tag')
  response = requests.post(url=URL_MASK_FOR_UPLOAD.format('tag'), 
                           files=files_to_upload)
  if response.status_code == 200:
    raise Exception('Response should not be 200. Url={0}'.format(post_url))
  response_after_post = requests.get(URL_FOR_STORAGE_STAT)
  stat_dict_after_post = json.loads(response_after_post.text)
  if stat_dict_after_post != stat_dict_before_post:
    raise Exception('Before and after post stat should not be changed. Stat are different')
  print('Test Passed')




if __name__ == '__main__':
  try:
    import requests
  except ImportError:
    print('Install requests to run custom tests')
    sys.exit(1)
  verify_is_home_page_is_running()
  verify_upload_is_incorrect_due_non_json_format()
  verify_upload_is_ok()


