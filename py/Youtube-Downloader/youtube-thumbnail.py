from uuid import uuid4
from requests import get
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TALB
from sys import argv
from os import system, remove

with open('youtube-dl-tempfile.txt', 'r') as f :
    file = f.readline()
    file = file.replace('\n', '')

with open('youtube-dl-tempfile.txt', 'w') as f :
    mp3file = file.replace('.m4a', '.mp3')
    f.write(mp3file)
    f.close()    
    
system(f'ffmpeg -i "{file}" "{mp3file}"')
remove(file)

url = argv[1]

if 'youtu.be' in url :  
    id = url.split("/",3)[3]
elif '&' in url :
    id = url.split("=",1)[1]
    id = id.split("&",1)[0]
else :
    id = url.split("=",1)[1]

thumbnailurl= f'https://img.youtube.com/vi/{id}/maxresdefault.jpg'
r = get(thumbnailurl)
thumbnail = f'{uuid4()}.jpg'

with open(thumbnail, 'wb') as f:
    f.write(r.content)

audio = ID3(mp3file)

with open(thumbnail, 'rb') as albumart:
    audio['APIC'] = APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3, desc=u'Cover',
                        data=albumart.read()
                    )

audio["TALB"] = TALB(encoding = 3, text = u'YouTube')
audio["TPE1"] = TPE1(encoding = 3, text = u'YouTube')
audio["TIT2"] = TIT2(encoding = 3, text = u''+mp3file.replace('.mp3', '')+'')
audio.save()

remove(thumbnail)
