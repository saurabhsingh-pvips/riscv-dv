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
import random
import vsc


@vsc.randobj
class riscv_program:
    def __init__(self):
        self.program_id = vsc.rand_bit_t(16)
        self.call_stack_level = vsc.rand_uint32_t()
        self.sub_program_id = vsc.rand_list_t(vsc.bit_t(16))

    @vsc.constraint
    def legel_c(self):
        vsc.unique(self.sub_program_id)
        with vsc.foreach(self.sub_program_id, idx = True) as i:
            self.sub_program_id[i] != self.program_id

    def convert2string(self):
        string = "PID[{}] Lv[{}] :".format(self.program_id, self.call_stack_level)
        for i in range(len(self.sub_program_id)):
            string = "{} {}".format(string, self.sub_program_id[i])
        return string


@vsc.randobj
class riscv_callstack_gen:
    def __init__(self):
        print("init from riscv_callstack_gen")
        # Number of programs in the call stack
        self.program_cnt = 10
        self.program_h = []
        # Maximum call stack level
        self.max_stack_level = 50
        # Call stack level of each program
        self.stack_level = vsc.randsz_list_t(vsc.bit_t(11))

    @vsc.constraint
    def program_stack_level_c(self):
        # The stack level is assigned in ascending order to avoid call loop
        self.stack_level.size == self.program_cnt
        self.stack_level[0] == 0
        """
        with vsc.foreach(self.stack_level, idx = True) as i:
            if(i > 0):
                self.stack_level[i] in vsc.rangelist(vsc.rng(1,self.program_cnt-1))
                self.stack_level[i] >= self.stack_level[i-1]
                self.stack_level[i] <= self.stack_level[i-1]+1
                self.stack_level[i] <= self.max_stack_level
        """

    # Init all program instances before randomization
    def init(self, program_cnt):
        self.program_cnt = program_cnt
        self.program_h = [0] * program_cnt
        for i in range(len(self.program_h)):
            object_name = f"program_{i}"
            object_name = riscv_program()
            self.program_h[i] = object_name

    def post_randomize(self):
        print("callstack post randomization")
        last_level = 0
        print(self.stack_level, last_level, self.program_cnt)
        last_level = self.stack_level[self.program_cnt - 1]
        for i in range(len(self.program_h)):
            self.program_h[i].program_id = i
            self.program_h[i].call_stack_level = self.stack_level[i]
        # Top-down generate the entire call stack.
        # A program can only call the programs in the next level.
        for i in range(last_level):
            total_sub_program_cnt = 0
            program_list = []
            next_program_list = []
            sub_program_id_pool = []
            sub_program_cnt = []
            idx = 0
            for j in range(program_cnt):
                if self.stack_level[j] == i:
                    program_list.append(j)
                if self.stack_level[j] == i + 1:
                    next_program_list.append(j)
            # Randmly duplicate some sub programs in the pool to create a case that
            # one sub program is called by multiple caller. Also it's possible to call
            # the same sub program in one program multiple times.
            total_sub_program_cnt = random.randrange(len(next_program_list),
                                                     len(next_program_list) + 1)
            sub_program_id_pool = [0] * total_sub_program_cnt
            # TODO std::randomize

            sub_program_id_pool.shuffle()
            sub_program_cnt = [0] * len(program_list)
            logging.info("%0d programs @Lv%0d-> %0d programs at next level",
                         len(program_list), i, len(sub_program_id_pool))
            # Distribute the programs of the next level among the programs of current level
            # Make sure all program has a caller so that no program is obsolete.

            for j in range(len(sub_program_id_pool)):
                caller_id = random.randrange(0, len(sub_program_cnt) - 1)
                sub_program_cnt[caller_id] += 1

            for j in range(len(program_list)):
                id = program_list[j]
                self.program_h[id].sub_program_id = [0] * sub_program_cnt[j]
                logging.info("%0d sub programs are assigned to program[%0d]",
                             sub_program_cnt[j], id)
                for k in range(len(program_h[id].sub_program_id)):
                    self.program_h[id].sub_program_id[k] = sub_program_id_pool[idx]
                    idx += 1

    def print_call_stack(self, program_id_t, i, string):
        if len(self.program_h[i].sub_program_id) == 0:
            logging.info("%s", string)
        else:
            for j in range(len(program_h[i].sub_program_id)):
                self.print_call_stack(self.program_h[i].sub_program_id[j],
                                      "{} -> {}".format(string, self.program_h[i].sub_program_id[j]))
