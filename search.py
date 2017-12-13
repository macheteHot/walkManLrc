import network
import sys
import rwfile


def getInput():
    musicName = input('Please Input you want download Music Name:')
    print('#########################################################################')
    return musicName


def searchNeteMusic(str):
    url = 'http://music.163.com/api/search/pc'
    header = {
        'Cookie': 'appver=1.5.0.75771',
        'Referer': 'http://music.163.com/'
    }
    values = {
        's': str,
        'offset': '1',
        'limit': '10',
        'type': '1'
    }
    html = network.post2web(url, values, header, str)
    return html


def getLrcUrl(musicinfo):
    try:
        musicid = musicinfo['id']
        url = 'http://music.163.com/api/song/lyric?id=' + str(musicid) + '&lv=-1&kv=-1'
        # translater lrc
        # tlycr = input('do you want download translate lry (y/n):')
        # if tlycr == 'y':
        #     url = url + '&tv=-1'
        # else:
        #     pass
        return url
    except Exception as e:
        return None
