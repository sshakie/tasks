import asyncio
import os


async def applying(plant):
    print(f'7 Application of fertilizers for {plant}')
    await asyncio.sleep(3 / 1000)
    print(f'7 Fertilizers for the {plant} have been introduced')


async def treating(plant):
    print(f'8 Treatment of {plant} from pests')
    await asyncio.sleep(5 / 1000)
    print(f'8 The {plant} is treated from pests')


async def growing(plant, soak, shelter, transplant):
    print(f'0 Beginning of sowing the {plant} plant')
    print(f'1 Soaking of the {plant} started')
    await asyncio.sleep(soak / 1000)
    print(f'2 Soaking of the {plant} is finished')
    print(f'3 Shelter of the {plant} is supplied')
    await asyncio.sleep(shelter / 1000)
    print(f'4 Shelter of the {plant} is removed')
    print(f'5 The {plant} has been transplanted')
    await asyncio.sleep(transplant / 1000)
    print(f'6 The {plant} has taken root')
    print(f'9 The seedlings of the {plant} are ready')


async def sowing(*plants):
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    tasks = []
    for i in plants:
        tasks.append(asyncio.create_task(growing(i[0], i[1], i[2], i[3])))
        asyncio.create_task(applying(i[0]))
        asyncio.create_task(treating(i[0]))
    await asyncio.gather(*tasks)

