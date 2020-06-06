import random
import array
import logging
import riscv_core_setting
from riscv_instr_pkg import *
from riscv_core_setting import *
from collections import deque


class riscv_instr_gen_config:
   
    def __init__(self):
  
        # dicts for exception_cause_t & interrupt_cause_t Enum classes
        self.m_mode_exception_delegation = {}
        self.s_mode_exception_delegation = {}
        self.m_mode_interrupt_delegation = {}
        self.s_mode_interrupt_delegation = {}
        self.support_supervisor_mode = 0
        self.no_wfi = 1 # default value
        self.min_stack_len_per_program = 10 * (riscv_core_setting.XLEN/8) # default value
        self.max_stack_len_per_program = 16 * (riscv_core_setting.XLEN/8) # default value
    
        # lists for mode_exception & mode_interrupt
        self.mode_exp_lst = list(map(lambda a: a.name, exception_cause_t))
        self.mode_intrpt_lst = list(map(lambda b: b.name, interrupt_cause_t))
    
        # list for init_privileged_mode
        self.init_privileged_mode = list(map(lambda mode: mode.name, privileged_mode_t))
    
        # list of main implemented CSRs
        self.invalid_priv_mode_csrs = [] 
     
        # initialsation for mode dicts
        for i in self.mode_exp_lst:
          self.m_mode_exception_delegation[i] = None
          self.s_mode_exception_delegation[i] = None
    
        for j in self.mode_intrpt_lst:
          self.m_mode_interrupt_delegation[j] = None
          self.s_mode_interrupt_delegation[j] = None
  
  
    def check_setting(self):
    
        support_64b = 0
        support_128b = 0

        # list of satp_mode_t from riscv_core_setting.py
        stp_md_lst = riscv_core_setting.SATP_MODE

        #list of riscv_instr_group_t with names of riscv_instr_name_t in it. 
        supported_isa_lst = list(map(lambda z: z.name, riscv_instr_group_t))

        # list of supported_isa from riscv_core_setting.py
        supported_isa_stng_lst = riscv_core_setting.supported_isa

        
        #logic to get names of satp_mode_t enum. this logic can be commented once
        # stp_md_lst is supplied from riscv_core_setting.py
        #stp_md_lst = list(map(lambda y: y.name, satp_mode_t))
        #print(stp_md_lst)  

        # check the valid isa support 
        for x in supported_isa_stng_lst: 
          if x == (supported_isa_lst[1] or supported_isa_lst[3] or supported_isa_lst[5] or supported_isa_lst[8] or supported_isa_lst[11] or supported_isa_lst[13] or supported_isa_lst[19]):
            support_64b = 1
            print(x)
          elif x == (supported_isa_lst[14] or supported_isa_lst[15]):
            support_128b = 1
            print(x)
             
        if (support_128b == 1) and (riscv_core_setting.XLEN != 128):
          logging.critical("XLEN should be set to 128 based on riscv_instr_pkg::supported_isa setting")
          print("XLEN Vlaue =", riscv_core_setting.XLEN)
            
        if (support_128b == 0) and (support_64b == 1) and (riscv_core_setting.XLEN != 64):
          logging.critical("XLEN should be set to 64 based on riscv_instr_pkg::supported_isa setting")
          print("XLEN Vlaue =",riscv_core_setting.XLEN)
            
        if not(support_128b or support_64b) and (riscv_core_setting.XLEN != 32):
          logging.critical("XLEN should be set to 32 based on riscv_instr_pkg::supported_isa setting")
          print("XLEN Vlaue =", riscv_core_setting.XLEN)
            
        if not(support_128b or support_64b) and not(('SV32' in stp_md_lst) or ('BARE' in stp_md_lst)):
          logging.critical("SATP mode %s is not supported for RV32G ISA", stp_md_lst)  
         
  
    def setup_instr_distribution():
        pass
        
  
    def init_delegation(self):
        
        for i in self.mode_exp_lst:
          if i == self.mode_exp_lst[0]:
            continue
          self.m_mode_exception_delegation[i] = 0
          self.s_mode_exception_delegation[i] = 0
          print(self.m_mode_exception_delegation)
          print(self.s_mode_exception_delegation)
    
        for j in self.mode_intrpt_lst:
          if j == self.mode_intrpt_lst[0]:
            continue
          self.m_mode_interrupt_delegation[j] = 0
          self.s_mode_interrupt_delegation[j] = 0
          print(self.m_mode_interrupt_delegation)
          print(self.s_mode_interrupt_delegation)
  
        
    def pre_randomize(self):
    
        supported_privileged_mode_lst = [] #list for privileged_mode_t.should be supplied from riscv_core_setting.py
    
        for x in privileged_mode_t: #once riscv_core_setting.py
          y = x.name
          if(y == "SUPERVISOR_MODE"):
            self.support_supervisor_mode = 1
  
  
    def get_non_reserved_gpr(self):
        pass
  
  
    def post_randomize(self):
    
        #Setup the list all reserved registers. This logic is not required as of now
        #reserved_regs = {tp, sp, scratch_reg};
    
        min_stack_len_per_program = 2 * (riscv_core_setting.XLEN/8)
        print("min_stack_len_per_program value = ",min_stack_len_per_program)
    
        self.check_setting() #to check the setting is legal
    
        if self.init_privileged_mode[0]:
          print("mode = ",privileged_mode_t.USER_MODE.name)
          no_wfi = 1
          print("no_wfi value :",no_wfi)
      
  
    def get_invalid_priv_lvl_csr(self):
        
        invalid_lvl = [] 
        invalid_lvl.append('D') # Debug CSRs are inaccessible from all but Debug Mode, and we cannot boot into Debug Mode.
    
        for mode in self.init_privileged_mode:
          if mode == 'SUPERVISOR_MODE':
            invalid_lvl.append('M')
            print("supr_mode---",invalid_lvl)
          if mode == 'USER_MODE':
            invalid_lvl.append('S')
            invalid_lvl.append('M')
            print("usr_mode---",invalid_lvl)
    
        for x in riscv_core_setting.implemented_csr: # implemented_csr should be supplied from riscv_core_setting.py
          if x[0] in invalid_lvl:
            self.invalid_priv_mode_csrs.append(x)
            print(self.invalid_priv_mode_csrs)
