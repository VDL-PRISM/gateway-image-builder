#!/bin/bash -e
set -x

# This script should be run only inside of a Docker container
if [ ! -f /.dockerenv ]; then
  echo "ERROR: script works only in a Docker container!"
  exit 1
fi

# Get versions for software that needs to be installed
source /workspace/versions.config

# Place to build our sd-image
BUILD_PATH="/build"
NEW_IMAGE_NAME="prisms-gateway-${PRISMS_GATEWAY_IMAGE_VERSION}.img"

# Download image
curl -OL "https://downloads.raspberrypi.org/raspbian_lite/images/${RASPBIAN_FOLDER}/${RASPBIAN_IMAGE_NAME}.zip"
unzip "${RASPBIAN_IMAGE_NAME}.zip"

# Create build directory for assembling our image filesystem
rm -rf ${BUILD_PATH}
mkdir ${BUILD_PATH}

update-binfmts --enable qemu-arm

# Mount the image
guestmount -a "${RASPBIAN_IMAGE_NAME}.img" -m /dev/sda2:/ -m /dev/sda1:/boot "${BUILD_PATH}"

# Mount pseudo filesystems
mount -o bind /dev ${BUILD_PATH}/dev
mount -o bind /dev/pts ${BUILD_PATH}/dev/pts
mount -t proc none ${BUILD_PATH}/proc
mount -t sysfs none ${BUILD_PATH}/sys

# Copy necessary executable
cp /usr/bin/qemu-arm-static "${BUILD_PATH}/usr/bin/"

# Comment out every line in file
sed -i 's/^/# /' ${BUILD_PATH}/etc/ld.so.preload

# Modify/add image files directly
cp -R ~/sensor-image-builder/files/* ${BUILD_PATH}/

# Install everything needed on the image
chroot ${BUILD_PATH} /bin/bash -x - << EOF

# Set default locales to 'en_US.UTF-8'
echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen
locale-gen

# apt-get update
# apt-get upgrade -y

# Install Docker
curl -sSL get.docker.com | sh

# Install basic software
apt-get install -y zip unzip avahi-daemon git

# Install ngrok
curl -O https://bin.equinox.io/c/gDfFGFRN2Jh/ngrok-link-stable-linux-arm.tgz
tar -xvzf ngrok-link-stable-linux-arm.tgz
mv ngrok /usr/local/bin
rm ngrok-link-stable-linux-arm.tgz

# Install YAML
pip install --no-cache-dir pyyaml

# Cleanup other stuff
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EOF # <<<<<<<<<<<<<<<<< END OF CHOWN

# Uncomment out every line in file
sed -i 's/^# //' ${BUILD_PATH}/etc/ld.so.preload

rm "${BUILD_PATH}/usr/bin/qemu-arm-static"

# Unmount pseudo filesystems
umount -l ${BUILD_PATH}/dev/pts
umount -l ${BUILD_PATH}/dev
umount -l ${BUILD_PATH}/proc
umount -l ${BUILD_PATH}/sys

# Unmount the image
guestunmount "${BUILD_PATH}" || true

# Rename image
mv "${RASPBIAN_IMAGE_NAME}.img" "${NEW_IMAGE_NAME}"

# Compress image
zip "${NEW_IMAGE_NAME}.zip" "${NEW_IMAGE_NAME}"
