import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{path}')

import paas.openapi_client

def create_sdk(token: str):
    config = paas.openapi_client.Configuration(
        host = "https://api.iran.liara.ir"
    )
    config.api_key['jwt'] = f'Bearer {token}'
    
    return paas.openapi_client.ApiClient(config)