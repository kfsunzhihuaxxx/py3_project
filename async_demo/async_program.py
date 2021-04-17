import asyncio
import random
from asyncio import AbstractEventLoop
import datetime
import colorama


async def generate_data(num: int, data: asyncio.Queue):
    for idx in range(1, num + 1):
        item = idx * idx
        # Use queue
        work = (item, datetime.datetime.now())
        # data.append(work)
        await data.put(work)

        print(colorama.Fore.YELLOW + " -- generated item {}".format(idx), flush=True)
        # Sleep better
         # time.sleep(random.random() + .5)
        await asyncio.sleep(random.random() + .5)


async def process_data(num: int, data: asyncio.Queue):
    processed = 0
    while processed < num:
        # Use queue
        # item = data.pop(0)
        # if not item:
        #     time.sleep(.01)
        #     continue
        item = await data.get()
        # item is tuple
        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t

        print(colorama.Fore.CYAN + "+++ Processed value {} after{:,.2f} sec.".format(value, dt.total_seconds()))
        # sleep better
        await asyncio.sleep(.5)


def main():
    # Create the asyncio loop
    loop: AbstractEventLoop = asyncio.get_event_loop()

    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "APP started.", flush=True)

    data = asyncio.Queue()

    # TODO: run these with asyncio.gather()

    task = asyncio.gather(
        generate_data(10, data),
        generate_data(10, data),
        process_data(20, data)
    )
    loop.run_until_complete(task)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting,total time:{:,.2f} sec.".format(dt.total_seconds()))


if __name__ == '__main__':
    main()
