import os
import json
from Channels import Channel
from Listeners import ListenerFactory
from Senders import SenderFactory


def read_channels_from_configfile(configfile):
    if not os.path.exists(configfile) or not os.path.isfile(configfile):
        raise ConfigFileError("Non-existent configuration file specified")

    with open(configfile) as infile:
        return read_channels_from_config(infile.read())


def read_channels_from_config(config_str):
    conf = json.loads(config_str)

    channels = []
    for channel in conf.keys():
        listener = ListenerFactory.create_listener_from_config(
                conf[channel]["listener"]
                )
        sender = SenderFactory.create_sender_from_config(
                conf[channel]["sender"]
                )
        channels.append(Channel(channel, listener, sender))

    return channels


class ConfigSyntaxError(BaseException):
    def __init__(self, value):
        BaseException.__init__(BaseException, value)
        self.parameter = value

    def __str__(self):
        return "Configuration syntax error: %s" % repr(self.parameter)


class ConfigFileError(IOError):
    def __init__(self, value):
        IOError.__init__(self, value)
        self.parameter = value

    def __str__(self):
        return "Configuration error: %s" % repr(self.parameter)
