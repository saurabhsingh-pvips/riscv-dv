
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

import sys
import random
import logging
import vsc
from enum import IntEnum, auto
from copy import deepcopy
from importlib import import_module
from pygen_src.riscv_instr_gen_config import cfg
from pygen_src.isa.riscv_instr import riscv_instr
from pygen_src.riscv_pseudo_instr import riscv_pseudo_instr
from pygen_src.riscv_directed_instr_lib import riscv_mem_access_stream
from pygen_src.riscv_instr_pkg import (riscv_reg_t, riscv_instr_name_t,
                                       riscv_instr_group_t, riscv_instr_category_t)
rcs = import_module("pygen_src.target." + cfg.argv.target + ".riscv_core_setting")


class locality_e(IntEnum):
    NARROW = 0
    HIGH = auto()
    MEDIUM = auto()
    SPARSE = auto()


# Base class for all load/store instruction stream
@vsc.randobj
class riscv_load_store_base_instr_stream(riscv_mem_access_stream):
    def __init__(self):
        super().__init__()
        self.num_load_store = vsc.rand_uint32_t()
        self.num_mixed_instr = vsc.rand_uint32_t()
        self.base = vsc.rand_int32_t()
        self.offset = []
        self.addr = []
        self.load_store_instr = []
        self.data_page_id = vsc.rand_uint32_t()
        self.rs1_reg = vsc.rand_enum_t(riscv_reg_t)
        self.locality = vsc.rand_enum_t(locality_e)
        self.max_load_store_offset = vsc.rand_int32_t()
        self.use_sp_as_rs1 = vsc.rand_bit_t()

    @vsc.constraint
    def sp_rnd_order_c(self):
        vsc.solve_order(self.use_sp_as_rs1, self.rs1_reg)

    @vsc.constraint
    def sp_c(self):
        vsc.dist(self.use_sp_as_rs1, [vsc.weight(1, 1), vsc.weight(0, 2)])
        with vsc.if_then(self.use_sp_as_rs1 == 1):
            self.rs1_reg == riscv_reg_t.SP

    # TODO Getting pyvsc error -- > rs1 has not been build yet
    '''@vsc.constraint
    def rs1_c(self):
        self.rs1_reg.not_inside(vsc.rangelist(cfg.reserved_regs,
                                              self.reserved_rd, riscv_reg_t.ZERO))'''

    @vsc.constraint
    def addr_c(self):
        # TODO solve_order
        # vsc.solve_order(self.data_page_id, self.max_load_store_offset)
        # vsc.solve_order(self.max_load_store_offset, self.base)
        self.data_page_id < self.max_data_page_id
        with vsc.foreach(self.data_page, idx = True) as i:
            with vsc.if_then(i == self.data_page_id):
                self.max_load_store_offset == self.data_page[i].size_in_bytes
        self.base in vsc.rangelist(vsc.rng(0, self.max_load_store_offset - 1))

    def randomize_offset(self):
        addr_ = vsc.rand_int32_t()
        offset_ = vsc.rand_int32_t()
        self.offset = [0] * self.num_load_store
        self.addr = [0] * self.num_load_store
        for i in range(self.num_load_store):
            try:
                if self.locality == locality_e.NARROW:
                    offset_ = random.randrange(-16, 16)
                elif self.locality == locality_e.HIGH:
                    offset_ = random.randrange(-64, 64)
                elif self.locality == locality_e.MEDIUM:
                    offset_ = random.randrange(-256, 256)
                elif self.locality == locality_e.SPARSE:
                    offset_ = random.randrange(-2048, 2047)
                var1 = self.base + offset_ - 1
                var2 = self.base + offset_ + 1
                addr_ = random.randrange(var1, var2)
            except Exception:
                logging.critical("Cannot randomize load/store offset")
                sys.exit(1)
            self.offset[i] = offset_
            self.addr[i] = addr_

    def pre_randomize(self):
        super().pre_randomize()
        if(riscv_reg_t.SP in [cfg.reserved_regs, self.reserved_rd]):
            self.use_sp_as_rs1 = 0
            with vsc.raw_mode():
                self.use_sp_as_rs1.rand_mode = False
            self.sp_rnd_order_c.constraint_mode(False)

    def post_randomize(self):
        self.randomize_offset()
        # rs1 cannot be modified by other instructions
        if not(self.rs1_reg in self.reserved_rd):
            self.reserved_rd.append(self.rs1_reg)
        self.gen_load_store_instr()
        self.add_mixed_instr(self.num_mixed_instr)
        self.add_rs1_init_la_instr(self.rs1_reg, self.data_page_id, self.base)
        super().post_randomize()

    # Generate each load/store instruction
    def gen_load_store_instr(self):
        allowed_instr = []
        enable_compressed_load_store = 0
        self.randomize_avail_regs()
        if ((self.rs1_reg in [riscv_reg_t.S0, riscv_reg_t.S1, riscv_reg_t.A0, riscv_reg_t.A1,
                              riscv_reg_t.A2, riscv_reg_t.A3, riscv_reg_t.A4, riscv_reg_t.A5,
                              riscv_reg_t.SP]) and not(cfg.disable_compressed_instr)):
            enable_compressed_load_store = 1
        for i in range(len(self.addr)):
            # Assign the allowed load/store instructions based on address alignment
            # This is done separately rather than a constraint to improve the randomization
            # performance
            allowed_instr.extend(
                [riscv_instr_name_t.LB, riscv_instr_name_t.LBU, riscv_instr_name_t.SB])
            if not cfg.enable_unaligned_load_store:
                if (self.addr[i] & 1) == 0:
                    allowed_instr.extend(
                        [riscv_instr_name_t.LH, riscv_instr_name_t.LHU, riscv_instr_name_t.SH])
                if self.addr[i] % 4 == 0:
                    allowed_instr.extend([riscv_instr_name_t.LW, riscv_instr_name_t.SW])
                    if cfg.enable_floating_point:
                        allowed_instr.extend([riscv_instr_name_t.FLW,
                                              riscv_instr_name_t.FSW])
                    if ((self.offset[i] in range(128)) and (self.offset[i] % 4 == 0) and
                        (riscv_instr_group_t.RV32C in rcs.supported_isa) and
                            (enable_compressed_load_store)):
                        if self.rs1_reg == riscv_reg_t.SP:
                            logging.info("Add LWSP/SWSP to allowed instr")
                            allowed_instr.extend(
                                [riscv_instr_name_t.C_LWSP, riscv_instr_name_t.C_SWSP])
                        else:
                            allowed_instr.extend(
                                [riscv_instr_name_t.C_LW, riscv_instr_name_t.C_SW])
                            if (cfg.enable_floating_point and
                                    riscv_instr_group_t.RV32FC in rcs.supported_isa):
                                allowed_instr.extend(
                                    [riscv_instr_name_t.C_FLW, riscv_instr_name_t.C_FSW])
                if (rcs.XLEN >= 64) and (self.addr[i] % 8 == 0):
                    allowed_instr.extend([riscv_instr_name_t.LWU,
                                          riscv_instr_name_t.LD,
                                          riscv_instr_name_t.SD])
                    if (cfg.enable_floating_point and
                            (riscv_instr_group_t.RV32D in rcs.supported_isa)):
                        allowed_instr.extend([riscv_instr_name_t.FLD,
                                              riscv_instr_name_t.FSD])
                    if (self.offset[i] in range(256) and (self.offset[i] % 8 == 0) and
                        (riscv_instr_group_t.RV64C in rcs.supported_isa) and
                            enable_compressed_load_store):
                        if self.rs1_reg == riscv_reg_t.SP:
                            allowed_instr.extend(
                                [riscv_instr_name_t.C_LDSP, riscv_instr_name_t.C_SDSP])
                        else:
                            allowed_instr.extend(
                                [riscv_instr_name_t.C_LD, riscv_instr_name_t.C_SD])
                            if (cfg.enable_floating_point and
                                    (riscv_instr_group_t.RV32DC in rcs.supported_isa)):
                                allowed_instr.extend(
                                    [riscv_instr_name_t.C_FLD, riscv_instr_name_t.C_FSD])
                else:  # unalligned load/store
                    allowed_instr.extend([riscv_instr_name_t.LW, riscv_instr_name_t.SW,
                                          riscv_instr_name_t.LH, riscv_instr_name_t.LHU,
                                          riscv_instr_name_t.SH])
                    # Compressed load/store still needs to be alligned
                    if (self.offset[i] in range(128) and (self.offset[i] % 4 == 0) and
                        (riscv_instr_group_t.RV32C in rcs.supported_isa) and
                            enable_compressed_load_store):
                        if self.rs1_reg == riscv_reg_t.SP:
                            allowed_instr.extend(
                                [riscv_instr_name_t.C_LWSP, riscv_instr_name_t.C_SWSP])
                        else:
                            allowed_instr.extend(
                                [riscv_instr_name_t.C_LW, riscv_instr_name_t.C_SW])
                    if rcs.XLEN >= 64:
                        allowed_instr.extend(
                            [riscv_instr_name_t.LWU, riscv_instr_name_t.LD, riscv_instr_name_t.SD])
                        if (self.offset[i] in range(256) and (self.offset[i] % 8 == 0) and
                            (riscv_instr_group_t.RV64C in rcs.supported_isa) and
                                enable_compressed_load_store):
                            if self.rs1_reg == riscv_reg_t.SP:
                                allowed_instr.extend(
                                    [riscv_instr_name_t.C_LWSP, riscv_instr_name_t.C_SWSP])
                            else:
                                allowed_instr.extend(
                                    [riscv_instr_name_t.C_LD, riscv_instr_name_t.C_SD])
            instr = riscv_instr.get_load_store_instr(allowed_instr)
            instr.has_rs1 = 0
            instr.has_imm = 0
            self.randomize_gpr(instr)
            instr.rs1 = self.rs1_reg
            logging.info("Instr_name {}".format(instr.instr_name.name))
            logging.info("OFFSET {}".format(self.offset[i]))
            instr.imm_str = str(instr.uintToInt(self.offset[i]))
            logging.info("instr.IMM_STR {}".format(instr.imm_str))
            instr.process_load_store = 0
            self.instr_list.append(instr)
            self.load_store_instr.append(instr)


