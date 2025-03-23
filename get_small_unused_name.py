import random
import math
from collections import abc

Callable = abc.Callable

_DIGITS: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def to_name(number: int) -> str:
    if number == 0:
        return _DIGITS[0]
    result: list[str] = []
    while number:
        number, remainder = divmod(number, len(_DIGITS))
        result.append(_DIGITS[remainder])
    return ''.join(reversed(result))

def get_small_unused_number(is_used: Callable[[int], bool]) -> int:
    cap: int = 1
    while True:
        n = random.randrange(cap)
        if not is_used(n):
            return n    
        cap = math.ceil(cap * 2)

def get_small_unused_name(is_used: Callable[[str], bool]) -> str:
    return to_name(get_small_unused_number(lambda n: is_used(to_name(n))))