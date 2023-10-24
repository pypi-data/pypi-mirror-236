""" Implements Automation Anywhere 360 API to use Credential Vault. """

from typing import Literal
import requests
from RPA.Robocorp.Vault import Secret

class Vault:
    """
    The library wraps Automation Anywhere 360 API, giving robots the ability to manage the values stored in the Credential Vault.

    Args:
            control_room_uri (str): URL of Automation Anywhere A360 Control Room
            username (str): user name with access to the Vault (API)
            password (str): user password
    """

    def __init__(self, control_room_uri: str, username: str, password: str):
        self.endpoints: dict = {
            'control_room': control_room_uri.rstrip('//'),
            'authentication': f'{control_room_uri.rstrip("//")}/v1/authentication',
            'credentials': f'{control_room_uri.rstrip("//")}/v2/credentialvault/credentials'
        }
        self.username: str = username
        self.password: str = password
        self.token = None

    def get_token(self) -> str:
        """
        Returns token generated

        Returns:
            str: token value
        """
        if self.token is None:
            self.__authenticate__()
        return self.token

    def get_credential(self, name: str) -> Secret:
        """
        Fetch credential from the credential vault.

        Args:
            name (str): credential name

        Raises:
            Exception: requests exceptions

        Returns:
            dict: dictionary of all credential's attributes
        """
        try:
            response = self.__get_credentials_list__()
            attributes: dict = {}
            for item in response['list']:
                if item['name'] == name:
                    for attribute in item['attributes']:
                        attributes[attribute['name']] = self.__get_attribute_value__(item['id'], attribute['id'])
                    return Secret(name=name, values=attributes)
            raise Exception(f'Cannot fetch credential {name} from the Credential Vault. Check if the name is correct.')
        except Exception as ex:
            raise Exception(f'Cannot fetch credential {name}.\n\r') from ex

    def __get_credential__(self, name: str) -> dict:
        for item in self.__get_credentials_list__()['list']:
            if item['name'].lower() == name.lower():
                return item
        return {}

    def __list_credentials__(self, output_format: Literal['json', 'string'] = 'json') -> list:
        try:
            response = self.__get_credentials_list__()

            credentials: list = []
            for item in response['list']:
                if output_format == 'json':
                    credential: dict = {'name': item['name'].replace(' ', '-').lower(), 'value': {}, 'content_type': 'json'}
                    for attribute in item['attributes']:
                        credential['value'][attribute['name']] = self.__get_attribute_value__(item['id'], attribute['id'])
                else:
                    credential: dict = {'name': item['name']}
                    for attribute in item['attributes']:
                        credential[attribute['name'].lower()] = self.__get_attribute_value__(item['id'], attribute['id'])
                credentials.append(credential)
            return credentials
        except Exception as ex:
            raise Exception('Cannot list credentials') from ex

    def __authenticate__(self) -> str:
        response = requests.post(
            url=self.endpoints['authentication'],
            json={"username": self.username, "password": self.password, "multipleLogin": True},
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=30
        )
        if response.status_code != 200:
            raise Exception(f'{response.status_code} : {response.text}') from requests.RequestException
        self.token = response.json()['token']
        return self.token
        
    def __get_headers__(self):
        if self.token is None:
            self.__authenticate__()
        return {'X-Authorization': self.token}

    def __get_credentials_list__(self):
        response = requests.post(
            url=f'{self.endpoints["credentials"]}/list',
            headers=self.__get_headers__(),
            json={"fields": []},
            timeout=360
        )

        if response.status_code != 200:
            raise Exception(f'{response.status_code} : {response.text}') from requests.RequestException

        return response.json()

    def __get_attribute_value__(self, credential_id: str, attribute_id: str):
        response = requests.get(
            url=f'{self.endpoints["credentials"]}/{credential_id}/attributevalues?credentialAttributeId={attribute_id}',
            headers=self.__get_headers__(),
            timeout=360
        )

        if response.status_code != 200:
            raise Exception(f'{response.status_code} : {response.text}') from requests.RequestException

        values = response.json()['list']
        for value in values:
            if value['credentialAttributeId'] == attribute_id:
                return value['value']
        raise Exception(f'Cannot get value for credential id: {credential_id}, attribute id: {attribute_id}') from ValueError

    def __get_file_extention__(self, file_path: str) -> str:
        return file_path.split('.')[-1].lower()