# A single load/store instruction
@vsc.randobj
class riscv_single_load_store_instr_stream(riscv_load_store_base_instr_stream):
    def __init__(self):
        super().__init__()

    @vsc.constraint
    def legal_c(self):
        self.num_load_store == 1
        self.num_mixed_instr < 5


# Back to back load/store instructions
@vsc.randobj
class riscv_load_store_stress_instr_stream(riscv_load_store_base_instr_stream):
    def __init__(self):
        super().__init__()
        self.max_instr_cnt = 30
        self.min_instr_cnt = 10

    @vsc.constraint
    def legal_c(self):
        self.num_load_store.inside(vsc.rangelist(vsc.rng(self.min_instr_cnt, self.max_instr_cnt)))
        self.num_mixed_instr == 0


# Back to back load/store instructions
@vsc.randobj
class riscv_load_store_shared_mem_stream(riscv_load_store_stress_instr_stream):
    def __init__(self):
        super().__init__()

    def pre_randomize(self):
        self.load_store_shared_memory = 1
        super().pre_randomize()


# Random load/store sequence
# A random mix of load/store instructions and other instructions
@vsc.randobj
class riscv_load_store_rand_instr_stream(riscv_load_store_base_instr_stream):
    def __init__(self):
        super().__init__()

    @vsc.constraint
    def legal_c(self):
        self.num_load_store.inside(vsc.rangelist(vsc.rng(10, 30)))
        self.num_mixed_instr.inside(vsc.rangelist(vsc.rng(10, 30)))


