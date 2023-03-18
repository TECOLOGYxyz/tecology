#!/bin/bash
echo "Installing AK7375 and IMX519_LOW_SPEED..."
echo "--------------------------------------"
uname=$(uname -r)
sudo install -p -m 755 ./arducam_camera_selector.sh /usr/bin/
sudo install -p -m 644 ./bin/$uname/imx519.ko.xz /lib/modules/$uname/kernel/drivers/media/i2c/
sudo install -p -m 644 ./bin/$uname/ak7375.ko.xz /lib/modules/$uname/kernel/drivers/media/i2c/
sudo install -p -m 644 ./bin/$uname/imx519.dtbo /boot/overlays/
sudo /sbin/depmod -a $(uname -r)

awk 'BEGIN{ count=0 }       \
{                           \
    if($1 == "dtoverlay=imx519"){       \
        count++;            \
    }                       \
}END{                       \
    if(count <= 0){         \
        system("sudo sh -c '\''echo dtoverlay=imx519 >> /boot/config.txt'\''"); \
    }                       \
}' /boot/config.txt
