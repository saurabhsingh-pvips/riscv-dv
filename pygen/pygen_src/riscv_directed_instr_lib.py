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
from riscv_instr_stream import riscv_rand_instr_stream

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

class riscv_int_numeric_corner_stream(riscv_directed_instr_stream):

    def __init__(self):
        riscv_directed_instr_stream.__init__(self)
        self.num_of_avail_regs = 10
        self.num_of_instr = 0
        #self.int_numeric_e = ['NormalValue', 'Zero', 'AllOne', 'NegativeMax']
        self.init_val_type = ['NormalValue', 'Zero', 'AllOne', 'NegativeMax']
        self.init_instr = []

        #TO DO
        constraint init_val_c {
            solve init_val_type before init_val;
            init_val_type.size() == num_of_avail_regs;
            init_val.size() == num_of_avail_regs;
            num_of_instr inside {[15:30]};
        }

        #TO DO
        constraint avail_regs_c {
            unique {avail_regs};
            foreach(avail_regs[i]) {
            !(avail_regs[i] inside {cfg.reserved_regs});
            avail_regs[i] != ZERO;
            }
        }

        def pre_randomize(self):
            self.avail_regs = [0] * self.num_of_avail_regs
            super().pre_randomize()

        def post_randomize(self):
            self.init_instr = [0] *  self.num_of_avail_regs
            for i in self.init_val_type:
                if self.init_val_type[i] == 'Zero':
                    self.init_val[i] = 0
                else if self.init_val_type[i] == 'AllOne':
                    self.init_val[i] = 1
                else if self.init_val_type[i] == 'NegativeMax':
                    self.init_val[i] = 1 << (riscv_instr_ins.XLEN-1)

                self.init_instr[i].rd = self.avail_regs[i]
                self.init_instr[i].pseudo_instr_name = LI
                self.init_instr[i].imm_str = "0x%0x" % (self.init_val[i])
                self.init_list.append(self.init_instr[i])
            
            for i in range(0, self.num_of_instr): 
                instr = riscv_instr_ins.get_rand_instr(\
                    include_category = ['ARITHMETIC']\
                    exclude_group = ['RV32C', 'RV64C', 'RV32F', 'RV64F', 'RV32D', 'RV64D'])
                instr = super().randomize_gpr(instr) 
                self.instr_list.append(instr)
            super().post_randomize()
