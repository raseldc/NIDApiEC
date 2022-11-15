# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import base64
import io
import re
from datetime import datetime
import requests
import time

from flask import Flask, request, make_response, jsonify
import requests
from datetime import datetime
import urllib.request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app, support_credentials=True)
CORS(app, origins="http://localhost",
     allow_headers=["Content-Type", "Authorization",
                    "Access-Control-Allow-Credentials"],
     supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

access_token = "eyJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkd2FfYWRtaW4iLCJyb2xlcyI6WyJDT01NT05fVVNFUl9GVUxMX05BTUUiLCJQQVJUTkVSX1NVQl9VU0VSX0NSRUFURSIsIlBBUlRORVJfU1VCX1VTRVJfSU5BQ1RJVkUiLCJQQVJUTkVSX1NVQl9VU0VSX0RFVEFJTFNfQllfSUQiLCJQQVJUTkVSX1NVQl9VU0VSX1VQREFURSIsIkNPTU1PTl9ST0xFU19CWV9VU0VSIiwiVk9URVJfREVUQUlMUyIsIlBBUlRORVJfU1VCX1VTRVJfUkVTRVRfUEFTU1dPUkQiLCJQQVJUTkVSX1NVQl9VU0VSX0xJU1QiLCJDT01NT05fQ0hBTkdFX1BBU1NXT1JEIl0sImlhdCI6MTY2Nzg5NDM2NSwiZXhwIjoxNjY3OTM3NTY1fQ.f1Sd6UerqrNJLyTVfis9xSmoxi33gkCiuRaGEWKPlHI"
refresh_token = ""
base_url = "https://prportal.nidw.gov.bd/partner-service/rest/"
name = ""
last_time_to_get_token = "2022-11-08 13:40:00"


@app.route('/api/nid/', methods=['GET', 'POST'])
def nid_data():
    global access_token
    global refresh_token
    print("Call NID Data")
    print("request.json")
    print("request.json ", request.json)

    data = request.json
    print("<-----------------------------------------------access_token----------------------------------------------->")
    print(access_token)
    print(is_token_time_expired())
    if is_token_time_expired():
        print("<-----------------------------------------------Start Get Token----------------------------------------------->")
        response = get_token()
        print("Response", response)
        if response['status'] == "OK":
            access_token = response["success"]["access_token"]
            refresh_token = response["success"]["refresh_token"]
    print("<-----------------------------------------------Start Get NID Info0000----------------------------------------------->")
    if access_token != "":
        nid_info = get_nid_info(data['nid'], data['dob'])
        print("NID INFO GET")
        # if nid_info !="" and nid_info["status"]=="OK":
        #     photoUrl=  nid_info["success"]["data"]["photo"]
        #     print(photoUrl)
        #     # result = getPhotoBase64(photoUrl)
        #     print("Get Phptp")
        return nid_info
    return {"status": "OK"}


def getPhotoBase64(photoUrl):
    # a = requests.get(photoUrl)
    # print(a.status_code)

    # photoUrl="https://prportal.nidw.gov.bd/file-02/2/4/9/4c610d2c-06e1-43a9-a950-687ee9328324/Photo-4c610d2c-06e1-43a9-a950-687ee9328324.jpg"
    token = "Bearer{}".format(access_token)
    headers = {'Content-type': 'file', 'Authorization': token}
    r = requests.get(photoUrl)

    if r.status_code == 200:
        r.raw.decode_content = True  # decompress as you read
        files = {
            'fieldname': ('filename', r.raw, r.headers['Content-Type'])
        }

    # # photoUrl = "http://site.meishij.net/r/58/25/3568808/a3568808_142682562777944.jpg"
    # token = "Bearer {}".format(access_token)
    # headers = {'Authorization':token}
    # # a = requests.get(photoUrl, "/root/ECNid/local-filename.jpg")
    # # urllib.request.urlretrieve(photoUrl, "/root/ECNid/local-filename.jpg")
    # opener = urllib.request.build_opener()
    # opener.addheaders = [('Authorization', token)]
    # urllib.request.install_opener(opener)
    # urllib.request.urlretrieve(photoUrl, "/root/ECNid/l12.jpg")

    # # a = urllib.request.urlretrieve(photoUrl, "/root/ECNid/l12.jpg",headers=headers)
    # #r = requests.post(photoUrl, headers=headers)
    # # print("a-------------",a.text)
    # # print(a.headers.get('content-type'))
    return


def is_token_time_expired():
    global last_time_to_get_token

    last_time = datetime.strptime(last_time_to_get_token, "%Y-%m-%d %H:%M:%S")
    current_time = datetime.now()

    time_differnce = current_time - last_time
    # seconds_in_day = 24 * 60 * 60
    duration_in_s = time_differnce.total_seconds()
    print("duration_in_s", duration_in_s)
    hours = divmod(duration_in_s, 3600)[0]
    print("HOUR-----------------", hours)
    if hours >= 10:
        return True
    else:
        return False


def get_token():

    # return {"status":"OK","statusCode":"SUCCESS","success":{"data":{"username":"dwa_admin","access_token":"eyJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkd2FfYWRtaW4iLCJyb2xlcyI6WyJDT01NT05fVVNFUl9GVUxMX05BTUUiLCJQQVJUTkVSX1NVQl9VU0VSX0NSRUFURSIsIlBBUlRORVJfU1VCX1VTRVJfSU5BQ1RJVkUiLCJQQVJUTkVSX1NVQl9VU0VSX0RFVEFJTFNfQllfSUQiLCJQQVJUTkVSX1NVQl9VU0VSX1VQREFURSIsIkNPTU1PTl9ST0xFU19CWV9VU0VSIiwiVk9URVJfREVUQUlMUyIsIlBBUlRORVJfU1VCX1VTRVJfUkVTRVRfUEFTU1dPUkQiLCJQQVJUTkVSX1NVQl9VU0VSX0xJU1QiLCJDT01NT05fQ0hBTkdFX1BBU1NXT1JEIl0sImlhdCI6MTY2Nzc5NTYyOCwiZXhwIjoxNjY3ODM4ODI4fQ.Dfq0ul4D587mdIfLi-7dYog4SlK_pAOfwQxtu5P8-X8","refresh_token":"eyJ0eXAiOiJyZWZyZXNoX3Rva2VuIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiJkd2FfYWRtaW4iLCJpYXQiOjE2Njc3OTU2MjgsImV4cCI6MTY2Nzg0NjAyOH0.mhiFPm2DUXzjM0fkeYZNXkZcqkqWSStYAtR0_Sz1oPI"}}}

    ploads = {
        "password": "DwA%2022#P@rTnEr",
        "username": "dwa_admin"
    }
    headers = {'Content-type': 'application/json'}
    url = '{}auth/login'.format(base_url)

    r = requests.post(url, json=ploads, headers=headers,
                        allow_redirects=True)

    # r = requests.post('https://jsonplaceholder.typicode.com/posts')
    data = r.json()

    return data
    
# def logOut():
#     https://prportal.nidw.gov.bd/partner-service/rest/auth/logout


def setToken():
    if not is_token_time_expired():
        return
    global last_time_to_get_token
    global access_token
    global refresh_token
    last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Call Set Token------------------------------->")
    print("last_time_to_get_token", last_time_to_get_token)
    response = get_token()
    if response['status'] == "OK":
        access_token = response["success"]['data']["access_token"]
        refresh_token = response["success"]['data']["refresh_token"]
        last_time_to_get_token = "{}".format(last_time)


def get_nid_info(nid, dob):
    if nid != "" and dob != "":
        ploads10 = {
            "dateOfBirth": dob,
            "nid10Digit": nid
        }
        ploads = {
            "dateOfBirth": dob,
            "nid17Digit": nid
        }
        token = "Bearer {}".format(access_token)
        headers = {'Content-type': 'application/json', 'Authorization': token}

        if len(nid) == 10:
            ploads = ploads10

        result = requests.post(
            '{}voter/details'.format(base_url), json=ploads, headers=headers)
        # r = requests.post('https://jsonplaceholder.typicode.com/posts')
        data = result.json()
        print("data--------- ", data)
        if data["status"] == "BAD_REQUEST":
            return data
        if data["statusCode"] == "SUCCESS" and data["success"]["data"] is not None:
            photoUrl = data["success"]["data"]["photo"]
            rPhoto = requests.get(photoUrl)
            encoded = base64.b64encode(rPhoto.content)
            data["success"]["data"]["photoBase64"] = encoded.decode()

        return data
    else:
        return {"message": "NID or Date of Birth Not Found"}


def get_info():
    global name
    print("Hit")
    r = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    data = r.json()
    name = data['title']
    print("name----------------", name)


if __name__ == '__main__':
    setToken()
    print("From main Access token : --------->", access_token)
    # get_token()
    # get_info()
    # print('name',name)
    # is_token_time_expired()
    app.run(host='0.0.0.0', port=5001)
