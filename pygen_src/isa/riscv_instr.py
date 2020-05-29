
from collections import defaultdict
from pygen_src.riscv_instr_gen_config import *
from pygen_src.riscv_instr_pkg import *
from pygen_src.isa import rv32i_instr
import random
class riscv_instr:
    instr_registry = {}
    def __init__(self): 
        self.instr_names = []
        self.instr_name = None
        self.instr_group =  defaultdict(list) 
        self.instr_category = defaultdict(list)
        self.basic_instr = []
        self.instr_template = {}
        
        self.exclude_reg = []
        self.include_reg = []

        self.group = None
        self.format = None
        self.category = None
        self.imm_type = None
        self.imm_len = None

        self.csr = None
        self.rs2 = None
        self.rs1 = None
        self.rd = None
        self.imm = None

        self.imm_mask = 0xffff_ffff 
        self.is_branch_target = None
        self.has_label  = 1
        self.atomic = 0
        self.branch_assigned = None
        self.process_load_store = 1
        self.is_compressed = None
        self.is_illegal_instr = None
        self.is_hint_instr = None
        self.is_floating_point = None
        self.imm_str = None
        self.comment = None
        self.label = None
        self.is_local_numeric_label = None
        self.idx = -1
        self.has_rs1 = 1
        self.has_rs2 = 1
        self.has_rd = 1
        self.has_imm = 1

        #Fields Added for debugging These fields are actually from a different files. 
        self.unsupported_instr = []
        self.XLEN = 32
        self.supported_isa  = [riscv_instr_group_t.RV32I]
        self.implemented_csr = [] 
    @classmethod
    def register (cls, instr_name):
        print("Registering {}".format(instr_name.name))
        cls.instr_registry[instr_name.name] = 1
        if instr_name == None:
            print("\n")
        return 1

    
    
    def create_instr_list(self, cfg):
        self.instr_names.clear()
        self.instr_group.clear()
        self.instr_category.clear()
        for instr_name, values in self.instr_registry.items():

            if(instr_name in self.unsupported_instr):
                continue
            instr_inst = self.create_instr(instr_name) #create_instr function TODO
            self.instr_template[instr_name] = instr_inst

            if (not instr_inst.is_supported(cfg)):
                continue
            if ((self.XLEN != 32) and (instr_name == "C_JAL")):
                continue
            if (("SP" in cfg.reserved_regs) and (instr_name == "C_ADDI16SP")):
                continue
            if (cfg.enable_sfence and instr_name == "SFENCE_VMA"):
                continue
            if (instr_name in ["FENCE","FENCE_I","SFENCE_VMA"]):
                continue
            if (instr_inst.group in self.supported_isa):
                self.instr_category[instr_inst.category.name].append(instr_name)
                self.instr_group[instr_inst.group.name].append(instr_name)
                self.instr_names.append(instr_name)
        print("Category: {} \n".format(dict(self.instr_category)))
        print("Group: {} \n".format(dict(self.instr_group)))
        print("Instruction Name: {} \n".format(self.instr_names))

        self.build_basic_instruction_list(cfg)
        self.create_csr_filter(cfg)
        
    
    def create_instr(self, instr_name):
        instr_inst = eval("rv32i_instr.riscv_"+instr_name+"_instr()")
        return instr_inst

    def is_supported(self, cfg):
        return 1

    def build_basic_instruction_list(self, cfg):
        self.basic_instr = (self.instr_category["SHIFT"] + self.instr_category["ARITHMETIC"] + self.instr_category["LOGICAL"] + self.instr_category["COMPARE"])
        if(cfg.no_ebreak):
            self.basic_instr.append("EBREAK")
            for items in self.supported_isa:
                if("RV32C" in self.supported_isa and not(cfg.disable_compressed_instr)):
                    self.basic_instr.append("C_EBREAK")
                    break
        if(cfg.no_dret==0):
            slef.basic_instr.append("DRET")
        if(cfg.no_fence==0):
            self.basic_instr.append(self.instr_category["SYNCH"])
        if(cfg.no_csr_instr == 0 and cfg.init_privileged_mode == "MACHINE_MODE"):
            self.basic_instr.append(self.instr_category["CSR"])
        if(cfg.no_wfi == 0):
            self.basic_instr.append("WFI")
        print("\n Basic_Instr: {} ".format(self.basic_instr))
    def create_csr_filter(self, cfg):
        self.include_reg.clear()
        self.exclude_reg.clear()

        if(cfg.enable_illegal_csr_instruction):
            self.exclude_reg = self.implemented_csr
        elif(cfg.enable_access_invalid_csr_level):
            self.include_reg = cfg.invalid_priv_mode_csrs
        else:
            if(cfg.init_privileged_mode == "MACHINE_MODE"): # Machine Mode
                self.include_reg.append("MSCRATCH")
            elif(cfg.init_privileged_mode=="SUPERVISOR_MODE"): # Supervisor Mode
                self.include_reg.append("SSCRATCH")
            else: # User Mode
                self.include_reg.append("USCRATCH") 

    def get_rand_instr(self):
        pass

    def get_load_store_instr(self):
        pass

    def get_instr(self):
        pass

    def set_rand_mode(self):
        pass

    def pre_randomize(self):
        pass

    def set_imm_len(self):
        pass

    def extend_imm(self):
        self.extend_imm()
        self.update_imm_str()

    def post_randomize(self):
        pass

    def convert2asm(self):
        pass

    def get_opcode(self):
        pass

    def get_func3(self):
        pass

    def get_func7(self):
        pass

    def convert2bin(self):
        pass

    def get_instr_name(self):
        pass

    def get_c_gpr(self):
        pass

    def get_imm(self):
        return imm_str

    def clear_unused_label(self):
        pass

    def do_copy(self):
        pass

    def update_imm_str(self):
        pass

riscv_instr_ins = riscv_instr()
cfg = riscv_instr_gen_config()
