import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{path}')

import openapi_client

def create_sdk(token: str):
    config = openapi_client.Configuration(
        host = "https://dns-service.iran.liara.ir"
    )
    config.api_key['jwt'] = f'Bearer {token}'
    
    return openapi_client.ApiClient(config)