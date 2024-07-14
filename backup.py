import re
from tqdm import tqdm
import requests
from pyquery import PyQuery
import time

name = input("name:")
file_all = input("file_all:")
url = 'https://www.2t58.com/so/{}/.html'.format(name)
response = requests.get(url)
doc = PyQuery(response.content)
names = doc(".name").items()
ex = '<div class="name"><a href="/song/(.*?).html" target="_mp3">.*?</a></div>'
musicIndex = re.findall(ex, response.text, re.S)
j = 1
for i in names:
    print(i.text(),[j])
    if j == 7:
        break
    j += 1
num = int(input("num:"))
smallmusicList = []
smallmusicList.append(musicIndex[num - 1])

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '26',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'Hm_lvt_b8f2e33447143b75e7e4463e224d6b7f=1690974946; Hm_lpvt_b8f2e33447143b75e7e4463e224d6b7f=1690976158',
    'Host': 'www.2t58.com',
    'Origin': 'https://www.2t58.com',
    'Referer': 'https://www.2t58.com/song/bWhzc3hud25u.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

for i in smallmusicList:
    data = {'id': i, 'type': 'music'}
    url2 = 'https://www.2t58.com/js/play.php'
    response2 = requests.post(url=url2, headers=headers, data=data)
    json_data = response2.json()
    musicList = json_data['url']
    musicResponse = requests.get(url=musicList)
    filename = json_data['title'] + '.mp3'

    qbar = tqdm(musicResponse.iter_content(chunk_size=1024),desc=filename,total=int(musicResponse.headers['Content-Length'])/1024,unit_scale=True)
    with open(file_all +"\\" + filename, 'wb') as f:
        for data in qbar:
            f.write(data)
        f.close()
        time.sleep(0.5)
        print(filename + '下载成功！')

