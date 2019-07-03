# coding: utf-8

import os
import sys
import time
from slackclient import SlackClient

kmcToken = os.environ["KMCtk"]
kc3Token = os.environ["KC3tk"]

kmcSC = SlackClient(kmcToken)
kc3SC = SlackClient(kc3Token)

def postKMC(msg, channel="C29T0SANS"):
    kmcSC.api_call(
        "chat.postMessage",
        channel=channel,
        text=msg,
        icon_emoji=":mawarunos:",
        unfurl_links=unfurl,
        username="KC3bot"
    )

def tunnelToKMC(rtm):
    try:
        postKMC(rtm["text"])
    except: # 一回だけリトライ
        time.sleep(5)
        postKMC(rtm["text"])


if __name__ == "__main__":
    if kc3SC.rtm_connect():
        postKMC("KC3に接続")
        while True:
            try:
                for rtm in kc3SC.rtm_read():
                    if rtm["type"] == "message":
                        if "subtype" not in rtm and "text" in rtm:
                            tunnelToKMC(rtm)
            except:
                print(str(datetime.datetime.now) + ":")
                print(sys.exc_info()[0])
                time.sleep(10)
                if kc3SC.rtm_connect():
                    pass
                else:
                    print("Connection Failed!")
                    time.sleep(100)
            time.sleep(5)
    else:
        print("Connection Failed")