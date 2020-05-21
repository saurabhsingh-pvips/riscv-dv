
from collections import defaultdict
class riscv_instr:
    
    def __init__(self):
        self.instr_registry = {}
        self.instr_names = []
        self.riscv_instr_name_t = None
        self.instr_name = None
        self.instr_group = defaultdict(list) # dictionary of list
        self.instr_category = defaultdict(list) # dictionary of list
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

    def register (self, instr_name):
        #`uvm_info("riscv_instr", $sformatf("Registering %0s", instr_name.name()), UVM_LOW)
        print("Registering {}".format(self.instr_name))
        self.instr_registry[self.instr_name] = 1
        return 1
        
    def create_instr_list(self, cfg):
        self.instr_names.clear()
        self.instr_group.clear()
        self.instr_category.clear()
        
        for _ in range(len(self.instr_registry)):
            instr_inst = riscv_instr() # Instance of class riscv_instr
            if(self.instr_name in unsupported_instr): #TODO - How to access the unsupported_instr
                continue
            instr_inst = create_instr(self.instr_name) #TODO - create_instr function 
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
                continue
            if ((instr_inst.group in supported_isa) and not ((cfg.disable_compressed_instr and \
            (instr_inst.group in (RV32C or RV64C or RV32DC or RV32FC or RV128C)))) and \
            not((cfg.enable_floating_point and (instr_inst.group in (RV32F or RV64F or RV32D or RV64D))))):
                instr_category[instr_inst.category].append(self.instr_name)
            
            self.instr_category[instr_inst.category].append(self.instr_name);
            self.instr_group[instr_inst.group].append(self.instr_name);
            self.instr_names.append(self.instr_name);

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
