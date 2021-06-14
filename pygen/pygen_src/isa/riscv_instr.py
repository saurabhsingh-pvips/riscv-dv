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
from enum import auto, IntEnum
from pygen_src.riscv_instr_pkg import (pkg_ins, riscv_instr_category_t, riscv_reg_t,
                                       riscv_instr_name_t, riscv_instr_format_t,
                                       riscv_instr_group_t, imm_t, privileged_reg_t,
                                       hazard_e, get_val)
from pygen_src.riscv_instr_gen_config import cfg
rcs = import_module("pygen_src.target." + cfg.argv.target + ".riscv_core_setting")
reload(logging)
logging.basicConfig(filename='{}'.format(cfg.argv.log_file_name),
                    filemode='w',
                    format="%(asctime)s %(filename)s %(lineno)s %(levelname)s %(message)s",
                    level=logging.DEBUG)


class operand_sign_e(IntEnum):
    POSITIVE = 0
    NEGATIVE = auto()


class div_result_e(IntEnum):
    DIV_NORMAL = 0
    DIV_BY_ZERO = auto()
    DIV_OVERFLOW = auto()


class div_result_ex_overflow_e(IntEnum):
    DIV_NORMAL = 0
    DIV_BY_ZERO = auto()


class compare_result_e(IntEnum):
    EQUAL = 0
    LARGER = auto()
    SMALLER = auto()


class logical_similarity_e(IntEnum):
    IDENTICAL = 0
    OPPOSITE = auto()
    SIMILAR = auto()
    DIFFERENT = auto()


