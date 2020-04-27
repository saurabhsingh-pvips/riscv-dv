Last Updated: 27th April, 2020.

****************************************************************************************************
Note: 

Instruction count reduced to 20 in order to verify the coverage result manually
by looking at the assembly file.

Test targetted for RV32I.

Change Seed value in run commands.

Available output files are for seed = 1870736950.

Increase iteration count to hit more bins.

****************************************************************************************************

Tests added:
	* riscv_custom_test_1
	* riscv_custom_test_2

****************************************************************************************************

Command:

run --test riscv_custom_test_2 --iterations 1 --iss spike --verbose --seed 1870736950 --target rv32i

cov --dir <out_dir>/spike_sim/ --verbose --target rv32i

urg -dir <cov_dir>/test.vdb/

Note: Change out_dir & cov_dir names according to workspace.

****************************************************************************************************

Modified Files:
	* src/riscv_instr_cov_item.sv
	* src/riscv_instr_cover_group.sv
	* src/riscv_instr_pkg.sv
	* test/riscv_instr_cov_test.sv
	* yaml/base_testlist.yaml

****************************************************************************************************
