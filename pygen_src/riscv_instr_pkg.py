from collections import defaultdict
class riscv_instr_pkg:
	def __init__(self):
		self.instr_name = ["LUI","AUIPC","JAL","JALR","BEQ","BNE","BLT","BGE","BLTU","BGEU","LB","LH","LW","LBU","LHU","SB","SFENCE_VMA"]
		self.instr_group = {"RV32I":["LUI","AUIPC","JAL","JALR","BEQ","BNE","BLT","BGE","BLTU","BGEU","LB","LH","LW","LBU","LHU","SB"]}
		self.instr_category = {"LOAD":["LB","LH","LW","LBU","LHU"],"STORE":["SB","SH","SW"],"SHIFT":["SLL","SLLI"],\
		"ARITHMETIC":["ADD","ADDI","NOP","SUB","LUI","AUIPC"],"LOGICAL":[],"COMPARE":[],"BRANCH":[],"JUMP":[]}

		self.group = list(self.instr_group.keys())
		self.category = list(self.instr_category.keys())