cp ./blind.service /etc/systemd/system/blind.service
cp ./tempcontrol.service /etc/systemd/system/tempcontrol.service
systemctl enable blind.service
systemctl enable tempcontrol.service
systemctl start blind.service
systemctl start tempcontrol.service