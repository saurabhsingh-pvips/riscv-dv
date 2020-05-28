class riscv_instr_gen_config:
	def __init__(self):
		self.reserved_regs = []
		self.enable_floating_point = 1
		self.disable_compressed_instr = 1
		self.num_of_test  = 3
		self.no_fence = 1
		self.enable_sfence = 0
		self.reserved_regs = ["ZERO","RA", "SP", "GP", "TP", "T0", "T1", "T2", "S0", "S1", "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", \
							   "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "T3", "T4", "T5", "T6"]
		self.enable_illegal_csr_instruction = 0
		self.enable_access_invalid_csr_level = 0 
		self.invalid_priv_mode_csrs = [] 
		self.init_privileged_mode = "MACHINE_MODE"
		self.no_ebreak = 1
		self.no_dret = 1
		self.no_csr_instr = 1
		self.no_wfi = 1