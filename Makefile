default: build

build:
	docker build -t gateway-image-builder .

sd-card: build
	docker run --rm --privileged -v $(shell pwd):/workspace -v /boot:/boot -v /lib/modules:/lib/modules gateway-image-builder

shell: build
	docker run --rm --privileged -v $(shell pwd):/workspace -v /boot:/boot -v /lib/modules:/lib/modules -it gateway-image-builder bash
