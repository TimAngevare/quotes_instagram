import requests
import pandas as pd 
from random import randint
from PIL import Image, ImageFont, ImageDraw, ImageStat
from instabot import Bot
from os import system
from datetime import datetime

today = datetime.now()


api_key_unsplash = "******"

def wrap_by_word(s, n):
    a = s.split()
    ret = ''
    for i in range(0, len(a), n):
        ret += ' '.join(a[i:i+n]) + '\n'

    return ret

def get():
    unsplash_link = "https://api.unsplash.com/photos/random/?client_id="
    query = "&query=dark"

    image_json = requests.get(unsplash_link + api_key_unsplash + query)
    parse = image_json.json()
    img_link = parse["urls"]['full']

    image = requests.get(img_link).content
    with open('insta_pic.jpg', 'wb') as image_file:
        image_file.write(image)
        image_file.close()

    quotes_data = pd.read_csv('quotes_data.csv')
    row = quotes_data.iloc[randint(0,len(quotes_data) - 1)]
    text = wrap_by_word(row['quote'], 3)
    author = row['author']
    try:
        author = author.split(',')[0]
    except:
        pass
    image = Image.open('insta_pic.jpg')
    image.thumbnail([1080, 1080], Image.ANTIALIAS)
    width, height = image.size
    print(width, height)
    if width / height < 0.8:
        image.resize((width,width),Image.ANTIALIAS)
    quote_font = ImageFont.truetype('RobotoMono.ttf', 45)

    editable_image = ImageDraw.Draw(image)
    stat = ImageStat.Stat(image)
    r,g,b = stat.mean
    brightness = r + g + b / 3 
    print(brightness)
    if brightness < 175:
        color = (225,225,225)
    else:
        color = (50,50,50)
    editable_image.text((width / 2 - 300,height / 2 - 50), text + '\n-' + author, color, font=quote_font)

    image.save('insta_pic.jpg')



def post_insta():
    system('rm -rf config')

    bot = Bot()
    bot.login(username = "your.quotedaily", password = '******')

    bot.upload_photo('insta_pic.jpg', caption= today.strftime("%a - %dst of %b") + '\n #dailyquotesforyou #dailyquotestoliveby #dailyquotes4u #dailyquoted')

def start():
    get()
    post_insta()