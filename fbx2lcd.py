#!/usr/bin/env python

import os, json, sys, requests, time, hmac
from hashlib import sha1
from subprocess import Popen, PIPE

def r(cmd_line):
    return Popen(cmd_line.split(), stdout=PIPE).communicate()[0]

CONFIG_FILE = 'config.json'
HOST = 'mafreebox.freebox.fr'

APP_ID = 'fbx2lcp.app'
APP_NAME = 'Freebox 2 Lcd'
APP_VERSION = '0.0.1'
DEVICE_NAME = r('hostname').strip()

STOK = ''

def req(path, data = ''):
    url = 'http://' + HOST + path
    if (data == ''):
        headers = {'X-Fbx-App-Auth': STOK}
        res = requests.get(url, headers=headers)
    else:
        headers = {'content-type': 'application/json', 'X-Fbx-App-Auth': STOK}
        res = requests.post(url, data=json.dumps(data), headers=headers)
    result = json.loads(res.text)
    return result

def authorize():
    data = {}
    data['app_id'] = APP_ID
    data['app_name'] = APP_NAME
    data['app_version'] = APP_VERSION
    data['device_name'] = DEVICE_NAME
    res = req('/api/v3/login/authorize/', data)
    if (res['success'] != True):
        print "Request failed"
        return False
    config = {}
    config['app_token'] = res['result']['app_token']
    print "app_token: " + APP_TOKEN
    print "Please authorize app on your freebox.. i'm waiting"
    while True:
        time.sleep(1)
        w = req('/api/v3/login/authorize/' + str(res['result']['track_id']))
        if (w['success'] != True):
            print "Request failed"
            return False
        print w['result']['status'] + "..."
        if (w['result']['status'] != 'pending'):
            print w
            if (w['result']['status'] == 'granted'):
                config['challenge'] = w['result']['challenge']
                config['password_salt'] = w['result']['password_salt']
                with open(CONFIG_FILE, 'w') as config_file:
                    config_file.write(json.dumps(config))
                    return (True)
            break
    print "Freebox app auth failed"
    sys.exit(1)

def get_session(config):
    tmp = req('/api/v3/login/')
    if (tmp['success'] == False):
        sys.exit(2)
    if (tmp['result']['logged_in'] == False):
        hashed = hmac.new(str(config['app_token']), str(tmp['result']['challenge']), sha1)
        password = hashed.hexdigest()
        data = {}
        data['app_id'] = APP_ID
        data['password'] = password
        session = req('/api/v3/login/session/', data)
        if (session['success'] == False):
            return (False)
        return (session['result']['session_token'])

def open_and_load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.loads(config_file.read())
    else:
        print "File [%s] doesn't exist, need to authorize." % (CONFIG_FILE)
        authorize()
        return open_and_load_config()

if __name__ == "__main__":
    config = open_and_load_config()
    while True:
        datas = req('/api/v3/connection/')
        if (datas['success'] == True):
            print str(datas['result']['rate_up']) + ':' + str(datas['result']['rate_down'])
        else:
            STOK = get_session(config)
            print STOK
        time.sleep(1)
