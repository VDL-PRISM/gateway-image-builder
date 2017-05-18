FROM ubuntu
LABEL maintainer "Philip Lundrigan <philipbl@cs.utah.edu>"

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    binfmt-support qemu qemu-user-static libguestfs-tools zip unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY builder/ /builder/

CMD /builder/build.sh