# Use a small set of GPR to create various WAW, RAW, WAR hazard scenario
@vsc.randobj
class riscv_load_store_hazard_instr_stream(riscv_load_store_base_instr_stream):
    def __init__(self):
        super().__init__()
        self.hazard_ratio = vsc.rand_int32_t()

    @vsc.constraint
    def hazard_ratio_c(self):
        self.hazard_ratio.inside(vsc.rangelist(vsc.rng(20, 100)))

    @vsc.constraint
    def legal_c(self):
        self.num_load_store.inside(vsc.rangelist(vsc.rng(10, 20)))
        self.num_mixed_instr.inside(vsc.rangelist(vsc.rng(1, 7)))

    def randomize_offset(self):
        addr_ = vsc.rand_int32_t()
        offset_ = vsc.rand_int32_t()
        self.offset = [0] * self.num_load_store
        self.addr = [0] * self.num_load_store
        rand_num = random.randrange(0, 100)
        for i in range(self.num_load_store):
            if (i > 0) and (rand_num < self.hazard_ratio):
                self.offset[i] = self.offset[i - 1]
                self.addr[i] = self.addr[i - 1]
            else:
                try:
                    if self.locality == locality_e.NARROW:
                        offset_ = random.randrange(-16, 16)
                    elif self.locality == locality_e.HIGH:
                        offset_ = random.randrange(-64, 64)
                    elif self.locality == locality_e.MEDIUM:
                        offset_ = random.randrange(-256, 256)
                    elif self.locality == locality_e.SPARSE:
                        offset_ = random.randrange(-2048, 2047)
                    var1 = self.base + offset_ - 1
                    var2 = self.base + offset_ + 1
                    addr_ = random.randrange(var1, var2)
                except Exception:
                    logging.critical("Cannot randomize load/store offset")
                    sys.exit(1)
                self.offset[i] = offset_
                self.addr[i] = addr_


