default: build

build:
        docker build -t gateway-image-builder .

sd-card: build
        docker run -it --rm --privileged=true -v /root/images:/usr/rpi/images -w /usr/rpi gateway-image-builder /bin/bash -c './run.sh images/2017-04-10-raspbian-jessie-lite.img < build.sh'

shell: build
        docker run -it --rm --privileged=true -v /root/images:/usr/rpi/images -w /usr/rpi gateway-image-builder /bin/bash -c './run.sh images/2017-04-10-raspbian-jessie-lite.img'
