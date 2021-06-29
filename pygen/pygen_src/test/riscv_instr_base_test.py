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
import logging
import time
import multiprocessing
import cProfile, pstats, io
sys.path.append("pygen/")
from pygen_src.riscv_instr_pkg import *
from pygen_src.riscv_instr_gen_config import cfg  # NOQA
for isa in rcs.supported_isa:
    import_module("pygen_src.isa." + isa.name.lower() + "_instr")
from pygen_src.isa.riscv_instr import riscv_instr  # NOQA
from pygen_src.riscv_asm_program_gen import riscv_asm_program_gen  # NOQA
from pygen_src.riscv_utils import gen_config_table


# Base test
class riscv_instr_base_test:
    def __init__(self):
        self.start_idx = cfg.argv.start_idx
        self.asm_file_name = cfg.argv.asm_file_name
        self.asm = ""

    # Commenting out multiprocessing feature for now as it is creating issue with profiling data
    '''def run(self):
        with multiprocessing.Pool(processes = cfg.num_of_tests) as pool:
            pool.map(self.run_phase, list(range(cfg.num_of_tests)))

    def run_phase(self, num):
        self.randomize_cfg()
        self.asm = riscv_asm_program_gen()
        riscv_instr.create_instr_list(cfg)
        if cfg.asm_test_suffix != "":
            self.asm_file_name = "{}.{}".format(self.asm_file_name,
                                                cfg.asm_test_suffix)
        self.asm.get_directed_instr_stream()
        test_name = "{}_{}.S".format(self.asm_file_name,
                                     num + self.start_idx)
        self.apply_directed_instr()
        logging.info("All directed instruction is applied")
        self.asm.gen_program()
        self.asm.gen_test_file(test_name)
        logging.info("TEST GENERATION DONE")'''

    def run_phase(self):
        for _ in range(cfg.num_of_tests):
            self.randomize_cfg()
            self.asm = riscv_asm_program_gen()
            riscv_instr.create_instr_list(cfg)
            if cfg.asm_test_suffix != "":
                self.asm_file_name = "{}.{}".format(self.asm_file_name,
                                                    cfg.asm_test_suffix)
            test_name = "{}_{}.S".format(self.asm_file_name,
                                         _ + self.start_idx)
            self.asm.get_directed_instr_stream()
            logging.info("All directed instruction is applied")
            self.asm.gen_program()
            self.asm.gen_test_file(test_name)
            logging.info("TEST GENERATION DONE")

    def randomize_cfg(self):
        cfg.randomize()
        logging.info("riscv_instr_gen_config is randomized")
        gen_config_table()

    def apply_directed_instr(self):
        pass


start_time = time.time()
pr = cProfile.Profile()
pr.enable()
riscv_base_test_ins = riscv_instr_base_test()
if cfg.argv.gen_test == "riscv_instr_base_test":
    riscv_base_test_ins.run_phase()
    end_time = time.time()
    logging.info("Total execution time: {}s".format(round(end_time - start_time)))
pr.disable()
s = io.StringIO()
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
logging.info("{}".format(s.getvalue()))
