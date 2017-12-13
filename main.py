import search
import json
import network
import format
import rwfile
import os
import sys


def selectmusic(musicName):
    try:
        html = search.searchNeteMusic(musicName)
        musicsInfo = json.loads(html)['result']['songs']
        print('please select you want download music Lrc ID:')
        print('#########################################################################')
        for index, song in enumerate(musicsInfo):
            songname = song['name']
            songartists = song['artists'][0]['name']
            print(str(index) + ' ' + songname + '- ' + songartists)
        musicid = input('please input you want download lrc id :')
        if musicid == '':
            musicid = str(0)
        return musicsInfo[int(musicid)]
    except Exception as e:
        return None


def control(musicName):
    musicinfo = selectmusic(musicName)
    if musicinfo is not None:
        lrcurl = search.getLrcUrl(musicinfo)
        if lrcurl is not None:
            lrchtml = network.gethtml(lrcurl)
            if lrchtml is not None:
                lrc = format.foramtlrc(lrchtml)
                if lrc is not None:
                    rwfile.Writelrc(musicName, lrc)
                    print('download over')
                else:
                    rwfile.writelErrorlist(musicName)
            else:
                rwfile.writelErrorlist(musicName)
        else:
            rwfile.writelErrorlist(musicName)
    else:
        rwfile.writelErrorlist(musicName)


if __name__ == '__main__':
    print('########################### Get netease lrc  ###########################')
    print('########################### Creat By Machete ###########################')
    print('###########################   Version v1.3   ###########################')
    os.chdir('lrcs')
    while 1:
        print('###########################   option 1 download use list   ###########################')
        print('###########################   option 2 download use music name   ###########################')
        getType = input('please switch you want download option ')
        con = ''
        if getType == '1':
            musiclist = rwfile.readfile()
            for musicNmae in musiclist:
                control(musicNmae)
        elif getType == '2':
            musicName = search.getInput()
            control(musicName)
        else:
            print('you send wrong!')
        con = input('if you want stop please input Y or input other to continue:')
        if con.lower() == 'y':
            break
    rwfile.writelErrorlist('The above is the wrong file name, please check the file and manual mode Download')
    print('Bye Bye')
