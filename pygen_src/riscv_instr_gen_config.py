class riscv_instr_gen_config:
	def __init__(self):
		self.reserved_regs = []
		self.enable_floating_point = 1
		self.disable_compressed_instr = 1
