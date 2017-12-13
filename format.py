# -*- coding: utf8 -*-
import json
import re
import sys


def formatjson(str):
    try:
        musicID = json.loads(str)['result']['songs']['id']
    except Exception as e:
        print('look like has wrong')
        sys.exit(0)
    return musicID


def reduce(str):
    newlrc = re.findall(r'\[[\d]{2}:[\d]{2}.[\d]{3}\]', str)
    if len(newlrc) != 0:
        for lrctime in newlrc:
            oldtime = re.findall(r'[\d]{3}', lrctime)[0]
            str_list = list(oldtime)
            str_list.pop()
            newtime = "".join(str_list)
            str = re.sub(r'[\d]{3}', newtime, str, 1)
    else:
        pass
    return str


def foramtlrc(html):
    try:
        lrc = json.loads(html)['lrc']['lyric']
        newlrc = reduce(lrc)
        return newlrc
    except Exception as e:
        return None
