from enum import Enum

from Adams_Bashforth import AdamsBashforth
from Adams_Moulton import AdamsMoulton
from Runge_Kutta4 import RungeKutta4


class MethodName(Enum):
    ADAMS_BASHFORTH = "Adams-Bashforth"
    ADAMS_MOULTON = "Adams-Moulton"
    RUNGE_KUTTA4 = "Runge-Kutta 4"


def get_method_classes():
    return {
        MethodName.ADAMS_BASHFORTH: AdamsBashforth,
        MethodName.ADAMS_MOULTON: AdamsMoulton,
        MethodName.RUNGE_KUTTA4: RungeKutta4,
    }
