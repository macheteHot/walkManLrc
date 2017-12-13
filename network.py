import urllib.request
import urllib.parse
import rwfile


def post2web(url, values, headers, musicname):
    # date format to reade
    data = urllib.parse.urlencode(values).encode('utf-8')
    #    create a  request,add url 、date、header
    request = urllib.request.Request(url, data, headers)
    try:
        html = urllib.request.urlopen(request).read().decode('utf-8')
        return html
    except Exception as e:
        print('look like you network has some error you error music is write to error.txt')
        print('please download later')
        rwfile.writelErrorlist(musicname)


def gethtml(url):
    try:
        request = urllib.request.Request(url)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        return html
    except Exception as e:
        return None
