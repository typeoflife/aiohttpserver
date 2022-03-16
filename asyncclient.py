import aiohttp
import asyncio

URL = 'http://127.0.0.1:8080/'

async def main():
    async with aiohttp.ClientSession() as session:

        # async with session.get(URL + health') as response:
        #     print(await response.json())

        # async  with session.get(URL +'user/1',) as response:
        #     print(await response.json())


        # async  with session.post(URL +'user', json={
        #     'username': 'maxim',
        #     'email': 'maxim@mail.ru',
        #     'password': '111222'
        # }) as response:
        #     print(await response.json())

        async  with session.get(URL +'adv/5',) as response:
            print(await response.json())

        # async  with session.post(URL +'adv', json={
        #     'title': 'theme2',
        #     'text': 'information_text',
        #     'user_id': '1'
        # }) as response:
        #     print(await response.json())



asyncio.run(main())
