# smartcar-app-v1

[! https://img.shields.io/github/license/nabsha/smartcar-app-v1] [! https://img.shields.io/badge/Made%20at-Starschema-red]
A short description of the project.


### Installation
```
sudo apt install git
sudo apt-get install i2c-tools
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install python3-smbus
sudo apt-get install python3-picamera
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt install libopenexr-dev
```
### Compile LED driver
```
git clone https://github.com/Freenove/Freenove_RPI_WS281x_Python.git
cd ~/Freenove_RPI_WS281x_Python
sudo python3 setup.py install
```

### Network config
Needs restart once following changes are done in `/etc/dhcpcd.conf`,
```
# Example static IP configuration:
interface wlan0
static ip_address=192.168.50.111/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.50.1
static domain_name_servers=192.168.50.250 8.8.8.8 fd51:42f8:caae:d92e::1
```
