import asyncio

from pysnail.pysnail import get_regular_snail


async def main() -> None:
  snail = await get_regular_snail()
  print(snail)


if __name__ == '__main__':
  asyncio.run(main())
