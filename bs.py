from bs4 import BeautifulSoup
import requests
import vk_requests
import time
import json


def upload_photo(url):
    pic = requests.get(url)  # requesting photo
    f = open('C:\\Users\\PIRAMIDA 1\\Desktop\\pics\\pic.jpg',
             'wb')
    f.write(pic.content)  # downloading picture
    f.close()
    uploading_photo = requests.post(server, files={'photo': open(f.name, 'rb')})  # uploading photo
    json_response = json.loads(uploading_photo.text)
    saved_photo = api.photos.saveMessagesPhoto(photo=json_response['photo'],
                                               server=json_response['server'],
                                               hash=json_response['hash'])[0]
    return saved_photo

def send_message(u_id, _attachment, _owner_id, _photo_id):  # method for sending posts
    api.messages.send(peer_id=u_id, attachment="{0}{1}_{2}".format(_attachment, _owner_id, _photo_id))


api = vk_requests.create_api(app_id='lul', login='nice', password='memes',
                             scope='messages, photos')

server = api.photos.getMessagesUploadServer()
server = server['upload_url']

user = '35933425'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

page = requests.get('http://www.reddit.com/r/me_irl/', headers=headers)

soup = BeautifulSoup(page.content, 'lxml')
# TODO: Add user-interactions with bot (i.e. let user choose when to get next meme/select next page)
# next_page = soup.find('span', {'class': 'next-button'}).find('a').get('href')
# print(next_page)
post_list = soup.findAll('p', {'class': 'title'})

for each in post_list:
    found = each.find('a').get('data-href-url')
    print('found: ', found)
    
    if found.find('/r/me_irl/comments/') != -1:
        found_page = requests.get('https://www.reddit.com' + found, headers=headers)
        soup_page = BeautifulSoup(found_page.content, 'lxml')

        image = soup_page.find('img', {'class': 'preview'}).get('src')
        saved_photo = upload_photo(image)

        send_message(user, _attachment="photo", _photo_id=saved_photo['id'], _owner_id=saved_photo['owner_id'])
        time.sleep(1)
        continue

    if found.find('reddituploads') != -1:
        saved_photo = upload_photo(found)
        send_message(user, _attachment="photo", _photo_id=saved_photo['id'], _owner_id=saved_photo['owner_id'])

        time.sleep(1)
        continue

    if ('.jpg' or '.png' or '.jpeg' or 'reddituploads') in found:
        saved_photo = upload_photo(found)
        send_message(user, _attachment="photo", _photo_id=saved_photo['id'], _owner_id=saved_photo['owner_id'])

        time.sleep(1)
        continue

    if 'imgur' in found:
        photo_url = 'http://i.imgur.com' + found[found.rfind('/'):] + '.jpg'
        saved_photo = upload_photo(photo_url)
        send_message(user, _attachment="photo", _photo_id=saved_photo['id'], _owner_id=saved_photo['owner_id'])

        time.sleep(1)
