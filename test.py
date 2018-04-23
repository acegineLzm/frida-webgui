import os
import time
import sys
import frida
#打印javascript脚本返回消息
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)
#获取设备应用名
def get_application_name(device, identifier):
    for p in device.enumerate_applications():
        if p.identifier == identifier:
            return p.name
#获取设备进程pid
def get_process_pid(device, application_name):
    for p in device.enumerate_processes():
        if p.name == application_name:
            return p.pid
    return -1
def main():
    #连接设备
    device = frida.get_device_manager().enumerate_devices()[-1]
    #需要attach的apk包名、javascript路径
    # package_name = input("Please input the package_name: ")
    # jsfile = input("Please input the js path: ")
    # if not os.path.exists(jsfile):
    #     sys.exit(0)
    with open("/Users/luziming/Desktop/frida/config.txt") as f:
        package_name, jsfile = [line.strip() for line in f]
    #发现进程存活则杀死进程，等待进程重启
    pid = get_process_pid(device, package_name)
    if pid != -1:
        print("[+] killing {0}".format(pid))
        device.kill(pid)
        time.sleep(0.3)

    os.system("./adb connect 172.16.104.22:5555")
    os.system("./adb -s 172.16.104.22:5555 shell am start {}/.MainActivity".format(package_name))
    time.sleep(0.5)

    while(1):
        pid = get_process_pid(device, package_name)
        if pid == -1:
            print("[-] {0} is not found...".format(package_name))
            time.sleep(2)
        else:
            break
    print("[+] Injecting script to {0}({1})".format(package_name, pid))
    session = None
    try:
        #attach目标进程
        session = frida.get_device_manager().enumerate_devices()[-1].attach(pid)
        #加载javaScript脚本
        script_content = open(jsfile).read()
        script = session.create_script(script_content)
        script.on("message", on_message)
        script.load()
        sys.stdin.read()
    except KeyboardInterrupt as e:
        if session is not None:
            session.detach()
            device.kill(pid)
        sys.exit(0)
if __name__ == "__main__":
    main()
