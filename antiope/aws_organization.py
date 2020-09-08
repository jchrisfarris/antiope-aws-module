
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import json
import os
import logging

from .vpc import *
from .config import *
from .aws_account import *

import logging
logger = logging.getLogger('antiope.AWSOrganizationMaster')


class AWSOrganizationMaster(AWSAccount):
    """Class to represent an AWS Organization Master Account"""
    def __init__(self, account_id, config=None):
        """ Create a new object representing the AWS orgs master account specified by account_id """
        # Execute any parent class init()
        super(AWSOrganizationMaster, self).__init__(account_id, config=None)
        org_client = self.get_client('organizations')
        describe_response = org_client.describe_organization()
        if describe_response['Organization']['MasterAccountId'] != account_id:
            raise NotAnAWSOrganizationMaster

        self.org_id = describe_response['Organization']['Id']
        self.organization = describe_response['Organization']


    def get_delegated_admin_status(self):
        """
        Call this function to get the list of service principals that have delegated access configured.
        This method will populate a instance attribute called 'org_enabled_service_principals'
        """
        org_client = self.get_client('organizations')

        enabled_response = org_client.list_aws_service_access_for_organization()

        self.org_enabled_service_principals = []
        for sp in enabled_response['EnabledServicePrincipals']:
            self.org_enabled_service_principals.append(sp['ServicePrincipal'])


    def get_delegated_admin_account_for_service(self, service):
        """
        Returns an AWSAccount object for the account that is the delegated admin for the specified service
        Returns None if the service is invalid or not configured in this organization
        """
        try:
            org_client = self.get_client('organizations')

            if not hasattr(self, "org_enabled_service_principals"):
                self.get_delegated_admin_status()

            if "amazonaws.com" not in service:
                service += ".amazonaws.com"

            if service not in self.org_enabled_service_principals:
                logger.error(f"Service {service} is not enabled for this organization.")
                return(None)

            admins_response = org_client.list_delegated_administrators(ServicePrincipal=service)
            if len(admins_response['DelegatedAdministrators']) == 0:
                return(None)
            elif len(admins_response['DelegatedAdministrators']) > 1:
                logger.error(f"More than one DelegatedAdministrators returned for {service}")
                return(None)
            else:
                account = AWSAccount(admins_response['DelegatedAdministrators'][0]['Id'], self.config)
                return(account)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConstraintViolationException':
                logger.error(f"Error getting delegated admin for {service} from {self.account_id}: {e}")
                return(None)
            else:
                raise

class NotAnAWSOrganizationMaster(Exception):
    '''Exception thrown when an account is not an Org Master account'''
