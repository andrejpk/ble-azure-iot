# TI Sensortag sensor reader

Built in Python 3 using the bluepy library.

## Installation

Install Python 3, PIP 3:

```
sudo apt-get install python3-pip libglib2.0-dev -y
sudo pip3 install bluepy
```

## Usage

Use the blescan tool to find your SensorTag MAC address (you may have to wake it up using the power button)
```
sudo blescan
```

Then run the tool to watch the sensors:

```
python3 st-sensors.py [Sensortag MAC address]
```

You should see a stream of temperature and light sensor data
