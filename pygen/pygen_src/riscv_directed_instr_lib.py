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

import random
import vsc
from enum import IntEnum, auto
from pygen_src.riscv_instr_stream import riscv_rand_instr_stream
from pygen_src.isa.riscv_instr import riscv_instr, riscv_instr_ins
from pygen_src.riscv_instr_gen_config import cfg
from pygen_src.riscv_instr_pkg import riscv_reg_t, riscv_pseudo_instr_name_t, riscv_instr_name_t, mem_region_t
from pygen_src.target.rv32i import riscv_core_setting as rcs
from pygen_src.riscv_pseudo_instr import riscv_pseudo_instr


class riscv_directed_instr_stream(riscv_rand_instr_stream):

    label = ""

    def __init__(self):
        super().__init__()
        self.name = ""

    def post_randomize(self):
        for i in range(len(self.instr_list)):
            self.instr_list[i].has_label = 0
            self.instr_list[i].atomic = 1
        self.instr_list[0].comment = "Start %0s" % (self.name)
        self.instr_list[-1].comment = "End %0s" % (self.name)
        if riscv_directed_instr_stream.label != "":
            self.instr_list[0].label = riscv_directed_instr_stream.label
            self.instr_list[0].has_label = 1


@vsc.randobj
class riscv_mem_access_stream(riscv_directed_instr_stream):
    def __init__(self):
        super().__init__()
        self.max_data_page_id = 0
        self.load_store_shared_memory = 0
        self.data_page = {}

    def pre_randomize(self):
        if(self.load_store_shared_memory):
            self.data_page = cfg.amo_region
        elif(self.kernel_mode):
            self.data_page = cfg.s_mem_region
        else:
            self.data_page = cfg.mem_region
        self.max_data_page_id = len(self.data_page)
    def add_rs1_init_la_instr(self, gpr, id, base):
        pass

    def add_mixed_instr(self, instr_cnt):
        pass


@vsc.randobj
class riscv_jal_instr(riscv_rand_instr_stream):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.jump = []
        self.jump_start = riscv_instr()
        self.jump_end = riscv_instr()
        self.num_of_jump_instr = vsc.rand_int_t()

    @vsc.constraint
    def instr_c(self):
        self.num_of_jump_instr in vsc.rangelist(vsc.rng(10, 30))

    def post_randomize(self):
        order = []
        RA = cfg.ra
        order = [0] * self.num_of_jump_instr
        self.jump = [0] * self.num_of_jump_instr
        for i in range(len(order)):
            order[i] = i
        random.shuffle(order)
        self.setup_allowed_instr(1, 1)
        jal = [riscv_instr_name_t.JAL]
        if(not cfg.disable_compressed_instr):
            jal.append(riscv_instr_name_t.C_J)
            if(rcs.XLEN == 32):
                jal.append(riscv_instr_name_t.C_JAL)
        self.jump_start = riscv_instr_ins.get_instr(riscv_instr_name_t.JAL.name)
        with self.jump_start.randomize_with() as it:
            self.jump_start.rd == RA
        self.jump_start.imm_str = "{}f".format(order[0])
        self.jump_start.label = self.label

        # Last instruction
        self.jump_end = self.randomize_instr(self.jump_end)
        self.jump_end.label = "{}".format(self.num_of_jump_instr)
        for i in range(self.num_of_jump_instr):
            self.jump[i] = riscv_instr_ins.get_rand_instr(include_instr = [jal[0].name])
            with self.jump[i].randomize_with() as it:
                if(self.jump[i].has_rd):
                    vsc.dist(self.jump[i].rd, [vsc.weight(riscv_reg_t.RA, 5), vsc.weight(
                        vsc.rng(riscv_reg_t.SP, riscv_reg_t.T0), 1),
                        vsc.weight(vsc.rng(riscv_reg_t.T2, riscv_reg_t.T6), 2)])
                    self.jump[i].rd.not_inside(cfg.reserved_regs)
            self.jump[i].label = "{}".format(i)

        for i in range(len(order)):
            if(i == self.num_of_jump_instr - 1):
                self.jump[order[i]].imm_str = "{}f".format(self.num_of_jump_instr)
            else:
                if(order[i + 1] > order[i]):
                    self.jump[order[i]].imm_str = "{}f".format(order[i+1])
                else:
                    self.jump[order[i]].imm_str = "{}b".format(order[i+1])
        self.instr_list.append(self.jump_start)
        self.instr_list.extend(self.jump)
        self.instr_list.append(self.jump_end)
        for i in range(len(self.instr_list)):
            self.instr_list[i].has_label = 1
            self.instr_list[i].atomic = 1


class int_numeric_e(IntEnum):
    NormalValue = auto()
    Zero = auto()
    AllOne = auto()
    NegativeMax = auto()


@vsc.randobj
class riscv_int_numeric_corner_stream(riscv_directed_instr_stream):
    def __init__(self):
        super().__init__()
        self.num_of_avail_regs = 10
        self.num_of_instr = vsc.rand_uint8_t()
        self.init_val = vsc.rand_list_t(vsc.rand_bit_t(rcs.XLEN - 1), sz = 10)
        self.init_val_type = vsc.rand_list_t(vsc.enum_t(int_numeric_e), sz =10)
        self.init_instr = []

    @vsc.constraint
    def init_val_c(self):
        # TO DO
        # solve init_val_type before init_val;
        self.init_val_type.size == self.num_of_avail_regs
        self.init_val.size == self.num_of_avail_regs
        self.num_of_instr in vsc.rangelist(vsc.rng(15, 30))

    @vsc.constraint
    def avail_regs_c(self):
        self.avail_regs.size == self.num_of_avail_regs
        vsc.unique(self.avail_regs)
        with vsc.foreach(self.avail_regs, idx = True) as i:
            self.avail_regs[i].not_inside(cfg.reserved_regs)
            self.avail_regs[i] != riscv_reg_t.ZERO

    def pre_randomize(self):
        pass

    def post_randomize(self):
        self.init_instr = [None] * self.num_of_avail_regs
        for i in range(len(self.init_val_type)):
            if self.init_val_type[i] == int_numeric_e.Zero:
                self.init_val[i] = 0
            elif self.init_val_type[i] == int_numeric_e.AllOne:
                self.init_val[i] = 1
            elif self.init_val_type[i] == int_numeric_e.NegativeMax:
                self.init_val[i] = 1 << (rcs.XLEN - 1)
            self.init_instr[i] = riscv_pseudo_instr()
            self.init_instr[i].rd = self.avail_regs[i]
            self.init_instr[i].pseudo_instr_name = riscv_pseudo_instr_name_t.LI
            self.init_instr[i].imm_str = "0x%0x" % (self.init_val[i])
            self.instr_list.append(self.init_instr[i])
        for i in range(self.num_of_instr):
            instr = riscv_instr_ins.get_rand_instr(
                include_category = ['ARITHMETIC'],
                exclude_group = ['RV32C', 'RV64C', 'RV32F', 'RV64F', 'RV32D', 'RV64D'])
            instr = self.randomize_gpr(instr)
            self.instr_list.append(instr)
        super().post_randomize()
