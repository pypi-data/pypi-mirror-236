import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{path}')

import openapi_client

__version__ = "1.0.0"

# import apis into sdk package
from openapi_client.api.check_name_servers_api import CheckNameServersApi
from openapi_client.api.dns_record_api import DnsRecordApi
from openapi_client.api.zone_api import ZoneApi

# import ApiClient
from openapi_client.api_response import ApiResponse
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from openapi_client.exceptions import OpenApiException
from openapi_client.exceptions import ApiTypeError
from openapi_client.exceptions import ApiValueError
from openapi_client.exceptions import ApiKeyError
from openapi_client.exceptions import ApiAttributeError
from openapi_client.exceptions import ApiException

# import models into sdk package
from openapi_client.models.all_dns_record_response import AllDnsRecordResponse
from openapi_client.models.create_zone import CreateZone
from openapi_client.models.create_zone_request import CreateZoneRequest
from openapi_client.models.dns_record import DnsRecord
from openapi_client.models.dns_record_id import DnsRecordId
from openapi_client.models.dns_record_response import DnsRecordResponse
from openapi_client.models.submitted import Submitted
from openapi_client.models.zone import Zone
from openapi_client.models.zones import Zones

def create_sdk(token: str):
    config = openapi_client.Configuration(
        host = "https://dns-service.iran.liara.ir"
    )
    config.api_key['jwt'] = f'Bearer {token}'
    
    return openapi_client.ApiClient(config)