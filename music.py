import re
from tqdm import tqdm
import requests
from pyquery import PyQuery


def get_music_index(name):
    url = f'https://www.2t58.com/so/{name}/.html'
    response = requests.get(url)
    doc = PyQuery(response.content)
    names = doc(".name").items()
    a = 1
    for j in names:
        print(f"选项 {a}: {j.text()}")
        a += 1
        if a == 8:
            break
    ex = '<div class="name"><a href="/song/(.*?).html" target="_mp3">.*?</a></div>'
    return re.findall(ex, response.text, re.S)

def download_music(file_all, music_id):
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
    data = {'id': music_id, 'type': 'music'}
    url2 = 'https://www.2t58.com/js/play.php'
    resp2 = requests.post(url=url2, headers=headers, data=data)
    json_data = resp2.json()
    music_url = json_data['url']
    music_response = requests.get(url=music_url, stream=True)
    filename = json_data['title'] + '.mp3'

    with open(f"{file_all}\\{filename}", 'wb') as f:
        qbar = tqdm(music_response.iter_content(chunk_size=1024), desc=filename, total=int(music_response.headers['Content-Length'])/1024, unit_scale=True)
        for data in qbar:
            f.write(data)
    print(f"{filename} 下载成功！")

def main():
    name = input("name:")
    file_all = input("file_all:")
    music_index = get_music_index(name)
    num = int(input("num:"))
    selected_music_id = music_index[num - 1]
    download_music(file_all, selected_music_id)

if __name__ == "__main__":
    main()
