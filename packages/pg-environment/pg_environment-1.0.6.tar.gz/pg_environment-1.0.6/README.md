# pg env

python game environment

## rules

- environment is depends on workspace directory name

    if dir name contains character like "prod", "test", "dev"

    global conf key "environment" will be set to "prod", "test", "dev"

    else it is "dev"

- default port depends on workspace directory name too

    if the last part of dir name split by "_" is all digit

    it will be set as global conf key "host_port"

    else "host_port" will be set as 8001

    or merged from json config file locate at ./conf/${environment}.json

- project dir name

  xxxxtest_channel_port

  xxxxprod_channel

  xxxxdev_port

  xxxxprod

  xxxx