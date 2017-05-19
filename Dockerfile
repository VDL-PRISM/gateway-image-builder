FROM ryankurte/docker-rpi-emu

COPY build.sh /usr/rpi/build.sh
COPY prisms-run.sh /usr/rpi/prisms-run.sh
COPY files /usr/rpi/files
