import aiohttp
import asyncio

URL = 'http://patiatest_web.test'

headers = {
    'Authorization': 'Bearer ' + 'cAQUqXpjrNzpoPkNiaYrwpXPw9l08kpO6rDZbyLi',
    'Accept': 'application/json'
}


async def get_config():
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(URL + '/api/config_data/') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            r = await response.text()
            return response

async def get_computer(serial_number):
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(URL + '/api/computer/' + serial_number) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            r = await response.text()
            return response
        
async def save_computer(computer):
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(URL + '/api/computers', data=computer) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            r = await response.text()
            return response
