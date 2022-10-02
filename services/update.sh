systemctl stop blind.service
systemctl stop tempcontrol.service
cp ./blind.service /etc/systemd/system/blind.service
cp ./tempcontrol.service /etc/systemd/system/tempcontrol.service
systemctl start blind.service
systemctl start tempcontrol.service