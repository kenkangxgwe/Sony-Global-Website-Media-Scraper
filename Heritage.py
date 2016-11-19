#-*- coding:utf-8 -*-
import os, sys
import requests
import PyV8, json
import zipfile

pwd = u"D:\Sony Global"
if not os.path.exists(pwd):
    os.mkdir(pwd)

heritage_data_js_address = 'http://www.sony.net/united/clock/assets/js/heritage_data.js' 
open("heritage_data.js","wb").write(requests.get(heritage_data_js_address).content)

def download(address):
    FileName = address.split('/')[-1]
    print('Downloading ' + FileName + ' ...')
    response = requests.get(address, stream = True)
    TotalLength = response.headers.get('content-length')
    with open(pwd + '\\Temp_Downloads\\' + FileName ,'wb') as f: # .write(urllib2.urlopen(address).read())
        if TotalLength is None:
            f.write(response.content)
        else:
            DownLength = 0
            TotalLength = int(TotalLength)
            for data in response.iter_content(chunk_size = TotalLength / 50):
                DownLength += len(data)
                f.write(data)
                Done = float(50 * DownLength / TotalLength)
                sys.stdout.write('\r[' + '=' * int(Done) + ' ' * (50 - int(Done)) + '] ' + str(int(Done * 2)) + '%')
                sys.stdout.flush()
            sys.stdout.write('\r\n')
        return pwd + '\\Temp_Downloads\\' + FileName

def unzip(path, target):
    if zipfile.is_zipfile(path):
        print('Extracting ' + path + ' to ' + target + ' ...')
        zipfile.ZipFile(path, 'r').extractall(target)
        os.remove(path)

def move(path, target):
    if os.path.exists(path):
        print('Moving ' + path + ' to ' + target + ' ...')
        os.rename(path, target + '\\' + path.split('\\')[-1])

fpfilename = lambda id, num : id + '_3840_2160_fp_' + num 
ssfilename = lambda id, num : id + '_3840_2160_ss_' + num 
musicfilename = lambda id : 'theme_song_of_world_heritage_' + id
soundfilename = lambda addr : addr.split('/')[-1].rsplit('.',1)[0]

fpaddress = lambda id, num : 'http://di.update.sony.net/ACLK/wallpaper/' + id + '/3840_2160/fp/' + fpfilename(id, num) + '.zip'
ssaddress = lambda id, num : 'http://di.update.sony.net/ACLK/wallpaper/' + id + '/3840_2160/ss/' + ssfilename(id, num) + '.zip'
musicaddress = lambda id : 'http://www.sony.net/united/clock/assets/sound/' + musicfilename(id) + '.mp3'
soundaddress = lambda addr : 'http://hq.update.sony.net.edgesuite.net/' + addr

JsExe = PyV8.JSContext()
JsExe.enter()
a_clock_heritage_data_json = JsExe.eval(open('heritage_data.js').read() + 'JSON.stringify(a_clock_heritage_data);')
open('heritage_data.json','w').write(a_clock_heritage_data_json)

heritage_data = json.loads(a_clock_heritage_data_json)

os.chdir(pwd)
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
    open(FolderName + '.json', 'w').write(json.dumps(heritage, ensure_ascii=False, sort_keys = True, indent=4, separators=(',', ': ')).encode('utf-8'))
    # Download fp photos
    if not os.path.exists(FolderName + '_fp'):
        os.mkdir(FolderName + '_fp')
    os.chdir(FolderName + '_fp')
    for num in heritage['fp']:
        try:
            trynum = int(num)
            if not os.path.exists(fpfilename(heritage['id'], num) + '.jpg'):
                unzip(download(fpaddress(heritage['id'], num)), os.getcwdu())
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
            if not os.path.exists(ssfilename(heritage['id'], ss['num']) + '.jpg'):
                unzip(download(ssaddress(heritage['id'], ss['num'])), os.getcwdu())
        except ValueError:
            pass
    os.chdir('..')
    # Download soundscape
    try:
        if not os.path.exists(soundfilename(heritage['soundscape']['media']['mp3']) + '.mp3'):
            move(download(soundaddress(heritage['soundscape']['media']['mp3'])), os.getcwdu())
    except TypeError:
        pass
    os.chdir(pwd + '\\Theme Song of World Heritage')
    # Download theme song
    try:
        if not os.path.exists(musicfilename(heritage['music']) + '.mp3'):
            move(download(musicaddress(heritage['music'])), os.getcwdu())
    except AttributeError:
        pass

if not os.listdir(pwd + '\\Temp_Downloads'):
    os.rmdir(pwd + '\\Temp_Downloads')
