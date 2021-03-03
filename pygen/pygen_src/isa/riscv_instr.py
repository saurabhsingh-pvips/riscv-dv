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

import logging
import copy
import sys
import random
import vsc
from imp import reload
from collections import defaultdict
from bitstring import BitArray
from importlib import import_module
from pygen_src.riscv_instr_pkg import (pkg_ins, riscv_instr_category_t, riscv_reg_t,
                                       riscv_instr_name_t, riscv_instr_format_t,
                                       riscv_instr_group_t, imm_t,
                                       privileged_mode_t)
from pygen_src.riscv_instr_gen_config import cfg
rcs = import_module("pygen_src.target." + cfg.argv.target + ".riscv_core_setting")
reload(logging)
logging.basicConfig(filename='{}'.format(cfg.argv.log_file_name),
                    filemode='w',
                    format="%(asctime)s %(filename)s %(lineno)s %(levelname)s %(message)s",
                    level=logging.DEBUG)


@vsc.randobj
class riscv_instr:
    # All derived instructions
    instr_registry = {}

    # Instruction list
    instr_names = []

    # Categorized instruction list
    instr_group = defaultdict(list)
    instr_category = defaultdict(list)
    basic_instr = []
    instr_template = {}

    # Privileged CSR filter
    exclude_reg = []
    include_reg = []

    def __init__(self):
        # Instruction attributes
        self.group = vsc.enum_t(riscv_instr_group_t)
        self.format = vsc.enum_t(riscv_instr_format_t)
        self.category = vsc.enum_t(riscv_instr_category_t)
        self.instr_name = vsc.enum_t(riscv_instr_name_t)
        self.imm_type = vsc.enum_t(imm_t)
        self.imm_len = vsc.bit_t(5)

        # Operands
        self.csr = vsc.rand_bit_t(12)
        self.rs2 = vsc.rand_enum_t(riscv_reg_t)
        self.rs1 = vsc.rand_enum_t(riscv_reg_t)
        self.rd = vsc.rand_enum_t(riscv_reg_t)
        self.imm = vsc.rand_bit_t(32)

        # Helper Fields
        self.imm_mask = vsc.uint32_t(0xffffffff)
        self.is_branch_target = None
        self.has_label = 1
        self.atomic = 0
        self.branch_assigned = None
        self.process_load_store = 1
        self.is_compressed = None
        self.is_illegal_instr = None
        self.is_hint_instr = None
        self.is_floating_point = None
        self.imm_str = None
        self.comment = ""
        self.label = ""
        self.is_local_numeric_label = None
        self.idx = -1
        self.has_rs1 = vsc.bit_t(1)
        self.has_rs2 = vsc.bit_t(1)
        self.has_rd = vsc.bit_t(1)
        self.has_imm = vsc.bit_t(1)
        self.has_rs1 = 1
        self.has_rs2 = 1
        self.has_rd = 1
        self.has_imm = 1
        self.shift_t = vsc.uint32_t(0xffffffff)
        self.XLEN = vsc.uint32_t(32)  # XLEN is used in constraint throughout the generator.
        # Hence, XLEN should be of PyVSC type in order to use it in a constraint block
        self.XLEN = rcs.XLEN

    @vsc.constraint
    def imm_c(self):
        with vsc.if_then(self.instr_name.inside(vsc.rangelist(riscv_instr_name_t.SLLIW,
                                                              riscv_instr_name_t.SRLIW,
                                                              riscv_instr_name_t.SRAIW))):
            self.imm[11:5] == 0
        with vsc.if_then(self.instr_name.inside(vsc.rangelist(riscv_instr_name_t.SLLI,
                                                              riscv_instr_name_t.SRLI,
                                                              riscv_instr_name_t.SRAI))):
            with vsc.if_then(self.XLEN == 32):
                self.imm[11:5] == 0
            with vsc.if_then(self.XLEN != 32):
                self.imm[11:6] == 0

    @vsc.constraint
    def csr_c(self):
        # TODO
        pass

    @classmethod
    def register(cls, instr_name, instr_group):
        logging.info("Registering {}".format(instr_name.name))
        cls.instr_registry[instr_name] = instr_group
        return 1

    # Create the list of instructions based on the supported ISA extensions and
    # configuration of the generator
    @classmethod
    def create_instr_list(cls, cfg):
        cls.instr_names.clear()
        cls.instr_group.clear()
        cls.instr_category.clear()
        for instr_name, instr_group in cls.instr_registry.items():
            if instr_name in rcs.unsupported_instr:
                continue
            instr_inst = cls.create_instr(instr_name, instr_group)
            cls.instr_template[instr_name] = instr_inst

            if not instr_inst.is_supported(cfg):
                continue
            # C_JAL is RV32C only instruction
            if ((rcs.XLEN != 32) and (instr_name == riscv_instr_name_t.C_JAL)):
                continue
            if ((riscv_reg_t.SP in cfg.reserved_regs) and
                    (instr_name == riscv_instr_name_t.C_ADDI16SP)):
                continue
            if (cfg.enable_sfence and instr_name == riscv_instr_name_t.SFENCE_VMA):
                continue
            if instr_name in [riscv_instr_name_t.FENCE, riscv_instr_name_t.FENCE_I,
                              riscv_instr_name_t.SFENCE_VMA]:
                continue
            if (instr_inst.group in rcs.supported_isa and
                    not(cfg.disable_compressed_instr and
                        instr_inst.group in [riscv_instr_group_t.RV32C, riscv_instr_group_t.RV64C,
                                             riscv_instr_group_t.RV32DC, riscv_instr_group_t.RV32FC,
                                             riscv_instr_group_t.RV128C]) and
                    not(not(cfg.enable_floating_point) and instr_inst.group in
                        [riscv_instr_group_t.RV32F, riscv_instr_group_t.RV64F,
                         riscv_instr_group_t.RV32D, riscv_instr_group_t.RV64D])):
                cls.instr_category[instr_inst.category.name].append(instr_name)
                cls.instr_group[instr_inst.group.name].append(instr_name)
                cls.instr_names.append(instr_name)
        cls.build_basic_instruction_list(cfg)
        cls.create_csr_filter(cfg)

    @classmethod
    def create_instr(cls, instr_name, instr_group):
        try:
            module_name = import_module("pygen_src.isa." + instr_group.name.lower() + "_instr")
            instr_inst = eval("module_name.riscv_" + instr_name.name + "_instr()")
        except Exception:
            logging.critical("Failed to create instr: {}".format(instr_name.name))
            sys.exit(1)
        return instr_inst

    def is_supported(self, cfg):
        return 1

    @classmethod
    def build_basic_instruction_list(cls, cfg):
        cls.basic_instr = (cls.instr_category["SHIFT"] + cls.instr_category["ARITHMETIC"] +
                           cls.instr_category["LOGICAL"] + cls.instr_category["COMPARE"])
        if cfg.no_ebreak == 0:
            cls.basic_instr.append("EBREAK")
            for _ in rcs.supported_isa:
                if(riscv_instr_group_t.RV32C in rcs.supported_isa and
                   not(cfg.disable_compressed_instr)):
                    cls.basic_instr.append("C_EBREAK")
                    break
        if cfg.no_dret == 0:
            cls.basic_instr.append("DRET")
        if cfg.no_fence == 0:
            cls.basic_instr.append(cls.instr_category["SYNCH"])
        if(cfg.no_csr_instr == 0 and cfg.init_privileged_mode == privileged_mode_t.MACHINE_MODE):
            cls.basic_instr.append(cls.instr_category["CSR"])
        if cfg.no_wfi == 0:
            cls.basic_instr.append("WFI")

    @classmethod
    def create_csr_filter(cls, cfg):
        cls.include_reg.clear()
        cls.exclude_reg.clear()

        if cfg.enable_illegal_csr_instruction:
            cls.exclude_reg = rcs.implemented_csr
        elif cfg.enable_access_invalid_csr_level:
            cls.include_reg = cfg.invalid_priv_mode_csrs
        else:
            # Use scratch register to avoid the side effect of modifying other privileged mode CSR.
            if cfg.init_privileged_mode == privileged_mode_t.MACHINE_MODE:  # Machine Mode
                cls.include_reg.append("MSCRATCH")
            elif cfg.init_privileged_mode == privileged_mode_t.SUPERVISOR_MODE:  # Supervisor Mode
                cls.include_reg.append("SSCRATCH")
            else:                                               # User Mode
                cls.include_reg.append("USCRATCH")

    @classmethod
    def get_rand_instr(cls, include_instr=[], exclude_instr=[],
                       include_category=[], exclude_category=[],
                       include_group=[], exclude_group=[]):
        idx = BitArray(uint = 0, length = 32)
        name = ""
        allowed_instr = []
        disallowed_instr = []
        # allowed_categories = []
        for items in include_category:
            allowed_instr.extend(cls.instr_category[items])
        for items in exclude_category:
            if items in cls.instr_category:
                disallowed_instr.extend(cls.instr_category[items])
        for items in include_group:
            allowed_instr.extend(cls.instr_group[items])
        for items in exclude_group:
            if items in cls.instr_group:
                disallowed_instr.extend(cls.instr_group[items])

        disallowed_instr.extend(exclude_instr)

        # TODO Randomization logic needs to be frame with PyVSC library
        if len(disallowed_instr) == 0:
            try:
                if len(include_instr) > 0:
                    if len(include_instr) == 1:
                        idx = 0
                    else:
                        idx = random.randrange(0, len(include_instr) - 1)
                    name = include_instr[idx]
                elif len(allowed_instr) > 0:
                    idx = random.randrange(0, len(allowed_instr) - 1)
                    name = allowed_instr[idx]
                else:
                    idx = random.randrange(0, len(cls.instr_names) - 1)
                    name = cls.instr_names[idx]
            except Exception:
                logging.critical(
                    "[{}] Cannot generate random instruction".format(riscv_instr.__name__))
                sys.exit(1)
        else:
            try:
                name = random.choice(cls.instr_names)
                if len(include_instr) > 0:
                    name = random.choice(include_instr)
                if len(allowed_instr) > 0:
                    name = random.choice(allowed_instr)
            except Exception:
                logging.critical(
                    "[{}] Cannot generate random instruction".format(riscv_instr.__name__))
                sys.exit(1)
        # rs1 rs2 values are overwriting and the last generated values are
        # getting assigned for a particular instruction hence creating different
        # object address and id to ratain the randomly generated values.
        # Shallow copy for all relevant fields, avoid using create() to improve performance
        instr_h = copy.deepcopy(cls.instr_template[name])
        return instr_h

    @classmethod
    def get_load_store_instr(cls, load_store_instr):
        instr_h = riscv_instr()
        if len(load_store_instr) == 0:
            load_store_instr = cls.instr_category["LOAD"] + \
                cls.instr_category["STORE"]
        # TODO
        # Filter out unsupported load/store instruction
        cls.idx = random.randrange(0, len(load_store_instr) - 1)
        name = load_store_instr[cls.idx]
        # Shallow copy for all relevant fields, avoid using create() to improve performance
        instr_h = copy.copy(cls.instr_template[name])
        return instr_h

    @classmethod
    def get_instr(cls, name):
        if not cls.instr_template.get(name):
            logging.critical("Cannot get instr {}".format(name))
            sys.exit(1)
        # Shallow copy for all relevant fields, avoid using create() to improve performance
        instr_h = copy.copy(cls.instr_template[name])
        return instr_h

    # Disable the rand mode for unused operands to randomization performance
    def set_rand_mode(self):
        # rand_mode setting for Instruction Format
        if self.format == riscv_instr_format_t.R_FORMAT:
            self.has_imm = 0
        if self.format == riscv_instr_format_t.I_FORMAT:
            self.has_rs2 = 0
        if self.format in [riscv_instr_format_t.S_FORMAT, riscv_instr_format_t.B_FORMAT]:
            self.has_rd = 0
        if self.format in [riscv_instr_format_t.U_FORMAT, riscv_instr_format_t.J_FORMAT]:
            self.has_rs1 = 0
            self.has_rs2 = 0

        # rand_mode setting for Instruction Category
        if self.category == riscv_instr_category_t.CSR:
            self.has_rs2 = 0
            if self.format == riscv_instr_format_t.I_FORMAT:
                self.has_rs1 = 0

    def pre_randomize(self):
        with vsc.raw_mode():
            self.rs1.rand_mode = bool(self.has_rs1)
            self.rs2.rand_mode = bool(self.has_rs2)
            self.rd.rand_mode = bool(self.has_rd)
            self.imm.rand_mode = bool(self.has_imm)
            if self.category != riscv_instr_category_t.CSR:
                self.csr.rand_mode = False

    def set_imm_len(self):
        if self.format in [riscv_instr_format_t.U_FORMAT, riscv_instr_format_t.J_FORMAT]:
            self.imm_len = 20
        elif self.format in [riscv_instr_format_t.I_FORMAT, riscv_instr_format_t.S_FORMAT,
                             riscv_instr_format_t.B_FORMAT]:
            if self.imm_type == imm_t.UIMM:
                self.imm_len = 5
            else:
                self.imm_len = 11
        self.imm_mask = (self.imm_mask << self.imm_len) & self.shift_t

    def extend_imm(self):
        sign = 0
        # self.shift_t = 2 ** 32 -1 is used to limit the width after shift operation
        self.imm = self.imm << (32 - self.imm_len) & self.shift_t
        sign = (self.imm & 0x80000000) >> 31
        self.imm = self.imm >> (32 - self.imm_len) & self.shift_t
        # Signed extension
        if(sign and not((self.format == riscv_instr_format_t.U_FORMAT) or
                        (self.imm_type in [imm_t.UIMM, imm_t.NZUIMM]))):
            self.imm = self.imm_mask | self.imm

    def post_randomize(self):
        self.extend_imm()
        self.update_imm_str()

    # Convert the instruction to assembly code
    def convert2asm(self, prefix = " "):
        asm_str = pkg_ins.format_string(string = self.get_instr_name(),
                                        length = pkg_ins.MAX_INSTR_STR_LEN)
        if self.category != riscv_instr_category_t.SYSTEM:
            if self.format == riscv_instr_format_t.J_FORMAT:  # instr rd,imm
                asm_str = '{} {}, {}'.format(asm_str, self.rd.name, self.get_imm())
            elif self.format == riscv_instr_format_t.U_FORMAT:  # instr rd,imm
                asm_str = '{} {}, {}'.format(asm_str, self.rd.name, self.get_imm())
            elif self.format == riscv_instr_format_t.I_FORMAT:  # instr rd,rs1,imm
                if self.instr_name == riscv_instr_name_t.NOP:
                    asm_str = "nop"
                elif self.instr_name == riscv_instr_name_t.WFI:
                    asm_str = "wfi"
                elif self.instr_name == riscv_instr_name_t.FENCE:
                    asm_str = "fence"
                elif self.instr_name == riscv_instr_name_t.FENCE_I:
                    asm_str = "fence.i"
                elif self.category == riscv_instr_category_t.LOAD:  # Use psuedo instruction format
                    asm_str = '{} {}, {} ({})'.format(
                        asm_str, self.rd.name, self.get_imm(), self.rs1.name)
                elif self.category == riscv_instr_category_t.CSR:
                    asm_str = '{} {}, 0x{}, {}'.format(
                        asm_str, self.rd.name, self.csr, self.get_imm())
                else:
                    asm_str = '{} {}, {}, {}'.format(
                        asm_str, self.rd.name, self.rs1.name, self.get_imm())
            elif self.format == riscv_instr_format_t.S_FORMAT:  # instr rs1,rs2,imm
                if self.category == riscv_instr_category_t.STORE:  # Use psuedo instruction format
                    asm_str = '{} {}, {} ({})'.format(
                        asm_str, self.rs2.name, self.get_imm(), self.rs1.name)
                else:
                    asm_str = '{} {}, {}, {}'.format(
                        asm_str, self.rs1.name, self.rs2.name, self.get_imm())

            elif self.format == riscv_instr_format_t.B_FORMAT:  # instr rs1,rs2,imm
                if self.category == riscv_instr_category_t.STORE:  # Use psuedo instruction format
                    asm_str = '{} {}, {} ({})'.format(
                        asm_str, self.rs2.name, self.get_imm(), self.rs1.name)
                else:
                    asm_str = '{} {}, {}, {}'.format(
                        asm_str, self.rs1.name, self.rs2.name, self.get_imm())

            elif self.format == riscv_instr_format_t.R_FORMAT:  # instr rd,rs1,rs2
                if self.category == riscv_instr_category_t.CSR:
                    asm_str = '{} {}, 0x{}, {}'.format(
                        asm_str, self.rd.name, self.csr, self.rs1.name)
                elif self.instr_name == riscv_instr_name_t.SFENCE_VMA:
                    asm_str = "sfence.vma x0, x0"
                else:
                    asm_str = '{} {}, {}, {}'.format(
                        asm_str, self.rd.name, self.rs1.name, self.rs2.name)
            else:
                asm_str = 'Fatal_unsupported_format: {} {}'.format(
                    self.format.name, self.instr_name.name)

        else:
            # For EBREAK,C.EBREAK, making sure pc+4 is a valid instruction boundary
            # This is needed to resume execution from epc+4 after ebreak handling
            if self.instr_name == riscv_instr_name_t.EBREAK:
                asm_str = ".4byte 0x00100073 # ebreak"

        if self.comment != "":
            asm_str = asm_str + " #" + self.comment
        return asm_str.lower()

    def get_opcode(self):
        if self.instr_name == riscv_instr_name_t.LUI:
            return (BitArray(uint = 55, length = 7).bin)
        elif self.instr_name == riscv_instr_name_t.AUIPC:
            return (BitArray(uint = 23, length = 7).bin)
        elif self.instr_name == riscv_instr_name_t.JAL:
            return (BitArray(uint = 23, length = 7).bin)
        elif self.instr_name == riscv_instr_name_t.JALR:
            return (BitArray(uint = 111, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.BEQ, riscv_instr_name_t.BNE,
                                 riscv_instr_name_t.BLT, riscv_instr_name_t.BGE,
                                 riscv_instr_name_t.BLTU, riscv_instr_name_t.BGEU]:
            return (BitArray(uint = 103, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.LB, riscv_instr_name_t.LH,
                                 riscv_instr_name_t.LW, riscv_instr_name_t.LBU,
                                 riscv_instr_name_t.LHU, riscv_instr_name_t.LWU,
                                 riscv_instr_name_t.LD]:
            return (BitArray(uint = 99, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.SB, riscv_instr_name_t.SH,
                                 riscv_instr_name_t.SW, riscv_instr_name_t.SD]:
            return (BitArray(uint = 35, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.ADDI, riscv_instr_name_t.SLTI,
                                 riscv_instr_name_t.SLTIU, riscv_instr_name_t.XORI,
                                 riscv_instr_name_t.ORI, riscv_instr_name_t.ANDI,
                                 riscv_instr_name_t.SLLI, riscv_instr_name_t.SRLI,
                                 riscv_instr_name_t.SRAI, riscv_instr_name_t.NOP]:
            return (BitArray(uint = 19, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.ADD, riscv_instr_name_t.SUB,
                                 riscv_instr_name_t.SLL, riscv_instr_name_t.SLT,
                                 riscv_instr_name_t.SLTU, riscv_instr_name_t.XOR,
                                 riscv_instr_name_t.SRL, riscv_instr_name_t.SRA,
                                 riscv_instr_name_t.OR, riscv_instr_name_t.AND,
                                 riscv_instr_name_t.MUL, riscv_instr_name_t.MULH,
                                 riscv_instr_name_t.MULHSU, riscv_instr_name_t.MULHU,
                                 riscv_instr_name_t.DIV, riscv_instr_name_t.DIVU,
                                 riscv_instr_name_t.REM, riscv_instr_name_t.REMU]:
            return (BitArray(uint = 51, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.ADDIW, riscv_instr_name_t.SLLIW,
                                 riscv_instr_name_t.SRLIW, riscv_instr_name_t.SRAIW]:
            return (BitArray(uint = 27, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.MULH, riscv_instr_name_t.MULHSU,
                                 riscv_instr_name_t.MULHU, riscv_instr_name_t.DIV,
                                 riscv_instr_name_t.DIVU, riscv_instr_name_t.REM,
                                 riscv_instr_name_t.REMU]:
            return (BitArray(uint = 51, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.FENCE, riscv_instr_name_t.FENCE_I]:
            return (BitArray(uint = 15, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.ECALL, riscv_instr_name_t.EBREAK,
                                 riscv_instr_name_t.CSRRW, riscv_instr_name_t.CSRRS,
                                 riscv_instr_name_t.CSRRC, riscv_instr_name_t.CSRRWI,
                                 riscv_instr_name_t.CSRRSI, riscv_instr_name_t.CSRRCI]:
            return (BitArray(uint = 115, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.ADDW, riscv_instr_name_t.SUBW,
                                 riscv_instr_name_t.SLLW, riscv_instr_name_t.SRLW,
                                 riscv_instr_name_t.SRAW, riscv_instr_name_t.MULW,
                                 riscv_instr_name_t.DIVW, riscv_instr_name_t.DIVUW,
                                 riscv_instr_name_t.REMW, riscv_instr_name_t.REMUW]:
            return (BitArray(uint = 59, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.ECALL, riscv_instr_name_t.EBREAK,
                                 riscv_instr_name_t.URET, riscv_instr_name_t.SRET,
                                 riscv_instr_name_t.MRET, riscv_instr_name_t.DRET,
                                 riscv_instr_name_t.WFI, riscv_instr_name_t.SFENCE_VMA]:
            return (BitArray(uint = 115, length = 7).bin)
        else:
            logging.critical("Unsupported instruction {}".format(self.instr_name.name))
            sys.exit(1)

    def get_func3(self):
        if self.instr_name in [riscv_instr_name_t.JALR, riscv_instr_name_t.BEQ,
                               riscv_instr_name_t.LB, riscv_instr_name_t.SB,
                               riscv_instr_name_t.ADDI, riscv_instr_name_t.NOP,
                               riscv_instr_name_t.ADD, riscv_instr_name_t.SUB,
                               riscv_instr_name_t.FENCE, riscv_instr_name_t.ECALL,
                               riscv_instr_name_t.EBREAK, riscv_instr_name_t.ADDIW,
                               riscv_instr_name_t.ADDW, riscv_instr_name_t.SUBW,
                               riscv_instr_name_t.MUL, riscv_instr_name_t.MULW,
                               riscv_instr_name_t.ECALL, riscv_instr_name_t.EBREAK,
                               riscv_instr_name_t.URET, riscv_instr_name_t.SRET,
                               riscv_instr_name_t.MRET, riscv_instr_name_t.DRET,
                               riscv_instr_name_t.WFI, riscv_instr_name_t.SFENCE_VMA]:
            return (BitArray(uint = 0, length = 3).bin)
        elif self.instr_name in [riscv_instr_name_t.BNE, riscv_instr_name_t.LH,
                                 riscv_instr_name_t.SH, riscv_instr_name_t.SLLI,
                                 riscv_instr_name_t.SLL, riscv_instr_name_t.FENCE_I,
                                 riscv_instr_name_t.CSRRW, riscv_instr_name_t.SLLIW,
                                 riscv_instr_name_t.SLLW, riscv_instr_name_t.MULH]:
            return (BitArray(uint = 1, length = 3).bin)
        elif self.instr_name in [riscv_instr_name_t.LW, riscv_instr_name_t.SW,
                                 riscv_instr_name_t.SLTI, riscv_instr_name_t.SLT,
                                 riscv_instr_name_t.CSRRS, riscv_instr_name_t.MULHS]:
            return (BitArray(uint = 2, length = 3).bin)
        elif self.instr_name in [riscv_instr_name_t.SLTIU, riscv_instr_name_t.SLTU,
                                 riscv_instr_name_t.CSRRC, riscv_instr_name_t.LD,
                                 riscv_instr_name_t.SD, riscv_instr_name_t.MULHU]:
            return (BitArray(uint = 3, length = 3).bin)
        elif self.instr_name in [riscv_instr_name_t.BLT, riscv_instr_name_t.LBU,
                                 riscv_instr_name_t.XORI, riscv_instr_name_t.XOR,
                                 riscv_instr_name_t.DIV, riscv_instr_name_t.DIVW]:
            return (BitArray(uint = 4, length = 3).bin)
        elif self.instr_name in [riscv_instr_name_t.BGE, riscv_instr_name_t.LHU,
                                 riscv_instr_name_t.SRLI, riscv_instr_name_t.SRAI,
                                 riscv_instr_name_t.SRL, riscv_instr_name_t.SRA,
                                 riscv_instr_name_t.CSRRWI, riscv_instr_name_t.SRLIW,
                                 riscv_instr_name_t.SRAIW, riscv_instr_name_t.SRLW,
                                 riscv_instr_name_t.SRAW, riscv_instr_name_t.DIVU,
                                 riscv_instr_name_t.DIVUW]:
            return (BitArray(uint = 5, length = 3).bin)
        elif self.instr_name in [riscv_instr_name_t.BLTU, riscv_instr_name_t.ORI,
                                 riscv_instr_name_t.OR, riscv_instr_name_t.CSRRSI,
                                 riscv_instr_name_t.LWU, riscv_instr_name_t.REM,
                                 riscv_instr_name_t.REMW]:
            return (BitArray(uint = 6, length = 3).bin)
        elif self.instr_name in [riscv_instr_name_t.BGEU, riscv_instr_name_t.ANDI,
                                 riscv_instr_name_t.AND, riscv_instr_name_t.CSRRCI,
                                 riscv_instr_name_t.REMU, riscv_instr_name_t.REMUW]:
            return (BitArray(uint = 7, length = 3).bin)
        else:
            logging.critical("Unsupported instruction {}".format(self.instr_name.name))
            sys.exit(1)

    def get_func7(self):
        if self.instr_name in [riscv_instr_name_t.SLLI, riscv_instr_name_t.SRLI,
                               riscv_instr_name_t.ADD, riscv_instr_name_t.SLL,
                               riscv_instr_name_t.SLT, riscv_instr_name_t.SLTU,
                               riscv_instr_name_t.XOR, riscv_instr_name_t.SRL,
                               riscv_instr_name_t.OR, riscv_instr_name_t.AND,
                               riscv_instr_name_t.FENCE, riscv_instr_name_t.FENCE_I,
                               riscv_instr_name_t.SLLIW, riscv_instr_name_t.SRLIW,
                               riscv_instr_name_t.ADDW, riscv_instr_name_t.SLLW,
                               riscv_instr_name_t.SRLW, riscv_instr_name_t.ECALL,
                               riscv_instr_name_t.EBREAK, riscv_instr_name_t.URET]:
            return (BitArray(uint = 0, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.SUB, riscv_instr_name_t.SRA,
                                 riscv_instr_name_t.SRAIW, riscv_instr_name_t.SUBW,
                                 riscv_instr_name_t.SRAW]:
            return (BitArray(uint = 32, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.MUL, riscv_instr_name_t.MULH,
                                 riscv_instr_name_t.MULHSU, riscv_instr_name_t.MULHU,
                                 riscv_instr_name_t.DIV, riscv_instr_name_t.DIVU,
                                 riscv_instr_name_t.REM, riscv_instr_name_t.REMU,
                                 riscv_instr_name_t.MULW, riscv_instr_name_t.DIVW,
                                 riscv_instr_name_t.DIVUW, riscv_instr_name_t.REMW,
                                 riscv_instr_name_t.REMUW]:
            return (BitArray(uint = 1, length = 7).bin)
        elif self.instr_name in [riscv_instr_name_t.SRET, riscv_instr_name_t.WFI]:
            return (BitArray(uint = 8, length = 7).bin)
        elif self.instr_name == riscv_instr_name_t.MRET:
            return (BitArray(uint = 24, length = 7).bin)
        elif self.instr_name == riscv_instr_name_t.DRET:
            return (BitArray(uint = 61, length = 7).bin)
        elif self.instr_name == riscv_instr_name_t.SFENCE_VMA:
            return (BitArray(uint = 9, length = 7).bin)
        else:
            logging.critical("Unsupported instruction {}".format(self.instr_name.name))
            sys.exit(1)

    # Convert the instruction to assembly code
    def convert2bin(self):
        pass  # TODO

    def get_instr_name(self):
        get_instr_name = self.instr_name.name
        get_instr_name = get_instr_name.replace("_", ".")
        return get_instr_name

    # Get RVC register name for CIW, CL, CS, CB format
    def get_c_gpr(self, gpr):
        return self.gpr

    # Default return imm value directly, can be overriden to use labels and symbols
    def get_imm(self):
        return self.imm_str

    def clear_unused_label(self):
        if(self.has_label and not(self.is_branch_target) and self.is_local_numeric_label):
            self.has_label = 0

    def do_copy(self):
        pass  # TODO

    def update_imm_str(self):
        self.imm_str = str(self.uintToInt(self.imm))

    def uintToInt(self, x):
        if x < (2 ** rcs.XLEN) / 2:
            signed_x = x
        else:
            signed_x = x - 2 ** rcs.XLEN
        return signed_x
