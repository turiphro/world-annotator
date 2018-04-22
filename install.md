# deps: 7min
sudo apt update
sudo apt upgrade
sudo apt install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libcairo2-dev libatlas-base-dev gfortran python2.7-dev python3-dev

# opencv: 6hrs
mkdir ~/workdir && cd ~/workdir
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.0.zip
unzip opencv_contrib.zip
mkdir opencv-3*/build && cd opencv-3*/build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/workdir/opencv_contrib-3.4.0/modules \
    -D BUILD_EXAMPLES=ON ..
time nice make -j4  # slow

# pycamera: TODO

# LCD
git clone https://github.com/goodtft/LCD-show.git
cd LCD-show && chmod +x LCD*
./LCD35-show
#change /boot/config.txt to have:
#dtoverlay=tft35a,rotate=270,swapxy=1
#add +x file .config/lxsession/LXDE-pi/touchscreen.sh with:
#DISPLAY=:0 xinput --set-prop 'ADS7846 Touchscreen' 'Evdev Axis Inversion' 1 1
echo "@lxterminal -e .config/lxsession/LXDE-pi/touchscreen.sh" >> .config/lxsession/LXDE-pi/autostart


# MXNet
sudo pip3 install graphviz
sudo apt-get -y install git cmake build-essential g++-4.8 c++-4.8 liblapack* libblas* libopenblas-base libopenblas-dev libopencv*
git clone --recursive https://github.com/apache/incubator-mxnet
cd incubator-mxnet
nice make USE_OPENCV=1 USE_BLAS=openblas # running with -j4 crashes
cd python
sudo python setup.py install
sudo python3 setup.py install

ERR:
/usr/bin/ld: cannot find -lopenblas
collect2: error: ld returned 1 exit status
Makefile:428: recipe for target 'lib/libmxnet.so' failed
make: *** [lib/libmxnet.so] Error 1

