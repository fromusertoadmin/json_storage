import argparse
import requests
import os

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', help = 'url to post files', required = True)
    parser.add_argument("-mode", help = "display a square of given numbers", default = 'upload')
    parser.add_argument('-files', help = 'file to upload', nargs = '+', required = True)
    args = parser.parse_args()

    for file in args.files:
        print (file)
        if not os.path.isfile(file):
            raise OSError ('File path = {} not found'.format(file))
    function_upload = requests.post
    if args.mode == 'update':
        function_upload = requests.put
    files_dict = {os.path.basename(f):open(f,'rb') for f in args.files}
    print (args.url)
    response = function_upload (args.url, files = files_dict)
    print(response.text)

