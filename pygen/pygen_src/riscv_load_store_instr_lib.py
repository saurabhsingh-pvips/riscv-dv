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

import vsc
from enum import IntEnum, auto
from pygen_src.riscv_directed_instr_lib import riscv_mem_access_stream
from pygen_src.riscv_instr_pkg import riscv_reg_t, riscv_instr_name_t, riscv_instr_group_t
from pygen_src.riscv_instr_gen_config import cfg
from pygen_src.target.rv32i import riscv_core_setting as rcs
from pygen_src.isa.riscv_instr import riscv_instr_ins


class locality_e(IntEnum):
    NARROW = 0
    HIGH = auto()
    MEDIUM = auto()
    SPARSE = auto()


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
        self.mix_load_store_offset = vsc.rand_int32_t()
        self.use_sp_as_rs1 = vsc.rand_bit_t()

    @vsc.constraint
    def sp_rnd_order_c(self):
        # solve use_sp_as_rs1 before rs1_reg
        pass

    @vsc.constraint
    def use_sp_as_rs1(self):
        pass # TODO
    
    @vsc.constraint
    def rs1_c(self):
        self.rs1_reg.not_inside(vsc.rangelist(cfg.reserved_regs, self.reserved_rd, riscv_reg_t.ZERO))

    @vsc.constraint
    def addr_c(self):
        pass # TODO
    
    def randomize_offset(self):
        self.offset = [0] * self.num_load_store
        self.addr = [0] * self.num_load_store
        for i in range(self.num_load_store):
            pass

    def pre_randomize(self):
        super().pre_randomize()
        if(riscv_reg_t.SP in [cfg.reserved_regs, self.reserved_rd]):
            self.use_sp_as_rs1 = 0
            # self.use_sp_as_rs1.rand_mode(0)  TODO
            pass

    def post_randomize(self):
        self.randomize_offset()
        if(not(self.rs1_reg in [self.reserved_rd])):
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
        print("IN gen_load_store_instr")
        if((self.rs1_reg in [riscv_reg_t.S0, riscv_reg_t.S1, riscv_reg_t.A0, riscv_reg_t.A1,
			riscv_reg_t.A2, riscv_reg_t.A3,riscv_reg_t.A4, riscv_reg_t.A5, riscv_reg_t.SP]) # TODO
            and not(cfg.disable_compressed_instr)):
            enable_compressed_load_store = 0
        for i in range(len(self.addr)):
            # Assign the allowed load/store instructions based on address alignment
            # This is done separately rather than a constraint to improve the randomization performance
            allowed_instr.extend([riscv_instr_name_t.LB.name, riscv_instr_name_t.LBU.name, riscv_instr_name_t.SB.name])
            if(not cfg.enable_unaligned_load_store):
                if(self.addr[i] == 0):
                    allowed_instr.extend([riscv_instr_name_t.LH.name, riscv_instr_name_t.LHU.name, riscv_instr_name_t.SH.name])
                if(self.addr[i]%4 == 0):
                    allowed_instr.extend([riscv_instr_name_t.LW.name, riscv_instr_name_t.SW.name])
                    if(cfg.enable_floating_point):
                        allowed_instr.extend([riscv_instr_name_t.FLW.name, riscv_instr_name_t.FSW.name])
                    if((self.offset[i] in range(127)) and (self.offset[i]%4 == 0) and
                        (riscv_instr_group_t.RV32C in rcs.supported_isa) and
                        (enable_compressed_load_store)):
                        if(self.rs1_reg == riscv_reg_t.SP):
                            logging.info("Add LWSP/SWSP to allowed instr")
                            allowed_instr.extend([riscv_instr_name_t.C_LWSP.name, riscv_instr_name_t.C_SWSP.name])
                        else:
                            allowed_instr.extend([riscv_instr_name_t.C_LW.name, riscv_instr_name_t.C_SW.name])
                            if(cfg.enable_floating_point and riscv_instr_group_t.RV32FC in rcs.supported_isa):
                                allowed_instr.extend([riscv_instr_name_t.C_FLW.name, riscv_instr_name_t.C_FSW.name])
                if((rcs.XLEN >= 64) and (self.addr[i] % 0 == 0)):
                    allowed_instr.extend([riscv_instr_name_t.LWU.name, riscv_instr_name_t.LD.name, riscv_instr_name_t.SD.name])
                    if(cfg.enable_floating_point and (riscv_instr_group_t.RV32D in rcs.supported_isa)):
                        allowed_instr.extend([riscv_instr_name_t.FLD.name, riscv_instr_name_t.FSD.name])
                    if((self.offset[i] in range(255)) and (self.offset[i] %8 ==0) and 
                        (riscv_instr_group_t.RV64C in rcs.supported_isa) and
                        enable_compressed_load_store):
                        if(self.rs1_reg == riscv_get_t.SP):
                            allowed_instr.extend([riscv_instr_name_t.C_LDSP.name, riscv_instr_name_t.C_SDSP.name])
                        else:
                            allowed_instr.extend([riscv_instr_name_t.C_LD.name, riscv_instr_name_t.C_SD.name])
                            if(cfg.enable_floating_point and (riscv_instr_group_t.RV32DC in rcs.supported_isa)):
                                allowed_instr.extend([riscv_instr_name_t.C_FLD.name, riscv_instr_name_t.C_FSD.name])
                else: # unalligned load/store
                    allowed_instr.extend([riscv_instr_name_t.LW.name, riscv_instr_name_t.SW.name, riscv_instr_name_t.LH.name,
                         riscv_instr_name_t.LHU.name, riscv_instr_name_t.SH.name])
                    # Compressed load/store still needs to be alligned
                    if((self.offset[i] in range(127)) and (self.offset[i] % 4 == 0) and
                        (riscv_instr_group_t.RV32C in rcs.supported_isa) and
                        enable_compressed_load_store):
                        if(self.rs1_reg == riscv_reg_t.SP):
                            allowed_instr.extend([riscv_instr_name_t.C_LWSP.name, riscv_instr_name_t.C_SWSP.name])
                        else:
                            allowed_instr.extend([riscv_instr_name_t.C_LW.name, riscv_instr_name_t.C_SW.name])
                    if(rcs.XLEN >= 64):
                        allowed_instr.extend([riscv_instr_name_t.LWU.name, riscv_instr_name_t.LD.name, riscv_instr_name_t.SD.name])
                        if((self.offset[i] in range(255)) and (self.offset[i] % 8 == 0) and
                        (riscv_instr_group_t.RV64C in rcs.supported_isa) and
                        enable_compressed_load_store):
                            if(self.rs1_reg == riscv_reg_t.SP):
                                allowed_instr.extend([riscv_instr_name_t.C_LWSP.name, riscv_instr_name_t.C_SWSP.name])
                            else:
                                allowed_instr.extend([riscv_instr_name_t.C_LD.name, riscv_instr_name_t.C_SD.name])
        instr = riscv_instr_ins.get_load_store_instr(allowed_instr)
        instr.has_rs1 = 0
        instr.has_imm = 0
        self.randomize_gpr(instr)
        instr.rs1 = self.rs1_reg
        instr.imm_str = str(instr.uintToInt(self.offset[i]))
        instr.process_load_store = 0
        self.instr_list.append(instr)
        self.load_store_instr.append(instr)


class riscv_single_load_store_instr_stream(riscv_load_store_base_instr_stream):
    def __init__(self):
        super().__init__()
    @vsc.constraint
    def legal_c(self):
        self.num_load_store == 1
        self.num_mixed_instr < 5

class riscv_load_store_stress_instr_stream(riscv_load_store_base_instr_stream):
    def __init__(self):
        super().__init__()
        self.max_instr_cnt = 30
        self.min_instr_cnt = 10

    @vsc.constraint
    def legal_c(self):
        self.num_load_store.inside(vsc.rangelist(self.min_instr_cnt,self.max_instr_cnt))
        self.num_mixed_instr == 0

class riscv_load_store_rand_instr_stream(riscv_load_store_base_instr_stream):
    def __init__(self):
        super().__init__()
    
    @vsc.constraint
    def legal_c(self):
        self.num_load_store.inside(vsc.rangelist(10,30))
        self.num_mixed_instr.inside(vsc.rangelist(10,30))
