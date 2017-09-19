#-*- coding:utf-8 -*-
""" This python scripts download the photographs in the highest resolution
and the sound scape and background music of all the locations in
[Sony Global - alpha CLOCK: WORLD TIME, CAPTURED BY alpha](www.sony.net/united/clock/).
For more infomation please check https://github.com/kenkangxgwe/Sony-Global-Website-Media-Scraper"""

import os
import sys
import zipfile
import json
import requests

def download(address, target):
    """Download file from the given address to a temp folder at target path."""
    FileName    = address.split('/')[-1]
    print('Downloading ' + FileName + ' ...')
    response    = requests.get(address, stream = True)
    TotalLength = response.headers.get('content-length')
    with open(target + '\\Temp_Downloads\\' + FileName, 'wb') as f: # .write(urllib2.urlopen(address).read())
        if TotalLength is None:
            f.write(response.content)
        else:
            DownLength  = 0
            TotalLength = int(TotalLength)
            for data in response.iter_content(chunk_size = TotalLength / 50):
                DownLength += len(data)
                f.write(data)
                Done = float(50 * DownLength / TotalLength)
                sys.stdout.write('\r[' + '=' * int(Done) + ' ' * (50 - int(Done)) + '] ' + str(int(Done * 2)) + '%')
                sys.stdout.flush()
            sys.stdout.write('\r\n')

        return target + '\\Temp_Downloads\\' + FileName

def unzip(path, target):
    """To unzip zipfile at path to target folder."""
    if zipfile.is_zipfile(path):
        print('Extracting ' + path + ' to ' + target + ' ...')
        zipfile.ZipFile(path, 'r').extractall(target)
        os.remove(path)

def move(path, target):
    """To move from path to target folder."""
    if os.path.exists(path):
        print('Moving ' + path + ' to ' + target + ' ...')
        os.rename(path, target + '\\' + path.split('\\')[-1])

def convert2json(address):
    """Convert the javascript object to json.
    Address: the javascript url"""
    import PyV8

    JsExe = PyV8.JSContext()
    JsExe.enter()

    open("heritage_data.js", "wb").write(requests.get(address).content)

    a_clock_heritage_data_json = JsExe.eval(open('heritage_data.js').read()
                                            + 'JSON.stringify(a_clock_heritage_data);')
    open('heritage_data.json', 'w').write(a_clock_heritage_data_json)

    return json.loads(a_clock_heritage_data_json)

def workflow():
    """The main workflow"""
    fp_filename              = lambda id, num: (id + '_3840_2160_fp_' + num)
    ss_filename              = lambda id, num: (id + '_3840_2160_ss_' + num)
    music_filename           = lambda id: ('theme_song_of_world_heritage_' + id)
    sound_filename           = lambda addr: (addr.split('/')[-1].rsplit('.', 1)[0])
    fp_address               = lambda id, num: ('http://di.update.sony.net/ACLK/wallpaper/' + id + '/3840_2160/fp/' + fp_filename(id, num) + '.zip')
    ss_address               = lambda id, num: ('http://di.update.sony.net/ACLK/wallpaper/' + id + '/3840_2160/ss/' + ss_filename(id, num) + '.zip')
    music_address            = lambda id: ('http://www.sony.net/united/clock/assets/sound/' + music_filename(id) + '.mp3')
    sound_address            = lambda addr: ('http://hq.update.sony.net.edgesuite.net/' + addr)
    heritage_data_js_address = 'http://www.sony.net/united/clock/assets/js/heritage_data.js'
    heritage_data            = convert2json(heritage_data_js_address)

    pwd = ur"D:\Sony Global"

    if not os.path.exists(pwd):
        os.mkdir(pwd)

    if not os.path.exists('Theme Song of World Heritage'):
        os.mkdir('Theme Song of World Heritage')

    if not os.path.exists('Temp_Downloads'):
        os.mkdir('Temp_Downloads')

    for heritage in heritage_data:
        os.chdir(pwd)
        FolderName = heritage['id'].capitalize()
        if not os.path.exists(FolderName):
            os.mkdir(FolderName)
        os.chdir(FolderName)

        # Write json file
        print('Writing ' + FolderName + '.json ...')
        open(FolderName + '.json', 'w').write(json
                                              .dumps(
                                                  heritage,
                                                  ensure_ascii=False,
                                                  sort_keys=True,
                                                  indent=4,
                                                  separators=(',', ': '))
                                              .encode('utf-8'))

        # Download fp photos
        if not os.path.exists(FolderName + '_fp'):
            os.mkdir(FolderName + '_fp')
        os.chdir(FolderName + '_fp')
        for num in heritage['fp']:
            try:
                trynum = int(num)
                if not os.path.exists(fp_filename(heritage['id'], num) + '.jpg'):
                    unzip(download(fp_address(heritage['id'], num), pwd), os.getcwdu())
            except ValueError:
                pass

        # Download ss photos
        os.chdir('..')
        if not os.path.exists(FolderName + '_ss'):
            os.mkdir(FolderName + '_ss')
        os.chdir(FolderName + '_ss')
        for ss in heritage['ex']:
            try:
                trynum = int(ss['num'])
                if not os.path.exists(ss_filename(heritage['id'], ss['num']) + '.jpg'):
                    unzip(download(ss_address(heritage['id'], ss['num']), pwd), os.getcwdu())
            except ValueError:
                pass

        # Download soundscape
        os.chdir('..')
        try:
            if not os.path.exists(sound_filename(heritage['soundscape']['media']['mp3']) + '.mp3'):
                move(download(sound_address(heritage['soundscape']['media']['mp3']), pwd),
                     os.getcwdu())
        except TypeError:
            pass

        # Download theme song
        os.chdir(pwd + '\\Theme Song of World Heritage')
        try:
            if not os.path.exists(music_filename(heritage['music']) + '.mp3'):
                move(download(music_address(heritage['music']), pwd), os.getcwdu())
        except AttributeError:
            pass

    if not os.listdir(pwd + '\\Temp_Downloads'):
        os.rmdir(pwd + '\\Temp_Downloads')

if __name__ == "__main__":
    workflow()
