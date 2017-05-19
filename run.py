import argparse
import os.path
import subprocess


parser = argparse.ArgumentParser(description='Run script to build gateway image')
parser.add_argument('command', choices=['shell', 'build'])
parser.add_argument('image', help='Image file you want to modify')

args = parser.parse_args()
path, name = os.path.split(args.image)

print("Building docker image")
subprocess.run('docker build -t gateway-image-builder .', shell=True)

if args.command == 'build':
    print("Creating image")
    subprocess.run('docker run -it --rm --privileged=true -v {}:/usr/rpi/images ' \
                   '-w /usr/rpi gateway-image-builder ' \
                   '/bin/bash -c \'./run.sh images/{} < build.sh\''.format(path, name),
                   shell=True)

elif args.command == 'shell':
    print("Entering shell")
    subprocess.run('docker run -it --rm --privileged=true -v {}:/usr/rpi/images ' \
                   '-w /usr/rpi gateway-image-builder ' \
                   '/bin/bash -c \'./run.sh images/{}\''.format(path, name), shell=True)

