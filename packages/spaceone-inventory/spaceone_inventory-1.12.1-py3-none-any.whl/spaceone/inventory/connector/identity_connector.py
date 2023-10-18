"""
Deprecated:
  Not used. Integrated with SpaceConnector.
"""

import logging

from google.protobuf.json_format import MessageToDict

from spaceone.core.connector import BaseConnector
from spaceone.core import pygrpc
from spaceone.core.utils import parse_grpc_endpoint
from spaceone.core.error import *


__all__ = ['IdentityConnector']
_LOGGER = logging.getLogger(__name__)


class IdentityConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'endpoint' not in self.config:
            raise ERROR_WRONG_CONFIGURATION(key='endpoint')

        if len(self.config['endpoint']) > 1:
            raise ERROR_WRONG_CONFIGURATION(key='too many endpoint')

        for version, uri in self.config['endpoint'].items():
            e = parse_grpc_endpoint(uri)
            self.client = pygrpc.client(endpoint=e['endpoint'], ssl_enabled=e['ssl_enabled'])

    def get_user(self, user_id, domain_id):
        return MessageToDict(self.client.User.get({'user_id': user_id, 'domain_id': domain_id},
                                                  metadata=self.transaction.get_connection_meta()),
                             preserving_proto_field_name=True)

    def list_users(self, query, domain_id):
        return MessageToDict(self.client.User.list({'query': query, 'domain_id': domain_id},
                                                   metadata=self.transaction.get_connection_meta()),
                             preserving_proto_field_name=True)

    def get_project(self, project_id, domain_id):
        return MessageToDict(self.client.Project.get({'project_id': project_id, 'domain_id': domain_id},
                                                     metadata=self.transaction.get_connection_meta()),
                             preserving_proto_field_name=True)

    def list_projects(self, query, domain_id):
        return MessageToDict(self.client.Project.list({'query': query, 'domain_id': domain_id},
                                                      metadata=self.transaction.get_connection_meta()),
                             preserving_proto_field_name=True)

    def list_domains(self, query):
        return MessageToDict(self.client.Domain.list({'query': query},
                                                   metadata=self.transaction.get_connection_meta()),
                             preserving_proto_field_name=True)
