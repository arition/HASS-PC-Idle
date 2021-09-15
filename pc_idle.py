import asyncio

import aiohttp
import win32api
import yaml

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)


def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


async def trigger(action):
    print(action)

    headers = {
        'Authorization': 'Bearer {}'.format(config['token']),
        'content-type': 'application/json',
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for entity_id in config['home_assistant_booleans']:
            try:
                url = f"{config['endpoint_url']}/services/input_boolean/{action}"
                data = {"entity_id": "input_boolean.{}".format(entity_id)}
                response = await session.post(url, json=data)
                await response.text()
                response.close()
            except Exception as e:
                print(e)


async def main():
    while True:
        if getIdleTime() > config['idle_time']:
            await trigger("turn_on")
        else:
            await trigger("turn_off")
        await asyncio.sleep(config['poll_time'])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
