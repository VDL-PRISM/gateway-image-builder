FROM debian:jessie

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    binfmt-support \
    qemu \
    qemu-user-static \
    libguestfs-tools \
    zip \
    unzip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY builder/ /builder/

# build sd card image
CMD /builder/build.sh
