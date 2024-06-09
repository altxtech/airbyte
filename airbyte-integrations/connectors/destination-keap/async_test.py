import asyncio


async def task():
    await asyncio.sleep(1)
    print("done")
    return 1

def main():
    
    tasks = []
    for _ in range(10):
        tasks.append(asyncio.create_task(task()))

main()
