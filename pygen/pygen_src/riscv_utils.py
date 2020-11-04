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
import pandas as pd
from tabulate import tabulate
from pygen_src.riscv_instr_gen_config import cfg
from pygen_src.riscv_directed_instr_lib import (riscv_directed_instr_stream,
                                                riscv_int_numeric_corner_stream,
                                                riscv_jal_instr)


def factory(obj_of):
    objs = {
        "riscv_directed_instr_stream": riscv_directed_instr_stream,
        "riscv_int_numeric_corner_stream": riscv_int_numeric_corner_stream,
        "riscv_jal_instr": riscv_jal_instr
    }

    try:
        return objs[obj_of]()
    except KeyError:
        logging.critical("Cannot Create object of %s", obj_of)
        sys.exit(1)


def get_object(instr_name):
    try:
        if cfg.argv.target == "rv32i":
            from pygen_src.isa import rv32i_instr
            instr_inst = eval("rv32i_instr.riscv_" + instr_name.name + "_instr()")
        if cfg.argv.target == "rv32imc":
            try:
                from pygen_src.isa import rv32i_instr
                instr_inst = eval("rv32i_instr.riscv_" + instr_name.name + "_instr()")
            except Exception:
                try:
                    from pygen_src.isa import rv32m_instr
                    instr_inst = eval("rv32m_instr.riscv_" + instr_name.name + "_instr()")
                except Exception:
                    try:
                        from pygen_src.isa import rv32c_instr
                        instr_inst = eval("rv32c_instr.riscv_" + instr_name.name + "_instr()")
                    except Exception:
                        logging.critical("Failed to create instr: %0s", instr_name.name)
                        sys.exit(1)
        if cfg.argv.target == "rv32imfdc":
            try:
                from pygen_src.isa import rv32i_instr
                instr_inst = eval("rv32i_instr.riscv_" + instr_name.name + "_instr()")
            except Exception:
                try:
                    from pygen_src.isa import rv32m_instr
                    instr_inst = eval("rv32m_instr.riscv_" + instr_name.name + "_instr()")
                except Exception:
                    try:
                        from pygen_src.isa import rv32c_instr
                        instr_inst = eval("rv32c_instr.riscv_" + instr_name.name + "_instr()")
                    except Exception:
                        try:
                            from pygen_src.isa import rv32f_instr
                            instr_inst = eval("rv32f_instr.riscv_" + instr_name.name + "_instr()")
                        except Exception:
                            try:
                                from pygen_src.isa import rv32fc_instr
                                instr_inst = eval("rv32fc_instr.riscv_" +
                                                  instr_name.name + "_instr()")
                            except Exception:
                                try:
                                    from pygen_src.isa import rv32d_instr
                                    instr_inst = eval("rv32d_instr.riscv_" +
                                                      instr_name.name + "_instr()")
                                except Exception:
                                    try:
                                        from pygen_src.isa import rv32dc_instr
                                        instr_inst = eval("rv32dc_instr.riscv_" +
                                                          instr_name.name + "_instr()")
                                    except Exception:
                                        logging.critical(
                                            "Failed to create instr: %0s", instr_name.name)
                                        sys.exit(1)
    except Exception:
        logging.critical("Failed to create instr: %0s", instr_name.name)
        sys.exit(1)
    return instr_inst


def gen_config_table():
    data = []
    for key, value in cfg.__dict__.items():
        # Ignoring the unneccesary attributes
        if key in ["_ro_int", "_int_field_info", "argv", "mem_region",
                   "amo_region", "s_mem_region", "args_dict"]:
            continue
        else:
            try:  # Fields values for the pyvsc data types
                data.append([key, type(key), sys.getsizeof(key), value.get_val()])
            except Exception:
                data.append([key, type(key), sys.getsizeof(key), value])
    df = pd.DataFrame(data, columns=['Name', 'Type', 'Size', 'Value'])
    df['Value'] = df['Value'].apply(str)
    logging.info('\n' + tabulate(df, headers='keys', tablefmt='psql'))
