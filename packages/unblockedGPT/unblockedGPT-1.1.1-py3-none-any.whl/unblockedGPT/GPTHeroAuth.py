import requests
from typing import Union
import random
import string
from unblockedGPT.auth import Database
import time

auth = Database.get_instance()

def gptHeroAuth() -> bool:
    """
    does gpthero authflow
    input: None
    output: true if authenticated, false if not
    """
    if auth.get_settings(7) != False:
        token = gptHeroAuthLogin(auth.get_settings(2), auth.get_settings(3))
        if token:
            auth.set_settings(7, token)
            return gptHeroSetTokes(token, auth.get_settings(0), auth.get_settings(1))

    token = gptHeroAuthSignUp()
    if token:
        auth.set_settings(7, token)
        return gptHeroSetTokes(token, auth.get_settings(0), auth.get_settings(1))
    return False
    



def gptHeroAuthSignUp() -> Union[str, bool]:
    """
        Creates the user
        input: None
        output: Token returned if authenticated, False if not
    """
    
        
    url = 'https://gpthero.dev/api/'
    flag = True
    
    while flag:
        username = "unblockedGPT"+ str(random.randint(0, 20))
        random_password = ''.join(random.choice(string.ascii_letters) for i in range(20))

        payload = {
            "user": {
                "username": username,
                "password": random_password
            }
        }
        r = requests.post(url + 'register', json=payload)
        if r.status_code == 200:
            if 'error' not in r.json():
                return gptHeroAuthLogin(username, random_password)
            elif r.json()['error'] != 'Username already exists':
                return False
             
        time.sleep(5)
                
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
        auth.set_settings(2, username)
        auth.set_settings(3, password)
        return r.json()['token']
    return False

def gptHeroSetTokes(heroToken:str, gptToken:str, pwToken:str):
    if heroToken == False or gptToken == False or pwToken == False:
        return False
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
    print(gptHeroAuth())