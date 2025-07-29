from dataclasses import dataclass


@dataclass
class Character16Entry:
    index: int
    width: int
    height: int
    u: int
    v: int
    advance_y: int
    x_offset: int
    y_offset: int
    num_kern: int
    kern_index: int
    advance_x: int
