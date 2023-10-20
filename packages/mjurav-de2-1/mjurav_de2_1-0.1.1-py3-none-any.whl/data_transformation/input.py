from typing import List, Union

import numpy as np
from pydantic import BaseModel, PositiveInt, conlist


class Transpose2DInput(BaseModel):
    input_matrix: conlist(conlist(float, min_length=1), min_length=1)  # type: ignore

    class Config:
        arbitrary_types_allowed = True


class Window1DInput(BaseModel):
    input_array: Union[List[float], np.ndarray]
    size: PositiveInt
    shift: PositiveInt = 1
    stride: PositiveInt = 1

    class Config:
        arbitrary_types_allowed = True


class Convolution2DInput(BaseModel):
    input_matrix: conlist(conlist(float, min_length=1), min_length=1)  # type: ignore
    kernel: conlist(conlist(float, min_length=1), min_length=1)  # type: ignore
    stride: PositiveInt = 1

    class Config:
        arbitrary_types_allowed = True
