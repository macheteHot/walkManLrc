# -*- coding: utf8 -*-
import tkinter as tk
import tkinter.filedialog
import platform
import time
import sys

def readfile():
    filename = ''
    sysstr = platform.system()
    if (sysstr == "Windows"):
        print('Please select list.txt in windows start with 2 sens later')
        time.sleep(2)
        root = tk.Tk()
        filename = tkinter.filedialog.askopenfilename(filetypes=[("txt格式", "txt")])
        root.destroy()
    else:
        filename = input('please input you list path like /home/list.txt:')
    try:
        file_object = open(filename, 'r', encoding='UTF-8')
    except Exception as e:
        print('you input error is not list text or encode is not utf-8')
        sys.exit(0)
    file_list = []
    try:
        while 1:
            lines = file_object.readlines(100000)
            if not lines:
                break
            for line in lines:
                file_list.append(line.replace("\n", ""))
    finally:
        file_object.close()
    return file_list


def Writelrc(filename, lrctxt):
    try:
        f = open(filename + '.lrc', "w+")
        f.writelines(lrctxt)
        f.close()
    except Exception as e:
        writelErrorlist(filename)


def writelErrorlist(musicname):
    ef = open('errors.txt', 'a+')
    ef.writelines(musicname + "\n")
    ef.close()
