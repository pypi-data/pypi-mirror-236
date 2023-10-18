import logging
import os
import sys

from prefect.blocks.system import Secret

DEFAULT_REGION_NAME = 'eu-west-1'

logging.debug(f"Invoked by process: {sys.argv[0]}")

env_type = os.environ.get('IRON_ENV')


def _get_local_env_variables():
    region = os.environ.get("REGION", DEFAULT_REGION_NAME)
    if not region:
        raise Exception("Environment variable \'region_name\' missing! Please add region name for s3 client!")

    access_key = os.environ.get("ACCESS_KEY")
    if not access_key:
        raise Exception("Environment variable \'ACCESS_KEY\' missing! Please add access key for s3 client!")

    secret_access_key = os.environ.get("SECRET_ACCESS_KEY")
    if not secret_access_key:
        raise Exception("Environment variable \'secret_access_key\' missing! Please add access key for s3 client!")
    return region, access_key, secret_access_key


def _prefect_access_variables():
    try:
        region_name = DEFAULT_REGION_NAME
        return region_name, Secret.load("aws-access-key").get(), Secret.load("aws-secret-key").get()
    except:
        print("An exception occurred while accessing Prefect Secrets. validate login and credentials")
        raise Exception("En exception occurred while accessing Prefect Secrets. validate login and credential")


def s3_access_data():
    # prefect env doesn't have "iron_env"
    if env_type is None:
        return _prefect_access_variables()
    elif env_type == 'local':
        return _get_local_env_variables()
    elif env_type == 'staging':
        return None, None, None
    else:
        raise Exception("Unknown environment.")
