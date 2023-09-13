import aiohttp
import asyncio


URL = 'http://patiatest_web.test'

headers = {
    'Authorization': 'Bearer ' + 'cAQUqXpjrNzpoPkNiaYrwpXPw9l08kpO6rDZbyLi',
    'Accept': 'application/json'
}


async def get_computer(serial_number):

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(URL + '/api/computer/') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html)

