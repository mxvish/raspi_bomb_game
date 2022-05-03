# raspi_bomb_game
source code after I reduced 252 lines
- This application works on Raspberry Pi Desktop

# Prerequisites 
- If this game doesn’t start, you may need to do some configuration.
- You can setup as follows automatically by using 
https://github.com/mxvish/raspi_auto_setup .
<pre>
sudo apt -y install raspberrypi-ui-mods
sudo apt -y install mpg321
sudo apt -y install fcitx-mozc
sudo apt -y install python3-pip 
sudo apt -y install python3-tk 

#install i2cdetect
sudo apt -y install i2c-tools

#install gpio command
sudo apt -y install git
git clone https://github.com/wiringpi/wiringpi
cd wiringpi
./build
#gpio -v
#gpio readall

pip3 install wiringpi
sudo apt -y install network-manager
sudo apt -y install network-manager-gnome --fix-missing
sudo apt -y install xfce4-power-manager --fix-missing

#enable i2c & sound
sudo raspi-config
#interface options -> i2c -> yes
#system options -> audio -> mai pcm i2s-hifi-0

reboot
</pre>

# Installation
<pre>
git clone https://github.com/mxvish/raspi_bomb_game.git
</pre>

# Usage
<pre>
cd raspi_bomb_game
python3 main_code.py
</pre>
and press "start" button on gui application.
