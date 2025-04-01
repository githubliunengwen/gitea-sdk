import requests
from typing import Optional, Dict, Union, Any

session = requests.Session()
session.headers.update({
            "Accept": "application/json",
            "Content-Type": "multipart/form-data",
            'Authorization': 'token 25ad59263c1d35a2b17b1af99b94a577dc76f815',
        })


def post(path: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], list]:
    """Make a POST request to the API.

    Args:
        path: API endpoint path
        params: Query parameters
        json_data: JSON data
        files: File data
    Returns:
        Response data
    """
    return session.request("POST", path, params=params, json=json_data, files=files)

url = "https://gitea.ailoveworld.cn/api/v1/repos/issues_api_test/issues_api_test/issues/1/assets"

payload={}
files=[
   ('attachment',('C:\\Users\\user\\Desktop\\全员AI.png',open('C:\\Users\\user\\Desktop\\全员AI.png','rb'),'image/png'))
]


response = session.post(url, files=files, data=payload)

print(response.json())