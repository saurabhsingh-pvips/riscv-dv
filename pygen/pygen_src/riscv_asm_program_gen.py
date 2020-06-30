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

"""
import subprocess
from pygen_src.riscv_instr_sequence import riscv_instr_sequence
from pygen_src.riscv_instr_pkg import (pkg_ins,privileged_reg_t)
from pygen_src.riscv_instr_gen_config import cfg
from pygen_src.target.rv32i import riscv_core_setting as rcs
import logging
import random
from bitstring import BitArray

class riscv_asm_program_gen:

    def __init__(self):
        self.instr_stream = []
        self.directed_instr_stream_ratio = []
        self.hart = 0
        self.page_table_list = []
        self.main_program = []
        self.sub_program = []

    logging.basicConfig(level = logging.INFO)
    
    # This is the main function to generate all sections of the program.
    def gen_program(self):
        # Generate program header
        self.instr_stream.clear()
        self.gen_program_header()
        for hart in range(cfg.num_of_harts):
            sub_program_name = []
            self.instr_stream.append(f"h{int(hart)}_start:")
            if(not(cfg.bare_program_mode)):
                self.setup_misa()
                # Create all page tables
                self.create_page_table(hart)
                # Setup privileged mode registers and enter target privileged mode
                self.pre_enter_privileged_mode(hart)
            # Init section
            self.gen_init_section(hart)
            # To DO
            if(rcs.support_pmp and not(cfg.bare_program_mode)):
                self.gen_trap_handlers(hart)
                # Ecall handler
                self.gen_ecall_handler(hart)
                # Instruction fault handler
                self.gen_instr_fault_handler(hart)
                # Load fault handler
                self.gen_load_fault_handler(hart)
                # Store fault handler
                self.gen_store_fault_handler(hart) 
                self.gen_test_done()

            #Generate sub program
            # self.gen_sub_program(self, hart, self.sub_program,
                            # sub_program_name, cfg.num_of_sub_program)
            gt_lbl_str = pkg_ins.get_label("main", hart)
            gt_lbl_str = riscv_instr_sequence()
            self.main_program.append(gt_lbl_str)
            self.main_program[hart].instr_cnt = cfg.main_program_instr_cnt
            self.main_program[hart].is_debug_program = 0
            self.main_program[hart].label_name = "main" + str(hart)
            """If PMP is supported, we want to generate the associated trap handlers and the test_done
            section at the start of the program so we can allow access through the pmpcfg0 CSR"""

            # self.generate_directed_instr_stream(hart = hart, label= main_program[hart].label_name,
            #                                     original_instr_cnt = main_program[hart].instr_cnt,
            #                                    min_insert_cnt = 1, instr_stream = main_program[hart].directed_instr)
            # `DV_CHECK_RANDOMIZE_FATAL(main_program[hart]) # TODO

            self.main_program[hart].gen_instr(is_main_program = 1, no_branch = cfg.no_branch_jump)
            # self.gen_callstack(main_program[hart], sub_program[hart], sub_program_name,
            #                     # cfg.num_of_sub_program)
            # # logging.info("Generating callstack...done")
            # main_program[hart].post_process_instr()
            # logging.info("Post-processing main program...done")
        self.main_program[hart].generate_instr_stream()
        logging.info("Generating main program instruction stream...done")
        self.instr_stream.extend(self.main_program[hart].instr_string_list)
        self.instr_stream.append("{}j test_done".format(pkg_ins.indent))

        if(hart == 0 and not(rcs.support_pmp)):
            self.gen_test_done()
        # self.insert_sub_program(sub_program[hart], self.instr_stream)
        # logging.info("Inserting sub-programs...done")
        # logging.info("Main/sub program generation...done")
        # program end
        self.gen_program_end(hart)

    def gen_kernel_sections(self, hart):
        pass

    def gen_kernel_program(self, hart, seq):
        pass

    def gen_sub_program(self, hart, sub_program,
                        sub_program_name, num_sub_program,
                        is_debug = 0, prefix = "sub"):
        pass

    def gen_callstack(self, main_program, sub_program,
                      sub_program_name, num_sub_program):
        pass

    def insert_sub_program(self, sub_program, instr_list):
        pass

    def gen_program_header(self):
        string = []
        self.instr_stream.append(".include \"user_define.h\"")
        self.instr_stream.append(".global_start")
        self.instr_stream.append(".section .text")
        if(cfg.disable_compressed_instr):
            self.instr_stream.append(".option norvc;")

        string.append("csrr x5 mhartid")

        for hart in range(cfg.num_of_harts):
            string.append("li x6, {}\n{}beq x5, x6, {}f".format(hart, pkg_ins.indent, hart))
            
        self.gen_section("_start", string)

        for hart in range(cfg.num_of_harts):
            self.instr_stream.append("{}: j h{}_start".format(hart, hart))

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
        string = pkg_ins.format_string("init:", pkg_ins.LABEL_STR_LEN)
        self.instr_stream.append(string)
        self.init_gpr()
        # Init stack pointer to point to the end of the user stack
        string = "{}la x{} {}user_stack_end".format(
            pkg_ins.indent, cfg.sp, pkg_ins.hart_prefix(hart))
        self.instr_stream.append(string)
        if (cfg.enable_floating_point):
            self.init_floating_point_gpr()
        if (cfg.enable_vector_extension):
            self.init_vector_engine()
        self.core_is_initialized()
        self.gen_dummy_csr_write()

        if (rcs.support_pmp):
            string = pkg_ins.indent + "j main"
            self.instr_stream.append(string)

    def setup_misa(self):
        # TO DO
        misa = 0b01000000
        self.instr_stream.append("{}li x{}, {}".format(pkg_ins.indent, cfg.gpr[0], hex(misa)))
        self.instr_stream.append("{}csrw misa, x{}".format(pkg_ins.indent, cfg.gpr[0]))

    def core_is_initialized(self):
        pass

    def gen_dummy_csr_write(self):
        pass

    def init_gpr(self):
        reg_val = BitArray(uint = 0, length = pkg_ins.DATA_WIDTH)
        dist_lst = []

        for dist_val in range(5):
            if dist_val == 0:
                reg_val = BitArray(hex='0x0')
                dist_lst.append(reg_val)
            elif dist_val == 1:
                reg_val = BitArray(hex='0x80000000')
                dist_lst.append(reg_val)
            elif dist_val == 2:
                temp = random.randrange(0x1, 0xf)
                reg_val = BitArray(hex(temp), length=32)
                dist_lst.append(reg_val)
            elif dist_val == 3:
                temp = random.randrange(0x10, 0xefffffff)
                reg_val = BitArray(hex(temp), length=32)
                dist_lst.append(reg_val)
            else:
                temp = random.randrange(0xf0000000, 0xffffffff)
                reg_val = BitArray(hex(temp), length=32)
                dist_lst.append(reg_val)

        for i in range(32):
            init_string = "{}li x{}, {}".format(pkg_ins.indent, i, random.choice(dist_lst))
            self.instr_stream.append(init_string)

    def init_floating_point_gpr(self):
        pass

    def init_vector_engine(self):
        pass

    def gen_test_done(self):
        string = pkg_ins.format_string("test_done:", pkg_ins.LABEL_STR_LEN)
        self.instr_stream.append(string)
        self.instr_stream.append(pkg_ins.indent + "li gp, 1")

        if(cfg.bare_program_mode):
            self.instr_stream.append(pkg_ins.indent + "j write_tohost")
        else:
            self.instr_stream.append(pkg_ins.indent + "ecall")

    def gen_register_dump(self):
        pass

    def pre_enter_privileged_mode(self, hart):
        instr = []
        string = []

        string.append("la x{}, {}kernel_stack_end".format(cfg.tp, pkg_ins.hart_prefix(hart)))
        self.gen_section(pkg_ins.get_label("kernel_sp", hart), string)

        if(not cfg.no_delegation and (cfg.init_privileged_mode != "MACHINE_MODE")):
            self.gen_delegation(hart)
        self.trap_vector_init(hart)
        self.setup_pmp(hart)

        if(cfg.virtual_addr_translation_on):
            self.page_table_list.process_page_table(instr)
            self.gen_section(pkg_ins.get_label("process_pt", hart), instr)

        self.setup_epc(hart)

        if(rcs.support_pmp):
            self.gen_privileged_mode_switch_routine(hart)

    def gen_privileged_mode_switch_routine(self, hart):
        pass

    def setup_epc(self, hart):
        instr = []
        instr.append("la x{}, {}init".format(cfg.gpr[0], pkg_ins.hart_prefix(hart)))
        # if(cfg.virtual_addr_translation_on):
        # instr.append("slli x{}, x{}")
        # TODO
        mode_name = cfg.init_privileged_mode
        instr.append("csrw mepc, x{}".format(cfg.gpr[0]))
        if(not rcs.support_pmp): # TODO
            instr.append("j {}init_{}".format(pkg_ins.hart_prefix(hart), mode_name.name.lower()))

        self.gen_section(pkg_ins.get_label("mepc_setup", hart), instr)

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
        instr = []
        for items in rcs.supported_privileged_mode:
            if(items == "MACHINE_MODE"):
                trap_vec_reg = privileged_reg_t.MTVEC
            elif(items == "SUPERVISOR_MODE"):
                trap_vec_reg = privileged_reg_t.STVEC
            elif(items == "USER_MODE"):
                trap_vec_reg = privileged_reg_t.UTVEC
            else:
                logging.critical(
                    "[riscv_asm_program_gen] Unsupported privileged_mode {}".format(items))

            if(items == "USER_MODE" and not (pkg_ins.support_umode_trap)):
                continue

            # if(items < cfg.init_privileged_mode):
                # continue

            tvec_name = trap_vec_reg.name
            tvec_name = tvec_name.lower()
            instr.append("la x{}, {}{}_handler".format(
                cfg.gpr[0], pkg_ins.hart_prefix(hart), tvec_name))
            if(rcs.SATP_MODE != "BARE" and items != "MACHINE_MODE"):
                instr.append("slli x{}, x{}, {}\n".format(cfg.gpr[0], cfg.gpr[0], rcs.XLEN - 20) +
                             "srli x{}, x{}, {}".format(cfg.gpr[0], cfg.gpr[0], rcs.XLEN - 20))

            instr.append("ori x{}, x{}, {}".format(cfg.gpr[0], cfg.gpr[0], cfg.mtvec_mode))
            instr.append("csrw {}, x{}, # {}".format(hex(trap_vec_reg.value), cfg.gpr[0], trap_vec_reg.name))

        self.gen_section(pkg_ins.get_label("trap_vec_init", hart), instr)

    def gen_all_trap_handler(self, hart):
        pass

    def gen_trap_handlers(self, hart):
        pass

    def gen_trap_handler_section(self, hart, mode, cause, tvec,
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
        if(label != ""):
            string = pkg_ins.format_string("{}:".format(label), pkg_ins.LABEL_STR_LEN)
            self.instr_stream.append(string)
        for items in instr:
            string = pkg_ins.indent + items
            self.instr_stream.append(string)
        self.instr_stream.append("")

    def dump_perf_stats(self):
        pass

    def gen_test_file(self, test_name):
        subprocess.run(["mkdir", "-p", "out"])
        file = open("./out/{}".format(test_name), "w+")
        for items in self.instr_stream:
            file.write("{}\n".format(items))

        file.close()
        logging.info("%0s is generated", test_name)

    def gen_signature_handshake(self, instr, signature_type, core_status = "INITIALIZED",
                                test_result = "TEST_FAIL", csr = "MSCRATCH", addr_lebel = ""):
        pass

    def add_directed_instr_stream(self, name, ratio):
        pass

    def get_directed_instr_stream(self):
        pass

    def generate_directed_instr_stream(self, hart=0, label="", original_instr_cnt=None,
        min_insert_cnt=0, kernel_mode=0, instr_stream=[]):
        pass
        
    def gen_debug_rom(self, hart):
        pass
