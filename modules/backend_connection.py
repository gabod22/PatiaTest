import aiohttp
import json

URL = 'http://patiatest_app.test'

headers = {
    'Authorization': 'Bearer ' + 'cAQUqXpjrNzpoPkNiaYrwpXPw9l08kpO6rDZbyLi',
    'Accept': 'application/json'
}


async def get_config():
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(URL + '/api/config_data/') as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                r = await response.text()
                res = json.loads(r)
                print(type(res))
                return res
    except aiohttp.ClientConnectionError as e:
        print('Error al conectar con el servidor, revisar el servidor o la url')

async def get_computer(serial_number):
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(URL + '/api/computer/' + serial_number) as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                r = await response.text()
                return response,r
    except aiohttp.ClientConnectionError as e:
        print('Error al conectar con el servidor, revisar el servidor o la url')
        
async def save_computer(computer):
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(URL + '/api/computers', data=computer) as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                r = await response.text()
                return (response,r)
    except aiohttp.ClientConnectionError as e:
        print('Error al conectar con el servidor, revisar el servidor o la url')
        return {'error': 'No se pudo conectar al servidor'}

async def save_inspection(computer):
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(URL + '/api/computers', data=computer) as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                r = await response.text()
                return response
    except aiohttp.ClientConnectionError as e:
        raise Exception("No se puede conectar el servidor, el servidor no responde o la url está mal")

