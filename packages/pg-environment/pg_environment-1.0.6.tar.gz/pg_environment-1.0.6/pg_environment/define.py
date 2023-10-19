from enum import Enum, unique
ENV_TIMEZONE = "time_zone"
ENV_HOSTIP = "host_ip"
ENV_HOSTPORT = "host_port"
ENV_ENVIRONMENT = "environment"
ENV_PWD = "pwd"
ENV_CHANNEL = "channel"
ENV_DEBUG = "debug"
DEFAULT_CONF = {
    ENV_TIMEZONE: "US/Eastern",
    ENV_HOSTIP: "0.0.0.0",
    ENV_HOSTPORT: 8001,
    ENV_DEBUG: True,
    ENV_CHANNEL: ""
}


@unique
class EnvType(Enum):
    TEST = "test"
    DEV = "dev"
    PROD = "prod"