class special_val_e(IntEnum):
    NORMAL_VAL = 0
    MIN_VAL = auto()
    MAX_VAL = auto()
    ZERO_VAL = auto()


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

    # class attr. to keep track of reg_name:reg_value throughout the program
    gpr_state = {}

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

        #---------------------------------Coverage Related variables------------------------
        self.pc = vsc.bit_t(rcs.XLEN)
        self.binary = vsc.bit_t(32)  # Instruction binary
        self.trace = "None"  # String representation of the instruction

        self.rs1_value = vsc.bit_t(rcs.XLEN)
        self.rs2_value = vsc.bit_t(rcs.XLEN)
        self.rs3_value = vsc.bit_t(rcs.XLEN)
        self.rd_value = vsc.bit_t(rcs.XLEN)
        self.fs1_value = vsc.bit_t(rcs.XLEN)
        self.fs2_value = vsc.bit_t(rcs.XLEN)
        self.fs3_value = vsc.bit_t(rcs.XLEN)
        self.fd_value = vsc.bit_t(rcs.XLEN)

        self.mem_addr = vsc.bit_t(rcs.XLEN)
        self.unaligned_pc = 0
        self.unaligned_mem_access = 0
        self.compressed = 0
        self.branch_hit = 0
        self.div_result = None
        self.rs1_sign = 0
        self.rs2_sign = 0
        self.rs3_sign = 0
        self.fs1_sign = 0
        self.fs2_sign = 0
        self.fs3_sign = 0
        self.imm_sign = 0
        self.rd_sign = 0
        self.fd_sign = 0
        self.gpr_hazard = hazard_e.NO_HAZARD
        self.lsu_hazard = hazard_e.NO_HAZARD
        self.rs1_special_value = 0
        self.rs2_special_value = 0
        self.rs3_special_value = 0
        self.rd_special_value = 0
        self.imm_special_value = 0
        self.compare_result = 0
        self.logical_similarity = 0

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

    # Create the list of instructions based on the supported ISA extensions and configuration
    # of the generator
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
                    instr_inst.group.name in ["RV32C", "RV64C", "RV32DC",
                                              "RV32FC", "RV128C"]) and
                    not(not(cfg.enable_floating_point) and instr_inst.group.name in
                    ["RV32F", "RV64F", "RV32D", "RV64D"])):
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
        if(cfg.no_csr_instr == 0 and cfg.init_privileged_mode == "MACHINE_MODE"):
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
            if cfg.init_privileged_mode == "MACHINE_MODE":      # Machine Mode
                cls.include_reg.append("MSCRATCH")
            elif cfg.init_privileged_mode == "SUPERVISOR_MODE":  # Supervisor Mode
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
                logging.critical("[%s] Cannot generate random instruction", riscv_instr.__name__)
                sys.exit(1)
        else:
            try:
                name = random.choice(cls.instr_names)
                if len(include_instr) > 0:
                    name = random.choice(include_instr)
                if len(allowed_instr) > 0:
                    name = random.choice(allowed_instr)
            except Exception:
                logging.critical("[%s] Cannot generate random instruction", riscv_instr.__name__)
                sys.exit(1)
        # rs1 rs2 values are overwriting and the last generated values are
        # getting assigned for a particular instruction hence creating different
        # object address and id to ratain the randomly generated values.
        instr_h = copy.deepcopy(cls.instr_template[name])
        return instr_h

    @classmethod
    def get_load_store_instr(cls, load_store_instr):
        instr_h = riscv_instr()
        if len(load_store_instr) == 0:
            load_store_instr = cls.instr_category["LOAD"] + \
                cls.instr_category["STORE"]
        cls.idx = random.randrange(0, len(load_store_instr) - 1)
        name = load_store_instr[cls.idx]
        instr_h = copy.copy(cls.instr_template[name])
        return instr_h

    @classmethod
    def get_instr(cls, name):
        if not cls.instr_template.get(name):
            logging.critical("Cannot get instr %s", name)
            sys.exit(1)
        instr_h = copy.copy(cls.instr_template[name])
        return instr_h

    def set_rand_mode(self):
        # rand_mode setting for Instruction Format
        if self.format.name == "R_FORMAT":
            self.has_imm = 0
        if self.format.name == "I_FORMAT":
            self.has_rs2 = 0
        if self.format.name in ["S_FORMAT", "B_FORMAT"]:
            self.has_rd = 0
        if self.format.name in ["U_FORMAT", "J_FORMAT"]:
            self.has_rs1 = 0
            self.has_rs2 = 0

        # rand_mode setting for Instruction Category
        if self.category.name == "CSR":
            self.has_rs2 = 0
            if self.format.name == "I_FORMAT":
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
        if self.format.name in ["U_FORMAT", "J_FORMAT"]:
            self.imm_len = 20
        elif self.format.name in ["I_FORMAT", "S_FORMAT", "B_FORMAT"]:
            if self.imm_type.name == "UIMM":
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
        if(sign and not((self.format.name == "U_FORMAT") or
                        (self.imm_type.name in ["UIMM", "NZUIMM"]))):
            self.imm = self.imm_mask | self.imm

    def post_randomize(self):
        self.extend_imm()
        self.update_imm_str()

    def convert2asm(self, prefix = " "):
        asm_str = pkg_ins.format_string(string = self.get_instr_name(),
                                        length = pkg_ins.MAX_INSTR_STR_LEN)
        if self.category != riscv_instr_category_t.SYSTEM:
            if self.format == riscv_instr_format_t.J_FORMAT:
                asm_str = '{} {}, {}'.format(asm_str, self.rd.name, self.get_imm())
            elif self.format == riscv_instr_format_t.U_FORMAT:
                asm_str = '{} {}, {}'.format(asm_str, self.rd.name, self.get_imm())
            elif self.format == riscv_instr_format_t.I_FORMAT:
                if self.instr_name == riscv_instr_name_t.NOP:
                    asm_str = "nop"
                elif self.instr_name == riscv_instr_name_t.WFI:
                    asm_str = "wfi"
                elif self.instr_name == riscv_instr_name_t.FENCE:
                    asm_str = "fence"
                elif self.instr_name == riscv_instr_name_t.FENCE_I:
                    asm_str = "fence.i"
                elif self.category == riscv_instr_category_t.LOAD:
                    asm_str = '{} {}, {} ({})'.format(
                        asm_str, self.rd.name, self.get_imm(), self.rs1.name)
                elif self.category == riscv_instr_category_t.CSR:
                    asm_str = '{} {}, 0x{}, {}'.format(
                        asm_str, self.rd.name, self.csr, self.get_imm())
                else:
                    asm_str = '{} {}, {}, {}'.format(
                        asm_str, self.rd.name, self.rs1.name, self.get_imm())
            elif self.format == riscv_instr_format_t.S_FORMAT:
                if self.category == riscv_instr_category_t.STORE:
                    asm_str = '{} {}, {} ({})'.format(
                        asm_str, self.rs2.name, self.get_imm(), self.rs1.name)
                else:
                    asm_str = '{} {}, {}, {}'.format(
                        asm_str, self.rs1.name, self.rs2.name, self.get_imm())

            elif self.format == riscv_instr_format_t.B_FORMAT:
                if self.category == riscv_instr_category_t.STORE:
                    asm_str = '{} {}, {} ({})'.format(
                        asm_str, self.rs2.name, self.get_imm(), self.rs1.name)
                else:
                    asm_str = '{} {}, {}, {}'.format(
                        asm_str, self.rs1.name, self.rs2.name, self.get_imm())

            elif self.format == riscv_instr_format_t.R_FORMAT:
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
            if self.instr_name == riscv_instr_name_t.EBREAK:
                asm_str = ".4byte 0x00100073 # ebreak"

        if self.comment != "":
            asm_str = asm_str + " #" + self.comment
        return asm_str.lower()

    def get_opcode(self):
        if self.instr_name == "LUI":
            return (BitArray(uint = 55, length = 7).bin)
        elif self.instr_name == "AUIPC":
            return (BitArray(uint = 23, length = 7).bin)
        elif self.instr_name == "JAL":
            return (BitArray(uint = 23, length = 7).bin)
        elif self.instr_name == "JALR":
            return (BitArray(uint = 111, length = 7).bin)
        elif self.instr_name in ["BEQ", "BNE", "BLT", "BGE", "BLTU", "BGEU"]:
            return (BitArray(uint = 103, length = 7).bin)
        elif self.instr_name in ["LB", "LH", "LW", "LBU", "LHU", "LWU", "LD"]:
            return (BitArray(uint = 99, length = 7).bin)
        elif self.instr_name in ["SB", "SH", "SW", "SD"]:
            return (BitArray(uint = 35, length = 7).bin)
        elif self.instr_name in ["ADDI", "SLTI", "SLTIU", "XORI", "ORI", "ANDI",
                                 "SLLI", "SRLI", "SRAI", "NOP"]:
            return (BitArray(uint = 19, length = 7).bin)
        elif self.instr_name in ["ADD", "SUB", "SLL", "SLT", "SLTU", "XOR", "SRL",
                                 "SRA", "OR", "AND", "MUL", "MULH", "MULHSU", "MULHU",
                                 "DIV", "DIVU", "REM", "REMU"]:
            return (BitArray(uint = 51, length = 7).bin)
        elif self.instr_name in ["ADDIW", "SLLIW", "SRLIW", "SRAIW"]:
            return (BitArray(uint = 27, length = 7).bin)
        elif self.instr_name in ["MULH", "MULHSU", "MULHU", "DIV", "DIVU", "REM", "REMU"]:
            return (BitArray(uint = 51, length = 7).bin)
        elif self.instr_name in ["FENCE", "FENCE_I"]:
            return (BitArray(uint = 15, length = 7).bin)
        elif self.instr_name in ["ECALL", "EBREAK", "CSRRW", "CSRRS", "CSRRC", "CSRRWI",
                                 "CSRRSI", "CSRRCI"]:
            return (BitArray(uint = 115, length = 7).bin)
        elif self.instr_name in ["ADDW", "SUBW", "SLLW", "SRLW", "SRAW", "MULW", "DIVW",
                                 "DIVUW", "REMW", "REMUW"]:
            return (BitArray(uint = 59, length = 7).bin)
        elif self.instr_name in ["ECALL", "EBREAK", "URET", "SRET", "MRET", "DRET", "WFI",
                                 "SFENCE_VMA"]:
            return (BitArray(uint = 115, length = 7).bin)
        else:
            logging.critical("Unsupported instruction %0s", self.instr_name)
            sys.exit(1)

    def get_func3(self):
        if self.instr_name in ["JALR", "BEQ", "LB", "SB", "ADDI", "NOP", "ADD", "SUB",
                               "FENCE", "ECALL", "EBREAK", "ADDIW", "ADDW", "SUBW", "MUL",
                               "MULW", "ECALL", "EBREAK", "URET", "SRET", "MRET", "DRET",
                               "WFI", "SFENCE_VMA"]:
            return (BitArray(uint = 0, length = 3).bin)
        elif self.instr_name in ["BNE", "LH", "SH", "SLLI", "SLL", "FENCE_I", "CSRRW", "SLLIW",
                                 "SLLW", "MULH"]:
            return (BitArray(uint = 1, length = 3).bin)
        elif self.instr_name in ["LW", "SW", "SLTI", "SLT", "CSRRS", "MULHS"]:
            return (BitArray(uint = 2, length = 3).bin)
        elif self.instr_name in ["SLTIU", "SLTU", "CSRRC", "LD", "SD", "MULHU"]:
            return (BitArray(uint = 3, length = 3).bin)
        elif self.instr_name in ["BLT", "LBU", "XORI", "XOR", "DIV", "DIVW"]:
            return (BitArray(uint = 4, length = 3).bin)
        elif self.instr_name in ["BGE", "LHU", "SRLI", "SRAI", "SRL", "SRA", "CSRRWI", "SRLIW",
                                 "SRAIW", "SRLW",
                                 "SRAW", "DIVU", "DIVUW"]:
            return (BitArray(uint = 5, length = 3).bin)
        elif self.instr_name in ["BLTU", "ORI", "OR", "CSRRSI", "LWU", "REM", "REMW"]:
            return (BitArray(uint = 6, length = 3).bin)
        elif self.instr_name in ["BGEU", "ANDI", "AND", "CSRRCI", "REMU", "REMUW"]:
            return (BitArray(uint = 7, length = 3).bin)
        else:
            logging.critical("Unsupported instruction %0s", self.instr_name)
            sys.exit(1)

    def get_func7(self):
        if self.instr_name in ["SLLI", "SRLI", "ADD", "SLL", "SLT", "SLTU", "XOR",
                               "SRL", "OR", "AND", "FENCE", "FENCE_I", "SLLIW",
                               "SRLIW", "ADDW", "SLLW", "SRLW", "ECALL", "EBREAK", "URET"]:
            return (BitArray(uint = 0, length = 7).bin)
        elif self.instr_name in ["SUB", "SRA", "SRAIW", "SUBW", "SRAW"]:
            return (BitArray(uint = 32, length = 7).bin)
        elif self.instr_name in ["MUL", "MULH", "MULHSU", "MULHU", "DIV", "DIVU", "REM",
                                 "REMU", "MULW", "DIVW", "DIVUW", "REMW", "REMUW"]:
            return (BitArray(uint = 1, length = 7).bin)
        elif self.instr_name in ["SRET", "WFI"]:
            return (BitArray(uint = 8, length = 7).bin)
        elif self.instr_name == "MRET":
            return (BitArray(uint = 24, length = 7).bin)
        elif self.instr_name == "DRET":
            return (BitArray(uint = 61, length = 7).bin)
        elif self.instr_name == "SFENCE_VMA":
            return (BitArray(uint = 9, length = 7).bin)
        else:
            logging.critical("Unsupported instruction %0s", self.instr_name)
            sys.exit(1)

    def convert2bin(self):
        pass  # TODO

    def get_instr_name(self):
        get_instr_name = self.instr_name.name
        get_instr_name = get_instr_name.replace("_", ".")
        return get_instr_name

    def get_c_gpr(self, gpr):
        return self.gpr

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

