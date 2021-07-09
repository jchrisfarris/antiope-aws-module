#!/usr/bin/env python3
# Copyright 2019-2020 Turner Broadcasting Inc. / WarnerMedia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import boto3
from botocore.exceptions import ClientError
import json
import os
import time
import datetime

from antiope import *

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


# Lambda main routine
def main(args, logger):

    antiope_config = AntiopeConfig(config= {
        'account_table_name': args.account_table,
        'vpc_table_name': args.vpc_table,
        'role_name': args.role_name,
        'role_session_name': args.role_session_name
        })

    # Get and then sort the list of accounts by name, case insensitive.
    active_accounts = get_active_accounts(table_name=args.account_table, antiope_config=antiope_config)  # TODO, make this part of the Organizations Class
    active_accounts.sort(key=lambda x: x.account_name.lower())

    for a in active_accounts:
        logger.info(f"{a.account_name} ({a.account_id}) is part of {a.payer_id} with email {a.root_email}")
        vpcs = a.get_vpcs()
        logger.info(f"\tThere are {len(vpcs)} VPCs in {a.account_name}")


def get_active_accounts(table_name=None, antiope_config=None):
    """Returns an array of all active AWS accounts as AWSAccount objects"""
    account_ids = get_account_ids(status="ACTIVE", table_name=table_name)
    output = []
    for a in account_ids:
        output.append(AWSAccount(a, config=antiope_config))
    return(output)


def get_foreign_accounts():
    """Returns an array of all active AWS accounts as AWSAccount objects"""
    foreign_account_ids = get_account_ids(status="FOREIGN")
    trusted_account_ids = get_account_ids(status="TRUSTED")
    output = []
    for a in trusted_account_ids:
        output.append(ForeignAWSAccount(a))
    for a in foreign_account_ids:
        output.append(ForeignAWSAccount(a))
    return(output)


def get_account_ids(status=None, table_name=None):
    """return an array of account_ids from the Accounts table. Optionally, filter by status"""
    dynamodb = boto3.resource('dynamodb')
    if table_name:
        account_table = dynamodb.Table(table_name)
    else:
        account_table = dynamodb.Table(os.environ['ACCOUNT_TABLE'])

    account_list = []
    response = account_table.scan(
        AttributesToGet=['account_id', 'account_status']
    )
    while 'LastEvaluatedKey' in response:
        # Means that dynamoDB didn't return the full set, so ask for more.
        account_list = account_list + response['Items']
        response = account_table.scan(
            AttributesToGet=['account_id', 'account_status'],
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
    account_list = account_list + response['Items']
    output = []
    for a in account_list:
        if status is None:  # Then we get everything
            output.append(a['account_id'])
        elif a['account_status'] == status:  # this is what we asked for
            output.append(a['account_id'])
        # Otherwise, don't bother.
    return(output)


def do_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="print debugging info", action='store_true')
    parser.add_argument("--error", help="print error info only", action='store_true')

    parser.add_argument("--account-table", help="Name of an Antiope Account Table", required=True)
    parser.add_argument("--vpc-table", help="Name of an Antiope Account Table", required=True)
    parser.add_argument("--role-name", help="Name of the cross account role", default="antiope-test-role")
    parser.add_argument("--role-session-name", help="cross account role session name", default="antiope-test-role-session")
    parser.add_argument("--ssm-param", help="Name of an Antiope SSM Parameter", default="antiope-test-role-session")
    args = parser.parse_args()

    return(args)

if __name__ == '__main__':

    args = do_args()

    # Logging idea stolen from: https://docs.python.org/3/howto/logging.html#configuring-logging
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    if args.debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # create formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    try:
        main(args, logger)
    except KeyboardInterrupt:
        exit(1)