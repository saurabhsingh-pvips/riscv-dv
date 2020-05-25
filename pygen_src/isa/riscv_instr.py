
from collections import defaultdict
from riscv_instr_gen_config import *
from riscv_instr_pkg import *
import pdb
import random
class riscv_instr:
	
    def __init__(self):
        self.instr_registry = {}
        self.instr_names = []
        #self.riscv_instr_name_t = None
        self.instr_name = [] 
        self.instr_group =  defaultdict(list) 
        self.instr_category = defaultdict(list)
        self.basic_instr = []
        self.instr_template = {}
        
        self.exclude_reg = []
        self.include_reg = []

        self.group = None
        self.format = None
        self.category = None

        self.csr = None
        self.rs2 = None
        self.rs1 = None
        self.rd = None

        self.supported_isa  = ["RV32I"] # Field Added for debugging. 

    def register (self, instr_name):
        for i in range(len(instr_name)):
            print("Registering {}".format(instr_name[i]))
            self.instr_registry[instr_name[i]] = 1
        return 1

    def create_instr_list(self, cfg):
        self.instr_names.clear()
        self.instr_group.clear()
        self.instr_category.clear()
        
        for i in range(len(self.instr_registry)):
            instr_inst = riscv_instr() # Instance of class riscv_instr
            '''if(self.instr_name in unsupported_instr):
                continue
            instr_inst = create_instr(self.instr_name) #create_instr function TODO
            self.instr_template[self.instr_name] = instr_inst
            if (not (self.is_supported(cfg))):
                continue
            if ((XLEN != 32) and (self.instr_name == "C_JAL")):
                continue
            if ((SP in cfg.reserved_regs) and (self.instr_name in C_ADDI16SP)):
                continue
            if (not (cfg.enable_sfence and self.instr_name == "SFENCE_VMA")):
                continue
            if (cfg.no_fence and (self.instr_name in (FENCE or FENCE_I or SFENCE_VMA))):
                continue'''
            #pdb.set_trace()
            if ((all(x in self.supported_isa for x in riscv_pkg.group)) and not ((cfg.disable_compressed_instr and \
            (riscv_pkg.group in ["RV32C","RV64C","RV32DC","RV32FC","RV128C"]))) and \
            not((cfg.enable_floating_point and (riscv_pkg.group in ["RV32F","RV64F","RV32D","RV64D"])))):
                pass 
            #riscv_instr_ins.instr_category[riscv_pkg.category[random.randint(0,4)]].append(riscv_pkg.instr_name[i])
            #self.instr_category[riscv_pkg.instr_category].append(self.instr_name);
            #self.instr_group[riscv_pkg.instr_group].append(self.instr_name);
            #self.instr_names.append(self.instr_name);

            self.build_basic_instruction_list(cfg)
            self.create_csr_filter(cfg)

    def create_instr(self, instr_name):
        pass
    
    def is_supported(self, cfg):
        return 1

    def build_basic_instruction_list(self, cfg):
        pass

    def create_csr_filter(self, cfg):
        pass
riscv_instr_ins = riscv_instr()
cfg = riscv_instr_gen_config()
riscv_pkg = riscv_instr_pkg()
riscv_instr_ins.register(riscv_pkg.instr_name)
riscv_instr_ins.create_instr_list(cfg)
print(riscv_instr_ins.instr_registry)   
print(riscv_instr_ins.instr_category)
