from pygen_src.riscv_instr_pkg import * 
from pygen_src.isa.riscv_instr import *

def DEFINE_INSTR(instr_n, instr_format, instr_category, instr_group, imm_tp = imm_t.IMM, g=globals()):
    class_name = f"riscv_{instr_n.name}_instr"
    def __init__(self):
        self.instr_name = instr_n
        self.format = instr_format
        self.category = instr_category
        self.group = instr_group
        self.imm_type = imm_tp

    NewClass = type(class_name, (riscv_instr,), {
    "__init__": __init__,
    "valid": riscv_instr.register(instr_n)
    }) 
    g[class_name] = NewClass
