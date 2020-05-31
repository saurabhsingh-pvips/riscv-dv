import sys
sys.path.append("../../")
from pygen_src.isa.rv32i_instr import *
class riscv_instr_base_test:
	def __init__(self):
		pass
print("\n instr_registry Contents = {} \n".format(riscv_instr_ins.instr_registry))
for i in range(cfg.num_of_test):
	riscv_instr_ins.create_instr_list(cfg)

