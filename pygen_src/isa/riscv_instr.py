
from collections import defaultdict
from riscv_instr_gen_config import *
from riscv_instr_pkg import *
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


        # Field Added for debugging These fields are actually from a different files. 
        self.unsupported_instr = []
        self.XLEN = 32
        self.supported_isa  = ["RV32I"]
        self.implemented_csr = [] 

    def register (self, instr_name):
        for i in range(len(instr_name)):
            print("Registering {}".format(instr_name[i]))
            self.instr_registry[instr_name[i]] = 1
        return 1

    

    def create_instr_list(self, cfg):
        self.instr_names.clear()
        self.instr_group.clear()
        self.instr_category.clear()
        
        for instr_name, values in self.instr_registry.items():
            if(instr_name in self.unsupported_instr):
                continue
            #instr_inst = create_instr(instr_name) #create_instr function TODO
            #self.instr_template[instr_name] = str(instr_inst)+instr_name
            if (not (self.is_supported(cfg))):
                continue
            if ((self.XLEN != 32) and (instr_name == "C_JAL")):
                continue
            if (("SP" in cfg.reserved_regs) and (instr_name == "C_ADDI16SP")):
                continue
            if (cfg.enable_sfence and instr_name == "SFENCE_VMA"):
                continue
            if (instr_name in ["FENCE","FENCE_I","SFENCE_VMA"]):
                continue
            if ((all(x in self.supported_isa for x in riscv_instr_pkg_inst.group)) and not ((cfg.disable_compressed_instr and \
            (riscv_instr_pkg_inst.group in ["RV32C","RV64C","RV32DC","RV32FC","RV128C"]))) and \
            not((cfg.enable_floating_point and (riscv_instr_pkg_inst.group in ["RV32F","RV64F","RV32D","RV64D"])))):
                print("Inside create_instr_list Function")

                #TO-DO
                #self.instr_category[riscv_instr_pkg_inst.category[random.randint(0,4)]].append(riscv_instr_pkg_inst.instr_name[instr_name])
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


riscv_instr_ins = riscv_instr()
cfg = riscv_instr_gen_config()
riscv_instr_pkg_inst = riscv_instr_pkg()
