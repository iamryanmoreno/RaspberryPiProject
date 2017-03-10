## Install dependencies

### Install Kivy
    
    sudo apt-get update
    sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
       pkg-config libgl1-mesa-dev libgles2-mesa-dev \
       python-setuptools libgstreamer1.0-dev git-core \
       gstreamer1.0-plugins-{bad,base,good,ugly} \
       gstreamer1.0-{omx,alsa} python-dev
    
    sudo pip install cython==0.23
    
    sudo pip install git+https://github.com/kivy/kivy.git@master
    
### Enable auto-start
    
It is assumed that source files are located in `/home/pi/parse_serial`

Open the file below.
    
    sudo nano /etc/profile
    
Add below at the end of the file.

    /usr/bin/python /home/pi/parse_serial.py
    
    