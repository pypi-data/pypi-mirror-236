from qlat_utils import *
import qlat.c as c

from qlat.propagator import *

@timer
def contract_chvp_16(prop1, prop2):
    chvp_16 = Field(ElemTypeComplex)
    c.contract_chvp_16_field(chvp_16, prop1, prop2)
    return chvp_16
