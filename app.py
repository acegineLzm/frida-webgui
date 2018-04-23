from flask import *
from jinja2 import Environment
from os import listdir
from os.path import isfile, join,dirname,realpath

import os
import sys
import frida
import requests
import json
import socket
import redis
import time


modulePath=os.path.dirname(os.path.realpath(__file__))+"/modules/"
device = None
remote = None
red = redis.Redis(host='redis', port=6379)
# red = redis.StrictRedis()

HTML = """{{title}}"""

app = Flask(__name__)


'''
landing page, ask for the remote address of the device, if no remote adresse juste let the input empty
'''
@app.route('/')
def hello_world():
    return render_template('intro.html')

'''
show list of running process on the device
'''
@app.route('/packages',methods=['GET'])
def show_packages():
    global device
    global remote
    try:
        remote = request.args.get('remote')
        if device == None:
            if len(remote) != 0:
                # check remote ip address
                try:
                    socket.inet_aton(remote)
                    print("adding remote device to device manager : ", remote)
                    device=frida.get_device_manager().add_remote_device(remote)
                    print("remote device : ", device)
                except socket.error:
                    return render_template('intro.html')
            else:
                device = frida.get_remote_device()

        # get list of apps
        packages=device.enumerate_processes()
        print(packages)
    except frida.ServerNotRunningError :
        return render_template('error.html',error="cannot connect to remote :(")
    return render_template('packages_list.html',
                           packages=packages)


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('diffdroid')
    print("JUST SUBSCRIBE TO DIFFDROID")
    for message in pubsub.listen():
        print("EVENT_STREAM : ",message)
        if message['type'] == 'message':
            yield 'data: %s\n\n' % message['data'].decode()


@app.route('/stream')
def stream():
    return Response(event_stream(),
                          mimetype="text/event-stream")


def get_messages_from_js(message,data):
    if message['type'] == 'send':
        msg = message['payload']
    else:
        msg = message
    red.publish('diffdroid', msg)
    print("JUST_PUBLISHED : ", msg)

def start_frida(x,bleeh):
    global device
    print(device)
    process = device.attach(bleeh)
    script = process.create_script(x)
    script.on('message',get_messages_from_js)
    script.load()

@app.route('/hack')
def hack():
    module = request.args.get('module')
    txt = open(modulePath+module,'r').read()
    return render_template('main.html',
                           content=txt)

def get_process_pid(device, application_name):
    for p in device.enumerate_processes():
        if p.name == application_name:
            return p.pid
    return -1


def rebootfun(package_name):
    global device
    global remote
    try:
        pid = get_process_pid(device, package_name)
        if pid != -1:
            print("killing packagename:{0} pid:{1}".format(package_name, pid))
            device.kill(pid)
            time.sleep(0.3)
        os.system("chmod a+x ./adb")
        re = os.popen("./adb connect {}:5555".format(remote)).read()
        re = os.popen("./adb -s {0}:5555 shell am start {1}/.MainActivity".format(remote, package_name)).read()
        time.sleep(0.5)
        while(1):
            pid = get_process_pid(device, package_name)
            if pid == -1:
                print("{0} is not found...".format(package_name))
                time.sleep(2)
            else:
                break
    except Exception as e:
        print(e)

@app.route('/reboot', methods=['GET', 'POST'])
def reboot():
    package_name = request.args.get('package_name')
    rebootfun(package_name)
    response = jsonify({"message": "ok"})
    response.status_code = 200
    return response


@app.route('/lol',methods=['GET', 'POST'])
def lol():
    try:
        blah = request.get_json()
        bleeh = request.args.get('package_name')
        count = request.args.get('count')
        if blah is None:
            return "boo"
        else:
            if int(count) > 1:
                rebootfun(bleeh)
            x = Environment().from_string(HTML).render(title=request.get_json())
            start_frida(x,bleeh)
            response = jsonify({"message":"ok"})
            response.status_code = 200
            return response
    except Exception as e:
        print(e)


@app.route('/list')
def list():
    bleeh = request.args.get('package_name')
    filess = [f for f in listdir(modulePath) if isfile(join(modulePath, f))]
    return render_template("list.html",
                           posts=filess,
                           package_name = bleeh)

@app.route('/update')
def update():
    return render_template("update.html")


if __name__ == '__main__':
    # main(sys.argv)
    app.run(host="0.0.0.0", threaded=True)
