import os
import json
import subprocess

import boto3


def handler(event, context):
    s3_client = boto3.client('s3')
    output = event['output']
    output_filename = os.path.join('/tmp', os.path.basename(output['key']))

    closed_urls = ['"{}"'.format(url) for url in event['urls']]
    cmd = 'python worker.py -t "{}" -f {} -u {}'.format(event['title'], output_filename, ' '.join(closed_urls))
    res = subprocess.check_output(cmd, shell=True)
    print '*' * 5 + '[EPUBIFY]' + '*' * 5
    print res
    print '*' * 5 + '[/EPUBIFY]' + '*' * 5

    s3_client.upload_file(output_filename, output['bucket'], output['key'])


if __name__ == '__main__':
    handler(json.load(open('example_input.json', 'r')), {})
