__author__ = 'ding'
from setting import clct_channel
from main import process_channel


def test():
    channel = clct_channel.find_one({"channelId":101446})
    process_channel(channel)