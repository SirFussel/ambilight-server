# Custom Ambilight using Raspberry Pi 3
## Hardware
- Raspberry Pi 3 or higher
- USB framegrabber
- WS2801 LED stripes
- HDPC compatible HDMI splitter
- Power supply
- Wires and cables
## Software
- Hyperion
## Additional Features
- Temperature controlled case using fan
- Blind service to disable the stripes when TV is off
## Pi Configuration
### WIFI configuration
1. Add following lines to ```/etc/network/interfaces``` in order to disable WIFI power save mode:
    ```
    allow-hotplug wlan0
    iface wlan0 inet manual
    post-up iw wlan0 set power_save off
    ```
2. Make sure ```/etc/wpa_supplicant/wpa_supplicant.conf``` looks similar to this and replace the placeholders:
    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=DE

    network={
            ssid="<ssid>"
            psk="<password>"
    }
    ```
    You can do this by using ```sudo wpa_passphrase "<ssid>" "<password>" >> /etc/wpa_supplicant/wpa_supplicant.conficant.conf``` instead of manually adding it to the file.
3. Restart WIFI by using ```sudo ifconfig wlan0 down``` and ```sudo ifconfig wlan0 up``` afterwards.
### Add services
1. Add a file to ```/etc/systems/system/``` folder and make sure its extension is ```.service```. Its content looks similar to:
    ```
    [Unit]
    Description=Temperature control service
    After=multi-user.target
    [Service]
    Type=simple
    Restart=always
    ExecStart=/usr/bin/python3 /home/pi/tempcontrol.py
    [Install]
    WantedBy=multi-user.target
    ```
2. Register the service using ```sudo service enable <servicename>.service```
3. Run the service using ```sudo service start <servicename>.service```
