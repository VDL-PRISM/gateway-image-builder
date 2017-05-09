default: build

build:
	docker build -t gateway-image-builder .

sd-image: build
	docker run --rm --privileged -v $(shell pwd):/workspace -v /boot:/boot -v /lib/modules:/lib/modules gateway-image-builder