# Back to back access to multiple data pages
# This is useful to test data TLB switch and replacement
@vsc.randobj
class riscv_multi_page_load_store_instr_stream(riscv_mem_access_stream):

    def __init__(self):
        super().__init__()
        self.load_store_instr_stream = vsc.list_t(vsc.attr(riscv_load_store_stress_instr_stream()))
        self.num_of_instr_stream = vsc.rand_uint32_t()
        self.data_page_id = vsc.rand_list_t(vsc.uint32_t())
        self.rs1_reg = vsc.rand_list_t(vsc.enum_t(riscv_reg_t))

    @vsc.constraint
    def default_c(self):
        with vsc.foreach(self.data_page_id, idx=True) as i:
            self.data_page_id[i] < self.max_data_page_id
        self.data_page_id.size == self.num_of_instr_stream
        self.rs1_reg.size == self.num_of_instr_stream
        vsc.unique(self.rs1_reg)
        with vsc.foreach(self.rs1_reg, idx=True) as i:
            self.rs1_reg[i].not_inside(vsc.rangelist(cfg.reserved_regs, riscv_reg_t.ZERO))

    @vsc.constraint
    def page_c(self):
        # vsc.solve_order(self.num_of_instr_stream, self.data_page_id)
        self.num_of_instr_stream.inside(vsc.rangelist(vsc.rng(1, self.max_data_page_id)))
        vsc.unique(self.data_page_id)

    # Avoid accessing a large number of pages because we may run out of registers for rs1
    # Each page access needs a reserved register as the base address of load/store instruction
    @vsc.constraint
    def reasonable_c(self):
        self.num_of_instr_stream.inside(vsc.rangelist(vsc.rng(2, 8)))

    def post_randomize(self):
        self.load_store_instr_stream = [0] * self.num_of_instr_stream
        for i in range(len(self.load_store_instr_stream)):
            self.load_store_instr_stream[i] = riscv_load_store_stress_instr_stream()
            self.load_store_instr_stream[i].min_instr_cnt = 5
            self.load_store_instr_stream[i].max_instr_cnt = 10
            self.load_store_instr_stream[i].hart = self.hart
            self.load_store_instr_stream[i].sp_c.constraint_mode(False)
            # Make sure each load/store sequence doesn't override the rs1 of other sequences.
            for j in range(len(self.rs1_reg)):
                if i != j:
                    self.load_store_instr_stream[i].reserved_rd = self.rs1_reg[i]
            try:
                with vsc.randomize_with(self.load_store_instr_stream[i]):
                    self.rs1_reg == self.rs1_reg[i]
                    self.data_page_id == self.data_page_id[i]
            except Exception:
                loagging.critical("Cannot randomize load/store instruction")
                sys.exit(1)
            # Mix the instruction stream of different page access, this could trigger the scenario of
            # frequent data TLB switch
            if i == 0:
                 self.instr_list = self.load_store_instr_stream[i].instr_list
            else:
                self.mix_instr_stream(self.load_store_instr_stream[i].instr_list)


# Access the different locations of the same memory regions
@vsc.randobj
class riscv_mem_region_stress_test(riscv_multi_page_load_store_instr_stream):

    def __init__(self):
        super().__init__()

    @vsc.constraint
    def page_c(self):
        self.num_of_instr_stream.inside(vsc.rangelist(vsc.rng(2, 5)))
        with vsc.foreach(self.data_page_id, idx=True) as i:
            with vsc.if_then(i > 0):
                self.data_page_id[i] == self.data_page_id[i-1]


