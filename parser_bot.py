

import csv
import datetime
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule
import time
import json
from aiogram import Bot, Dispatcher, executor, types
API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_message(msg: types.Message):
    number = 0
    def parser():
        if not os.path.exists(r''):
            os.mkdir(r'')
            os.mkdir(r'')

        pagenation = 1

        data_croniter = datetime.datetime.now()
        data_now = data_croniter.strftime('%m.%d.%Y %H:%M')
        print(data_now)
        while True:

            url = f'{pagenation}'
            print(url)
            headers = {                       }
            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            all_product_href = soup.find_all(
                class_='')
            info = []
            if (len(all_product_href)):
                for item in all_product_href:
                    item_memory = item.find(
                        class_='').next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.text
                    memory = item_memory.strip()[:-3]
                    if str(memory) != 'GD' is not int(memory) > 6:
                        item_name = item.find('a', class_='').text
                        item_article = item.find(class_='').text
                        article = str(item_article).strip()
                        article = article[12:]
                        try:
                            item_sale = item.find(
                                class_='').text
                            item_sale = item_sale.replace(' ', '')
                        except AttributeError:
                            item_sale = '0'
                        info.append(
                            {
                                'артикль': article,
                                'время': data_now,
                                'название': item_name,
                                'аперативка': item_memory.strip(),
                                'цена': item_sale.strip(),
                            }
                        )

                pagenation += 1
            else:
                break
            with open(f'{pagenation}.json',
                      mode='w') as file:
                json.dump(info, file, indent=4, ensure_ascii=False)

        direct = os.listdir(r'')
        col_files = len(direct)
        number_file = 2

        df = pd.read_json(f'{direct[1]}')
        df.to_csv(f'{number}.csv', mode='w')
        for i in range(2, col_files):
            pd.set_option('display.max_columns', 7)
            df = pd.read_json(f'{direct[i]}')
            number_file += 1
            df.to_csv(f'{number}.csv', mode='a',
                      header=False)
        sump_last_file = os.listdir(r'')
        df1 = pd.read_csv('.csv')
        df2 = pd.read_csv(f'{sump_last_file[-1]}')
        df3 = df1.merge(df2, how='outer', left_on='артикль', right_on='артикль', indicator=True)
        df3['разница цен'] = df3['цена_x'] - df3['цена_y']
        up = df3[df3['разница цен'] < 0][['время_x', 'артикль', 'название_y', 'цена_x', 'цена_y']]
        down = df3[df3['разница цен'] > 0][['время_x', 'артикль', 'название_y', 'цена_x', 'цена_y']]
        print('подорожание', up)
        print('дешевеет', down)

    sump_last_file = os.listdir(r'')
    df1 = pd.read_csv('.csv')
    df2 = pd.read_csv(
        f'{sump_last_file[-1]}')
    df3 = df1.merge(df2, how='outer', left_on='артикль', right_on='артикль', indicator=True)
    df3['разница цен'] = df3['цена_x'] - df3['цена_y']
    up = df3[df3['разница цен'] < 0][['артикль', 'название_y', 'цена_x', 'цена_y']]
    down = df3[df3['разница цен'] > 0][['артикль', 'название_y', 'цена_x', 'цена_y']]
    print('подорожание', up)
    print('дешевеет', down)
    w = 'подорожание', up, 'дешевеет', down
    r = 'дешевеет', down
    await bot.send_message(msg.from_user.id, r)

    schedule.every(1).seconds.do(parser)
    while True:
        schedule.run_pending()
        time.sleep(1)
        number += 1
        print(number)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)