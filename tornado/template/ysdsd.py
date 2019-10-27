# def gen(dictt):
#     ret=zip(dictt.items())
#     yield from ret
#
#
# dictts ={'sd':1,'sdd':'sds'}
# print(type(*list(gen(dictts))[0]))
# print(*set(dictts.items()))
# print(type(dictts))


import asyncio


async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')


asyncio.run(main())
