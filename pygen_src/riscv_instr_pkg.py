##############################################################################
##           Convertion of riscv_instr_pkg.sv into python                   ##
##############################################################################


from enum import *
from random import *
from struct import *
from bitstring import BitArray, BitStream



class riscv_instr_pkg:

    import dv_defines
    import riscv_defines
    import uvm_macros

    #import uvm_pkg:: *
    #import riscv_signature_pkg:: *
    #`define include_file(f) `include `"f`"           
    
    inst = uvm_cmdline_processor()                     # uvm_cmdline_processor  inst;

    # Data section setting
    class mem_region_t:
	name
        size_in_bytes
        xwr                                             # xwr = Excutable,Writable,Readale

  
    class satp_mode_t(Enum):
        BARE = 0b0000
        SV32 = 0b0001
        SV39 = 0b1000
        SV48 = 0b1001
        SV57 = 0b1010
        SV64 = 0b1011

    class f_rounding_mode_t(Enum):
        RNE = 0b000
        RTZ = 0b001
        RDN = 0b010
        RUP = 0b011
        RMM = 0b100

    class mtvec_mode_t(Enum):
        DIRECT = 0b00
        VECTORED = 0b01


    class imm_t(Enum):
        IMM    = 0        # Signed immediate
        UIMM   = auto()   # Unsigned immediate
        NZUIMM = auto()   # Non-zero unsigned immediate
        NZIMM  = auto()   # Non-zero signed immediate


    class privileged_mode_t(Enum):
        USER_MODE       = 0b00
        SUPERVISOR_MODE = 0b01
        RESERVED_MODE   = 0b10
        MACHINE_MODE    = 0b11


    class riscv_instr_group_t(Enum):
        RV32I = 0
        RV64I = auto()
        RV32M = auto()
        RV64M = auto()
        RV32A = auto()
        RV64A = auto()
        RV32F = auto()
        RV32FC = auto()
        RV64F = auto()
        RV32D = auto()
        RV32DC = auto()
        RV64D = auto()
        RV32C = auto()
        RV64C = auto()
        RV128I = auto()
        RV128C = auto()
        RV32V = auto()
        RV32B = auto()
        RV64V = auto()
        RV64B = auto()
        RV32X = auto()
        RV64X = auto()

    class riscv_instr_name_t(Enum):
        # RV32I instructions
        LUI = 0
        AUIPC = auto()
        JAL = auto()
        JALR = auto()
        BEQ = auto()
        BNE = auto()
        BLT = auto()
        BGE = auto()
        BLTU = auto()
        BGEU = auto()
        LB = auto()
        LH = auto()
        LW = auto()
        LBU = auto()
        LHU = auto()
        SB = auto()
        SH = auto()
        SW = auto()
        ADDI = auto()
        SLTI = auto()
        SLTIU = auto()
        XORI = auto()
        ORI = auto()
        ANDI = auto()
        SLLI = auto()
        SRLI = auto()
        SRAI = auto()
        ADD = auto()
        SUB = auto()
        SLL = auto()
        SLT = auto()
        SLTU = auto()
        XOR = auto()
        SRL = auto()
        SRA = auto()
        OR = auto()
        AND = auto()
        NOP = auto()
        FENCE = auto()
        FENCE_I = auto()
        ECALL = auto()
        EBREAK = auto()
        CSRRW = auto()
        CSRRS = auto()
        CSRRC = auto()
        CSRRWI = auto()
        CSRRSI = auto()
        CSRRCI = auto()
        # RV32B instructions
        ANDN = auto()
        ORN = auto()
        XNOR = auto()
        GORC = auto()
        SLO = auto()
        SRO = auto()
        ROL = auto()
        ROR = auto()
        SBCLR = auto()
        SBSET = auto()
        SBINV = auto()
        SBEXT = auto()
        GREV = auto()
        SLOI = auto()
        SROI = auto()
        RORI = auto()
        SBCLRI = auto()
        SBSETI = auto()
        SBINVI = auto()
        SBEXTI = auto()
        GORCI = auto()
        GREVI = auto()
        CMIX = auto()
        CMOV = auto()
        FSL = auto()
        FSR = auto()
        FSRI = auto()
        CLZ = auto()
        CTZ = auto()
        PCNT = auto()
        SEXT_B = auto()
        SEXT_H = auto()
        CRC32_B = auto()
        CRC32_H = auto()
        CRC32_W = auto()
        CRC32C_B = auto()
        CRC32C_H = auto()
        CRC32C_W = auto()
        CLMUL = auto()
        CLMULR = auto()
        CLMULH = auto()
        MIN = auto()
        MAX = auto()
        MINU = auto()
        MAXU = auto()
        SHFL = auto()
        UNSHFL = auto()
        BDEP = auto()
        BEXT = auto()
        PACK = auto()
        PACKU = auto()
        BMATOR = auto()
        BMATXOR = auto()
        PACKH = auto()
        BFP = auto()
        SHFLI = auto()
        UNSHFLI = auto()
        # RV64B instructions
        ADDIWU = auto()
        SLLIU_W = auto()
        ADDWU = auto()
        SUBWU = auto()
        BMATFLIP = auto()
        CRC32_D = auto()
        CRC32C_D = auto()
        ADDU_W = auto()
        SUBU_W = auto()
        SLOW = auto()
        SROW = auto()
        ROLW = auto()
        RORW = auto()
        SBCLRW = auto()
        SBSETW = auto()
        SBINVW = auto()
        SBEXTW = auto()
        GORCW = auto()
        GREVW = auto()
        SLOIW = auto()
        SROIW = auto()
        RORIW = auto()
        SBCLRIW = auto()
        SBSETIW = auto()
        SBINVIW = auto()
        GORCIW = auto()
        GREVIW = auto()
        FSLW = auto()
        FSRW = auto()
        FSRIW = auto()
        CLZW = auto()
        CTZW = auto()
        PCNTW = auto()
        CLMULW = auto()
        CLMULRW = auto()
        CLMULHW = auto()
        SHFLW = auto()
        UNSHFLW = auto()
        BDEPW = auto()
        BEXTW = auto()
        PACKW = auto()
        PACKUW = auto()
        BFPW = auto()
        # RV32M instructions
        MUL = auto()
        MULH = auto()
        MULHSU = auto()
        MULHU = auto()
        DIV = auto()
        DIVU = auto()
        REM = auto()
        REMU = auto()
        # RV64M instructions
        MULW = auto()
        DIVW = auto()
        DIVUW = auto()
        REMW = auto()
        REMUW = auto()
        # RV32F instructions
        FLW = auto()
        FSW = auto()
        FMADD_S = auto()
        FMSUB_S = auto()
        FNMSUB_S = auto()
        FNMADD_S = auto()
        FADD_S = auto()
        FSUB_S = auto()
        FMUL_S = auto()
        FDIV_S = auto()
        FSQRT_S = auto()
        FSGNJ_S = auto()
        FSGNJN_S = auto()
        FSGNJX_S = auto()
        FMIN_S = auto()
        FMAX_S = auto()
        FCVT_W_S = auto()
        FCVT_WU_S = auto()
        FMV_X_W = auto()
        FEQ_S = auto()
        FLT_S = auto()
        FLE_S = auto()
        FCLASS_S = auto()
        FCVT_S_W = auto()
        FCVT_S_WU = auto()
        FMV_W_X = auto()
        # RV64F instruction
        FCVT_L_S = auto()
        FCVT_LU_S = auto()
        FCVT_S_L = auto()
        FCVT_S_LU = auto()
        # RV32D instructions
        FLD = auto()
        FSD = auto()
        FMADD_D = auto()
        FMSUB_D = auto()
        FNMSUB_D = auto()
        FNMADD_D = auto()
        FADD_D = auto()
        FSUB_D = auto()
        FMUL_D = auto()
        FDIV_D = auto()
        FSQRT_D = auto()
        FSGNJ_D = auto()
        FSGNJN_D = auto()
        FSGNJX_D = auto()
        FMIN_D = auto()
        FMAX_D = auto()
        FCVT_S_D = auto()
        FCVT_D_S = auto()
        FEQ_D = auto()
        FLT_D = auto()
        FLE_D = auto()
        FCLASS_D = auto()
        FCVT_W_D = auto()
        FCVT_WU_D = auto()
        FCVT_D_W = auto()
        FCVT_D_WU = auto()
        # RV64D
        FCVT_L_D = auto()
        FCVT_LU_D = auto()
        FMV_X_D = auto()
        FCVT_D_L = auto()
        FCVT_D_LU = auto()
        FMV_D_X = auto()
        # RV64I
        LWU = auto()
        LD = auto()
        SD = auto()
        ADDIW = auto()
        SLLIW = auto()
        SRLIW = auto()
        SRAIW = auto()
        ADDW = auto()
        SUBW = auto()
        SLLW = auto()
        SRLW = auto()
        SRAW = auto()
        # RV32C
        C_LW = auto()
        C_SW = auto()
        C_LWSP = auto()
        C_SWSP = auto()
        C_ADDI4SPN = auto()
        C_ADDI = auto()
        C_LI = auto()
        C_ADDI16SP = auto()
        C_LUI = auto()
        C_SRLI = auto()
        C_SRAI = auto()
        C_ANDI = auto()
        C_SUB = auto()
        C_XOR = auto()
        C_OR = auto()
        C_AND = auto()
        C_BEQZ = auto()
        C_BNEZ = auto()
        C_SLLI = auto()
        C_MV = auto()
        C_EBREAK = auto()
        C_ADD = auto()
        C_NOP = auto()
        C_J = auto()
        C_JAL = auto()
        C_JR = auto()
        C_JALR = auto()
        # RV64C
        C_ADDIW = auto()
        C_SUBW = auto()
        C_ADDW = auto()
        C_LD = auto()
        C_SD = auto()
        C_LDSP = auto()
        C_SDSP = auto()
        # RV128C
        C_SRLI64 = auto()
        C_SRAI64 = auto()
        C_SLLI64 = auto()
        C_LQ = auto()
        C_SQ = auto()
        C_LQSP = auto()
        C_SQSP = auto()
        # RV32FC
        C_FLW = auto()
        C_FSW = auto()
        C_FLWSP = auto()
        C_FSWSP = auto()
        # RV32DC
        C_FLD = auto()
        C_FSD = auto()
        C_FLDSP = auto()
        C_FSDSP = auto()
        # RV32A
        LR_W = auto()
        SC_W = auto()
        AMOSWAP_W = auto()
        AMOADD_W = auto()
        AMOAND_W = auto()
        AMOOR_W = auto()
        AMOXOR_W = auto()
        AMOMIN_W = auto()
        AMOMAX_W = auto()
        AMOMINU_W = auto()
        AMOMAXU_W = auto()
        # RV64A
        LR_D = auto()
        SC_D = auto()
        AMOSWAP_D = auto()
        AMOADD_D = auto()
        AMOAND_D = auto()
        AMOOR_D = auto()
        AMOXOR_D = auto()
        AMOMIN_D = auto()
        AMOMAX_D = auto()
        AMOMINU_D = auto()
        AMOMAXU_D = auto()
        # Vector instructions
        VSETVL = auto()
        VSETVLI = auto()
        VADD = auto()
        VSUB = auto()
        VRSUB = auto()
        VWADDU = auto()
        VWSUBU = auto()
        VWADD = auto()
        VWSUB = auto()
        VADC = auto()
        VMADC = auto()
        VSBC = auto()
        VMSBC = auto()
        VAND = auto()
        VOR = auto()
        VXOR = auto()
        VSLL = auto()
        VSRL = auto()
        VSRA = auto()
        VNSRL = auto()
        VNSRA = auto()
        VMSEQ = auto()
        VMSNE = auto()
        VMSLTU = auto()
        VMSLT = auto()
        VMSLEU = auto()
        VMSLE = auto()
        VMSGTU = auto()
        VMSGT = auto()
        VMINU = auto()
        VMIN = auto()
        VMAXU = auto()
        VMAX = auto()
        VMUL = auto()
        VMULH = auto()
        VMULHU = auto()
        VMULHSU = auto()
        VDIVU = auto()
        VDIV = auto()
        VREMU = auto()
        VREM = auto()
        VWMUL = auto()
        VWMULU = auto()
        VWMULSU = auto()
        VMACC = auto()
        VNMSAC = auto()
        VMADD = auto()
        VNMSUB = auto()
        VWMACCU = auto()
        VWMACC = auto()
        VWMACCSU = auto()
        VWMACCUS = auto()
        
        #VQMACCU = auto()
        #VQMACC = auto()
        #VQMACCSU = auto()
        #VQMACCUS = auto()
        
        VMERGE = auto()
        VMV = auto()
        VSADDU = auto()
        VSADD = auto()
        VSSUBU = auto()
        VSSUB = auto()
        VAADDU = auto()
        VAADD = auto()
        VASUBU = auto()
        VASUB = auto()
        VSSRL = auto()
        VSSRA = auto()
        VNCLIPU = auto()
        VNCLIP = auto()
        VFADD = auto()
        VFSUB = auto()
        VFRSUB = auto()
        VFMUL = auto()
        VFDIV = auto()
        VFRDIV = auto()
        VFWMUL = auto()
        VFMACC = auto()
        VFNMACC = auto()
        VFMSAC = auto()
        VFNMSAC = auto()
        VFMADD = auto()
        VFNMADD = auto()
        VFMSUB = auto()
        VFNMSUB = auto()
        VFWMACC = auto()
        VFWNMACC = auto()
        VFWMSAC = auto()
        VFWNMSAC = auto()
        VFSQRT_V = auto()
        VFMIN = auto()
        VFMAX = auto()
        VFSGNJ = auto()
        VFSGNJN = auto()
        VFSGNJX = auto()
        VMFEQ = auto()
        VMFNE = auto()
        VMFLT = auto()
        VMFLE = auto()
        VMFGT = auto()
        VMFGE = auto()
        VFCLASS_V = auto()
        VFMERGE = auto()
        VFMV = auto()
        VFCVT_XU_F_V = auto()
        VFCVT_X_F_V = auto()
        VFCVT_F_XU_V = auto()
        VFCVT_F_X_V = auto()
        VFWCVT_XU_F_V = auto()
        VFWCVT_X_F_V = auto()
        VFWCVT_F_XU_V = auto()
        VFWCVT_F_X_V = auto()
        VFWCVT_F_F_V = auto()
        VFNCVT_XU_F_W = auto()
        VFNCVT_X_F_W = auto()
        VFNCVT_F_XU_W = auto()
        VFNCVT_F_X_W = auto()
        VFNCVT_F_F_W = auto()
        VFNCVT_ROD_F_F_W = auto()
        # Vector reduction instruction
        VREDSUM_VS = auto()
        VREDMAXU_VS = auto()
        VREDMAX_VS = auto()
        VREDMINU_VS = auto()
        VREDMIN_VS = auto()
        VREDAND_VS = auto()
        VREDOR_VS = auto()
        VREDXOR_VS = auto()
        VWREDSUMU_VS = auto()
        VWREDSUM_VS = auto()
        VFREDOSUM_VS = auto()
        VFREDSUM_VS = auto()
        VFREDMAX_VS = auto()
        VFWREDOSUM_VS = auto()
        VFWREDSUM_VS = auto()
        # Vector mask instruction
        VMAND_MM = auto()
        VMNAND_MM = auto()
        VMANDNOT_MM = auto()
        VMXOR_MM = auto()
        VMOR_MM = auto()
        VMNOR_MM = auto()
        VMORNOT_MM = auto()
        VMXNOR_MM = auto()
        VPOPC_M = auto()
        VFIRST_M = auto()
        VMSBF_M = auto()
        VMSIF_M = auto()
        VMSOF_M = auto()
        VIOTA_M = auto()
        VID_V = auto()
        # Vector permutation instruction
        VMV_X_S = auto()
        VMV_S_X = auto()
        VFMV_F_S = auto()
        VFMV_S_F = auto()
        VSLIDEUP = auto()
        VSLIDEDOWN = auto()
        VSLIDE1UP = auto()
        VSLIDE1DOWN = auto()
        VRGATHER = auto()
        VCOMPRESS = auto()
        VMV1R_V = auto()
        VMV2R_V = auto()
        VMV4R_V = auto()
        VMV8R_V = auto()
        # Supervisor instruction
        DRET = auto()
        MRET = auto()
        URET = auto()
        SRET = auto()
        WFI = auto()
        SFENCE_VMA = auto()
        # Custom instructions
        # import riscv_custom_instr_enum #TODO: Right now it's not working as expected fix it
        # You can add other instructions here
        INVALID_INSTR = auto()

    #Maximum virtual address bits used by the program parameter

    def MAX_USED_VADDR_BITS():                # parameter intMAX_USED_VADDR_BITS = 30
        return 30


    class riscv_reg_t(Enum):
        ZERO = 0
        RA   = auto()
        SP   = auto()
        GP   = auto()
        TP   = auto()
        T0   = auto()
        T1   = auto()
        T2   = auto()
        S0   = auto()
        S1   = auto()
        A0   = auto()
        A1   = auto()
        A2   = auto()
        A3   = auto()
        A4   = auto()
        A5   = auto()
        A6   = auto()
        A7   = auto()
        S2   = auto()
        S3   = auto()
        S4   = auto()
        S5   = auto()
        S6   = auto()
        S7   = auto()
        S8   = auto()
        S9   = auto()
        S10  = auto()
        S11  = auto()
        T3   = auto()
        T4   = auto()
        T5   = auto()
        T6   = auto()


    class riscv_fpr_t(Enum):
        FT0 = auto()
        FT1 = auto()
        FT2 = auto()
        FT3 = auto()
        FT4 = auto()
        FT5 = auto()
        FT6 = auto()
        FT7 = auto()
        FS0 = auto()
        FS1 = auto()
        FA0 = auto()
        FA1 = auto()
        FA2 = auto()
        FA3 = auto()
        FA4 = auto()
        FA5 = auto()
        FA6 = auto()
        FA7 = auto()
        FS2 = auto()
        FS3 = auto()
        FS4 = auto()
        FS5 = auto()
        FS6 = auto()
        FS7 = auto()
        FS8 = auto()
        FS9 = auto()
        FS10 = auto()
        FS11 = auto()
        FT8 = auto()
        FT9 = auto()
        FT10 = auto()
        FT11 = auto()


    class riscv_vreg_t(Enum):
        V0 = auto()
        V1 = auto()
        V2 = auto()
        V3 = auto()
        V4 = auto()
        V5 = auto()
        V6 = auto()
        V7 = auto()
        V8 = auto()
        V9 = auto()
        V10 = auto()
        V11 = auto()
        V12 = auto()
        V13 = auto()
        V14 = auto()
        V15 = auto()
        V16 = auto()
        V17 = auto()
        V18 = auto()
        V19 = auto()
        V20 = auto()
        V21 = auto()
        V22 = auto()
        V23 = auto()
        V24 = auto()
        V25 = auto()
        V26 = auto()
        V27 = auto()
        V28 = auto()
        V29 = auto()
        V30 = auto()
        V31 = auto()

    class riscv_instr_format_t(Enum):
        J_FORMAT = 0
        U_FORMAT = auto()
        I_FORMAT = auto()
        B_FORMAT = auto()
        R_FORMAT = auto()
        S_FORMAT = auto()
        R4_FORMAT = auto()
        # Compressed instruction format
        CI_FORMAT = auto()
        CB_FORMAT = auto()
        CJ_FORMAT = auto()
        CR_FORMAT = auto()
        CA_FORMAT = auto()
        CL_FORMAT = auto()
        CS_FORMAT = auto()
        CSS_FORMAT = auto()
        CIW_FORMAT = auto()
        # Vector instruction format
        VSET_FORMAT = auto()
        VA_FORMAT = auto()
        VS2_FORMAT = auto()  # op vd,vs2
        VL_FORMAT = auto()
        VS_FORMAT = auto()

    # Vector arithmetic instruction variant
    class va_variant_t(Enum):
        VV = auto()
        VI = auto()
        VX = auto()
        VF = auto()
        WV = auto()
        WI = auto()
        WX = auto()
        VVM = auto()
        VIM = auto()
        VXM = auto()
        VFM = auto()
        VS = auto()
        VM = auto()

    class riscv_instr_category_t(Enum):
        LOAD = 0
        STORE = auto()
        SHIFT = auto()
        ARITHMETIC = auto()
        LOGICAL = auto()
        COMPARE = auto()
        BRANCH = auto()
        JUMP = auto()
        SYNCH = auto()
        SYSTEM = auto()
        COUNTER = auto()
        CSR = auto()
        CHANGELEVEL = auto()
        TRAP = auto()
        INTERRUPT = auto()
        # `VECTOR_INCLUDE("riscv_instr_pkg_inc_riscv_instr_category_t.sv") TODO: Fix this
        AMO = auto()  # (last one)

    #typedef bit[11:0] riscv_csr_t;

    class privileged_reg_t(Enum):

        #User mode register
        USTATUS = 0x000           #User status
        UIE = 0x004               #User interrupt-enable register
        UTVEC = 0x005             #User trap-handler base address
        USCRATCH = 0x040          #Scratch register for user trap handlers
        UEPC = 0x041              #User exception program counter
        UCAUSE = 0x042            #User trap cause
        UTVAL = 0x043             #User bad address or instruction
        UIP = 0x044               #User interrupt pending
        FFLAGS = 0x001            #Floating-Point Accrued Exceptions
        FRM = 0x002               #Floating-Point Dynamic Rounding Mode
        FCSR = 0x003              #Floating-Point Control/Status Register (FRM + FFLAGS)
        CYCLE = 0xC00             #Cycle counter for RDCYCLE instruction
        TIME = 0xC01              #Timer for RDTIME instruction
        INSTRET = 0xC02           #Instructions-retired counter for RDINSTRET instruction
        HPMCOUNTER3 = 0xC03       #Performance-monitoring counter
        HPMCOUNTER4 = 0xC04       #Performance-monitoring counter
        HPMCOUNTER5 = 0xC05       #Performance-monitoring counter
        HPMCOUNTER6 = 0xC06       #Performance-monitoring counter
        HPMCOUNTER7 = 0xC07       #Performance-monitoring counter
        HPMCOUNTER8 = 0xC08       #Performance-monitoring counter
        HPMCOUNTER9 = 0xC09       #Performance-monitoring counter
        HPMCOUNTER10 = 0xC0A      #Performance-monitoring counter
        HPMCOUNTER11 = 0xC0B      #Performance-monitoring counter
        HPMCOUNTER12 = 0xC0C      #Performance-monitoring counter
        HPMCOUNTER13 = 0xC0D      #Performance-monitoring counter
        HPMCOUNTER14 = 0xC0E      #Performance-monitoring counter
        HPMCOUNTER15 = 0xC0F      #Performance-monitoring counter
        HPMCOUNTER16 = 0xC10      #Performance-monitoring counter
        HPMCOUNTER17 = 0xC11      #Performance-monitoring counter
        HPMCOUNTER18 = 0xC12      #Performance-monitoring counter
        HPMCOUNTER19 = 0xC13      #Performance-monitoring counter
        HPMCOUNTER20 = 0xC14      #Performance-monitoring counter
        HPMCOUNTER21 = 0xC15      #Performance-monitoring counter
        HPMCOUNTER22 = 0xC16      #Performance-monitoring counter
        HPMCOUNTER23 = 0xC17      #Performance-monitoring counter
        HPMCOUNTER24 = 0xC18      #Performance-monitoring counter
        HPMCOUNTER25 = 0xC19      #Performance-monitoring counter
        HPMCOUNTER26 = 0xC1A      #Performance-monitoring counter
        HPMCOUNTER27 = 0xC1B      #Performance-monitoring counter
        HPMCOUNTER28 = 0xC1C      #Performance-monitoring counter
        HPMCOUNTER29 = 0xC1D      #Performance-monitoring counter
        HPMCOUNTER30 = 0xC1E      #Performance-monitoring counter
        HPMCOUNTER31 = 0xC1F      #Performance-monitoring counter
        CYCLEH = 0xC80            #Upper 32 bits of CYCLE, RV32I only
        TIMEH = 0xC81             #Upper 32 bits of TIME, RV32I only
        INSTRETH = 0xC82          #Upper 32 bits of INSTRET, RV32I only
        HPMCOUNTER3H = 0xC83      #Upper 32 bits of HPMCOUNTER3, RV32I only
        HPMCOUNTER4H = 0xC84      #Upper 32 bits of HPMCOUNTER4, RV32I only
        HPMCOUNTER5H = 0xC85      #Upper 32 bits of HPMCOUNTER5, RV32I only
        HPMCOUNTER6H = 0xC86      #Upper 32 bits of HPMCOUNTER6, RV32I only
        HPMCOUNTER7H = 0xC87      #Upper 32 bits of HPMCOUNTER7, RV32I only
        HPMCOUNTER8H = 0xC88      #Upper 32 bits of HPMCOUNTER8, RV32I only
        HPMCOUNTER9H = 0xC89      #Upper 32 bits of HPMCOUNTER9, RV32I only
        HPMCOUNTER10H = 0xC8A     #Upper 32 bits of HPMCOUNTER10, RV32I only
        HPMCOUNTER11H = 0xC8B     #Upper 32 bits of HPMCOUNTER11, RV32I only
        HPMCOUNTER12H = 0xC8C     #Upper 32 bits of HPMCOUNTER12, RV32I only
        HPMCOUNTER13H = 0xC8D     #Upper 32 bits of HPMCOUNTER13, RV32I only
        HPMCOUNTER14H = 0xC8E     #Upper 32 bits of HPMCOUNTER14, RV32I only
        HPMCOUNTER15H = 0xC8F     #Upper 32 bits of HPMCOUNTER15, RV32I only
        HPMCOUNTER16H = 0xC90     #Upper 32 bits of HPMCOUNTER16, RV32I only
        HPMCOUNTER17H = 0xC91     #Upper 32 bits of HPMCOUNTER17, RV32I only
        HPMCOUNTER18H = 0xC92     #Upper 32 bits of HPMCOUNTER18, RV32I only
        HPMCOUNTER19H = 0xC93     #Upper 32 bits of HPMCOUNTER19, RV32I only
        HPMCOUNTER20H = 0xC94     #Upper 32 bits of HPMCOUNTER20, RV32I only
        HPMCOUNTER21H = 0xC95     #Upper 32 bits of HPMCOUNTER21, RV32I only
        HPMCOUNTER22H = 0xC96     #Upper 32 bits of HPMCOUNTER22, RV32I only
        HPMCOUNTER23H = 0xC97     #Upper 32 bits of HPMCOUNTER23, RV32I only
        HPMCOUNTER24H = 0xC98     #Upper 32 bits of HPMCOUNTER24, RV32I only
        HPMCOUNTER25H = 0xC99     #Upper 32 bits of HPMCOUNTER25, RV32I only
        HPMCOUNTER26H = 0xC9A     #Upper 32 bits of HPMCOUNTER26, RV32I only
        HPMCOUNTER27H = 0xC9B     #Upper 32 bits of HPMCOUNTER27, RV32I only
        HPMCOUNTER28H = 0xC9C     #Upper 32 bits of HPMCOUNTER28, RV32I only
        HPMCOUNTER29H = 0xC9D     #Upper 32 bits of HPMCOUNTER29, RV32I only
        HPMCOUNTER30H = 0xC9E     #Upper 32 bits of HPMCOUNTER30, RV32I only
        HPMCOUNTER31H = 0xC9F     #Upper 32 bits of HPMCOUNTER31, RV32I only

        #Supervisor mode register
        SSTATUS = 0x100          #Supervisor status
        SEDELEG = 0x102          #Supervisor exception delegation register
        SIDELEG = 0x103          #Supervisor interrupt delegation register
        SIE = 0x104              #Supervisor interrupt-enable register
        STVEC = 0x105            #Supervisor trap-handler base address
        SCOUNTEREN = 0x106       #Supervisor counter enable
        SSCRATCH = 0x140         #Scratch register for supervisor trap handlers
        SEPC = 0x141             #Supervisor exception program counter
        SCAUSE = 0x142           #Supervisor trap cause
        STVAL = 0x143            #Supervisor bad address or instruction
        SIP = 0x144              #Supervisor interrupt pending
        SATP = 0x180             #Supervisor address translation and protection

        #Machine mode register
        MVENDORID = 0xF11        #Vendor ID
        MARCHID = 0xF12          #Architecture ID
        MIMPID = 0xF13           #Implementation ID
        MHARTID = 0xF14          #Hardware thread ID
        MSTATUS = 0x300          #Machine status
        MISA = 0x301             #ISA and extensions
        MEDELEG = 0x302          #Machine exception delegation register
        MIDELEG = 0x303          #Machine interrupt delegation register
        MIE = 0x304              #Machine interrupt-enable register
        MTVEC = 0x305            #Machine trap-handler base address
        MCOUNTEREN = 0x306       #Machine counter enable
        MSCRATCH = 0x340         #Scratch register for machine trap handlers
        MEPC = 0x341             #Machine exception program counter
        MCAUSE = 0x342           #Machine trap cause
        MTVAL = 0x343            #Machine bad address or instruction
        MIP = 0x344              #Machine interrupt pending
        PMPCFG0 = 0x3A0          #Physical memory protection configuration
        PMPCFG1 = 0x3A1          #Physical memory protection configuration, RV32 only
        PMPCFG2 = 0x3A2          #Physical memory protection configuration
        PMPCFG3 = 0x3A3          #Physical memory protection configuration, RV32 only
        PMPADDR0 = 0x3B0         #Physical memory protection address register
        PMPADDR1 = 0x3B1         #Physical memory protection address register
        PMPADDR2 = 0x3B2         #Physical memory protection address register
        PMPADDR3 = 0x3B3         #Physical memory protection address register
        PMPADDR4 = 0x3B4         #Physical memory protection address register
        PMPADDR5 = 0x3B5         #Physical memory protection address register
        PMPADDR6 = 0x3B6         #Physical memory protection address register
        PMPADDR7 = 0x3B7         #Physical memory protection address register
        PMPADDR8 = 0x3B8         #Physical memory protection address register
        PMPADDR9 = 0x3B9         #Physical memory protection address register
        PMPADDR10 = 0x3BA        #Physical memory protection address register
        PMPADDR11 = 0x3BB        #Physical memory protection address register
        PMPADDR12 = 0x3BC        #Physical memory protection address register
        PMPADDR13 = 0x3BD        #Physical memory protection address register
        PMPADDR14 = 0x3BE        #Physical memory protection address register
        PMPADDR15 = 0x3BF        #Physical memory protection address register
        MCYCLE = 0xB00           #Machine cycle counter
        MINSTRET = 0xB02         #Machine instructions-retired counter
        MHPMCOUNTER3 = 0xB03     #Machine performance-monitoring counter
        MHPMCOUNTER4 = 0xB04     #Machine performance-monitoring counter
        MHPMCOUNTER5 = 0xB05     #Machine performance-monitoring counter
        MHPMCOUNTER6 = 0xB06     #Machine performance-monitoring counter
        MHPMCOUNTER7 = 0xB07     #Machine performance-monitoring counter
        MHPMCOUNTER8 = 0xB08     #Machine performance-monitoring counter
        MHPMCOUNTER9 = 0xB09     #Machine performance-monitoring counter
        MHPMCOUNTER10 = 0xB0A    #Machine performance-monitoring counter
        MHPMCOUNTER11 = 0xB0B    #Machine performance-monitoring counter
        MHPMCOUNTER12 = 0xB0C    #Machine performance-monitoring counter
        MHPMCOUNTER13 = 0xB0D    #Machine performance-monitoring counter
        MHPMCOUNTER14 = 0xB0E    #Machine performance-monitoring counter
        MHPMCOUNTER15 = 0xB0F    #Machine performance-monitoring counter
        MHPMCOUNTER16 = 0xB10    #Machine performance-monitoring counter
        MHPMCOUNTER17 = 0xB11    #Machine performance-monitoring counter
        MHPMCOUNTER18 = 0xB12    #Machine performance-monitoring counter
        MHPMCOUNTER19 = 0xB13    #Machine performance-monitoring counter
        MHPMCOUNTER20 = 0xB14    #Machine performance-monitoring counter
        MHPMCOUNTER21 = 0xB15    #Machine performance-monitoring counter
        MHPMCOUNTER22 = 0xB16    #Machine performance-monitoring counter
        MHPMCOUNTER23 = 0xB17    #Machine performance-monitoring counter
        MHPMCOUNTER24 = 0xB18    #Machine performance-monitoring counter
        MHPMCOUNTER25 = 0xB19    #Machine performance-monitoring counter
        MHPMCOUNTER26 = 0xB1A    #Machine performance-monitoring counter
        MHPMCOUNTER27 = 0xB1B    #Machine performance-monitoring counter
        MHPMCOUNTER28 = 0xB1C    #Machine performance-monitoring counter
        MHPMCOUNTER29 = 0xB1D    #Machine performance-monitoring counter
        MHPMCOUNTER30 = 0xB1E    #Machine performance-monitoring counter
        MHPMCOUNTER31 = 0xB1F    #Machine performance-monitoring counter
        MCYCLEH = 0xB80          #Upper 32 bits of MCYCLE, RV32I only
        MINSTRETH = 0xB82        #Upper 32 bits of MINSTRET, RV32I only
        MHPMCOUNTER3H = 0xB83    #Upper 32 bits of HPMCOUNTER3, RV32I only
        MHPMCOUNTER4H = 0xB84    #Upper 32 bits of HPMCOUNTER4, RV32I only
        MHPMCOUNTER5H = 0xB85    #Upper 32 bits of HPMCOUNTER5, RV32I only
        MHPMCOUNTER6H = 0xB86    #Upper 32 bits of HPMCOUNTER6, RV32I only
        MHPMCOUNTER7H = 0xB87    #Upper 32 bits of HPMCOUNTER7, RV32I only
        MHPMCOUNTER8H = 0xB88    #Upper 32 bits of HPMCOUNTER8, RV32I only
        MHPMCOUNTER9H = 0xB89    #Upper 32 bits of HPMCOUNTER9, RV32I only
        MHPMCOUNTER10H = 0xB8A   #Upper 32 bits of HPMCOUNTER10, RV32I only
        MHPMCOUNTER11H = 0xB8B   #Upper 32 bits of HPMCOUNTER11, RV32I only
        MHPMCOUNTER12H = 0xB8C   #Upper 32 bits of HPMCOUNTER12, RV32I only
        MHPMCOUNTER13H = 0xB8D   #Upper 32 bits of HPMCOUNTER13, RV32I only
        MHPMCOUNTER14H = 0xB8E   #Upper 32 bits of HPMCOUNTER14, RV32I only
        MHPMCOUNTER15H = 0xB8F   #Upper 32 bits of HPMCOUNTER15, RV32I only
        MHPMCOUNTER16H = 0xB90   #Upper 32 bits of HPMCOUNTER16, RV32I only
        MHPMCOUNTER17H = 0xB91   #Upper 32 bits of HPMCOUNTER17, RV32I only
        MHPMCOUNTER18H = 0xB92   #Upper 32 bits of HPMCOUNTER18, RV32I only
        MHPMCOUNTER19H = 0xB93   #Upper 32 bits of HPMCOUNTER19, RV32I only
        MHPMCOUNTER20H = 0xB94   #Upper 32 bits of HPMCOUNTER20, RV32I only
        MHPMCOUNTER21H = 0xB95   #Upper 32 bits of HPMCOUNTER21, RV32I only
        MHPMCOUNTER22H = 0xB96   #Upper 32 bits of HPMCOUNTER22, RV32I only
        MHPMCOUNTER23H = 0xB97   #Upper 32 bits of HPMCOUNTER23, RV32I only
        MHPMCOUNTER24H = 0xB98   #Upper 32 bits of HPMCOUNTER24, RV32I only
        MHPMCOUNTER25H = 0xB99   #Upper 32 bits of HPMCOUNTER25, RV32I only
        MHPMCOUNTER26H = 0xB9A   #Upper 32 bits of HPMCOUNTER26, RV32I only
        MHPMCOUNTER27H = 0xB9B   #Upper 32 bits of HPMCOUNTER27, RV32I only
        MHPMCOUNTER28H = 0xB9C   #Upper 32 bits of HPMCOUNTER28, RV32I only
        MHPMCOUNTER29H = 0xB9D   #Upper 32 bits of HPMCOUNTER29, RV32I only
        MHPMCOUNTER30H = 0xB9E   #Upper 32 bits of HPMCOUNTER30, RV32I only
        MHPMCOUNTER31H = 0xB9F   #Upper 32 bits of HPMCOUNTER31, RV32I only
        MCOUNTINHIBIT = 0x320    #Machine counter-inhibit register
        MHPMEVENT3 = 0x323       #Machine performance-monitoring event selector
        MHPMEVENT4 = 0x324       #Machine performance-monitoring event selector
        MHPMEVENT5 = 0x325       #Machine performance-monitoring event selector
        MHPMEVENT6 = 0x326       #Machine performance-monitoring event selector
        MHPMEVENT7 = 0x327       #Machine performance-monitoring event selector
        MHPMEVENT8 = 0x328       #Machine performance-monitoring event selector
        MHPMEVENT9 = 0x329       #Machine performance-monitoring event selector
        MHPMEVENT10 = 0x32A      #Machine performance-monitoring event selector
        MHPMEVENT11 = 0x32B      #Machine performance-monitoring event selector
        MHPMEVENT12 = 0x32C      #Machine performance-monitoring event selector
        MHPMEVENT13 = 0x32D      #Machine performance-monitoring event selector
        MHPMEVENT14 = 0x32E      #Machine performance-monitoring event selector
        MHPMEVENT15 = 0x32F      #Machine performance-monitoring event selector
        MHPMEVENT16 = 0x330      #Machine performance-monitoring event selector
        MHPMEVENT17 = 0x331      #Machine performance-monitoring event selector
        MHPMEVENT18 = 0x332      #Machine performance-monitoring event selector
        MHPMEVENT19 = 0x333      #Machine performance-monitoring event selector
        MHPMEVENT20 = 0x334      #Machine performance-monitoring event selector
        MHPMEVENT21 = 0x335      #Machine performance-monitoring event selector
        MHPMEVENT22 = 0x336      #Machine performance-monitoring event selector
        MHPMEVENT23 = 0x337      #Machine performance-monitoring event selector
        MHPMEVENT24 = 0x338      #Machine performance-monitoring event selector
        MHPMEVENT25 = 0x339      #Machine performance-monitoring event selector
        MHPMEVENT26 = 0x33A      #Machine performance-monitoring event selector
        MHPMEVENT27 = 0x33B      #Machine performance-monitoring event selector
        MHPMEVENT28 = 0x33C      #Machine performance-monitoring event selector
        MHPMEVENT29 = 0x33D      #Machine performance-monitoring event selector
        MHPMEVENT30 = 0x33E      #Machine performance-monitoring event selector
        MHPMEVENT31 = 0x33F      #Machine performance-monitoring event selector
        TSELECT = 0x7A0          #Debug/Trace trigger register select
        TDATA1 = 0x7A1           #First Debug/Trace trigger data register
        TDATA2 = 0x7A2           #Second Debug/Trace trigger data register
        TDATA3 = 0x7A3           #Third Debug/Trace trigger data register
        DCSR = 0x7B0             #Debug control and status register
        DPC = 0x7B1              #Debug PC
        DSCRATCH0 = 0x7B2        #Debug scratch register
        DSCRATCH1 = 0x7B3        #Debug scratch register (last one)
        VSTART = 0x008           #Vector start position
        VXSTAT = 0x009           #Fixed point saturate flag
        VXRM = 0x00A             #Fixed point rounding mode
        VL = 0xC20               #Vector length
        VTYPE = 0xC21            #Vector data type register
        VLENB = 0xC22            #VLEN/8 (vector register length in bytes)


    class privileged_reg_fld_t(Enum):
        RSVD = auto()           #Reserved field
        MXL = auto()            #mis.mxl
        EXTENSION = auto()      #mis.extension
        MODE = auto()           #satp.mode
        ASID = auto()           #satp.asid
        PPN = auto()            #satp.ppn



    class privileged_level_t(Enum):
        M_LEVEL = 0b11          #Machine mode
        S_LEVEL = 0b01          #Supervisor mode
        U_LEVEL = 0b00          #User mode


    class reg_field_access_t(Enum):
        WPRI = auto()          #Reserved Writes Preserve Values, Reads Ignore Value
        WLRL = auto()          #Write/Read Only Legal Values
        WARL = auto()          #Write Any Values, Reads Legal Values


    #Pseudo instructions
    class riscv_pseudo_instr_name_t(Enum):
        LI = 0
        LA = auto()

    # Data pattern of the memory model
    class data_pattern_t(Enum):
        RAND_DATA = 0
        ALL_ZERO = auto()
        INCR_VAL = auto()

    class pte_permission_t(Enum):
        NEXT_LEVEL_PAGE = 0b000    #Pointer to next level of page table.
        READ_ONLY_PAGE = 0b001     #Read-only page.
        READ_WRITE_PAGE = 0b011    #Read-write page.
        EXECUTE_ONLY_PAGE = 0b100  #Execute-only page.
        READ_EXECUTE_PAGE = 0b101  #Read-execute page.
        R_W_EXECUTE_PAGE = 0b111   #Read-write-execute page


    class interrupt_cause_t(Enum):
        U_SOFTWARE_INTR = 0x0
        S_SOFTWARE_INTR = 0x1
        M_SOFTWARE_INTR = 0x3
        U_TIMER_INTR = 0x4
        S_TIMER_INTR = 0x5
        M_TIMER_INTR = 0x7
        U_EXTERNAL_INTR = 0x8
        S_EXTERNAL_INTR = 0x9
        M_EXTERNAL_INTR = 0xB



    class exception_cause_t(Enum):
        INSTRUCTION_ADDRESS_MISALIGNED = 0x0
        INSTRUCTION_ACCESS_FAULT = 0x1
        ILLEGAL_INSTRUCTION = 0x2
        BREAKPOINT = 0x3
        LOAD_ADDRESS_MISALIGNED = 0x4
        LOAD_ACCESS_FAULT = 0x5
        STORE_AMO_ADDRESS_MISALIGNED = 0x6
        STORE_AMO_ACCESS_FAULT = 0x7
        ECALL_UMODE = 0x8
        ECALL_SMODE = 0x9
        ECALL_MMODE = 0xB
        INSTRUCTION_PAGE_FAULT = 0xC
        LOAD_PAGE_FAULT = 0xD
        STORE_AMO_PAGE_FAULT = 0xF



    class misa_ext_t(Enum):
        MISA_EXT_A = 0
        MISA_EXT_B = auto()
        MISA_EXT_C = auto()
        MISA_EXT_D = auto()
        MISA_EXT_E = auto()
        MISA_EXT_F = auto()
        MISA_EXT_G = auto()
        MISA_EXT_H = auto()
        MISA_EXT_I = auto()
        MISA_EXT_J = auto()
        MISA_EXT_K = auto()
        MISA_EXT_L = auto()
        MISA_EXT_M = auto()
        MISA_EXT_N = auto()
        MISA_EXT_O = auto()
        MISA_EXT_P = auto()
        MISA_EXT_Q = auto()
        MISA_EXT_R = auto()
        MISA_EXT_S = auto()
        MISA_EXT_T = auto()
        MISA_EXT_U = auto()
        MISA_EXT_V = auto()
        MISA_EXT_W = auto()
        MISA_EXT_X = auto()
        MISA_EXT_Y = auto()
        MISA_EXT_Z = auto()


    class hazard_e(Enum):
        NO_HAZARD = auto()
        RAW_HAZARD = auto()
        WAR_HAZARD = auto()
        WAW_HAZARD = auto()

    import riscv_core_setting
    #import riscv_core_setting

    # PMP address matching mode
    class pmp_addr_mode_t(Enum):
        OFF = 0b00
        TOR = 0b01
        NA4 = 0b10
        NAPOT = 0b11

    #PMP configuration register layout
    #This configuration struct includes the pmp address for simplicity
    #TODO (udinator) allow a full 34 bit address for rv32?


     ######################################### to do #########################################

    #`ifdef _VCP // GRK958
    if _VCP:
        pmp_cfg_reg_t = struct.pack('????????', 1, zero,a, x, w, r, addr, offset)
        #RV32: the pmpaddr is the top 32 bits of a 34 bit PMP address
        #RV64: the pmpaddr is the top 54 bits of a 56 bit PMP address
        #The offset from the address of <main> - automatically populated by the PMP generation routine.
    else:
        pmp_cfg_reg_t = struct.pack('????????', 1, zero, a, x, w, r, addr, offset)



    def hart_prefix(self,hart = 0):
        if NUM_HARTS <= 1:
            return ""
        else:
            return print("hart")



    def get_label(self, label,hart = 0 ):
        return {hart_prefix(hart), label}   # to do

    vtype_t = struct.pack('?????', ill, reserved, vediv, vsew, vlmul)

    class vxrm_t(Enum):
        RoundToNearestUp = auto()
        RoundToNearestEven = auto()
        RoundDown = auto()
        RoundToOdd = auto()

    class b_ext_group_t(Enum):
        ZBB = auto()
        ZBS = auto()
        ZBP = auto()
        ZBE = auto()
        ZBF = auto()
        ZBC = auto()
        ZBR = auto()
        ZBM = auto()
        ZBT = auto()
        ZB_TMP = auto()
        #for uncategorized instructions

    #`VECTOR_INCLUDE("riscv_instr_pkg_inc_variables.sv")

    #typedef bit [15:0] program_id_t;    #to do........

    # xSTATUS bit mask
    #parameter bit[XLEN - 1: 0] MPRV_BIT_MASK = 'h1 << 17;
    #parameter bit [XLEN - 1 : 0] SUM_BIT_MASK  = 'h1 << 18;
    #parameter bit [XLEN - 1 : 0] MPP_BIT_MASK  = 'h3 << 11;


    #parameter int IMM25_WIDTH = 25;
    #parameter int IMM12_WIDTH = 12;
    #parameter int INSTR_WIDTH = 32;
    #parameter int DATA_WIDTH  = 32;

    #Parameters for output assembly program formatting
    #parameter int MAX_INSTR_STR_LEN = 11;
    #parameter int LABEL_STR_LEN     = 18;

    #Parameter for program generation
    #parameter int MAX_CALLSTACK_DEPTH = 20;
    #parameter int MAX_SUB_PROGRAM_CNT = 20;
    #parameter int MAX_CALL_PER_FUNC   = 5;

    #string indent = {LABEL_STR_LEN{" "}};




    #Format the string to a fixed length

    def format_string(self, str, len=10):
        formatted_str= auto()
        formatted_str = (len(" "))
        if (len < str.len()):
            return str
        formatted_str = {str, formatted_str.substr(0, len - str.len() - 1)}
        return formatted_str


    #Print the data in the following format 0xabcd, 0x1234, 0x3334 ...

    def format_data(self, data, byte_per_group = 4):
        str = auto()
        cnt =auto()
        str = "0x"
        for i in data[i]:
            if ((i % byte_per_group == 0) and (i != data.size() - 1) and (i != 0)):
                str = {str, ", 0x"}

            str = {str, print("%2x", data[i])}
        return str


    #Get the instr name enum from a string
    def get_instr_name(self, str):
        instr = riscv_instr_name_t()
        instr = instr.first
        while(1):
            if (str.toupper() == instr.name()):
                return instr
            if (instr == instr.last)
                return INVALID_INSTR
            instr = instr.next                   #to do...


    #Push general purpose register to stack, this is needed before trap handling
    def push_gpr_to_kernel_stack(self, status, scratch, mprv, sp, tp, ref string instr[$])):
		status = privileged_reg_t()
		scratch = privileged_reg_t()
		sp = riscv_reg_t()
		tp = riscv_reg_t()                #ref string instr[$]))  #to do

		store_instr = (XLEN == 32) ? "sw" : "sd"

                if (scratch inside {implemented_csr}):    #coverage part....
		#Use kernal stack for handling exceptions
		#Save the user mode stack pointer to the scratch register
		    instr.push_back(print("csrrw ", sp, scratch, sp))
		    #Move TP to SP
		    instr.push_back(print("add ", sp, tp))	
		        # If MPRV is set and MPP is S/U mode, it means the address translation and memory protection
                        # for load/store instruction is the same as the mode indicated by MPP. In this case, we
                        # need to use the virtual address to access the kernel stack.
		
		if((status == MSTATUS) and (SATP_MODE != BARE)):
		    #We temporarily use tp to check mstatus to avoid changing other GPR. The value of sp has
		    #been saved to xScratch and can be restored later.
		    if(mprv):
			instr.push_back(print("csrr // MSTATUS", tp, status))
                        instr.push_back(print("srli ", tp, tp))                # Move MPP to bit 0
                        instr.push_back(print("andi ", tp, tp))                # keep the MPP bits
                        #Check if MPP equals to M-mode('b11)
                        instr.push_back(print("xori ", tp, tp))
                        instr.push_back(print("bnez ", tp))                    #Use physical address for kernel SP
                        #Use virtual address for stack pointer
                        instr.push_back(print("slli ", sp, sp, XLEN - MAX_USED_VADDR_BITS))
                        instr.push_back($sformatf("srli ", sp, sp, XLEN - MAX_USED_VADDR_BITS))

		#Reserve space from kernel stack to save all 32 GPR except for x0
		instr.push_back(print("1: addi x%0d, x%0d, -%0d", sp, sp, 31 * (XLEN/8)))
		#Push all GPRs to kernel stack
		for i in range(0,32):
			instr.push_back(print(" the store_instr, sp", store_instr, i, i * (XLEN/8), sp))
		#Pop general purpose register from stack, this is needed before returning to user program

    def pop_gpr_from_kernel_stack(self,status, scratch, mprv, sp, tp, ref string instr[$])):
		status = privileged_reg_t()
		scratch = privileged_reg_t()
		sp = riscv_reg_t()
		tp = riscv_reg_t()                #ref string instr[$]))  #to do

		load_instr = (XLEN == 32) ? "lw" : "ld"
		#Pop user mode GPRs from kernel stack
		
		for i in range(0,32):
			instr.push_back(print("the store_instr, sp", load_instr, i, i * (XLEN/8), sp))
		#Restore kernel stack pointer
		instr.push_back(print("addi x%0d, x%0d, %0d", sp, sp, 31 * (XLEN/8)))
		if (scratch inside {implemented_csr}) :    # to do................
			#Move SP to TP
			instr.push_back(print("add ", tp, sp))
			#Restore user mode stack pointer
			instr.push_back(print("csrrw ", sp, scratch, sp))
    
    #Get an integer argument from comand line
    def get_int_arg_value(self,cmdline_str,val):
		s = auto()
		if(inst.get_arg_value(cmdline_str, s)):
			val = s.atoi()

    #Get a hex argument from command line
    def get_hex_arg_value(self, cmdline_str, val):
		s = auto()
		if(inst.get_arg_value(cmdline_str, s)):
			val = s.atohex()

    class cmdline_enum_processor #(parameter type T = riscv_instr_group_t)        #to do............
		def get_array_values(self, cmdline_strcmdline_str, ref T vals[])  #ref T vals[] to do .....
			s = auto()
			#void'(inst.get_arg_value(cmdline_str, s))      #to do type casting.............
			if(s != " "):
				cmdline_list[$]   #to do....
				T value
				#uvm_split_string(s, ",", cmdline_list);
				vals = new[cmdline_list.size]
				for i in range(0,):
					if (uvm_enum_wrapper#(T)::from_name(cmdline_list[i].toupper(), value)):  #to do....
						vals[i] = value
					else:
						print( "Invalid value (%0s) specified in command line: %0s", cmdline_list[i], cmdline_str))  #uvm_fatal

    
    riscv_reg_t   all_gpr[]   = {ZERO, RA, SP, GP, TP, T0, T1, T2, S0, S1, A0,   #to do..........
                             A1, A2, A3, A4, A5, A6, A7, S2, S3, S4, S5, S6,
                             S7, S8, S9, S10, S11, T3, T4, T5, T6};
    
    


    riscv_reg_t compressed_gpr[] = {S0, S1, A0, A1, A2, A3, A4, A5};    #to do .........



   riscv_instr_category_t all_categories[] = {                                  #to do...........
    LOAD, STORE, SHIFT, ARITHMETIC, LOGICAL, COMPARE, BRANCH, JUMP,
    SYNCH, SYSTEM, COUNTER, CSR, CHANGELEVEL, TRAP, INTERRUPT, AMO
    };




    def get_val(self, str, val, hex=0):
	if (str.len() > 2):
		if (str.substr(0, 1) == "0x"):
			str = str.substr(2, str.len() -1)
			val = str.atohex()
			return
	if (hex):
		val = str.atohex()
	else:
		if (str.substr(0, 0) == "-"):
			str = str.substr(1, str.len() - 1)
			val = -str.atoi()

		else:
			val = str.atoi()

	print("riscv_instr_pkg imm:", str, val)   # to do $signed(val)


