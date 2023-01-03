import asyncio
import signal

import aiohttp
import win32api
import yaml

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)


def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


async def trigger_idle(action):
    print(f'idle: {action}')

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


async def trigger_start(action):
    print(f'start: {action}')

    headers = {
        'Authorization': 'Bearer {}'.format(config['token']),
        'content-type': 'application/json',
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for entity_id in config['home_assistant_start_booleans']:
            try:
                url = f"{config['endpoint_url']}/services/input_boolean/{action}"
                data = {"entity_id": "input_boolean.{}".format(entity_id)}
                response = await session.post(url, json=data)
                await response.text()
                response.close()
            except Exception as e:
                print(e)


async def main():
    await trigger_start("turn_on")

    run_loop = True

    async def on_close(*args):
        nonlocal run_loop
        run_loop = False
        await trigger_start("turn_off")
        return True

    signal.signal(signal.SIGINT, lambda *args: asyncio.create_task(on_close()))
    signal.signal(signal.SIGTERM, lambda *args: asyncio.create_task(on_close()))

    while run_loop:
        if getIdleTime() > config['idle_time']:
            await trigger_idle("turn_on")
        else:
            await trigger_idle("turn_off")
        await asyncio.sleep(config['poll_time'])

asyncio.run(main())
