## Overview

RISCV-DV-PyFlow is a python based open-source instruction generator for RISC-V
processor verification. It currently supports the following features:

- Supported instruction set: RV32IMAFDC
- Supported privileged mode: machine mode
- Illegal instruction and HINT instruction generation
- Random forward/backward branch instructions
- Supports mixing directed instructions with random instruction stream
- Support for direct & vectored interrupt table.
- Multi-hart support
- Instruction generation coverage model(Currently supports RV32I and RV32M only)
- Co-simulation with multiple ISS : spike, riscv-ovpsim

## Supported tests

- riscv_arithmetic_basic_test
- riscv_amo_test
- riscv_floating_point_arithmetic_test
- riscv_floating_point_rand_test
- riscv_floating_point_mmu_stress_test
- riscv_b_ext_test
- riscv_rand_instr_test
- riscv_jump_stress_test
- riscv_rand_jump_test
- riscv_mmu_stress_test
- riscv_illegal_instr_test
- riscv_unaligned_load_store_test
- riscv_single_hart_test
- riscv_non_compressed_instr_test


## Getting Started

### Prerequisites

To be able to run the generator, you need to have RISCV-GCC compiler toolchain and ISS
(Instruction Set Simulator) installed.


### Install RISCV-DV-PyFlow

Getting the source
```bash
git clone https://github.com/google/riscv-dv.git
```

```bash
pip3 install -r requirements.txt    # install dependencies (only once)
python3 run.py --help
```

## Running the Generator

Command to run a single test:
```bash
python3 run.py --test=riscv_arithmetic_basic_test --simulator=pyflow
```
--simulator=pyflow will invoke the python generator.

Run a single test 10 times
```bash
python3 run.py --test=riscv_arithmetic_basic_test --iterations=10 --simulator=pyflow
```
Run the generator only, do not compile and simluation with ISS
```bash
python3 run.py --test=riscv_arithmetic_basic_test --simulator=pyflow --steps gen
```

## Note
Time to generate more than 10k instructions for single iteration is around 10-12 minutes.
For multiple iterations, there will be overhead of ~2-5 minutes over time taken for single
iteration.
