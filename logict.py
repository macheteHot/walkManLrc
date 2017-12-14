# -*- coding: utf8 -*-
import tkinter
from tkinter import *
from tkinter.filedialog import askdirectory
import platform, time, os, json, re, sys, urllib.request, urllib.parse


def searchNeteMusic(str):
    url = 'http://music.163.com/api/search/pc'
    header = {
        'Cookie': 'appver=1.5.0.75771',
        'Referer': 'http://music.163.com/'
    }
    values = {
        's': str,
        'offset': '1',
        'limit': '15',
        'type': '1'
    }
    html = post2web(url, values, header, str)
    return html


def formatjson(str):
    try:
        musicID = json.loads(str)['result']['songs']['id']
    except Exception as e:
        print('look like has wrong')
        sys.exit(0)
    return musicID


def getLrcUrl(musicinfo):
    try:
        musicid = musicinfo['id']
        url = 'http://music.163.com/api/song/lyric?os=osx&id=' + str(musicid) + '&lv=-1&kv=-1&tv=-1'
        return url
    except Exception as e:
        return None


def fixTimeLabel(str):
    str = re.sub(r'^\[[^\d].*\]', '', str)
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
    lyrics = []
    lrcs = json.loads(html)
    try:
        if 'lyric' in lrcs['lrc'] and lrcs['lrc']['lyric'] is not None:
            newlrc = fixTimeLabel(lrcs['lrc']['lyric'])
            lyrics.append(newlrc)
        if 'tlyric' in lrcs and lrcs['tlyric'].get('lyric') is not None:
            newtlrc = fixTimeLabel(lrcs['tlyric']['lyric'])
            lyrics.append(newtlrc)
        return lyrics
    except Exception as e:
        return None


def post2web(url, values, headers, musicname):
    # date format to reade
    data = urllib.parse.urlencode(values).encode('utf-8')
    #    create a  request,add url 、date、header
    request = urllib.request.Request(url, data, headers)
    try:
        html = urllib.request.urlopen(request).read().decode('utf-8')
        return html
    except Exception as e:
        print('网络出错啦，出错的音乐已经写入到error.txt文件中啦，请稍后手动下载')
        print('please download later')
        writelErrorlist(musicname)


def gethtml(url):
    try:
        request = urllib.request.Request(url)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        return html
    except Exception as e:
        return None


def post2web(url, values, headers, musicname):
    # date format to reade
    data = urllib.parse.urlencode(values).encode('utf-8')
    #    create a  request,add url 、date、header
    request = urllib.request.Request(url, data, headers)
    try:
        html = urllib.request.urlopen(request).read().decode('utf-8')
        return html
    except Exception as e:
        print('网络出错啦，出错的音乐已经写入到error.txt文件中啦，请稍后手动下载')
        writelErrorlist(musicname)


def getInput():
    musicName = input('请输入你想下载的音乐名(越详细越好 例如:暖暖 梁静茹):')
    print('#########################################################################')
    return musicName


def gethtml(url):
    try:
        request = urllib.request.Request(url)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        return html
    except Exception as e:
        return None


##循环数组
def eachFile(filepath):
    musicExnameList = ['.mp3', '.wav', '.dsf', '.dff', '.ogg', '.ape', '.cda', '.aac', '.mqa', 'm4a''.aif',
                       '.aiff', '.afc', '.aifc', '.mqa', '.flac']
    musiclist = []
    musicPath = os.listdir(filepath)
    for file in musicPath:
        exname = os.path.splitext(file)[1]
        if exname in musicExnameList:
            musiclist.append(os.path.splitext(file)[0])
    return musiclist


def readfile():
    sysstr = platform.system()
    if (sysstr == "Windows"):
        filePath = getMusicPath()
    else:
        filePath = input('please input you list path like /home/music:')
    musiclist = eachFile(filePath)
    return musiclist


def Writelrc(filename, lrctxt):
    try:
        os.remove(filename + '.lrc')
    except Exception:
        pass
    try:
        if len(lrctxt) == 1:
            f = open(filename + '.lrc', "w+")
            f.writelines(lrctxt[0])
            f.close()
        elif len(lrctxt) == 2:
            print('#####################检测到有翻译歌词#####################')
            print('####################选项1 下载混合歌词####################')
            print('####################选项2 下载原版歌词####################')
            print('####################选项3 下载翻译歌词####################')
            option = input('请输入下载选项,直接回车默认下载混合歌词:')
            if option == '':
                option = '1'
            if option == '1':
                lrcs = tolist(lrctxt[0])
                tlrcs = tolist(lrctxt[1])
                newlrcs = mixlrc(lrcs, tlrcs)
                nerlrc = "\n".join(newlrcs)
                f = open(filename + '.lrc', "a+")
                f.writelines(nerlrc)
                f.close()
            elif option == '2':
                f = open(filename + '.lrc', "a+")
                f.writelines(lrctxt[0])
                f.close()
            elif option == '3':
                f = open(filename + '.lrc', "a+")
                f.writelines(lrctxt[1])
                f.close()
            else:
                print('输入错误,已加入错误列表')
                writelErrorlist(filename)
        else:
            writelErrorlist(filename)
    except Exception as e:
        writelErrorlist(filename)


def writelErrorlist(musicname):
    ef = open('errors.txt', 'a+')
    ef.writelines(musicname + "\n")
    ef.close()


def getMusicPath():
    root = Tk()
    root.withdraw()
    dirname = askdirectory(parent=root, initialdir="/", title='请选择你的音乐目录')
    return dirname


def tolist(str):
    fixlist = fixTimeLabel(str)
    list = re.findall(r'\[.*', fixlist)
    return list


def mixlrc(lrcs, tlrcs):
    lrcslist = []
    for lrc in lrcs:
        lrcTimelabel = re.findall(r'\[.*\]', lrc)[0]
        lrcslist.append(lrcTimelabel)
    for forindex, tlrc in enumerate(tlrcs):
        tlrctimelabel = re.findall(r'\[.*\]', tlrc)[0]
        if tlrctimelabel in lrcslist:
            lrcs.insert(int(lrcslist.index(tlrctimelabel)) + forindex + 1, tlrc)
    return lrcs
