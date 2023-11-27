import boto3
import json
from botocore.exceptions import ClientError
import os
import mysql.connector
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig


def get_secret():

    secret_name = os.environ.get('AWS_DB_SECRET_NAME')
    region_name = os.environ.get('AWS_REGION')

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Create a cache
        cache = SecretCache(SecretCacheConfig(),client)

        # Get secret string from the cache
        get_secret_value_response = cache.get_secret_string(secret_name)

    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        secret = get_secret_value_response
        return json.loads(secret)


def get_db_credentials(database: str):
    secret_data = get_secret()

    return {
        'user': secret_data["username"],
        'password': secret_data["password"],
        'host': os.environ.get('AWS_DB_HOST'),
        'port': os.environ.get('AWS_DB_PORT'),
        'database': database
    }


def get_db_connection(db_config):
    conn = mysql.connector.connect(**db_config)
    return conn





if __name__ == '__main__':
    get_secret() 