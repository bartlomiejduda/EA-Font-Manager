from dataclasses import dataclass
from typing import Optional


@dataclass
class Character12Entry:
    index: int
    width: int
    height: int
    u: int
    v: int
    advance: int
    x_offset: int
    y_offset: int
    num_kern: Optional[int]
