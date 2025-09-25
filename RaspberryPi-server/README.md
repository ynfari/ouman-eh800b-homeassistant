# Prerequisites
- Python3
- pip


# Setup instructions

1. Create a new virtual enviroment to opt/OumanHA folder
`python3 -m venv /opt/OumanHA`

2. Copy the _OumanHA.py_ and _requirements.txt_ to the created directory.

4. `cd /opt/OumanHA`
and run
`source bin/activate`

3. install the requirements:
`pip install -r requirements.txt`

4. Add pi user to dialout group, if not allready member:
`sudo usermod -a -G dialout pi`

5. Connect your Ouman to RPI and check the usb serial port of your Ouman using dmesg
`dmesg -w`

```
cdc_acm 1-1.3:1.0: ttyACM0: USB ACM device
usbcore: registered new interface driver cdc_acm
cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
```

In this case the port is `ttyACM0`.

Edit the port to your `/opt/OumanHA/OumanHA.py` file on read_measurements section if necessary.

```
def read_measurements():
    # Open the serial port
    try:
        ser = serial.Serial(
            port='/dev/ttyACM0', 

```

# Set up the service to automatically start the server when rpi boots

1. Copy the _OumanHA.service_ file to _/etc/systemd/system/_ folder.

2. Reload system services
`systemctl daemon-reload`

4. Activate the service
`systemctl enable OumanHA.service`

5. Start the new service
`systemctl start OumanHA.service`

Now the Flask Api should start providing the data on your RPI. You can navigate to http://<your rpi address>/measurements and see the 27 different measurements received from Ouman.

The measurements might change on different configurations. Below table is from my controller, that is used to control hydronic heating from wood burner.

| Number | Measurement |
| ------ | ------ |
|    1    |    Supply water temp according to the control curve    |
|    2    |    Rooom compensation    |
|    3    |    Room compensation with time adjustment   |
|    4    |    Unknown    |
|   5   |      Unknown  |
|   6     |    Unknown    |
|    7    |    Calculated supply water temp    |
|    8    |    Setpoint with time adjustment  |
|    9    |    Supplywater temperature    |
|    10    |   Outside temperature     |
|    11    |   Outside temperature with time adjustment |
|    12    |   Room temperature         |
|    13    |   Room temperature with time adjustment      |
|    14    |   Room remote potentiometer     |
|  15   |   L1 valve calculated position %     |
|   16     |  L1 valve real position %      |
|   17    |     Unknown     |
|    18    |    Unknown      |
|    19    |     Unknown     |
|    20    |    Unknown      |
|    21    |    Delayed outdoor temp measurement     |
|    22    |   Unknown       |
|   23    |    Unknown      |
|    24    |   Unknown       |
|   25   |     Unknown     |
|   26     |   Unknown       |
|    27    |    Unknown      |