# Random load/store sequence to full address range
# The address range is not preloaded with data pages, use store instruction to initialize first
@vsc.randobj
class riscv_load_store_rand_addr_instr_stream(riscv_load_store_base_instr_stream):

    def __init__(self):
        super().__init__()
        self.addr_offset = vsc.rand_bit_t(rcs.XLEN)

    # Find an unused 4K page from address 1M onward
    @vsc.constraint
    def addr_offset_c(self):
        self.addr_offset[rcs.XLEN - 1:20] == 1  # TODO
        self.addr_offset[rcs.XLEN-1:31] == 0
        self.addr_offset[11:0] == 0

    @vsc.constraint
    def legal_c(self):
        self.num_load_store.inside(vsc.rangelist(vsc.rng(5,10)))
        self.num_mixed_instr.inside(vsc.rangelist(vsc.rng(5,10)))

    def randomize_offset(self):
        addr_ = vsc.rand_int32_t()
        offset_ = vsc.rand_int32_t()
        self.offset = [0] * self.num_load_store
        self.addr = [0] * self.num_load_store
        for i in range(self.num_load_store):
            try:
                offset_ = random.randrange(-2048, 2047)
            except Exception:
                logging.critical("Cannot randomize load/store offset")
                sys.exit(1)
            self.offset[i] = offset_
            self.addr[i] = self.addr_offset + offset_

    def add_rs1_init_la_instr(gpr, id, base=0):
        li_instr = vsc.attr(riscv_pseudo_instr())
        store_instr = vsc.attr(riscv_instr())
        add_instr = vsc.attr(riscv_instr())
        min_offset = []
        max_offset = []
        min_offset = min([item for item in self.offset])
        max_offset = max([item for item in self.offset])
        # Use LI to initialize the address offset
        li_instr = riscv_pseudo_instr()
        with vsc.randomize_with(li_instr):
            li_instr.pseudo_instr_name == riscv_instr_name_t.LI
            li_instr.rd.inside(vsc.rangelist(cfg.gpr))
            li_instr.rd != gpr
        li_instr.imm_str = "{}".format(hex(self.addr_offset))
        # Add offset to the base address
        add_instr = riscv_instr.get_instr(riscv_instr_name_t.ADD)
        with vsc.randomize_with(add_instr):
            add_instr.rs1 == gpr
            add_instr.rs2 == li_instr.rd
            add_instr.rd == gpr
        instr.extend((li_instr, add_instr))
        # Create SW instruction template
        store_instr = riscv_instr.get_instr(riscv_instr_name_t.SB)
        with vsc.randomize_with(store_instr):
            store_instr.instr_name == riscv_instr_name_t.SB
            store_instr.rs1 == gpr
        # Initialize the location which used by load instruction later
        for i in range(len(self.load_store_instr)):
            if self.load_store_instr[i].category == riscv_instr_category_t.LOAD:
                store = riscv_instr()
                store.deepcopy(store_instr)
                val = i % 32
                store.rs2 = riscv_reg_t.val
                store.imm_str = self.load_store_instr[i].imm_str
                # TODO: C_FLDSP is in both rv32 and rv64 ISA
                if self.load_store_instr[i].instr_name in [riscv_instr_name_t.LB,
                                                           riscv_instr_name_t.LBU]:
                    store.instr_name = riscv_instr_name_t.SB
                elif self.load_store_instr[i].instr_name in [riscv_instr_name_t.LH,
                                                             riscv_instr_name_t.LHU]:
                    store.instr_name = riscv_instr_name_t.SH
                elif self.load_store_instr[i].instr_name in [riscv_instr_name_t.LW,
                                                             riscv_instr_name_t.C_LW,
                                                             riscv_instr_name_t.C_LWSP,
                                                             riscv_instr_name_t.FLW,
                                                             riscv_instr_name_t.C_FLW,
                                                             riscv_instr_name_t.C_FLWSP]:
                    store.instr_name = riscv_instr_name_t.SW
                elif self.load_store_instr[i].instr_name in [riscv_instr_name_t.LD,
                                                             riscv_instr_name_t.C_LD,
                                                             riscv_instr_name_t.C_LDSP,
                                                             riscv_instr_name_t.FLD,
                                                             riscv_instr_name_t.C_FLD,
                                                             riscv_instr_name_t.LWU]:
                    store.instr_name = riscv_instr_name_t.SD
                else:
                    logging.critical("Unexpected op: {}".format(self.load_store_instr[i].convert2asm()))
                    sys.exit(1)
                instr.append(store)
        self.instr_list.extend(instr, self.instr_list)
        super().add_rs1_init_la_instr(gpr, id, 0)


class riscv_vector_load_store_instr_stream(riscv_mem_access_stream):
    # TODO
    pass



