#import urllib.request
import json

from fabric.api import *
from time import sleep


RPi_IPs = [
            {"column_num": 1, "ip_addr": "129.217.152.74", "mac_id": "b8:27:eb:41:99:a0", "hostname": "raspberrypi"},
            {"column_num": 2, "ip_addr": "129.217.152.111", "mac_id": "b8:27:eb:c0:fd:6a", "hostname": "raspberrypi"},
            {"column_num": 3, "ip_addr": "129.217.152.79", "mac_id": "b8:27:eb:18:92:c7", "hostname": "raspberrypi"},
            {"column_num": 4, "ip_addr": "129.217.152.54", "mac_id": "b8:27:eb:53:f2:33", "hostname": "raspberrypi"},
            {"column_num": 5, "ip_addr": "129.217.152.86", "mac_id": "b8:27:eb:e7:6f:dc", "hostname": "raspberrypi"},
            {"column_num": 6, "ip_addr": "129.217.152.89", "mac_id": "b8:27:eb:38:4b:07", "hostname": "raspberrypi"},
            {"column_num": 7, "ip_addr": "129.217.152.84", "mac_id": "b8:27:eb:1b:cf:26", "hostname": "raspberrypi"},
            {"column_num": 8, "ip_addr": "129.217.152.119", "mac_id": "b8:27:eb:6d:0e:53", "hostname": "raspberrypi"},
            {"column_num": 9, "ip_addr": "129.217.152.77", "mac_id": "b8:27:eb:b7:a3:b7", "hostname": "raspberrypi"},
            {"column_num": 10, "ip_addr": "129.217.152.118", "mac_id": "b8:27:eb:be:dc:32", "hostname": "raspberrypi"},
            {"column_num": 11, "ip_addr": "129.217.152.69", "mac_id": "b8:27:eb:ff:a4:48", "hostname": "raspberrypi"},
            {"column_num": 12, "ip_addr": "129.217.152.59", "mac_id": "b8:27:eb:a9:7d:4d", "hostname": "raspberrypi"},
            {"column_num": 13, "ip_addr": "129.217.152.85", "mac_id": "b8:27:eb:c4:f8:c7", "hostname": "raspberrypi"},
            {"column_num": 14, "ip_addr": "129.217.152.48", "mac_id": "b8:27:eb:e4:43:6d", "hostname": "raspberrypi"},
            {"column_num": 15, "ip_addr": "129.217.152.63", "mac_id": "b8:27:eb:98:69:6e", "hostname": "raspberrypi"},
            {"column_num": 16, "ip_addr": "129.217.152.50", "mac_id": "b8:27:eb:75:c7:a2", "hostname": "raspberrypi"},
            {"column_num": 17, "ip_addr": "129.217.152.37", "mac_id": "b8:27:eb:09:3d:77", "hostname": "raspberrypi"},
            {"column_num": 18, "ip_addr": "129.217.152.60", "mac_id": "b8:27:eb:05:d8:4d", "hostname": "raspberrypi"},
            {"column_num": 19, "ip_addr": "129.217.152.64", "mac_id": "b8:27:eb:36:da:22", "hostname": "raspberrypi"},
            {"column_num": 20, "ip_addr": "129.217.152.62", "mac_id": "b8:27:eb:f5:5d:04", "hostname": "raspberrypi"},
            {"column_num": 21, "ip_addr": "129.217.152.51", "mac_id": "b8:27:eb:88:8d:56", "hostname": "raspberrypi"},
            {"column_num": 22, "ip_addr": "129.217.152.87", "mac_id": "b8:27:eb:00:be:93", "hostname": "raspberrypi"},
            {"column_num": 23, "ip_addr": "129.217.152.33", "mac_id": "b8:27:eb:c0:10:ae", "hostname": "raspberrypi"},
            ]

for hosts in RPi_IPs:
    env.hosts.append(hosts['ip_addr'])

env.user = "pi"
env.password = "raspberry" # ofc we use the default password

# some stats to printout
success_list = []
error_list = []
env.reject_unknown_hosts = False

@parallel
def r():
    with cd('~/sensorfloor'):
        run('git config --global user.email "aswinkarthik.ramachandran@tu-dortmund.de"')
        run('git config --global user.name "akrv"')

        run('git stash')
        run('git pull')
    # run('ntpstat')


@parallel
def imuread():
    with cd('~/sensorfloor/imu_reader'):
        run('python read_past_imu.py')

@parallel
def deploy():
    with cd('~/sensorfloor'):
        run('git pull')
    result = run('sudo cp -rf sensorfloor /var/www/')
    if result.failed:
        print('failed: ',env.host)

@parallel
def webui():
    try:
        with cd('~/sensorfloor'):
            run('git pull')
            run('pip install -r requirements.txt')
        with cd('~/'):
            run('sudo cp sensorfloor/sensorfloor.conf /etc/sites-available')

            run('sudo cp -rf sensorfloor /var/www/')

            run('sudo a2ensite sensorfloor.conf')
            run('sudo systemctl reload apache2')
        success_list.append(env.host)
    except:
        error_list.append(env.host)
    print(error_list)


@parallel
def reboot():
    run('sudo reboot now')

@parallel
def turnon():
    with cd('~/sensorfloor/floor_flasher'):
        run('python all_turn_on_comm_off.py --turn-on')

@parallel
def turnoff():
    with cd('~/sensorfloor/floor_flasher'):
        run('python all_turn_on_comm_off.py --turn-off')

@parallel
def save_log():
    with cd('~/sensorfloor/floor_flasher'):
        run('python save_log.py')

@parallel
def brokennodes():
    with cd('/home/pi/sensorfloor/imu_reader/'):
        run('git checkout read_past_imu.py')

# /Users/akrv/Documents/dev/sensorfloor/imu_app/imu_ti_workspace/imu_data_interrupt/Release/imu_data_interrupt.bin

def cssh():
    result = run('uname')
    if result.failed:
        print('failed: ',env.host)


# @parallel
# def setup():
#     # install apache2 and mod-wsgi
#     run('sudo apt-get update')
#     run('sudo apt-get install -y apache2 libapache2-mod-wsgi git libcairo2-dev libjpeg-dev libgif-dev')
#     with cd('~/'):
#         run('sudo rm -rf sensorfloor')
#         # git clone
#         run('git clone --recurse-submodules http://github.com/akrv/sensorfloor')
#         # copy conf and the rest of the folder
#         run('sudo cp sensorfloor/sensorfloor.conf /etc/apache2/sites-available')
#     with cd('~/sensorfloor'):
#         run('pip install -r requirements.txt')
#         run('mkdir -p /home/pi/sensorfloor/flash')
#     with cd('~/sensorfloor/addr_finder'):
#         run('python main.py')
#         # copy to www folder the source code
#     with cd('~/'):
#         run('sudo cp -rf sensorfloor /var/www/')
#
#     # disable default conf
#     run('sudo a2dissite 000-default.conf')
#     # enable site
#     run('sudo a2ensite sensorfloor.conf')
#     run('sudo systemctl reload apache2')
