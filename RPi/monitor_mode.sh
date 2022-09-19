iw dev
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
sudo iw dev wlan1 set freq 2432
sudo iw dev wlan1 set channel 5
