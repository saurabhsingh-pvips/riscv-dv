class c_1_38;
    integer num_of_sub_program = 5;
    integer instr_cnt = 50;
    rand bit[30:0] sub_program_instr_cnt_size_; // rand_mode = ON 
    rand integer main_program_instr_cnt; // rand_mode = ON 
    rand integer fv_temp_80; // rand_mode = ON 
    rand integer fv_temp_81; // rand_mode = ON 
    rand integer fv_temp_83; // rand_mode = ON 
    rand integer fv_temp_84; // rand_mode = ON 

    constraint default_c_this    // (constraint_mode = ON) (/DATA/anil/GitHub/RISC-V/riscv-dv/src/riscv_instr_gen_config.sv:265)
    {
       (sub_program_instr_cnt_size_ == num_of_sub_program);
       (main_program_instr_cnt inside {[10:instr_cnt]});
       sub_program_instr_cnt_size_ -> (fv_temp_81 inside {[10:instr_cnt]});
    }
    constraint debug_mode_c_this    // (constraint_mode = ON) (/DATA/anil/GitHub/RISC-V/riscv-dv/src/riscv_instr_gen_config.sv:284)
    {
       (fv_temp_83 == (sub_program_instr_cnt_size_ * fv_temp_81));
       ((fv_temp_80 >= fv_temp_83) && (fv_temp_80 <= fv_temp_84));
       ((main_program_instr_cnt + fv_temp_80) == instr_cnt);
    }
endclass

program p_1_38;
    c_1_38 obj;
    string randState;

    initial
        begin
            obj = new;
            randState = "z01z1x10zx11z01001000xx0zxx0xxxxxxxzxxxxzxxxxxxxxxzzzxzxxxzxxxxx";
            obj.set_randstate(randState);
            obj.randomize();
        end
endprogram
