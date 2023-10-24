import json
import time
from pprint import pprint

import boto3

from dml.DmlClient import Client
from dml.storage.commands.CommandError import CommandErrorException, CommandErrorCode


def get_object_from_s3(s3, bucket, key):
    return s3.get_object(
        Bucket=bucket,
        Key=key
    )['Body'].read()


def create_key_on_dml(dml, key):
    # create key on the DML if it does not exist
    try:
        dml.create(key)
    except CommandErrorException as err:
        if err.num != CommandErrorCode.KEY_ALREADY_EXISTS.value:
            raise


def main(args):
    s3 = boto3.client('s3')
    dml = Client(args['dmlHostname'], args['dmlPort'])
    dml.connect()

    times = {}

    bucket = args['bucket']

    for key in args['keys']:
        times[key] = {}

        # download object from S3
        start = time.time()
        obj = get_object_from_s3(s3, bucket, key)
        times[key]['s3_download'] = time.time() - start

        create_key_on_dml(dml, key)

        # upload object to the DML
        start = time.time()
        dml.set(key, obj)
        times[key]['dml_upload'] = time.time() - start

    dml.disconnect()

    return times


def lambda_handler(event, _):
    # check whether the request is an HTTP request (via the Amazon Gateway API or Function URL)
    if 'httpMethod' in event:
        # read in the args from the POST object
        post_req_json_input = json.loads(event['body'])
        res = main(post_req_json_input)
        return {
            'statusCode': 200,
            'body': json.dumps(res)
        }
    return main(event)


if __name__ == '__main__':
    with open('s3_to_dml.json') as json_file:
        input_args = json.load(json_file)

    result = main(input_args)

    # write to std out
    pprint(result)
