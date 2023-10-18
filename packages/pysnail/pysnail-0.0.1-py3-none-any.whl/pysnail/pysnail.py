"""Core module of pysnail package."""
import asyncio
import math


async def get_regular_snail() -> str:
  """
  A regular snail is on it's way to you.
  :return: returns a flavored markdown snail
  """
  await asyncio.sleep(10)
  return ':snail:'


async def get_blazingly_fast_snail() -> str:
  """A blazingly fast snail is on it's way to you.
  
  Hint: you'd better not wait for this snail :)
  """
  await asyncio.sleep(math.inf)
  return ':snail:'

