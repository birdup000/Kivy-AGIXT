import os

from agixtsdk import AGiXTSDK

base_uri = "http://localhost:7437"
agixt_api_key = "your_agixt_api_key"
ApiClient = AGiXTSDK(base_uri=base_uri, api_key=agixt_api_key)
