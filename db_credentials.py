import boto3
import json
from botocore.exceptions import ClientError
import os
import mysql.connector


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
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret_string = get_secret_value_response['SecretString']
    return json.loads(secret_string)


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