#-----------Coverage Related Functions--------------------------------------------------

    def pre_sample(self):
        unaligned_pc = self.pc % 4 != 0
        self.rs1_sign = self.get_operand_sign(self.rs1_value)
        self.rs2_sign = self.get_operand_sign(self.rs2_value)
        self.rs3_sign = self.get_operand_sign(self.rs3_value)
        self.rd_sign = self.get_operand_sign(self.rd_value)
        self.fs1_sign = self.get_operand_sign(self.fs1_value)
        self.fs2_sign = self.get_operand_sign(self.fs2_value)
        self.fs3_sign = self.get_operand_sign(self.fs3_value)
        self.fd_sign = self.get_operand_sign(self.fd_value)
        self.imm_sign = self.get_imm_sign(self.imm)
        self.rs1_special_value = self.get_operand_special_value(self.rs1_value)
        self.rd_special_value = self.get_operand_special_value(self.rd_value)
        self.rs2_special_value = self.get_operand_special_value(self.rs2_value)
        self.rs3_special_value = self.get_operand_special_value(self.rs3_value)
        if self.format.name not in ["R_FORMAT", "CR_FORMAT"]:
            self.imm_special_value = self.get_imm_special_val(self.imm)
        if self.category.name in ["COMPARE", "BRANCH"]:
            self.compare_result = self.get_compare_result()
        if self.category.name in ["LOAD", "STORE"]:
            self.mem_addr = self.rs1_value + self.imm
            self.unaligned_mem_access = self.is_unaligned_mem_access()
            if self.unaligned_mem_access:
                logging.info("Unaligned: {}, mem_addr: {}".format(
                    self.instr_name.name, self.mem_addr))
        if self.category.name == "LOGICAL":
            self.logical_similarity = self.get_logical_similarity()
        if self.category.name == "BRANCH":
            self.branch_hit = self.is_branch_hit()
        if self.instr_name.name in ["DIV", "DIVU", "REM", "REMU", "DIVW", "DIVUW",
                               "REMW", "REMUW"]:
            self.div_result = self.get_div_result()

    @staticmethod
    def get_operand_sign(operand):
        # TODO: Currently handled using string formatting as part select
        #  isn't yet supported for global vsc variables
        operand_bin = format(operand, '#0{}b'.format(rcs.XLEN + 2))
        # "0b" is the prefix, so operand_bin[2] is the sign bit
        if operand_bin[2] == "0":
            return operand_sign_e["POSITIVE"]
        else:
            return operand_sign_e["NEGATIVE"]

    def is_unaligned_mem_access(self):
        if (self.instr_name.name in ["LWU", "LD", "SD", "C_LD", "C_SD"] and
                self.mem_addr % 8 != 0):
            return 1
        elif (self.instr_name.name in ["LW", "SW", "C_LW", "C_SW"] and
              self.mem_addr % 4 != 0):
            return 1
        elif (self.instr_name.name in ["LH", "LHU", "SH"] and
              self.mem_addr % 2 != 0):
            return 1
        return 0

    @staticmethod
    def get_imm_sign(imm):
        # TODO: Currently handled using string formatting as part select
        #  isn't yet supported for global vsc variables
        imm_bin = format(imm, '#0{}b'.format(rcs.XLEN + 2))
        # "0b" is the prefix, so imm_bin[2] is the sign bit
        if imm_bin[2] == "0":
            return operand_sign_e["POSITIVE"]
        else:
            return operand_sign_e["NEGATIVE"]


    def get_div_result(self):
        if self.rs2_value == 0:
            return div_result_e["DIV_BY_ZERO"]
        elif (self.rs2_value == 1
              and self.rs1_value == (1 << (rcs.XLEN - 1))):
            return div_result_e["DIV_OVERFLOW"]
        else:
            return div_result_e["DIV_NORMAL"]

    @staticmethod
    def get_operand_special_value(operand):
        if operand == 0:
            return special_val_e["ZERO_VAL"]
        elif operand == 1 << (rcs.XLEN - 1):
            return special_val_e["MIN_VAL"]
        elif operand == 1 >> 1:
            return special_val_e["MAX_VAL"]
        else:
            return special_val_e["NORMAL_VAL"]

    def get_imm_special_val(self, imm):
        if imm == 0:
            return special_val_e["ZERO_VAL"]
        elif self.format == riscv_instr_format_t.U_FORMAT:
            # unsigned immediate value
            max_val = (1 << self.imm_len) - 1
            if imm == 0:
                return special_val_e["MIN_VAL"]
            if imm == max_val:
                return special_val_e["MAX_VAL"]
        else:
            # signed immediate value
            max_val = 2 ** (self.imm_len - 1) - 1
            min_val = -2 ** (self.imm_len - 1)
            if min_val == imm:
                return special_val_e["MIN_VAL"]
            if max_val == imm:
                return special_val_e["MAX_VAL"]
        return special_val_e["NORMAL_VAL"]

    def get_compare_result(self):
        val1 = self.rs1_value
        val2 = (self.imm if (self.format == riscv_instr_format_t.I_FORMAT)
                        else self.rs2_value)
        if val1 == val2:
            return compare_result_e["EQUAL"]
        elif val1 < val2:
            return compare_result_e["SMALLER"]
        else:
            return compare_result_e["LARGER"]
    def is_branch_hit(self):
        if self.instr_name.name == "BEQ":
            return int(self.rs1_value == self.rs2_value)
        elif self.instr_name.name == "C_BEQZ":
            return int(self.rs1_value == 0)
        elif self.instr_name.name == "BNE":
            return int(self.rs1_value != self.rs2_value)
        elif self.instr_name.name == "C_BNEZ":
            return int(self.rs1_value != 0)
        elif self.instr_name.name == "BLT" or self.instr_name.name == "BLTU":
            return int(self.rs1_value < self.rs2_value)
        elif self.instr_name.name == "BGE" or self.instr_name.name == "BGEU":
            return int(self.rs1_value >= self.rs2_value)
        else:
            logging.error("Unexpected instruction {}".format(self.instr_name.name))

    def get_logical_similarity(self):
        val1 = self.rs1_value
        val2 = (self.imm if self.format == riscv_instr_format_t.I_FORMAT
                                    else self.rs2_value)
        temp = bin(val1 ^ val2)
        bit_difference = len([[ones for ones in temp[2:] if ones == '1']])
        if val1 == val2:
            return logical_similarity_e["IDENTICAL"]
        elif bit_difference == 32:
            return logical_similarity_e["OPPOSITE"]
        elif bit_difference < 5:
            return logical_similarity_e["SIMILAR"]
        else:
            return logical_similarity_e["DIFFERENT"]

    def check_hazard_condition(self, pre_instr):
        '''TODO: There are cases where instruction actually has destination but
        ovpsim doesn't log it because of no change in its value. Hence,
        the result of the check_hazard_condition won't be accurate. Need to
        explicitly extract the destination register from the operands '''
        if pre_instr.has_rd:
            if ((self.has_rs1 and self.rs1 == pre_instr.rd) or
                    (self.has_rs2 and self.rs1 == pre_instr.rd)):
                self.gpr_hazard = hazard_e["RAW_HAZARD"]
            elif self.has_rd and self.rd == pre_instr.rd:
                self.gpr_hazard = hazard_e["WAW_HAZARD"]
            elif (self.has_rd and
                  ((pre_instr.has_rs1 and (pre_instr.rs1 == self.rd)) or
                   (pre_instr.has_rs2 and (pre_instr.rs2 == self.rd)))):
                self.gpr_hazard = hazard_e["WAR_HAZARD"]
            else:
                self.gpr_hazard = hazard_e["NO_HAZARD"]
        if self.category == riscv_instr_category_t.LOAD:
            if (pre_instr.category == riscv_instr_category_t.STORE and
                    pre_instr.mem_addr == self.mem_addr):
                self.lsu_hazard = hazard_e["RAW_HAZARD"]
            else:
                self.lsu_hazard = hazard_e["NO_HAZARD"]
        if self.category == riscv_instr_category_t.STORE:
            if (pre_instr.category == riscv_instr_category_t.STORE and
                    pre_instr.mem_addr == self.mem_addr):
                self.lsu_hazard = hazard_e["WAW_HAZARD"]
            elif (pre_instr.category == riscv_instr_category_t.LOAD and
                  pre_instr.mem_addr == self.mem_addr):
                self.lsu_hazard = hazard_e["WAR_HAZARD"]
            else:
                self.lsu_hazard = hazard_e["NO_HAZARD"]
        logging.debug("Pre PC/name: {}/{}, Cur PC/name: {}/{}, "
                      "Hazard: {}/{}".format(pre_instr.pc,
                                             pre_instr.instr_name.name,
                                             self.pc,
                                             self.instr_name.name,
                                             self.gpr_hazard.name,
                                             self.lsu_hazard.name))

    def update_src_regs(self, operands):
        if self.format.name in ["J_FORMAT", "U_FORMAT"]:
            # instr rd,imm
            assert len(operands) == 2
            self.imm = get_val(operands[1])
        elif self.format.name == "I_FORMAT":
            assert len(operands) == 3
            if self.category.name == "LOAD":
                # load rd, imm(rs1)
                self.rs1 = self.get_gpr(operands[2])
                self.rs1_value = self.get_gpr_state(operands[2])
                self.imm = get_val(operands[1])
            elif self.category.name == "CSR":
                # csrrwi rd, csr, imm
                self.imm = get_val(operands[2])
                if operands[1].upper() in privileged_reg_t.__members__:
                    self.csr = privileged_reg_t[operands[1].upper()].value
                else:
                    self.csr = get_val(operands[1])
            else:
                # addi rd, rs1, imm
                self.rs1 = self.get_gpr(operands[1])
                self.rs1_value = self.get_gpr_state(operands[1])
                self.imm = get_val(operands[2])
        elif self.format.name in ["S_FORMAT", "B_FORMAT"]:
            assert len(operands) == 3
            if self.category.name == "STORE":
                self.rs2 = self.get_gpr(operands[0])
                self.rs2_value = self.get_gpr_state(operands[0])
                self.rs1 = self.get_gpr(operands[2])
                self.rs1_value = self.get_gpr_state(operands[2])
                self.imm = get_val(operands[1])
            else:
                # bne rs1, rs2, imm
                self.rs1 = self.get_gpr(operands[0])
                self.rs1_value = self.get_gpr_state(operands[0])
                self.rs2 = self.get_gpr(operands[1])
                self.rs2_value = self.get_gpr_state(operands[1])
                self.imm = get_val(operands[2])
        elif self.format.name == "R_FORMAT":
            if self.has_rs2 or self.category.name == "CSR":
                assert len(operands) == 3
            else:
                assert len(operands) == 2
            if self.category.name == "CSR":
                # csrrw rd, csr, rs1
                if operands[1].upper() in privileged_reg_t.__members__:
                    self.csr = privileged_reg_t[operands[1].upper()].value
                else:
                    self.csr = get_val(operands[1])
                self.rs1 = self.get_gpr(operands[2])
                self.rs1_value = self.get_gpr_state(operands[2])
            else:
                # add rd, rs1, rs2
                self.rs1 = self.get_gpr(operands[1])
                self.rs1_value = self.get_gpr_state(operands[1])
                if self.has_rs2:
                    self.rs2 = self.get_gpr(operands[2])
                    self.rs2_value = self.get_gpr_state(operands[2])
        elif self.format.name == "R4_FORMAT":
            assert len(operands) == 4
            self.rs1 = self.get_gpr(operands[1])
            self.rs1_value = self.get_gpr_state(operands[1])
            self.rs2 = self.get_gpr(operands[2])
            self.rs2_value = self.get_gpr_state(operands[2])
            self.rs2 = self.get_gpr(operands[3])
            self.rs2_value = self.get_gpr_state(operands[3])
        elif self.format.name in ["CI_FORMAT", "CIW_FORMAT"]:
            if self.instr_name.name == "C_ADDI16SP":
                self.imm = get_val(operands[1])
                self.rs1 = riscv_reg_t.SP
                self.rs1_value = self.get_gpr_state("sp")
            elif self.instr_name.name == "C_ADDI4SPN":
                self.rs1 = riscv_reg_t.SP
                self.rs1_value = self.get_gpr_state("sp")
            elif self.instr_name.name in ["C_LDSP", "C_LWSP", "C_LQSP"]:
                # c.ldsp rd, imm
                self.imm = get_val(operands[1])
                self.rs1 = riscv_reg_t.SP
                self.rs1_value = self.get_gpr_state("sp")
            else:
                # c.lui rd, imm
                self.imm = get_val(operands[1])
        elif self.format.name == "CL_FORMAT":
            # c.lw rd, imm(rs1)
            self.imm = get_val(operands[1])
            self.rs1 = self.get_gpr(operands[2])
            self.rs1_value = self.get_gpr_state(operands[2])
        elif self.format.name == "CS_FORMAT":
            # c.sw rs2,imm(rs1)
            self.rs2 = self.get_gpr(operands[0])
            self.rs2_value = self.get_gpr_state(operands[0])
            self.rs1 = self.get_gpr(operands[2])
            self.rs1_value = self.get_gpr_state(operands[2])
            self.imm = get_val(operands[1])
        elif self.format.name == "CA_FORMAT":
            # c.and rd, rs2 (rs1 == rd)
            self.rs2 = self.get_gpr(operands[1])
            self.rs2_value = self.get_gpr_state(operands[1])
            self.rs1 = self.get_gpr(operands[0])
            self.rs1_value = self.get_gpr_state(operands[0])
        elif self.format.name == "CB_FORMAT":
            # c.beqz rs1, imm
            self.rs1 = self.get_gpr(operands[0])
            self.rs1_value = self.get_gpr_state(operands[0])
            self.imm = get_val(operands[1])
        elif self.format.name == "CSS_FORMAT":
            # c.swsp rs2, imm
            self.rs2 = self.get_gpr(operands[0])
            self.rs2_value = self.get_gpr_state(operands[0])
            self.rs1 = riscv_reg_t.SP
            self.rs1_value = self.get_gpr_state("sp")
            self.imm = get_val(operands[1])
        elif self.format.name == "CR_FORMAT":
            if self.instr_name.name in ["C_JR", "C_JALR"]:
                # c.jalr rs1
                self.rs1 = self.get_gpr(operands[0])
                self.rs1_value = self.get_gpr_state(operands[0])
            else:
                # c.add rd, rs2
                self.rs2 = self.get_gpr(operands[1])
                self.rs2_value = self.get_gpr_state(operands[1])
        elif self.format.name == "CJ_FORMAT":
            # c.j imm
            self.imm = get_val(operands[0])
        else:
            logging.error("Unsupported format {}".format(self.format.name))

    def update_dst_regs(self, reg_name, val_str):
        self.gpr_state[reg_name] = get_val(val_str, hexa=1)
        self.rd = self.get_gpr(reg_name)
        self.rd_value = self.get_gpr_state(reg_name)

    @staticmethod
    def get_gpr(reg_name):
        reg_name = reg_name.upper()
        if reg_name not in riscv_reg_t.__members__:
            logging.error("Cannot convert {} to GPR".format(reg_name))
        return riscv_reg_t[reg_name]

    @staticmethod
    def get_gpr_state(name):
        if name in ["zero", "x0"]:
            return 0
        elif name in riscv_instr.gpr_state:
            return riscv_instr.gpr_state[name]
        else:
            logging.warning(
                "Cannot find GPR state: {}; initialize to 0".format(name))
            if name.upper() in riscv_reg_t.__members__:
                riscv_instr.gpr_state[name] = 0
            return 0
