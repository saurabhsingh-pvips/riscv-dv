from rv32i_instr import *
class riscv_instr_base_test:
	def __init__(self):
		pass

for i in range(cfg.num_of_test):
	print("Test {} Started \n".format(i+1))
	riscv_instr_ins.create_instr_list(cfg)

print("instr_registry Contents = {}".format(riscv_instr_ins.instr_registry))