import riscv_vector_cfg
import riscv_pmp_cfg
typedef class riscv_instr
typedef class riscv_b_instr
import riscv_instr_gen_config
import isa/riscv_instr
import isa/riscv_amo_instr
import isa/riscv_b_instr
import isa/riscv_floating_point_instr
import isa/riscv_vector_instr
import isa/riscv_compressed_instr
import isa/rv32a_instr
import isa/rv32c_instr
import isa/rv32dc_instr
import isa/rv32d_instr
import isa/rv32fc_instr
import isa/rv32f_instr
import isa/rv32i_instr
import isa/rv32b_instr
import isa/rv32m_instr
import isa/rv64a_instr
import isa/rv64b_instr
import isa/rv64c_instr
import isa/rv64d_instr
import isa/rv64f_instr
import isa/rv64i_instr
import isa/rv64m_instr
import isa/rv128c_instr
import isa/rv32v_instr
import isa/custom/riscv_custom_instr
import isa/custom/rv32x_instr
import isa/custom/rv64x_instr

import riscv_pseudo_instr
import riscv_illegal_instr
import riscv_reg
import riscv_privil_reg
import riscv_page_table_entry
import riscv_page_table_exception_cfg
import riscv_page_table
import riscv_page_table_list
import riscv_privileged_common_seq
import riscv_callstack_gen
import riscv_data_page_gen

import riscv_instr_stream
import riscv_loop_instr
import riscv_directed_instr_lib
import riscv_load_store_instr_lib
import riscv_amo_instr_lib

import riscv_instr_sequence
import riscv_asm_program_gen
import riscv_debug_rom_gen
import riscv_instr_cover_group
import user_extension
     












































		
		    
		


                               



































