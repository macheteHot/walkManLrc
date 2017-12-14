import logict
import os
import json


def selectmusic(musicName):
    try:
        html = logict.searchNeteMusic(musicName)
        musicsInfo = json.loads(html)['result']['songs']
        print('#########################################################################')
        for index, song in enumerate(musicsInfo):
            songname = song['name']
            songartists = song['artists'][0]['name']
            print(str(index + 1) + ' ' + songname + '- ' + songartists)
        musicid = input('请输入你想要下载的音乐ID ，直接回车默认选择1号:')
        if musicid == '':
            musicid = 0
        else:
            musicid = int(musicid) - 1
        return musicsInfo[int(musicid)]
    except Exception as e:
        return None


def control(musicName):
    musicinfo = selectmusic(musicName)
    if musicinfo is not None:
        lrcurl = logict.getLrcUrl(musicinfo)
        if lrcurl is not None:
            lrchtml = logict.gethtml(lrcurl)
            if lrchtml is not None:
                lrc = logict.foramtlrc(lrchtml)
                if lrc is not None and len(lrc) != 0:
                    logict.Writelrc(musicName, lrc)
                    print('下载完成')
                else:
                    logict.writelErrorlist(musicName)
            else:
                logict.writelErrorlist(musicName)
        else:
            logict.writelErrorlist(musicName)
    else:
        logict.writelErrorlist(musicName)


if __name__ == '__main__':
    print('########################### Machete 歌词下载器  ###########################')
    print('########################### Creat By Machete ###########################')
    print('###########################   Version v2.4   ###########################')
    os.chdir('lrcs')
    while 1:
        getType = None
        print('###########################   选项1 批量下载   ###########################')
        print('###########################   选项2 单首下载   ###########################')
        getType = input('请输入选项号 ')
        con = ''
        if getType == '1':
            musiclist = logict.readfile()
            for musicNmae in musiclist:
                control(musicNmae)
        elif getType == '2':
            musicName = logict.getInput()
            control(musicName)
        else:
            print('输入错误啦')
        con = None
        con = input('如果想继续使用，请输入y，输入其他或回车停止')
        if con.lower() != 'y':
            break
    logict.writelErrorlist('#######################以上是错误的歌曲信息，请对照使用选项2单首下载模式下载，下载完成后请删除本文件#######################')
    print('再见！')
