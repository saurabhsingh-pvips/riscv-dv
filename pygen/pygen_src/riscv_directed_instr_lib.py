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
from pygen_src.riscv_instr_stream import riscv_rand_instr_stream
from pygen_src.isa.riscv_instr import riscv_instr_ins, cfg
from enum import Enum, auto
import vsc


class riscv_directed_instr_stream(riscv_rand_instr_stream):

    def __init__(self):
        riscv_rand_instr_stream.__init__(self)
        self.label = ""

    def post_randomize(self):
        for i in self.instr_list:
            self.instr_list[i].has_label = 0
            self.instr_list[i].atomic = 1
        self.instr_list[0].comment = "Start %0s" % (self.__class__.__name__)
        self.instr_list[-1].comment = "End %0s" % (self.__class__.__name__)

        if self.label != "":
            self.instr_list[0].label = self.label
            self.instr_list[0].has_label = 1


class int_numeric_e(Enum):
    NormalValue = auto()
    Zero = auto()
    AllOne = auto()
    NegativeMax = auto()


@vsc.randobj
class riscv_int_numeric_corner_stream(riscv_directed_instr_stream):

    def __init__(self):
        riscv_directed_instr_stream.__init__(self)
        self.num_of_avail_regs = vsc.uint8_t(10)
        self.num_of_instr = vsc.rand_uint8_t()
        self.init_val = vsc.randsz_list_t(vsc.rand_bit_t())
        self.init_val_type = vsc.randsz_list_t(vsc.enum_t(int_numeric_e))
        self.init_instr = []

    @vsc.constraint
    def init_val_c(self):
        # TO DO
        # solve init_val_type before init_val;
        self.init_val_type.size in vsc.rangelist(self.num_of_avail_regs)
        self.init_val.size in vsc.rangelist(self.num_of_avail_regs)
        self.num_of_instr in vsc.rangelist(vsc.rng(15, 30))

    @vsc.constraint
    def avail_regs_c(self):
        vsc.unique(self.avail_regs)
        with vsc.foreach(self.avail_regs, idx = True) as i:
            self.avail_regs[i].not_inside(cfg.reserved_regs)
            self.avail_regs[i] != 0

    def pre_randomize(self):
        self.avail_regs = [0] * self.num_of_avail_regs
        super().pre_randomize()

    def post_randomize(self):
        self.init_instr = [0] * self.num_of_avail_regs
        for i in range(len(self.init_val_type)):
            if self.init_val_type[i] == int_numeric_e.Zero:
                self.init_val[i] = 0
            elif self.init_val_type[i] == int_numeric_e.AllOne:
                self.init_val[i] = 1
            elif self.init_val_type[i] == int_numeric_e.NegativeMax:
                self.init_val[i] = 1 << (riscv_instr_ins.XLEN - 1)

            self.init_instr[i].rd = self.avail_regs[i]
            self.init_instr[i].pseudo_instr_name = 'LI'
            self.init_instr[i].imm_str = "0x%0x" % (self.init_val[i])
            self.instr_list.append(self.init_instr[i])
        for i in range(0, self.num_of_instr):
            instr = riscv_instr_ins.get_rand_instr(
                include_category = ['ARITHMETIC'],
                exclude_group = ['RV32C', 'RV64C', 'RV32F', 'RV64F', 'RV32D', 'RV64D'])
            instr = super().randomize_gpr(instr)
            self.instr_list.append(instr)
        super().post_randomize()
