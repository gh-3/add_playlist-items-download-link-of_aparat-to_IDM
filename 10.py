import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# first page that extract playlist items

url = 'https://www.aparat.com/v/uRCsU'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

playlist_body = soup.find('div', attrs={'class': 'playlist-body'})
playlist_items = playlist_body.find_all('div', attrs={'class': 'item'})
no_items = len(playlist_items)

playlist = soup.find('header', attrs={'class': 'playlist-head'})
path = 'd:\\hello\\' + \
    playlist.find('a', attrs={'id': 'playlistTitle'}).get_text()
try:
    os.mkdir(path)
except:
    print('This folder is exist')


# add zero's befor index
def fix_index(index):
    a = str(index)
    b = str(no_items)
    c = len(b) - len(a)
    a = "0" * c + a
    return a


# second page that open desired item and download it
def downlaod_video(url, path=os.getcwd(), index=None):
    # درخواست صفحه وب
    page = requests.get(url)

    # بارگزاری صفحه وب
    soup = BeautifulSoup(page.content, 'html.parser')
    # دریافت عنوان ویدیو

    # id=videoTitle
    title = soup.find('h1', attrs={'id': 'videoTitle'}).text.strip()
    # ایجاد مسیر ذخیر فایل
    file_name = fix_index(index) + '_' + title + \
        '.mp4' if index != None else title + '.mp4'
    # print(file_name)
    file_path = os.path.join(path, file_name)

    # اگر فایل قبلا وجود داشت دانلود نمی کنه
    if os.path.exists(file_path) == False:
        # بدست آوردن آدرس فایل ویدیو
        file_url = soup.find(
            'div', attrs={'class': 'download-dropdown'}).find_all('li')[-1].find('a')['href']
        command = f"idman /d {file_url} /p \"{path}\" /f \"{file_name}\" /a"
        os.system(command)


with tqdm(range(no_items)) as pbar:
    for index, a in enumerate(playlist_items):
        a_tag = a.find('a', href=True, text=True)
        item_url = 'https://www.aparat.com' + a_tag['href']
        downlaod_video(item_url, path, index + 1)
        pbar.update(1)
