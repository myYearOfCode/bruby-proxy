#this file will set a raspberry pi zero w up as a proxy server to redirect
#from picobrew to 
#hardware: 
#raspi zero w with a usb wifi card connected.
#STEPS
# image raspbian onto a memory card.
# mount the card and copy wpa_supplicant.conf with your pertinent wifi creds 
# onto the boot volume.
# create a file named `ssh` on the boot volume (unless you want to connect another way)
# eject card, start up raspberry pi and ssh in.
# wget https://raw.githubusercontent.com/myYearOfCode/bruby-proxy/master/bruby_raspi_setup.sh
# chmod +x bruby_raspi_setup.sh 
# sudo ./bruby_raspi_setup.sh (and then wait a while for updates to happen)
#######
# when you are finished a new network should appear named 'bruby' with the p: 'brubybruby'
# logging in should give you internet, but will redirect picobrew to bruby.
# NOTE: most browsers cache if a site is using https, so they will not work with this.
# test this with 'curl picobrew.com' and you should get bruby mentions.
#######
#hotspot setup
cd /usr/local/sbin
sudo rm hotspot                           # just remove old hotspot script
sudo wget https://raw.githubusercontent.com/rudiratlos/hotspot/master/hotspot
sudo chmod +x hotspot
sudo apt-get update
sudo apt-get -y upgrade                      # optional

sudo hotspot setup

sudo hotspot modpar hostapd ssid bruby 
sudo hotspot modpar hostapd wpa_passphrase brubybruby
sudo hotspot modpar hostapd country_code US
sudo hotspot modpar crda REGDOMAIN US
sudo hotspot modpar self autostart yes    # optional autostart enable

#bruby-setup.sh
# add redirect to hardcoded pi ip address.
echo "address=/picobrew.com/10.3.141.1" | sudo tee -a  /etc/dnsmasq.conf

# download proxy server 
sudo mkdir /lib/bruby_proxy
sudo mkdir /lib/bruby_proxy/logs
cd /lib/bruby_proxy
sudo wget "https://raw.githubusercontent.com/myYearOfCode/bruby-proxy/master/bruby_proxy.py"
sudo chmod +x bruby_proxy.py

# start proxy server on boot.
sudo sed '/exit 0/i sudo python /lib/bruby_proxy/bruby_proxy.py 80 & ' /etc/rc.local -i.bkp

sudo reboot  