from flask import Flask, redirect, request, render_template,jsonify
import os 
import lxml.etree as ET
import requests 
import re

app = Flask(__name__)
internal =  ['127.0.0.1']
base_url = "http://85.214.190.217:1337"
whitelist = [r'http://85\.214\.190\.217:1337/']
links = {
    "  Employees 👔": f"{base_url}/employees",
    "  Interns 👶": f"{base_url}/interns",
    "  Flag ⚙️": f"{base_url}/flag",
    "  Login Panel 📍": f"{base_url}/login", 
    "  Admin Panel ⚙️": f"{base_url}/admin" 
}
@app.route('/')
def index(): 
    return render_template("index.html", links=links)

@app.route('/admin',methods=['GET','POST'])
def admin():
    query = "string(//user[username='admin']/password)"
    root = ET.parse('./users.xml').getroot()
    password = root.xpath(query)
    if request.remote_addr not in internal or 'key' not in request.form or request.form['key'] != password:
        return "Access Denied!",401
    else:
        return render_template('flag.html',flag=os.getenv('FLAG','FAKE_FLAG'))

@app.route('/employees')
def employees(): 
    return render_template('employees.html')

@app.route('/interns')
def interns(): 
    return render_template('interns.html')

@app.route('/status-check')
def status_check():
    url = request.args.get('url')
    if not url:
        return 'Missing Url!', 400
    if not re.match(whitelist[0], url): # theres only one rn 
        return 'Not Allowed!',401
    try:   
        response = requests.get(url,data=request.form) # we may use the data field in the future when implementing elastic (https://www.elastic.co/guide/en/elasticsearch/guide/current/_empty_search.html)
        response.raise_for_status()
        if request.args.get('debug') == 'true':
            return jsonify({'status': 'success', 'message': f'{url} is up and running', 'content': response.text})
        return jsonify({'status': 'success', 'message': f'{url} is up and running'})
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': f'{url} is down or inaccessible: {str(e)}'})


@app.route('/redirect')
def redirect_to_url():
    s = request.args.get('s')
    return redirect(request.args['url'], int(s) if s else 301)


FORBIDDEN_FUNCTIONS = ['string', 'starts-with', 'concat', 'translate', 'position'] 

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":    
        username = request.form.get('username').replace('\'','').replace('"','') 
        password = request.form.get('password').replace('\'','').replace('"','')  
        sso_token = request.form.get('sso_token')
        if not username or not password or len(password) < 6 or not sso_token:
            return 'Invalid username, password, or SSO token',403
        for func in FORBIDDEN_FUNCTIONS:
            if func in username or func in password or func in sso_token:
                return 'Invalid username, password, or SSO token',403
        query = f"/users/user[username='{username}' and password='{password}' and sso_token='{sso_token}']"
        root = ET.parse('./users.xml').getroot()
        result = root.xpath(query)
        if len(result) > 0:
            return 'Login successfull !'
        else:
            return 'Invalid username, password, or SSO token',403
    else :
         return render_template('login.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=1337)
    
