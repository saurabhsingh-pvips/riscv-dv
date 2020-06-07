"""
Copyright 2020 Google LLC
Copyright 2020 PerfectVIPs Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Regression script for RISC-V random instruction generator

"""

class riscv_asm_program_gen():

	def __init__(self):
		self.instr_stream = []
		self.directed_instr_stream_ratio = []
		self.hart = 0


	def gen_program(self):
		pass

	def gen_kernel_sections(self, hart):
		pass

	def gen_kernel_program(self, hart, seq):
		pass

	def gen_sub_program(self, hart, sub_program,
			sub_program_name, num_sub_program,
			is_debug = 0, prefix = "sub"):
		pass

	def gen_callstack(self, main_program, sub_program, \
						sub_program_name, num_sub_program ):
		pass

	def insert_sub_program(self, sub_program, instr_list):
		pass

	def gen_program_header(self):
		pass

	def gen_program_end(self, hart):
		if(hart == 0):
			self.gen_section("write_tohost", ["sw gp", "tohost", "t5"])
			self.gen_section("_exit", ["j write_tohost"])

	def gen_data_page_begin(self, hart):
		pass

	def gen_data_page(self, hart, is_kernel = 0, amo = 0):
		pass

	def gen_stack_section(self, hart):
		pass

	def gen_kernel_stack_section(self, hart):
		pass

	def gen_init_section(self, hart):
		pass

	def setup_misa(self):
		pass

	def core_is_initialized(self):
		pass

	def gen_dummy_csr_write(self):
		pass

	def init_gpr(self):
		pass

	def init_floating_point_gpr(self):
		pass

	def init_vector_engine(self):
		pass

	def gen_test_done(self):
		pass

	def gen_register_dump(self):
		pass

	def pre_enter_privileged_mode(self, hart):
		pass

	def gen_privileged_mode_switch_routine(self, hart):
		pass

	def setup_epc(self, hart):
		pass

	def setup_pmp(self, hart):
		pass

	def gen_delegation(self, hart):
		self.gen_delegation_instr(hart, "MEDELEG", "MIDELEG",
					cfg.m_mode_exception_delegation,
					cfg.m_mode_interrupt_delegation)
		if(riscv_instr_pkg.support_umode_trap):
			self.gen_delegation_instr(hart, "SEDELEG", "SIDELEG",
					cfg.s_mode_exception_delegation,
					cfg.s_mode_interrupt_delegation)


	def gen_delegation_instr(self, hart, edeleg, ideleg,
				edeleg_enable, ideleg_enable):
		pass

	def trap_vector_init(self, hart):
		pass

	def gen_all_trap_handler(self, hart):
		pass

	def gen_trap_handlers(self, hart):
		pass

	def gen_trap_handler_section(self, hart, mode , cause, tvec,
					tval, epc, scratch, status, ie, ip):
		pass

	def gen_interrupt_vector_table(self, hart, mode, status, cause, ie,
					ip, scratch, instr):
		pass

	def gen_ecall_handler(self, hart):
		pass

	def gen_ebreak_handler(self, hart):
		pass

	def gen_illegal_instr_handler(self, hart):
		pass

	def gen_instr_fault_handler(self, hart):
		pass

	def gen_load_fault_handler(self, hart):
		pass

	def gen_store_fault_handler(self, hart):
		pass

	def create_page_table(self, hart):
		pass

	def gen_page_table_section(self, hart):
		pass

	def gen_plic_section(self, interrupt_handler_instr):
		pass

	def gen_interrupt_handler_section(self, mode, hart):
		pass

	def format_section(self, instr):
		pass

	def gen_section(self, label, instr):
		pass

	def dump_perf_stats(self):
		pass

	def gen_test_file(self, test_name):
		pass

	def gen_signature_handshake(self, instr, signature_type, core_status = "INITIALIZED",
				test_result = "TEST_FAIL", csr = "MSCRATCH", addr_lebel = ""):
		pass

	def add_directed_instr_stream(self, name, ratio):
		pass

	def get_directed_instr_stream(self):
		pass

	def generate_directed_instr_stream(self, hart, label, original_instr_cnt,
					min_insert_cnt = 0, kernel_mode = 0, instr_stream):
		pass

	def gen_debug_rom(self, hart):
		pass



