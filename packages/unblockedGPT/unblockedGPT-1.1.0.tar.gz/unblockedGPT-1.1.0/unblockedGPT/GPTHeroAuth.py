import requests
from typing import Union


def gptHeroAuthSignUp(username:str, password:str) -> Union[str, bool]:
    """
        Creates the user
        input: username, password
        output: True if authenticated, False if not
    """
    url = 'https://gpthero.dev/api/'
    payload = {
        "user": {
            "username": username,
            "password": password
        }
    }
    r = requests.post(url + 'register', json=payload)
    if r.status_code == 200:
        return gptHeroAuthLogin(username, password)
    return False
        
        

def gptHeroAuthLogin(username:str, password:str) -> Union[str, bool]:
    """
    login to the api
    input: username, password
    output: token
    """
    url = 'https://gpthero.dev/api/'
    payload = {
        "user":{
            "username": username,
            "password": password
        }
    }
    r = requests.post(url + 'login', json=payload)
    if r.status_code == 200:
        return r.json()['token']
    return False

def gptHeroSetTokes(heroToken:str, gptToken:str, pwToken:str):
    """
        uses api_keys enpoint to set gpt and pw tokens for gpthero
        input: heroToken, gptToken, pwToken
        output: True if saved, False if not
    """
    url = 'https://gpthero.dev/api/'
    payload = {
        "user":{
            "auth_token": heroToken,
        },
        "api_config":{
            "openai_api_key": gptToken,
            "prowritingaid_api_key": pwToken
        }
    }
    r = requests.post(url + 'api_keys', json=payload)
    if r.status_code == 200:
        return True
    return False


if __name__ == '__main__':
    print(gptHeroAuthLogin('ommmm', 'P@$$word'))