.include "user_define.h"
.globl _start
.section .text
_start:           
                  .include "user_init.s"
                  csrr x5, 0xf14
                  li x6, 0
                  beq x5, x6, 0f

0: la x2, h0_start
jalr x0, x2, 0
h0_start:
                  li x14, 0x40001104
                  csrw 0x301, x14
kernel_sp:        
                  la x30, kernel_stack_end

trap_vec_init:    
                  la x14, mtvec_handler
                  ori x14, x14, 1
                  csrw 0x305, x14 # MTVEC

mepc_setup:       
                  la x14, init
                  csrw 0x341, x14

init_machine_mode:
                  li x14, 0x1e00
                  csrw 0x300, x14 # MSTATUS
                  li x14, 0x0
                  csrw 0x304, x14 # MIE
                  mret
init:             
                  li x0, 0xf0000000
                  li x1, 0x80000001
                  li x2, 0x0
                  li x3, 0x8
                  li x4, 0xf0000000
                  li x5, 0x80000001
                  li x7, 0x0
                  li x8, 0x8
                  li x9, 0x0
                  li x10, 0xf0000000
                  li x11, 0x80000001
                  li x12, 0x80000000
                  li x13, 0xf0000000
                  li x14, 0x8
                  li x15, 0x8
                  li x16, 0x80000000
                  li x17, 0x80000000
                  li x18, 0x80000001
                  li x19, 0x80000001
                  li x20, 0x0
                  li x21, 0x8
                  li x22, 0x0
                  li x23, 0xf0000000
                  li x24, 0x8
                  li x25, 0x0
                  li x26, 0x8
                  li x27, 0x0
                  li x28, 0x8
                  li x29, 0x80000000
                  li x31, 0x0
                  la x6, user_stack_end
main:             la         zero, region_1+0 #start riscv_load_store_rand_instr_stream_0
                  sb          t3, -3 (zero)
                  lhu         zero, 117 (sp)
                  c.xor       s0, a2
                  sh          a6, 76 (sp)
                  sb          t3, -189 (zero)
                  lbu         t4, -53 (sp)
                  lhu         zero, 187 (sp)
                  c.li        gp, 0
                  lbu         t4, 129 (sp)
                  sb          t3, -195 (zero)
                  sltiu       gp, s4, 608
                  lbu         t4, 33 (sp)
                  and         ra, s8, a6
                  sltu        t6, s4, s4
                  lhu         zero, 30 (sp)
                  lw          s11, -204 (sp)
                  lhu         zero, -186 (sp)
                  lui         gp, 875531
                  lhu         zero, 46 (sp)
                  andi        gp, t6, 730
                  lbu         t4, 39 (sp)
                  sh          a6, -10 (sp)
                  sb          t3, 5 (zero)
                  lhu         zero, 105 (sp)
                  lhu         zero, 90 (sp)
                  lbu         t4, 3 (sp)
                  lbu         t4, -85 (sp)
                  lb          ra, 157 (zero)
                  lh          a3, -171 (sp)
                  lh          a3, 124 (sp)
                  sw          t6, 60 (zero)
                  sw          t6, 170 (zero)
                  lw          s11, 26 (sp)
                  sra         ra, zero, s11
                  lw          s11, -191 (sp)
                  slli        gp, s4, 4
                  c.li        a0, 0
                  sub         s2, zero, s8
                  lh          a3, 227 (sp)
                  lw          s11, 47 (sp) #end riscv_load_store_rand_instr_stream_0
                  c.and       s0, s0
                  c.bnez      s0, 8f
                  la         sp, region_0+1011 #start riscv_load_store_hazard_instr_stream_0
                  lh          a3, 12 (sp)
                  lbu         t4, 12 (sp)
                  lhu         zero, 12 (sp)
                  c.or        s0, s0
                  lh          a3, 12 (sp)
                  sh          a6, 12 (sp)
                  auipc       t0, 913226
                  sll         zero, zero, a6
                  lh          a3, 12 (sp)
                  lh          a3, 12 (sp)
                  rem         zero, s8, s5
                  c.lwsp      gp, 12(sp)
                  lh          a3, 12 (sp)
                  lw          s11, 12 (sp) #end riscv_load_store_hazard_instr_stream_0
                  c.sub       s0, s0
                  bne         a5, tp, 9f
                  xor         zero, s10, t5
                  c.and       s0, s0
                  bge         s2, tp, 9f
                  c.sub       s0, a2
8:                sltiu       zero, s10, 520
9:                slti        gp, tp, 293
                  la x2, test_done
                  jalr x0, x2, 0
test_done:        
                  li gp, 1
                  ecall
write_tohost:     
                  sw gp, tohost, t5

_exit:            
                  j write_tohost

instr_end:        
                  nop

.section .data
.align 6; .global tohost; tohost: .dword 0;
.align 6; .global fromhost; fromhost: .dword 0;
.section .region_0,"aw",@progbits;
region_0:
.word 0xca11ca8d, 0x5b371345, 0x5b92c7dc, 0x54a522bc, 0x1880c690, 0xa37bf86b, 0x779b1ff1, 0xa9ccd80a
.word 0x0c61a38a, 0x34d7b2d0, 0x334caa12, 0x0300b0d9, 0x0264adb9, 0x0b3239df, 0xfaecd8f0, 0xeb4251f2
.word 0x81ec485d, 0x77f3b15e, 0x58e6b9e5, 0x41966f8a, 0x3715a627, 0x2e45e8fa, 0x5d1b5eac, 0x3edd9028
.word 0x0c7c1f1d, 0xa8414baa, 0x082e2dfe, 0x132dadbc, 0xae084308, 0x324f7573, 0x4c29b42f, 0x1383c24c
.word 0x4ae2b54d, 0x1b5e6e89, 0xbd4d3b7a, 0x4a1129e9, 0xd58fecf6, 0xbbd96963, 0x707d994d, 0x994cb489
.word 0x63b23eb0, 0x67d51a48, 0xdc1c6861, 0x3290f0f2, 0xe1683ee1, 0x85f6873f, 0xa2e05a71, 0xa87bcc25
.word 0xf4294e94, 0x09d0b2af, 0x8f13c441, 0x721d56ea, 0x47df145f, 0x3efbdb43, 0x8172d0b0, 0xbc539b31
.word 0xc9de956a, 0xefa26182, 0x87271c2b, 0x97ecc1e3, 0x75f787a4, 0x4a78a1e7, 0xce2dd375, 0x69d9cbca
.word 0x9a208a60, 0xafab18b0, 0x17454691, 0x480bde83, 0x88005c03, 0x0fa131a1, 0x5fb49b31, 0x4e242cd8
.word 0xb38bb0c9, 0x37ebeaac, 0x83e7075f, 0x417c567e, 0x2015b48e, 0x737a6832, 0x086ca51e, 0xbea3713f
.word 0x580ffe3e, 0x14c89146, 0xeba97804, 0x69b2c456, 0x2e8a8944, 0xa46ee8d8, 0xf12670e4, 0x7e6d8514
.word 0x549a590d, 0xb42e3717, 0xac991780, 0x25a4098a, 0x4fcd01d1, 0xf2ea01a1, 0xcc618a9c, 0x54df086e
.word 0x2199ba71, 0xb8cb319e, 0xa6523371, 0x22caf269, 0x1e4fdcec, 0xd5144650, 0xe81d0a8e, 0x5e96cdae
.word 0x7e069ae6, 0x3c1dd1bf, 0x414475d4, 0xfcd58894, 0x5d9a1f5d, 0x95ca7607, 0x32cf741f, 0x4e1a5c63
.word 0x729a0bbf, 0x83d792d5, 0x692af933, 0xdfbd3df6, 0xb5f0de97, 0x06ef4530, 0xac268814, 0x210274c6
.word 0x0683f67d, 0xe0cb1415, 0x1afd4980, 0x2ffaf595, 0xb1bec650, 0x59c7ca77, 0xfdb0f5fc, 0xf1572ce2
.word 0xaab40084, 0xe5b101e9, 0xeb70f742, 0xd51e0888, 0x8e57c6d4, 0x93d61239, 0xe1fe3956, 0xf256320b
.word 0x345b0905, 0x3da102f9, 0x9c37bcd3, 0x793a95ed, 0xcd0bb124, 0xe7bdb825, 0xc177e09f, 0x4b5852bb
.word 0xb6cc1f1d, 0xe11300ac, 0xc3b4711a, 0x639edc76, 0x635d8986, 0xfbfae1a2, 0xa0d03860, 0xb0461350
.word 0x1720adba, 0x21fee66e, 0x65d91444, 0x0a1f807a, 0x20f56faa, 0x41e44b0b, 0x363ed75a, 0x282ab623
.word 0x40ec16dc, 0xcfd365c9, 0xd5d9ae83, 0x45552357, 0xd1961ce9, 0x849327a2, 0x072c8925, 0xd5fc2ec4
.word 0x21d6ac74, 0xc83e4e66, 0xb9a860a8, 0xfced817c, 0xd64fca13, 0x2c5f1f30, 0x0650aac1, 0x476b1ee6
.word 0x9cc44857, 0x892e13a5, 0xc5ebc259, 0xa86460e0, 0x7eaa79c5, 0xd00e1097, 0x2576c036, 0x9d7b6861
.word 0x73479d03, 0x71f393df, 0xbb93026d, 0x60f47d32, 0x1e558a43, 0x75dd2676, 0x677d702b, 0xa547fe09
.word 0x38a13c51, 0xa6b80e86, 0x97e3f431, 0x50bd7d40, 0x5b81956d, 0x2fb0b5df, 0x450e0ec4, 0x6267987f
.word 0x2ddc388e, 0xb00fa5fc, 0xf09dd862, 0xa6afe7f9, 0x25769604, 0xdf874bc6, 0xbb4c8daf, 0x99b37d85
.word 0xbe7c748b, 0xc77e6189, 0xa059007c, 0xa4c0eb10, 0xd77debe8, 0xb906471e, 0x16178598, 0x68776945
.word 0x858b1ed0, 0x5e4aef58, 0xdac3f98c, 0x8a07b0f0, 0xf4cafd97, 0x356b33ef, 0xa97291f4, 0x62e7f19f
.word 0x51c552f8, 0x55b098ee, 0x69db45ee, 0x022b2b67, 0x957459c6, 0xd724bc9f, 0xd0173bfa, 0x420e8c3a
.word 0x86bf9c28, 0xb70bd1b6, 0x23b05f13, 0xece56a09, 0xb427bf53, 0xb17e38ae, 0x2f82b17f, 0x66e9226e
.word 0xdaaebe43, 0x1cb5ce64, 0xd387eaf4, 0x9a2c2c39, 0x4c09ab15, 0xa2d49ea0, 0xf5724953, 0xce72d167
.word 0x6c8d5c57, 0x7b446893, 0xeec94940, 0x368706e6, 0x8b382c4d, 0x8988ccf1, 0x82ea2216, 0x0e26096b
.word 0x0a096850, 0xb5a8bc6c, 0x45fdb2b9, 0x1b55643c, 0x01bb8cb1, 0x23ae8824, 0xbb2c1048, 0xd77ecebf
.word 0xf3b96cc9, 0x973f59c0, 0x969392a8, 0x8ff426df, 0xaa9ca096, 0xeb7e4c2c, 0x77799d18, 0x764dcc82
.word 0x7980570f, 0xe595ce63, 0x71dce775, 0x5f197656, 0x661b05f4, 0xef7a7028, 0x4783198b, 0x17de9c6c
.word 0x5b251fe5, 0xe0216efc, 0xbb9b8249, 0xcb19c9b5, 0xb5b78ee5, 0x9be9911e, 0x4bc98dba, 0x720d581c
.word 0xcaf794b0, 0x8e0219e5, 0x29107a88, 0x590d7c45, 0x0ebc3bc5, 0x324ed12f, 0x582d969b, 0x9d7f2583
.word 0xb417448c, 0x29c9fee9, 0xcaf9794b, 0xceebf990, 0x445056ac, 0x791b7958, 0x76a9459e, 0x949a8097
.word 0x0d9c4ae9, 0x6b7fde96, 0x85804dc3, 0x95b8acfe, 0x6263b772, 0xc9d243a5, 0xa5d1f401, 0x7f589adc
.word 0x689f476d, 0x7ff919a2, 0x6f776b2a, 0xb6784ab8, 0xef057719, 0xe6eb8c3b, 0x7b07b7d7, 0x7df6179a
.word 0x0e7ab5f0, 0xa54e4c97, 0x30df2551, 0xe085acbf, 0x9c78a99d, 0x2f28e413, 0x35a3a367, 0x63d0f6bb
.word 0x2f415cb7, 0x8c8097eb, 0x3efed815, 0x36bbbf50, 0x01a9106c, 0xed1b19ae, 0x7a1aaeb5, 0xdb66a17f
.word 0xa21e36be, 0xb7c1d27c, 0x7ae21cc3, 0xbd9aca0c, 0x81f7365e, 0x8a971b26, 0x3ec97b91, 0xb2381de5
.word 0x45093566, 0x0712c293, 0x82c7e6a6, 0x9886c7c4, 0xf80de457, 0x28779b70, 0xc6a5872e, 0x1fbe551d
.word 0x850d93fa, 0xa9f27584, 0x78e14083, 0x2ea6a56d, 0x0bdb1654, 0xb61ec202, 0x50bbaae7, 0x66a15648
.word 0x51641710, 0x632802bc, 0x1b2211f6, 0x9d2d799b, 0x190fe847, 0xe0ccf295, 0xf7573c30, 0x763895d6
.word 0xa8ebed79, 0x2e2d7a1c, 0x7f4ea84a, 0x080d9c53, 0xbb59ccbd, 0x7bf6b1b9, 0x14065ceb, 0x4eb8ca34
.word 0xa6ea228b, 0xe1fe20ed, 0x02013a30, 0xf9cf2d3e, 0x0bad3a5c, 0xc7e05a2b, 0x7909b67e, 0xb49069b9
.word 0xe414606f, 0x91b4da9e, 0x1bc9289d, 0x635f6009, 0x74074b96, 0xb1478ecb, 0x3b041a17, 0xed56fadd
.word 0x3e92e5ba, 0xb78fb52c, 0x14efd758, 0x76315258, 0xdb98b4b5, 0x2ca79255, 0x5348ef9e, 0xecac05f1
.word 0xfdd0fe73, 0xd895460e, 0x23b53535, 0x65408f69, 0x858eebdd, 0x156543e0, 0x0f8ef142, 0x3609fe49
.word 0x356f2655, 0xa54411f2, 0xa89f4fab, 0xcf2e7c57, 0xb68d03de, 0xb760135b, 0x40fc3c52, 0x105a01b7
.word 0xad77fe5d, 0xe5d07626, 0x1ee89cfd, 0x224a49a5, 0x51a0d19d, 0xebe46a3c, 0xcfcb0920, 0x813f38be
.word 0xf31bc1d6, 0x5a42ac23, 0x75c06c1a, 0xac871c36, 0x97db3585, 0x534fcf8d, 0x3ecac7cd, 0x87c9616c
.word 0x8260f819, 0xfb9c546a, 0xb631e321, 0x70ce6817, 0x1f8026f4, 0xe39e9550, 0xa628106a, 0x8d4a92b0
.word 0x6168b18a, 0xf8ee9809, 0xec111269, 0x305b9ea9, 0x63d543a7, 0xb365ca12, 0x8de19294, 0xbbfb22cb
.word 0x1ad06baa, 0x8b58d759, 0xcaa3c6ba, 0x7763242b, 0x0a231a8b, 0xa27645ef, 0x2337117d, 0xc6abd1fd
.word 0xef977d56, 0x2a38b4ce, 0x3edb6dd4, 0x9dd440c0, 0xa0390747, 0xab888a26, 0x8b9e8ea3, 0x860a0987
.word 0x04d3dedb, 0x2a333fe6, 0xd9dc53bb, 0xee413c5c, 0x64ba36f3, 0x99e878c8, 0x4a6d8b92, 0xfc8931d3
.word 0x740aee5b, 0xf1cd3013, 0x9d31bdbb, 0xfa076c13, 0x868f72bd, 0xef5d10d9, 0x14881630, 0x7ee83e71
.word 0xdb50217d, 0xe14b3287, 0x2746213c, 0x68b5c88b, 0x7961605a, 0xdad6cc82, 0xd0549d33, 0xb8b2b18a
.word 0x32811e66, 0x3633b93d, 0x624d08a3, 0x4209eda2, 0x8603eee2, 0x682722bc, 0xe137025a, 0x50a98598
.word 0x232c5785, 0x4cd2faec, 0xa3d0c829, 0xd3ccbfa1, 0xc2a14907, 0xe78b1594, 0x751b83e6, 0x347b441b
.word 0x0ad1bfab, 0x6fde241f, 0xd998f691, 0xced21f4f, 0x0e2fd2ed, 0x443c0e04, 0x106d252a, 0x1e8d0807
.word 0x1c5b7f26, 0x55422bc9, 0x8b8736e7, 0x21f63624, 0x10785d9d, 0x9780301b, 0xf3cc9c9b, 0xb3592b6a
.word 0xc198ee0e, 0x90c9e647, 0x25e23dc9, 0x0995cc49, 0xfde3f930, 0x8a9d6390, 0xa79803b0, 0x5cb62f4d
.word 0x735af24f, 0xda3f241e, 0x33b493bf, 0xf41c78b0, 0x353ea0e0, 0x11903266, 0x8380cefc, 0x7dea3f1b
.word 0x1ae8ecf0, 0x639bdd1d, 0xc2fa8f74, 0x3529baf9, 0xc4f74900, 0x8479dfd5, 0x1e5746d1, 0x4a6f792e
.word 0xa5954a76, 0xb0dd9fea, 0xa8981ac7, 0xa63711cc, 0xe695fbb0, 0x12d4fd79, 0x4586d4c2, 0x664c0373
.word 0x4c1a10bc, 0x161ab8ec, 0x0a374f02, 0x77ae3a8f, 0x807886fa, 0xd0612b63, 0xdbc7b0d4, 0x9c8669ee
.word 0x92f8dfe2, 0xc49f24b9, 0xadcb40a0, 0xb9615362, 0x50084f3b, 0x449b0a67, 0xf9dccaca, 0x1e684b3a
.word 0x1c26480a, 0x79222362, 0x9bece6e1, 0x3854fe77, 0x26f3fbd9, 0xd23c9647, 0xe0215aef, 0x208d23c7
.word 0x12e340d5, 0xe4b9c316, 0xfe37134f, 0x15a19694, 0x159a5528, 0xd4782f2b, 0x4c92133b, 0x5d5e3bdb
.word 0x9e2f2dde, 0xaea3ee84, 0x9ad0f0e2, 0x0e8a0a27, 0x3ad529f7, 0xec09b6ad, 0xa799a996, 0x70bd0b3a
.word 0x983b7a68, 0x41b9a691, 0xd3465e88, 0x847800a1, 0xfd28a54b, 0x7c43c2ee, 0x4621fd41, 0xf2fe4ce8
.word 0xefb41e14, 0xdcd65839, 0x7e74aa1e, 0xbe258e32, 0xa97f7aaf, 0x45a46c42, 0x370df90d, 0x77280707
.word 0x22b1f0b2, 0x5780848e, 0xfeada1f7, 0xfbfefd69, 0x7b0a49c1, 0xd8dcd511, 0x01a4ae27, 0x046e0773
.word 0x6acde7b3, 0xa3abc087, 0x3dc052c1, 0x99e67bab, 0xbe72e815, 0xc2fccf48, 0x5c8c60fb, 0x066223a0
.word 0x2f19589e, 0x946a6c16, 0x94dcf637, 0xf998aa9a, 0xecbd727f, 0x647e3369, 0x57ba8b32, 0x0cdaa39d
.word 0xfc8ed0af, 0x35eb1127, 0xfd560b3d, 0x75f78a31, 0x3f70e0f5, 0xb11b8e81, 0xeb98f483, 0x974e3b47
.word 0x235ae9b3, 0x40498ffe, 0xb5bdf4d9, 0xc73f551d, 0x045e9374, 0xdcae841b, 0x0daa4907, 0xbaea31cc
.word 0x9511e6c9, 0x7cb86b65, 0xe1193e87, 0xfe0bc6f9, 0x76b534f1, 0x6281db96, 0x8da33ae3, 0xc5c90a7e
.word 0xf1caac7e, 0x68fcd229, 0x7c399b58, 0x9b0f6259, 0x1d94f94c, 0x382fd56b, 0x15bb46df, 0x9b6e0ffa
.word 0x2e0fcae6, 0x31dea226, 0x58df89ee, 0xc1aa7c09, 0x45ba3b4c, 0xf1b540d1, 0x2a27ab31, 0xce7232d1
.word 0x3e3621f6, 0x1fe8a396, 0xcd985deb, 0xa3fcee76, 0x50fcfd3e, 0x5212a139, 0x6788be47, 0x3330d965
.word 0xb8ad7bcf, 0xfce29340, 0xe1e94ec0, 0x66cba6bd, 0x14e24239, 0x17829e01, 0x8e2c3fbb, 0x3d44f6d8
.word 0xd42f374d, 0x477c417a, 0x87ac8858, 0x8fb9c60b, 0xd45081c0, 0x09169b6e, 0x5667b9b9, 0xbac1860f
.word 0x4d505821, 0x2da0d385, 0x484f9234, 0x52610077, 0xe48286c2, 0x7ec296e5, 0x492ec307, 0x11a1d263
.word 0xac87c1bd, 0xa376f499, 0x4a921c71, 0x7479e753, 0x7868f233, 0xd26f9b95, 0xc61dfaf0, 0x369bc748
.word 0x4f73ee95, 0x1be795eb, 0xc6f2bf35, 0x44aa1f98, 0x3fe5fa73, 0x376d07db, 0xa504e861, 0xb338f641
.word 0xbfabb071, 0x51b04607, 0x47ab699d, 0x02267e4a, 0x90d1236d, 0x323fd9fb, 0x9a3b2986, 0x7e456293
.word 0x0e96950a, 0xc84c53d0, 0xef23f2c4, 0x5448cbe8, 0xe9059272, 0xd58a4a44, 0xf30fd956, 0x3efb7623
.word 0xa5471f7b, 0x05ce7d6c, 0x8b5422a6, 0xefda79d1, 0x00237aa0, 0xb91ecc88, 0x3d9f1758, 0xd6e72a76
.word 0x3762b0b9, 0xc3502b86, 0x44a5b83a, 0x6663d853, 0xfc33b990, 0xf7176bf8, 0x41b791f8, 0x520b4fc4
.word 0x565e4031, 0xa54e89cf, 0x82e270eb, 0x1518a4bb, 0xdc4b8a12, 0x59ebd1d4, 0x01662be2, 0x3e3818ad
.word 0x82f58c99, 0x016e6375, 0x7e121102, 0x9f76116c, 0x3e7bd764, 0x33d0775c, 0x9753ea12, 0x4b43648d
.word 0x6beee9eb, 0xc87c5d15, 0x5619d88c, 0xb769cc66, 0x4c1c6a10, 0x469418d9, 0xfcd236f0, 0x5bf13c77
.word 0x2b71e0b4, 0xf8c891f1, 0x7dce2a3e, 0x8cd22459, 0xcca6750a, 0x1ac8b961, 0x7f883ad1, 0x23af8154
.word 0x8a8b047f, 0xd30071d4, 0xe2be9846, 0x09d8515c, 0x49da68f6, 0x2eeed546, 0x45da180f, 0xfb55e138
.word 0x6dedd0ab, 0x50d29a0b, 0xa32156c3, 0x39abd0e5, 0x17e811d6, 0x7e48f528, 0xde74e748, 0xb3bbacab
.word 0xd8d4f43e, 0xb6f11d4a, 0xa7023966, 0xfcd4320a, 0x899efede, 0xbbafad13, 0xf0791a4b, 0xcca7072e
.word 0x1b1f8154, 0x1fa35c39, 0xa8d37ce1, 0x730f480b, 0x0401f665, 0x75f7df0f, 0x0b7454df, 0x883acfac
.word 0x9ebe448e, 0x3e00379c, 0xd14edd2c, 0x87ab3625, 0x17d5b200, 0x3934bff3, 0x18091cee, 0x53ddd7d4
.word 0xd370a386, 0xabf0275e, 0x686b39d1, 0x6f08d674, 0xed889095, 0x0566da50, 0xfe0125b9, 0x47c06d41
.word 0x8ac29b7f, 0xa3c1f16d, 0xe669b49f, 0xe9cca89b, 0x420f3eb9, 0xd6cd28e2, 0x9786eec4, 0x15ab2558
.word 0xd38c0952, 0xd1fe060b, 0x5344fbbc, 0x29109817, 0xb4cfa421, 0x7ebb835c, 0xe79b9311, 0x6127e934
.word 0xcfccf880, 0xaf6663be, 0xe6ebe3a0, 0x9801696d, 0xf9cbb7df, 0x871a9013, 0x3400f040, 0x41f6134a
.word 0x27e25e44, 0x8dcc2fa1, 0x63be3376, 0x9b9666b7, 0x74ea81e9, 0x08f1939c, 0x12361705, 0xa939739b
.word 0x12580e88, 0x54de3859, 0xa389f35e, 0x4b702141, 0xdef7ed44, 0x956ffed7, 0x60a7c5fe, 0xc92591b8
.word 0x3a31d78f, 0xfb9c2888, 0xd3df0a2d, 0xb948f702, 0xd3b1180a, 0x219c69ad, 0x167b06c6, 0x815f54b6
.word 0xdd089958, 0x71541fc8, 0xf5820c52, 0x41ebc3df, 0x0089ef28, 0x65f5dcbb, 0x4580ca6d, 0x33db829b
.word 0xbd50d10e, 0x7f0a4291, 0xfc8834cf, 0x468ee756, 0xfb4075ef, 0x8bb54b42, 0x2f20675d, 0x78f1f511
.word 0xeea07c4d, 0x6b0c6a33, 0xb842aa99, 0x0716df44, 0x9053005e, 0xe8586f12, 0xbb9903e0, 0x6b383583
.word 0xf6e2d426, 0xe34ec946, 0xa2f59fb3, 0x7def2ce8, 0xfcdb6b84, 0x53077a72, 0x80a511e9, 0xaa199a47
.word 0x1c9a2122, 0xeaa6614b, 0x2c1910f4, 0x5301ca98, 0x202922f1, 0x4165ebb1, 0x2ca24e65, 0xc233c172
.word 0x1bed6d50, 0x52259a90, 0x5197c288, 0x921bb5ee, 0x6eab1d93, 0x04c4a280, 0x565acce8, 0xc19d6874
.word 0x1f99c576, 0x536ec4e9, 0xce9d5e26, 0x369d5cab, 0xd61465c0, 0x00c6bc5d, 0x8bd1915a, 0xd90543a0
.word 0x0aeef883, 0x478004a4, 0x26e5935c, 0x58a46962, 0x0a53b543, 0x0403fc16, 0xb47fb62a, 0xa49bb750
.word 0xe1816f38, 0x25d34bf0, 0x08e8662d, 0x119c21e3, 0xe86be39c, 0x1a5559ce, 0x84626a90, 0xdbb391bb
.word 0x3202e8a3, 0x9a1ab20b, 0x5c5695bd, 0x4deade2d, 0x6eb53111, 0xb92d7223, 0xac8657b6, 0x502a578a
.word 0xe9b798dd, 0xf20efc57, 0xcd1427cd, 0xc1d5edbd, 0xb482b6f6, 0xba2929fc, 0x27ba849e, 0xb3fc3668
.word 0x2f1887ec, 0x8f40c51b, 0xa9c4371a, 0x770c838b, 0x79182e65, 0xebaf3577, 0x5e8d3f90, 0x07c953dd
.word 0xdf5f2a27, 0x459380f7, 0xeb7c1f60, 0x8a4374e5, 0x5494cb66, 0x7bfb29ba, 0xae392034, 0x091228a9
.word 0xe1925dbd, 0xcc8340cd, 0x13c39e94, 0x3bc77863, 0x9aceaf51, 0x88d8c2c3, 0xe219416f, 0xe79508cc
.word 0x213b33a0, 0x96651ec1, 0x662d4286, 0x03bce39f, 0x59ddb71a, 0xfb4cb4e6, 0x6ae42c27, 0x6702b3cc
.word 0xe2a14cad, 0x69f7f62f, 0xa4f21ad9, 0x1e26ad40, 0xf77014e7, 0x21689531, 0x3e3dd48a, 0x809f1254
.word 0x8c66310a, 0xba81cc80, 0x6cfecebf, 0x46b0f4cf, 0xb519df65, 0xfddd2835, 0xe32b87dd, 0xeb5cb7a1
.word 0x30bcd207, 0x5c60d0c0, 0x04b036db, 0x0a982662, 0x1383db9c, 0x0c96cc5e, 0x0023841e, 0x70a92443
.section .region_1,"aw",@progbits;
region_1:
.word 0xe8762afd, 0x0a26fc24, 0x920e7fb0, 0x8d2e0124, 0xb19ff640, 0x1947e22d, 0xef3b7495, 0x00cc73b0
.word 0x8a78d6d0, 0x027d21ea, 0x67048a44, 0x1135c426, 0x75ebe3c1, 0xe5112a51, 0xa51d787a, 0x5bfc851f
.word 0x04d18dbd, 0x261f3ef6, 0xf5e08bf2, 0x07449731, 0x5f198a62, 0xcf1af717, 0x001a9cc0, 0x0b8a55d1
.word 0x77f9617c, 0xeb568f47, 0x03311924, 0x8c70bb76, 0xd483265e, 0x595c5b42, 0xb0ab3457, 0xf6299a8d
.word 0x9ca404eb, 0x36554d6b, 0x22bf4776, 0x64ba812a, 0x02ca0f6c, 0xea9b73ee, 0xb3c49260, 0xcacbd2db
.word 0x0e4a46c2, 0x9cbada41, 0xcfd58dd5, 0x4efe002a, 0x7b23ae30, 0x566e054e, 0x8bfb6a30, 0x93f948d7
.word 0xb344b33c, 0x80891d34, 0xb0addd6e, 0x8f6c743b, 0x3b72c9c6, 0xf3978a96, 0xca08a2db, 0xce8c53aa
.word 0xfbcbfe51, 0x9fc3387d, 0xd6dad4c3, 0xb9c2b709, 0xc30a1d6a, 0xc87e5f9f, 0xe22b8a98, 0xb2d02298
.word 0xd04ff338, 0x710ee8ec, 0x694a0ef1, 0xf276ce45, 0x198ce393, 0x453d779f, 0xfc1ddada, 0x5c9917b2
.word 0x53685cde, 0x395c19fe, 0x3da0a8b4, 0x4efb7a8b, 0x4990f36d, 0xd82a4d08, 0x833e3da8, 0xa01123b5
.word 0x612486ed, 0x5d281da1, 0xa3079ab1, 0x1260fd20, 0x2a230053, 0x547f09c5, 0x9a08550b, 0xa1b4b027
.word 0x24e62524, 0x6e0388fc, 0x89c1c1c8, 0x0bde1422, 0xa4548583, 0xbf42af9e, 0xb0ee83f1, 0xbf01b90d
.word 0x7b86879b, 0xf92b8192, 0xb703d7e5, 0xf9fd8cec, 0x80663797, 0x30ac8086, 0x54b11d61, 0x3b15fc43
.word 0xcc80e1f3, 0xc642e459, 0xa703249b, 0xd81fcf19, 0xd0cf3057, 0xdb3ce256, 0x88712fcf, 0x768fc418
.word 0x5a7e9030, 0x1154f94a, 0x56762ab2, 0xaf30ca74, 0x91655e4d, 0x46f11f5f, 0x9ac9236b, 0xb3c83a3c
.word 0x1bce07ed, 0x772598ca, 0xc32d01a2, 0x9d14e90b, 0x2f49d66b, 0xf7882670, 0x62ca486e, 0xab0c6d41
.word 0x5a317129, 0x732fba62, 0x9144e5f2, 0xc16e46c0, 0xa5bee213, 0x1c0cd40b, 0xf87a2ef9, 0xbfd9d2a4
.word 0xd53b2670, 0x7ad91092, 0xe4a37f3a, 0x56fc8522, 0x5d49a509, 0x32f9531c, 0x0e8e87ad, 0x040858d5
.word 0x28682e3e, 0x88b54e48, 0xaead9f54, 0xf017c143, 0x522f84eb, 0x23759f7c, 0xf65c1ba7, 0xaa6d5449
.word 0x01091952, 0x7b2de074, 0xf2f4b115, 0xe771c99a, 0xad6d9711, 0xedca61ec, 0x5429045d, 0x368eb77e
.word 0x2c013cb2, 0xaf6a8d51, 0xab6488d9, 0x99ba5c0b, 0xcdb108fc, 0x7fe26a3a, 0xeeb44771, 0x6abb7d05
.word 0xacfe96df, 0x33792f53, 0x825c309b, 0x27324e65, 0x92364c0a, 0xf3efcc3d, 0x551b1757, 0x320ac36a
.word 0x0a89d3fe, 0xfc817679, 0xa5a76ece, 0xe7ca1799, 0x9124ae87, 0xd3ab75e2, 0xd1f9ef8d, 0xf3d5caf0
.word 0x255e68e2, 0xd1cc179c, 0x74dfa207, 0xb9cc5ced, 0x142820bd, 0x749b7067, 0x8e7fad9b, 0x7d1d537a
.word 0x593fde4b, 0xc7d83195, 0x6e6aee86, 0x66e17a03, 0x2ec9b7a7, 0xfd05f10c, 0xa53834b2, 0xf3cf73c8
.word 0x2cf030f0, 0xa1533543, 0x0b777c55, 0x720aa92f, 0xe9da4fb8, 0x7cb9e8f2, 0x9dd5a082, 0x488c2ff2
.word 0x952f7bf1, 0x574c3e59, 0x5c7e54be, 0x0f44f5aa, 0x42e34cf4, 0x1e6c5228, 0x091ab3df, 0xde63ca1e
.word 0x24554d94, 0xace5e080, 0xac96476d, 0xc0f4a8f6, 0x67206329, 0xfc338108, 0x7bbfea37, 0x0e49e532
.word 0x6f46e9c9, 0xd1beb65b, 0x9e515fcc, 0x9342fd8d, 0xc92cad18, 0x2a5d9934, 0x5a9486b0, 0xe68aa7db
.word 0x91804284, 0x03cc5605, 0x2dd80bd1, 0x43aed0b1, 0x9988dc5e, 0xe4fc5fe7, 0xba1f5066, 0x321d2a0b
.word 0xb69537d0, 0x288638d0, 0xaffdf57e, 0x8102429b, 0xa17b4253, 0x5c4b1cad, 0x760c4b7f, 0x877221d6
.word 0xd82957d1, 0x10261496, 0x9437b484, 0xe1194c4b, 0x8d86e2a3, 0x3f70a707, 0xbed8994e, 0xb82410f6
.word 0x5e2f8818, 0x2aa49c10, 0x22ee3b90, 0x9d80c497, 0xd394dbeb, 0x198c791b, 0x06cffdc8, 0x2bc0a5f1
.word 0x77cc9db3, 0xc99e6eda, 0xa212675f, 0x43220b3b, 0x9e3fa9d9, 0xdda72c5f, 0x72ac162c, 0x9d3d927f
.word 0xfedf84f9, 0x5346de6f, 0x5cc8d4c5, 0x27a031b4, 0x759bca43, 0xc484869b, 0xca9e4af7, 0x120d2faf
.word 0x312c92f1, 0x4ea965fe, 0xe89ae567, 0xa06414fc, 0x071bc448, 0x2cc5125a, 0x32e5e567, 0xdfd6dc65
.word 0xb958fe90, 0x8d427def, 0xbe2ccba9, 0xf00d21c6, 0x1d6b5d3c, 0x9f20850c, 0xfbbaac2a, 0x6a893867
.word 0x1cfcd504, 0x7f1601c7, 0x49225f00, 0x69ace1ed, 0xefa1aa67, 0x89102722, 0x00ccd01b, 0x1c0475e8
.word 0x41db9539, 0xae2223c8, 0xafe51b69, 0x5574c3c3, 0x3fce6fd9, 0x0317fc2a, 0x8b24119a, 0xc68a0286
.word 0x8559209a, 0xa352770d, 0xddc84001, 0x0190e5f0, 0xf8dbde63, 0x4b3e5ebc, 0x62ccab63, 0xb3e05281
.word 0xf7dfe33b, 0x10250d18, 0xd1d7f0b9, 0xf781bfe6, 0x472b9222, 0xfa66234a, 0xe3ca3ce9, 0x3966e5c4
.word 0x526a8df2, 0x30ac9e6f, 0x99f77350, 0x334f6697, 0x8589de99, 0x86e6f1d4, 0xdd388990, 0x479285fd
.word 0x77cd1ecc, 0x5becf158, 0x0532d372, 0x447b2a38, 0x1d6c2808, 0x31ba9b49, 0x81603fea, 0x9fa83a60
.word 0x0beda505, 0xcfaf2e07, 0x1d20d891, 0x9b4c3573, 0x20a14966, 0x5d8abf98, 0xd116e569, 0x5f155ac0
.word 0xfbe1f0a3, 0x28b5f058, 0x36d70e13, 0x972088eb, 0x3e13a521, 0x1c422621, 0x748fc40e, 0xc326f1ab
.word 0xe091216f, 0x88e95729, 0x3e16d772, 0xecaddacb, 0x980a44ed, 0x00bb9361, 0x31717fc4, 0x2fa18cba
.word 0x1810dc4e, 0x7b5e16ca, 0x722d33bb, 0x296af9fd, 0x39a7d802, 0x23714055, 0xf431e615, 0x4e4d5684
.word 0x073ada45, 0xf1d52a6e, 0x706a7590, 0xddf31f50, 0x434fd2e6, 0x75caf3c4, 0xab4d7b83, 0x45b6bce3
.word 0xb2029145, 0x949c8ea0, 0x9a1e4daf, 0x8fa26aa4, 0x2d004dbc, 0xe6d17498, 0xca3e04fd, 0xcdcda42e
.word 0x05debeb6, 0xccf12b58, 0x5c2a2a7f, 0xb6505359, 0x7fb6f7e7, 0xf6d2f8ba, 0x53feb60d, 0x185cab79
.word 0xb0a404c6, 0x8a8bfc19, 0x0b144363, 0x20656cf8, 0x22135a76, 0x9a82d465, 0x76760738, 0x5c529c4c
.word 0xee782f52, 0x5ed6c4fd, 0x690fd170, 0x35c39e81, 0xd3c327c4, 0x103c86c3, 0x5b4b83cf, 0x70c8ee70
.word 0x20819f57, 0xde91400f, 0xd2744770, 0x10b4cbf1, 0x9bade71b, 0x861ae014, 0x586e5740, 0xb9239da0
.word 0xb762e7ee, 0xba450dd8, 0x485ed231, 0xb7cefcc8, 0x9e9d8dd7, 0xbc56b593, 0xa08a4895, 0x06d64dac
.word 0xf7f391b2, 0x3ac69427, 0x171ada20, 0x4735ab01, 0x42c16395, 0xd997d9ad, 0xa4fd38bb, 0x295e9896
.word 0x8bc916b0, 0xdb81fe40, 0x9dbb7a01, 0x7daa3acc, 0x73fd7a69, 0x36c628ef, 0xe12f625f, 0xf7c5b4f3
.word 0x1a01a865, 0x9c5e0d99, 0x0acb7b60, 0xe289b1e5, 0xe1366da7, 0x0ad82ecc, 0x5be95bef, 0xb829b421
.word 0x4d52a304, 0xce79925d, 0x379f6b29, 0x2aa625e2, 0xef24d821, 0x7713dd57, 0x4d53d09d, 0xb2b41109
.word 0x32c83ffc, 0x54a68502, 0x5f363c49, 0x4ce64e59, 0x74352b34, 0x0b50aad0, 0x329417cb, 0x6aed9e06
.word 0x54644d25, 0x1b45b088, 0x6207b786, 0x8ea69267, 0xe0096343, 0xdf43fc06, 0xd9032b40, 0x076a455d
.word 0x22d34137, 0x62438d3f, 0xcf102765, 0x62f4850c, 0x6f25ba27, 0xae1fb2be, 0xf48089b2, 0xbde0dddd
.word 0x510b07d6, 0x0fb397e1, 0x9cd7a43c, 0x386f89da, 0xfbfd4c7a, 0xe2eb6c72, 0xc020c5de, 0x537fc671
.word 0x430a713f, 0xaaa8ad6c, 0x63e4f6b2, 0xde597098, 0x822e2da4, 0x4eb8a343, 0x4ed2780c, 0x04e25504
.word 0xee9e7706, 0x492a1b45, 0x7425bef2, 0x6fa332fa, 0xb8f8bbea, 0xd2c4cc1c, 0x03a848a2, 0x16ed2638
.word 0xb0fdebfa, 0x30e30390, 0x97307b9c, 0xbcdfa7fe, 0xcb8d316e, 0xda8af8a5, 0x55f54221, 0x3b8cdf39
.word 0xd6a7f2d8, 0x236d90e8, 0x70ac0313, 0x294fac69, 0x979ddaa3, 0xf4aa864c, 0xc84345f1, 0x55913fa2
.word 0x1be168c5, 0xcc4927b0, 0x366f2ef6, 0xeff334bf, 0xadc402b1, 0x2454ac15, 0x855cc8ef, 0x2c44287d
.word 0x5db4e133, 0x29efcfb7, 0xef67d68f, 0xd4939a53, 0x83e96437, 0xac90a426, 0xd2e4d9eb, 0x6ef290bb
.word 0x5615c0cc, 0xbb26b7e3, 0xc5cb3787, 0x329b5090, 0x1f73eb13, 0xa7e316c8, 0x921079c1, 0xb876a342
.word 0xccb51461, 0x77844a7c, 0xf5532c81, 0x3d14f46b, 0xf4b1bf67, 0x0ddc1f9c, 0x7cbfe11c, 0x6688d49c
.word 0x94431819, 0x196b0081, 0x91190793, 0xd89e8d6c, 0xb2f8119f, 0xea27ae37, 0xa5a09439, 0x4df34d80
.word 0xf7696bd8, 0xcf238aee, 0xe82b5b23, 0x6731de5c, 0xa34d56a1, 0x0fb1e2d5, 0x9e75ace0, 0x3bbfea80
.word 0x3d43fc37, 0x9c787401, 0x7b62e706, 0x8f235366, 0x3486cca2, 0xd85728ef, 0x52e2bad1, 0xc4932870
.word 0xc98e8cbf, 0x6e54dc85, 0x3ee4ae03, 0x8bdd7a00, 0xfd58a530, 0x995cba07, 0x217feaf1, 0xbcc404c4
.word 0x90d7893d, 0x6d1b4f25, 0xb55e5139, 0xd928eed9, 0x56233c13, 0x73c89295, 0xfb8424bc, 0x59b95c3e
.word 0xe53b11fd, 0x731566fd, 0xe547f1b3, 0x4c333bf7, 0xa4988efc, 0x24380561, 0xcdbd60cb, 0xd99af736
.word 0xfec92af5, 0xf20ad2dd, 0x3f74d8a8, 0x56d29239, 0x907bd75a, 0xb470a633, 0x3403da0d, 0xa8a9469d
.word 0xc0e717a4, 0xfc1e1476, 0x0fda6ff0, 0x006cc9a4, 0x7f7c01f7, 0x24c9868d, 0xeeb40992, 0xb05c0eb1
.word 0x65448d60, 0x51389346, 0x8243adc4, 0x3c8b9340, 0x8a1dd6a1, 0xdb5898fb, 0x19e9c449, 0x79997767
.word 0x414cfbc7, 0x527efb76, 0xf7c6403f, 0x4d6d5471, 0x2b83c980, 0x18c7083e, 0xaee13193, 0x2feb5e9f
.word 0x590a40f9, 0x928514bd, 0xda4a4693, 0xc6270de2, 0x9e743e16, 0xef36c5b1, 0x6bf7c2e6, 0x98942c7e
.word 0xdb5aad2c, 0x42928c2b, 0x6414b5f2, 0x13b94b75, 0x71af3532, 0x13c71294, 0x985e9e2b, 0x92067ce1
.word 0xf5ce432c, 0x264fab03, 0x9bcf3f65, 0xe226e7cc, 0x0e72e3d2, 0xb605070c, 0xf916788e, 0x681abbfc
.word 0x6ae46170, 0x25021937, 0xc42b61a8, 0xe5402578, 0x93a30b8b, 0x5e3bd618, 0x780da7a2, 0x8a43abdd
.word 0x4351a115, 0x1beabb1e, 0xe4b4df76, 0x411adbb4, 0x52eabbf9, 0xa1fbc315, 0xd79d335d, 0x8bab86da
.word 0xe79ce619, 0x45d644f2, 0x35bb4a3f, 0x60ef3c4e, 0x1af28579, 0x42bb07e2, 0xa7802e48, 0xac551e8e
.word 0xe5d325cf, 0xa2a38668, 0x4ac85489, 0xf5d64056, 0xf39c06a9, 0x25f8bcd2, 0xc8c2abae, 0x462e93c3
.word 0xe8ca8644, 0xc2601778, 0xc89dfbfb, 0xc219ee4c, 0xc3f17e9c, 0xee10e666, 0xec123ffb, 0x112fd5bb
.word 0x61daef94, 0xbdd589f4, 0xc0cbf474, 0x5c0de905, 0x84e1fbc2, 0xbdd1b1ed, 0xbfa7ea3f, 0xd1b64f2b
.word 0xd905bd73, 0x3f58397f, 0xe397a590, 0x1b6b5b13, 0x3415421a, 0xea69593c, 0xb7f6acae, 0x1d19e7a0
.word 0x945a99da, 0xf2d93f68, 0xa7e883f0, 0x0810abe9, 0x3994a3ac, 0x8edabdf0, 0x790bc7ac, 0x3a0a1901
.word 0xd631cd48, 0xd875eafa, 0x08d0da00, 0x1fe81f1f, 0xdde120bd, 0xbcaff79c, 0xa8946b18, 0x8a1a81cd
.word 0x0d21fcbe, 0x1c986d50, 0xfe9caf49, 0x40f7b403, 0xa5567efb, 0x0c3cf811, 0x6ae63d34, 0xb655baca
.word 0x2cfea28d, 0xadc49990, 0x3e14c28d, 0x006c50f3, 0x4ae4754e, 0x6d540b2f, 0x37ed9c1c, 0xd298a7c6
.word 0x3274f0fc, 0xf65b48db, 0x4e22c88b, 0xcddea517, 0x7e9c3c61, 0x29b29b92, 0x7be93e17, 0xaa343b04
.word 0x073c278b, 0x4f71aa71, 0x2c3cf16e, 0xcb9b3255, 0xf22def06, 0x84eb589c, 0xbe4b07c8, 0xf4baa2c1
.word 0x44f9f6e6, 0x4f92a87f, 0x48edcc0e, 0x6758f970, 0x707eac9c, 0xf4e45c0f, 0xa74d2eeb, 0x3c7813b9
.word 0x860b5770, 0x546fe8b6, 0x88273f65, 0x7404b3d7, 0xa581d3ac, 0xb6884dc8, 0x6ad78848, 0xb949a7c3
.word 0xcff2a795, 0x0a419f75, 0xec2c15b8, 0x3fb2ba86, 0x06504881, 0x09e7bd03, 0x7ffcb136, 0x71b71995
.word 0x035ba70e, 0x92654eb5, 0x24b5877a, 0x85be13f3, 0x47f539a3, 0x067a8875, 0x9c76d910, 0x04823ffa
.word 0x9d439154, 0xde8388b4, 0x09cfb863, 0x4254f567, 0xfb274999, 0x9bb90820, 0xe8fc35bc, 0x01f2288a
.word 0x0cb0ac5e, 0xd27c7c81, 0xa29fcac5, 0x1af21c20, 0xc645f399, 0x3aecac9d, 0xfda99d98, 0xd1c90bcb
.word 0x046d7f3b, 0x4b97aa50, 0x3e4bb3eb, 0x46a1809f, 0xcf261d93, 0x56b0f7b4, 0x9116a125, 0x394bd46c
.word 0x9cef76cc, 0xdcae07c4, 0xfa3e9d83, 0xccf3266b, 0xe9b81d39, 0x9130d176, 0xca8be96f, 0x522fe642
.word 0x372197e3, 0xf3f7d042, 0xa8567b6d, 0xd7ddea9c, 0x67d0ecc6, 0x65ea34dc, 0x82ba271a, 0x5182545c
.word 0x8ca14292, 0xb58ec3ee, 0x2dc8a8b5, 0x70be17c9, 0x3ad8cfc3, 0x0c9c01ea, 0x5a492574, 0x4f608167
.word 0xe5ad450b, 0x4f0a3cab, 0x0f950dc1, 0x0ed113f1, 0x548f19c3, 0xb8f43cb4, 0x01af858f, 0x98d06589
.word 0xc9c26700, 0xb2c90902, 0x59c9632f, 0xf9290d1a, 0x0cd3ed2b, 0x41bd8219, 0x169d904f, 0x1b8cf77f
.word 0x54d10e11, 0x4cf9db77, 0xa13a78dc, 0x379497d0, 0xec004e78, 0x84a75496, 0xf6001cce, 0xd53c7329
.word 0xdd501e7f, 0xfbd2dfe6, 0x636af132, 0x9774f562, 0x9d4644ea, 0xa417f281, 0xd3d21868, 0x590875c2
.word 0xb585c284, 0xea140ac9, 0x2c85ec7f, 0xd05d764c, 0x168f9860, 0x2efb049e, 0xbab3d428, 0xbbd4fe1c
.word 0x0e4926e7, 0x11d1655f, 0x460d9a91, 0xf7136d22, 0x182f2978, 0xfbd0aa9d, 0x9b205b0b, 0x304b6290
.word 0x53954a28, 0x80b57ee6, 0xaf03e5fd, 0x27b982e9, 0xfc0ed4bd, 0x2556a8ac, 0x8f874684, 0x9693f1e7
.word 0x9ddbd492, 0xcd2ba0d0, 0x2b3d48f1, 0x0790b7b5, 0x2bec9806, 0x80f02170, 0x5660eb82, 0xdd989c31
.word 0x054c8a90, 0xc04eb4cd, 0x72551d90, 0x6717b815, 0xb62fa627, 0xe0554f21, 0xa6743936, 0xf5f92869
.word 0x421c769c, 0x18a3f062, 0xe2cc907f, 0x1bf1432a, 0xcfd74e04, 0x2806e0f2, 0x7f1a006f, 0x0c248082
.word 0xd7f881ad, 0xa00e76f8, 0xb1d0d64a, 0xa1c2707a, 0x52bf9ac1, 0x47eebcca, 0x9766bcc2, 0x57ad9cb1
.word 0x4ad7c161, 0x59a2d637, 0x0129f36d, 0x078a4a15, 0x6408f531, 0xac47f7a6, 0x1b5176f4, 0x935546b4
.word 0x744b6f4b, 0x0d2476df, 0xea2cdeb2, 0x6849cce3, 0xcf9ddf8c, 0x8acaba15, 0xa0dd11c5, 0x8d00aca6
.word 0x5adde24a, 0x2a4fd1c7, 0x82a62ac0, 0x8d23b475, 0x08a1a399, 0x8d6e8074, 0x4c45a149, 0x1eea6617
.word 0xa0f78dc2, 0x892ad99a, 0x115afc27, 0x2f9dcd05, 0xaea2db4c, 0x82305686, 0x5580cf2f, 0xcac5358a
.word 0xcb273540, 0xb30e5ab7, 0xc8c29074, 0xa22ba359, 0xfbb20216, 0xd4b3ebd2, 0x30371af0, 0x24a6d6fd
.word 0x8f18840f, 0x8caff8ec, 0x0b0b7874, 0x87d8b1c1, 0xb84cba59, 0xa489c13d, 0x98f52045, 0x72a7de48
.word 0x80130caf, 0xe98c98b3, 0xd5b24d25, 0x95aec91e, 0x73747ecb, 0xeff94509, 0x57849c83, 0x4028801c
.word 0x0aa63932, 0x182394c8, 0xa249831b, 0xfe14c332, 0x2cdb6b6d, 0x73bdf597, 0x80b47f4a, 0x3c2b3aa9
.word 0x7da2c5ac, 0x68c350a8, 0x90bc1e50, 0x99c5f214, 0xf5537393, 0x60c4eac8, 0xab2823ea, 0x9a8f0c6b
.word 0xe258d00a, 0x7e82b855, 0x390c232d, 0x9249e97f, 0x1d737657, 0x5ee3f022, 0x0918f46d, 0x19bcec38
.word 0x1a66e7ca, 0x6dfaf274, 0x6baf0379, 0x80ca9784, 0x5db71262, 0xdcc49052, 0x4248acfb, 0xecfa669f
.section .user_stack,"aw",@progbits;
.align 2
user_stack_start:
.rept 4999
.4byte 0x0
.endr
user_stack_end:
.4byte 0x0
.align 2
kernel_instr_start:
.text
mmode_intr_vector_1:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_2:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_3:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_4:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_5:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_6:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_7:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_8:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_9:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_10:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_11:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_12:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_13:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_14:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

mmode_intr_vector_15:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x342 # MCAUSE
                  srli x14, x14, 0x1f
                  beqz x14, 1f
                  j mmode_intr_handler
                  1: la x2, test_done
                  jalr x0, x2, 0

.align 4
mtvec_handler:    
                  .option norvc;
                  j mmode_exception_handler
                  j mmode_intr_vector_1
                  j mmode_intr_vector_2
                  j mmode_intr_vector_3
                  j mmode_intr_vector_4
                  j mmode_intr_vector_5
                  j mmode_intr_vector_6
                  j mmode_intr_vector_7
                  j mmode_intr_vector_8
                  j mmode_intr_vector_9
                  j mmode_intr_vector_10
                  j mmode_intr_vector_11
                  j mmode_intr_vector_12
                  j mmode_intr_vector_13
                  j mmode_intr_vector_14
                  j mmode_intr_vector_15
                  .option rvc;

mmode_exception_handler:
                  csrrw x6, 0x340, x6
                  add x6, x30, zero
                  1: addi x6, x6, -124
                  sw x1, 4(x6)
                  sw x2, 8(x6)
                  sw x3, 12(x6)
                  sw x4, 16(x6)
                  sw x5, 20(x6)
                  sw x6, 24(x6)
                  sw x7, 28(x6)
                  sw x8, 32(x6)
                  sw x9, 36(x6)
                  sw x10, 40(x6)
                  sw x11, 44(x6)
                  sw x12, 48(x6)
                  sw x13, 52(x6)
                  sw x14, 56(x6)
                  sw x15, 60(x6)
                  sw x16, 64(x6)
                  sw x17, 68(x6)
                  sw x18, 72(x6)
                  sw x19, 76(x6)
                  sw x20, 80(x6)
                  sw x21, 84(x6)
                  sw x22, 88(x6)
                  sw x23, 92(x6)
                  sw x24, 96(x6)
                  sw x25, 100(x6)
                  sw x26, 104(x6)
                  sw x27, 108(x6)
                  sw x28, 112(x6)
                  sw x29, 116(x6)
                  sw x30, 120(x6)
                  sw x31, 124(x6)
                  csrr x14, 0x341 # MEPC
                  csrr x14, 0x342 # MCAUSE
                  li x4, 0xb # ECALL_MMODE
                  beq x14, x4, ecall_handler
                  li x4, 0x2 # ILLEGAL_INSTRUCTION
                  beq x14, x4, illegal_instr_handler
                  csrr x4, 0x343 # MTVAL
                  1: la x2, test_done
                  jalr x1, x2, 0

ecall_handler:    
                  la x14, _start
                  sw x0, 0(x14)
                  sw x1, 4(x14)
                  sw x2, 8(x14)
                  sw x3, 12(x14)
                  sw x4, 16(x14)
                  sw x5, 20(x14)
                  sw x6, 24(x14)
                  sw x7, 28(x14)
                  sw x8, 32(x14)
                  sw x9, 36(x14)
                  sw x10, 40(x14)
                  sw x11, 44(x14)
                  sw x12, 48(x14)
                  sw x13, 52(x14)
                  sw x14, 56(x14)
                  sw x15, 60(x14)
                  sw x16, 64(x14)
                  sw x17, 68(x14)
                  sw x18, 72(x14)
                  sw x19, 76(x14)
                  sw x20, 80(x14)
                  sw x21, 84(x14)
                  sw x22, 88(x14)
                  sw x23, 92(x14)
                  sw x24, 96(x14)
                  sw x25, 100(x14)
                  sw x26, 104(x14)
                  sw x27, 108(x14)
                  sw x28, 112(x14)
                  sw x29, 116(x14)
                  sw x30, 120(x14)
                  sw x31, 124(x14)
                  la x2, write_tohost
                  jalr x0, x2, 0

illegal_instr_handler:
                  csrr  x14, 0x341
                  addi  x14, x14, 4
                  csrw  0x341, x14
                  lw x1, 4(x6)
                  lw x2, 8(x6)
                  lw x3, 12(x6)
                  lw x4, 16(x6)
                  lw x5, 20(x6)
                  lw x6, 24(x6)
                  lw x7, 28(x6)
                  lw x8, 32(x6)
                  lw x9, 36(x6)
                  lw x10, 40(x6)
                  lw x11, 44(x6)
                  lw x12, 48(x6)
                  lw x13, 52(x6)
                  lw x14, 56(x6)
                  lw x15, 60(x6)
                  lw x16, 64(x6)
                  lw x17, 68(x6)
                  lw x18, 72(x6)
                  lw x19, 76(x6)
                  lw x20, 80(x6)
                  lw x21, 84(x6)
                  lw x22, 88(x6)
                  lw x23, 92(x6)
                  lw x24, 96(x6)
                  lw x25, 100(x6)
                  lw x26, 104(x6)
                  lw x27, 108(x6)
                  lw x28, 112(x6)
                  lw x29, 116(x6)
                  lw x30, 120(x6)
                  lw x31, 124(x6)
                  addi x6, x6, 124
                  add x30, x6, zero
                  csrrw x6, 0x340, x6
                  mret

pt_fault_handler: 

.align 2
mmode_intr_handler:
                  csrr  x14, 0x300 # MSTATUS;
                  csrr  x14, 0x304 # MIE;
                  csrr  x14, 0x344 # MIP;
                  csrrc x14, 0x344, x14 # MIP;
                  lw x1, 4(x6)
                  lw x2, 8(x6)
                  lw x3, 12(x6)
                  lw x4, 16(x6)
                  lw x5, 20(x6)
                  lw x6, 24(x6)
                  lw x7, 28(x6)
                  lw x8, 32(x6)
                  lw x9, 36(x6)
                  lw x10, 40(x6)
                  lw x11, 44(x6)
                  lw x12, 48(x6)
                  lw x13, 52(x6)
                  lw x14, 56(x6)
                  lw x15, 60(x6)
                  lw x16, 64(x6)
                  lw x17, 68(x6)
                  lw x18, 72(x6)
                  lw x19, 76(x6)
                  lw x20, 80(x6)
                  lw x21, 84(x6)
                  lw x22, 88(x6)
                  lw x23, 92(x6)
                  lw x24, 96(x6)
                  lw x25, 100(x6)
                  lw x26, 104(x6)
                  lw x27, 108(x6)
                  lw x28, 112(x6)
                  lw x29, 116(x6)
                  lw x30, 120(x6)
                  lw x31, 124(x6)
                  addi x6, x6, 124
                  add x30, x6, zero
                  csrrw x6, 0x340, x6
                  mret;

kernel_instr_end: nop
.align 2
kernel_data_start:
.section .s_region_0,"aw",@progbits;
s_region_0:
.word 0xb1ca356a, 0xb3c0904f, 0x02b85a73, 0x34c7041e, 0x4a85d547, 0x19c6b542, 0xa9580b4e, 0x2ec2d877
.word 0x6bc9b497, 0x07e638d1, 0xeb67363e, 0x8db01a3e, 0xafc1823a, 0x5cbb6678, 0xaad4d9be, 0x178e1635
.word 0x2018c251, 0x00fcdc55, 0x94908914, 0xf09823b0, 0x02e98530, 0x90fb75d7, 0xba78cd42, 0xa9841e32
.word 0x879b8e93, 0x707852cc, 0x1062d091, 0x52f8dd51, 0xf7bbddea, 0xb87270c7, 0xf4d0443e, 0x31e0a350
.word 0xdda7f8eb, 0xea7cbb3c, 0x89bf98fa, 0x74c369fd, 0x409a3d1a, 0xd242f7db, 0xa5781cda, 0x80731047
.word 0x64080520, 0x8d5a7376, 0x624f68e3, 0x887e5b2b, 0x44ddc057, 0x1c22e00e, 0x9100e52b, 0x32a232bf
.word 0x40f2a13c, 0xe6674064, 0x3e1529cb, 0xf1071df1, 0xf1b19af7, 0xf3f35d5f, 0x3786f836, 0xd92bcf93
.word 0xcc0baacf, 0x3a4d88c3, 0x9585193c, 0x9a2ad716, 0x1183b695, 0x584643f5, 0x339b2c66, 0xab6abe8a
.word 0x7977dd67, 0xc549259f, 0xcb3ad30a, 0x8336df9c, 0x3033ce1a, 0x1343bdb8, 0xa44daa5c, 0xa2092ef6
.word 0x479806b8, 0xca4f57ae, 0x1abe6919, 0xbd679b27, 0x93d706c7, 0xc7aed34f, 0x61cd53dd, 0xaa93abb5
.word 0x7067d797, 0x0e92283a, 0x983106d2, 0x76fdf957, 0xa3403ad1, 0x19c0136d, 0x4e5206d0, 0xfa28c092
.word 0x95ee6b7c, 0x1fb7d13c, 0x086a423a, 0xe69787ba, 0x4a56cfbf, 0x26a86b1f, 0x9a4aa2e9, 0x3ab4a5e4
.word 0x01bcfdfc, 0xcc98ccd7, 0xaad04eac, 0x5952d9fa, 0x6a1127b8, 0xfae769c5, 0xb9c00744, 0x9a476b5c
.word 0xa65e37e8, 0x367b4fcd, 0x5c1df67b, 0xb705b8b4, 0x92178a12, 0x090931f5, 0x3e4497e8, 0x6eef6da0
.word 0x44818819, 0x5c0043f2, 0x6de0ecf5, 0xd55978a2, 0x0b802417, 0xbf9c17f7, 0x58fe9bd1, 0xf0240ef9
.word 0x8b3a71a4, 0xc9545607, 0x75f9e318, 0xf0f89192, 0xe2cea150, 0xea05485a, 0x35f20b44, 0xccab3f58
.word 0xc70cab08, 0xc9d5d527, 0x8599acad, 0x90e5d361, 0x680ff2c6, 0x3b9d9238, 0xb4ce129d, 0x00519e66
.word 0x848f7e6b, 0xadc5ac89, 0x6bc3625c, 0xe90e0dbd, 0xb0f10fbf, 0x613f5390, 0x000e525b, 0xee3715f7
.word 0xde367145, 0x773a4ba2, 0x8d038c0f, 0xf47a51b6, 0x64a64dfb, 0x05b8a527, 0x5aae5324, 0x7f2f7635
.word 0x36d5fc51, 0x8e627059, 0x264e9e8d, 0x0b6f1193, 0x24c39dd1, 0xdd9de05b, 0xa71099d0, 0x08a36798
.word 0x28d42370, 0x3376c67a, 0x08af87b2, 0x7c883101, 0x89e1dc07, 0xcdbd59ba, 0x5e99453f, 0x17e0c93c
.word 0x261df917, 0x478c509e, 0x833043c1, 0x2f66ebe3, 0xaa3344e9, 0x21125f27, 0xd03d9c27, 0xdcf30bb6
.word 0x149a5aeb, 0x83d9224a, 0x65b8d0ba, 0xa4c612b9, 0xd1be31df, 0x4435bae2, 0x4650a65b, 0x6dc1ede7
.word 0x743b3e39, 0x525aa79a, 0x79e5e21c, 0x87df41fb, 0x4f070059, 0x0cd2cd5b, 0x5a96e3b6, 0x52f68d4d
.word 0xd847166b, 0xab915e5b, 0x17aa7669, 0x4ca9cbd4, 0x737c7b6c, 0xafe2e6c0, 0x7beb9af2, 0xd80a95ed
.word 0xc3a4dc73, 0x5429bc7a, 0xba019529, 0x760cb2ea, 0x51572e39, 0x691db5b7, 0x4fab3664, 0x3f4c0133
.word 0x8d373fbd, 0x7bb32d2c, 0xd3d38e54, 0x12df6919, 0x2cf4626a, 0xedcc0e33, 0x8dcea962, 0xa4e91bb0
.word 0xc0b64611, 0x46a3c00e, 0x8533bdc1, 0xe304766f, 0x26264828, 0x701edc3f, 0x1834a1c6, 0xbfcc1082
.word 0x0c1ebd92, 0x7ec494cf, 0xa604efac, 0x7027a097, 0x8cb82fae, 0x687a0200, 0xc7c1c157, 0xebc494e1
.word 0xda42eaac, 0x9a1271a0, 0x17c4566a, 0xd7d1f02d, 0x59a9e529, 0x33c53d58, 0x4e97aad1, 0xed1d6dd3
.word 0x5b77631d, 0xa92154b3, 0xcc4c23ce, 0xc1b2482d, 0xf283007f, 0x561980e0, 0xa3e2a8db, 0x7511e5fe
.word 0x78ad927c, 0x5524a4c0, 0xb3208e2c, 0x5535157a, 0x3cebac42, 0xc2f5daf1, 0xe54dedd3, 0xda6876d6
.word 0x72e9a1d6, 0x430cd0da, 0xfa6b513a, 0x7426d829, 0xc3663652, 0xaf5675c3, 0x3759f8fe, 0xf2a3eeec
.word 0x3f6c4533, 0x0061c3cf, 0xd874f762, 0x92769880, 0xd9d13380, 0xd9d16ccb, 0xdb6920a2, 0xf99b015f
.word 0xaee91e37, 0xf3ce78f0, 0x23f00e23, 0x720b2d60, 0x6af264c7, 0x070e987f, 0x8856dc21, 0x068f1459
.word 0x4035d3fe, 0x504a0c0f, 0x62912e6f, 0x1cb4f588, 0x4086c649, 0x8c10b376, 0x479e50c2, 0xfda2fa1a
.word 0x80182753, 0x1a770e5c, 0x87e6f483, 0x7fad725e, 0x61a0c50e, 0xddf4f0d9, 0x527e1f7e, 0xd97a9cab
.word 0x65db9a38, 0x06d69ea0, 0x9d1603f9, 0x9ea49755, 0x8bc8fb80, 0x32135688, 0x127196c9, 0xccf7c148
.word 0x03cb6861, 0x07135bfd, 0x165aa732, 0x6131b13e, 0x0c9b60b0, 0xa7371175, 0xba909208, 0x2b97bf55
.word 0x63ecbc8a, 0xcd33f8b0, 0x94ba08e5, 0x693f003e, 0x0477327d, 0x4d760c22, 0x286e0d40, 0xd800df27
.word 0x2964c61d, 0x1070231b, 0x98e7355c, 0x15288ebe, 0x1339e6c5, 0x091c04c4, 0x1dc7a1a8, 0x9bedbfc1
.word 0x5c1ca516, 0x37342e13, 0x8f7597b6, 0x1f66560e, 0x1516d82a, 0x624f1286, 0x19a1cef8, 0x9b2f6627
.word 0x75e4315a, 0x92ac2e70, 0x86fbacce, 0xf54d930d, 0xb2e18f29, 0x2bf02c91, 0xc0c5e963, 0xe7ba9493
.word 0x24d52501, 0xe818b2d1, 0x6a95df9f, 0x6d3d6f26, 0x0e6c337b, 0x1a8c19b2, 0x3d6f46be, 0x1a9fa92c
.word 0x8c9c010e, 0x6b710e70, 0xa8102b45, 0x02590e30, 0x2b1c5e12, 0xb99f4292, 0x56f62841, 0xd77777bc
.word 0x0f3046f4, 0x5e22a316, 0x5a4af80f, 0xc39cf3ab, 0xe3883a2e, 0x3f4bd4f5, 0xbfb82c5e, 0x85afe8d1
.word 0x3ec70cde, 0x4dbd9b8d, 0x2bbae3fc, 0xf21649a1, 0x7365bbd4, 0x91406c53, 0xca3d758a, 0x02737e1f
.word 0xb74f4d3f, 0x504f8047, 0xd0c042fc, 0x196fc87a, 0x4ae0bc3b, 0x47308500, 0x40c0ac6f, 0x6637b540
.word 0xcb6c521c, 0x2f74f8dc, 0xb2abd7bd, 0x0d35b544, 0x052c28d7, 0x4cc25e68, 0xf2c24a54, 0xe8f97c50
.word 0x0f9282d0, 0x43b5801b, 0x82c67120, 0x4a617653, 0x2966417a, 0x81710bac, 0x557ef368, 0xc7dabdd8
.word 0x3e321a5a, 0x573c0d2b, 0x2b64fd78, 0xccce24fd, 0x00e00996, 0x5a1191e0, 0x4bd28299, 0x8e2de873
.word 0x951b7357, 0x7e00a1a1, 0xc8c189fd, 0x850ff65f, 0xdafb0c79, 0xe9195702, 0xca36b7bf, 0x4d8b7ff1
.word 0xe419ded9, 0xfd2737a2, 0xfd7c1fba, 0xed7e9ccf, 0x04c962f4, 0x7bb03495, 0xb455a06f, 0xdafbdf2f
.word 0x1679d884, 0xf420ee0e, 0x416eac10, 0x1eecb081, 0x45321219, 0xb228526e, 0x584f3a8f, 0xa2a1e7b9
.word 0xbbbf86a1, 0x03e617f3, 0x7d072f30, 0x0d4ced91, 0x1fa18e24, 0x6ef213fb, 0x961fdfed, 0x8b83523f
.word 0xd57047f0, 0x486ea33c, 0x87cc4be6, 0x5191dd89, 0xf264d990, 0xeb7fd582, 0x57f884e0, 0xa2a7291c
.word 0xc1781dfe, 0xd430d18e, 0x5bf92c85, 0xfb8399a0, 0xc2c6a5ae, 0x865f8e43, 0x433fb619, 0x8dc77319
.word 0x1b963984, 0xd3726fc4, 0xd558ae20, 0xe9463569, 0x499a09ea, 0x3dbb2713, 0xa3bfa2ee, 0x0c7d9c36
.word 0xb3483d43, 0x3d425af1, 0x6c1f02fe, 0x744d674c, 0xb72f7cf5, 0x34f60f91, 0xaec41216, 0x5c86c8ef
.word 0x3b33b956, 0x72edd56f, 0xaf903af1, 0x28861591, 0x83fc04f0, 0xdd92c77e, 0x42491ad1, 0x6d026390
.word 0x92c7fb62, 0xa16e5521, 0x6d82e00d, 0x3a948143, 0x14f75429, 0xe8b4f263, 0xd4911163, 0x50362cf9
.word 0xc8dc23f1, 0xa72e512a, 0xb7628204, 0xbd1695dc, 0x782b4097, 0x6cbb27e2, 0x4cfe7562, 0x54b9b3a8
.word 0xe610f0cd, 0x871ced32, 0x6ba91d5d, 0x8390daa2, 0xbd9366bb, 0x045e4688, 0x9b7ada88, 0x98670fcc
.word 0x917c0dcc, 0xb828a626, 0xc17a34ea, 0xc8f9fe4e, 0x7c649a28, 0x124a23fc, 0x8c00b6e9, 0xa7a48b1f
.word 0x9047ef81, 0xccfcf822, 0xd23fd41d, 0x4dd13041, 0x979e14fc, 0x787aeaf5, 0xd0896747, 0xb8d19011
.word 0x0e761026, 0x9230d5b3, 0x1fdc68dc, 0x69f8e3de, 0x063d38a2, 0xaad22038, 0x5b4ee13a, 0xc462184d
.word 0x0c75e86a, 0xcb6a3302, 0x34574c9a, 0x901ba647, 0x5672ed63, 0x40ba91c1, 0xc782e6fe, 0xbfbafb65
.word 0x75130ad5, 0x16e25248, 0x9cbbe507, 0x2c577a04, 0x7fe344c2, 0x59615671, 0x5cfe947e, 0xbe777cac
.word 0x93ba71b3, 0x97ed51a3, 0xdc04ea8d, 0x78d08abd, 0x86029239, 0xb2dc1643, 0x1f84b68c, 0xd59ca80e
.word 0x93da5fde, 0x57f3bc48, 0x5f4e65fa, 0x8f8a4420, 0x227f0153, 0x7bba004c, 0xc1f0ae1b, 0x1474ce11
.word 0xc7708df5, 0xee2867e1, 0xa6c2dbbc, 0x2bfa3345, 0x535c07a3, 0x46ccfddd, 0x8ce1f474, 0xa582bb2b
.word 0xc536cae1, 0x6ea5496f, 0x2dc16bde, 0xfb90679e, 0xe4c97d92, 0x9ab4597c, 0x8f6dbb2d, 0xa924b8ee
.word 0x06912f8e, 0x5889b39b, 0x2016451e, 0x7fab30b0, 0xf47d24b7, 0xfc9f6124, 0x14f9592d, 0x5e045d1a
.word 0xbfe79e9e, 0xeb229a7e, 0x79f2f4bc, 0xbd33bfe6, 0xda5141b6, 0xacaecd84, 0xa2d6f970, 0xa8809900
.word 0x80b44cc2, 0xbc587072, 0x663dba1f, 0x62f2338b, 0xeb24fe71, 0xf41f14fc, 0xb4522e8f, 0x901e5e51
.word 0x42a6db95, 0x3bdb1685, 0xf946a6fd, 0x3e2ba23e, 0x027a929b, 0x76da9fbf, 0xa676d65d, 0x33c19d77
.word 0xb5c1f09c, 0xae4bf518, 0x691de145, 0xcad06256, 0x237fe9af, 0x36760540, 0x1767a44f, 0x1242c231
.word 0xc271bde7, 0x676da7bd, 0xfa810785, 0x95a4d044, 0x058995cf, 0x336b8aba, 0xbf2d7649, 0xf1b6076e
.word 0x2e085991, 0x34c79f6b, 0x20267dc5, 0x5b8eb577, 0xa0c9484f, 0x3c155433, 0x0e9d8ff9, 0x1c27ceab
.word 0x4282d11b, 0x88e2091c, 0x5fec1bf1, 0xbfeffc15, 0x5cc46bc5, 0x11b0e72f, 0x8b0ed168, 0xb3b6e645
.word 0x34ef9502, 0x9902e846, 0x46dc1e9c, 0x39a776a0, 0x31f1f244, 0x09cbe606, 0xb7952448, 0x9014f2a0
.word 0xe50451d0, 0x9df89014, 0xbe69e547, 0xd79ae10b, 0x06edb995, 0x562ff786, 0x195642da, 0x102e7bf3
.word 0x69b13bcf, 0x8a6f0a76, 0x0867a15b, 0x5899e196, 0xc0a38775, 0x5cab3a95, 0x192adcb2, 0x65f54035
.word 0x9cfab7b0, 0xb16f121c, 0x45324489, 0xf2b494f9, 0x539b728b, 0x26790e9c, 0x13cf26cb, 0xe72cf8c2
.word 0xca5c8baa, 0x7bd04ced, 0x84a35f54, 0x22acd6ba, 0xcf9893b9, 0xd70d5851, 0x8fb4baca, 0x3ba06e21
.word 0xd5db2365, 0x2f9cc5a0, 0x47ce72f3, 0x840be5d7, 0x4bb11242, 0x5c900041, 0x21e22253, 0xfd03a5a3
.word 0xd884ce53, 0xbc8f3580, 0xbd7348e5, 0xa4e0965a, 0xe47fab9e, 0x77c53e34, 0x49fadce7, 0xcc77f13d
.word 0xc4a18a75, 0x88f770eb, 0xadf606bc, 0x10e18fc7, 0x7736f5eb, 0x0bc8c86f, 0x315062a8, 0x5677839a
.word 0x6fcb799e, 0x853a48c1, 0xd0dbd564, 0x63a1ba34, 0x33f57967, 0x91c2aa73, 0xcb675a45, 0x4e6e69e1
.word 0xca27c8e1, 0xb8e01161, 0x5fbaf210, 0xac328968, 0xf7996c96, 0x0b2c4462, 0xb7486a26, 0xc2d9264e
.word 0xc856511b, 0xe0f6907d, 0x984675a3, 0xc4f04094, 0x4f9962a6, 0xbf60b758, 0x936959ab, 0x83902f4f
.word 0xbd34be4b, 0x3ae5df02, 0xd6968874, 0xc7017585, 0xc63cbbf7, 0x246a2f68, 0x2ad88b42, 0xd561d48f
.word 0x6de8fe20, 0xde71e450, 0x24ba44eb, 0xcef7c910, 0x489a547d, 0xb47609cd, 0xb6d9de86, 0xf99c1442
.word 0x49fc1d4a, 0xc1834dcf, 0xfc6383f7, 0xac8ca6e0, 0x557a8962, 0x655d6c91, 0x2dcab999, 0xa299d154
.word 0xe4898202, 0xb6881134, 0xb97bc83a, 0x6117afd6, 0x9b6bcb66, 0x9a8adae2, 0x56685f99, 0x93873f7d
.word 0x74ec6f32, 0xe48cc563, 0x9b430162, 0xf2083d57, 0x16ab5a3c, 0xd6de2aa9, 0x4b0d05c7, 0x693ef065
.word 0xe78ce671, 0x4f6c7e22, 0x64ba452a, 0xa60faa13, 0x30bcae94, 0x2aef0333, 0x1195758d, 0xb263b966
.word 0x37a4be2e, 0x687ca128, 0xef989040, 0x35b4e60c, 0xe7b88d65, 0xf942d638, 0x8aa6a12d, 0xfcf9cf15
.word 0xcdbe3a62, 0x3903dce9, 0xf74b0e4c, 0x7daa223f, 0x0537f352, 0x9d15b970, 0xbcedb5bd, 0xe76d81ac
.word 0x0526199c, 0xaaa28629, 0x68f9da6d, 0x081471c1, 0xf284cc57, 0x2520e579, 0x7cb84e10, 0x73694424
.word 0x3831e098, 0xf88e5f92, 0x9b3234f1, 0x15710ce0, 0x7457130e, 0x3667c385, 0x06c801e0, 0x21abfa70
.word 0xec48b479, 0x6f582e9c, 0xc429c7c0, 0x9af6e17b, 0x5b2dca14, 0xfb98f6e6, 0x56563bee, 0x728edc38
.word 0x1683342b, 0x36466784, 0xe17a2a0b, 0x5f22bbf1, 0x74bab4f4, 0x83efb3c3, 0x34c9c612, 0x7129aa06
.word 0x77c2f7bd, 0x54ed169e, 0x342a7ea5, 0x97776aa3, 0xb67df99b, 0x7e41343f, 0xd8d889b8, 0xf3bf8c93
.word 0x92256331, 0x5ca24162, 0x69d07d80, 0xd42053aa, 0xcfc4c57c, 0x8158ddf1, 0x2a0a81bd, 0xa045a68e
.word 0x3e46c089, 0x38df75d4, 0xe933a945, 0x92ec99f2, 0x1c35e6bb, 0xdbbf504b, 0x8862a6ef, 0x21145209
.word 0x4fa839bd, 0x65402a01, 0x1556ad97, 0x699b6e2d, 0xe079e164, 0x5ed4c42a, 0xf9570029, 0xbcd791ef
.word 0xaf2e7994, 0x27f88d64, 0x1ecd987a, 0x3680790f, 0x6ad40336, 0x3c272bb1, 0x98896331, 0x569deb43
.word 0x28d26ff0, 0x3675e8d3, 0x8e6898d9, 0x9ab24fee, 0x845cf760, 0xe20bf5c1, 0xacc89990, 0x06a6be24
.word 0x8eb1968b, 0x19235653, 0x711eb008, 0x489ccd7b, 0x88eb6058, 0x1bf5da06, 0x19c06c40, 0x6d004e86
.word 0x173f3943, 0x0335a5a6, 0x22c0db28, 0x2edbc2d6, 0x064a0545, 0x044bb786, 0x7e801af2, 0x69161946
.word 0x887105b3, 0x3461aae0, 0x3614dcb1, 0x1a0e176b, 0x87b3ae82, 0x51020f0f, 0x277da95c, 0x02ed01b7
.word 0xdfc4317b, 0x88244d22, 0x058c923e, 0x62f493d3, 0x08083461, 0xb0745e0a, 0xfb0c24a0, 0x6f992547
.word 0x187796cf, 0xdf6fadd6, 0xe724e85a, 0x04faa095, 0xdc8fce1f, 0x740ee207, 0xef24c423, 0x2c9de7c8
.word 0x6937a414, 0x11e5b85a, 0x69f34feb, 0xe83bb93e, 0x8bcc6aaf, 0x17a67a0b, 0x94a7efd1, 0x78bd8089
.word 0xde84b867, 0x93a96c24, 0x122fba9f, 0x9a4a1502, 0x2b72c647, 0xdd76caa4, 0x8f15159f, 0x6afd402e
.word 0x0017b8f9, 0x051b2055, 0xdfdcd441, 0x9bde2ad9, 0x801a29a6, 0x3cc83eb3, 0xbaf4a4ae, 0xf3ac405c
.word 0x7462a470, 0x2c0888d7, 0x6943027e, 0xc49c2d93, 0xd52f46b7, 0xbf502d93, 0xb1e19e3d, 0x47fd416c
.word 0x97399dd5, 0xda227e4f, 0x2e79a67a, 0xf2c635d6, 0x5564d282, 0xe2731bad, 0x497f81a4, 0xa9a26d53
.word 0xfda6e621, 0xcdc37c70, 0x82c1610c, 0x9f1e2544, 0x220b6401, 0x1b970563, 0xdf2ac3fd, 0xfb515476
.word 0x3e2df765, 0x92fc2d36, 0x75b3d177, 0x81263e53, 0x310a645e, 0xa4880c2e, 0x2d4435ef, 0xfc06be14
.word 0x6c1ddfe8, 0xc786746d, 0xe9ca4cba, 0xc41eef71, 0xcf3a15f0, 0x293582f3, 0x313fb5ec, 0x29c8490b
.word 0x59d8fa6f, 0x59c9e349, 0xa8543c2f, 0x0cd678ec, 0x00bb0be8, 0x30680c63, 0x3768e52a, 0x260dec90
.word 0x2fe0ca2b, 0xd25653ef, 0x52ac0ea6, 0xb16c17b3, 0xb322da47, 0x01c0a58e, 0xc42c1ae6, 0x96f3ade0
.word 0x14868448, 0x31892286, 0x9c550f52, 0x785551ea, 0x97a61edd, 0xd584cac4, 0xc077ad27, 0x8b6e81dd
.word 0x0622398d, 0x192c1031, 0x10f9a7c7, 0x456b89d6, 0x9863ed50, 0x6da63835, 0x2a67b70f, 0x7a2d2704
.word 0x678017c3, 0x907f7ee0, 0xc9beada9, 0x60015b19, 0xd67a83d8, 0x61a685ce, 0x6df68654, 0xa1fc9ea0
.word 0x3d8d29e5, 0xb45161ca, 0x030f50e8, 0xcf5dba51, 0xefac5ab7, 0x99664bbb, 0x31ecd6fc, 0xb6b6148e
.section .s_region_1,"aw",@progbits;
s_region_1:
.word 0x537c8a61, 0x7bc306a8, 0xc5f2c6fd, 0xfda5afbe, 0x65e7f539, 0x76d9e7df, 0x47c94e94, 0xdbc1876a
.word 0xf657b96a, 0xa66ae7ea, 0x19bc5621, 0xdd37ec2c, 0x69239aaa, 0x7cdda1aa, 0xf0a2f6dc, 0x32a70c39
.word 0x36066679, 0xd08c2f58, 0x7e86cb00, 0xf3ca2956, 0x1ef2b34d, 0x6a7aa44b, 0x35c0f5f9, 0x9fca8d46
.word 0xd212bff6, 0x22c27fac, 0x42683f2e, 0x51ab48f3, 0xeca5ca63, 0xc1b18c96, 0x2de40564, 0xd37b62b3
.word 0xdf3d0ce8, 0xe4110feb, 0x07e17e0f, 0x86d469eb, 0x7d962e5f, 0xaa1f5a13, 0x994f2ab7, 0xfac13bc0
.word 0x3837972a, 0x44edd78e, 0xcf56f145, 0x58d58f1f, 0x9e12c305, 0x9cf256e8, 0x0c9178d5, 0x74b6df1f
.word 0x927d8643, 0x9a92ca41, 0x0c031268, 0x4e9eaa48, 0x40fbaea0, 0x9eede444, 0x2b0fef82, 0x004b63dd
.word 0x9da7255a, 0x2a77d363, 0xfd5c9981, 0x288d619f, 0xd933edac, 0xbc67cec3, 0xae45b2cb, 0x60f9856a
.word 0xbfa98201, 0x335d21fe, 0x755e6bbd, 0x5a40c147, 0xd24824f2, 0x9957da22, 0x24469b75, 0x2c2ddb41
.word 0xa782646e, 0x7db1c163, 0x8c7ed9ab, 0xfb9cf112, 0x3d4a4134, 0x4fee7a08, 0x5504e40e, 0x574c4f56
.word 0xe413b9bf, 0x44be36c2, 0x5c17ca10, 0x6486f637, 0xcb414814, 0x66b42878, 0x46ccee40, 0xc50aa9b1
.word 0x4c67b1e7, 0xaaba4333, 0xd8e7b29e, 0xbc8fbe49, 0x2c7f3b68, 0x4b3c03fe, 0x0924594c, 0xc4a0b712
.word 0xfec1c180, 0xfed48d46, 0xcbb7a5f5, 0x26cfdaf9, 0xd6c523a8, 0x7e564803, 0xd66a8121, 0x117b5af7
.word 0xcee0fb59, 0x658f4274, 0x6f581688, 0x3a110088, 0x538ad6d0, 0x040a04e8, 0xed2a3f47, 0xee93f06c
.word 0x2173ee0f, 0xcfb03424, 0xe74c55c0, 0x5d39ba1b, 0xfb7a8e01, 0x0afcd607, 0x75b20ad1, 0x9e08dc0d
.word 0x05fc41c0, 0x3fc5b874, 0x728ab887, 0xedd83c29, 0xd895d1cb, 0x7c5ae2ea, 0x2335f764, 0xc2fe698e
.word 0x7bc82db3, 0x132b3ad5, 0x621625fa, 0x317c5f47, 0xcfa50e7f, 0xa198c8bb, 0x72a5bcb1, 0xaa6d975d
.word 0x1397f4dd, 0x26409ceb, 0x41e3fea8, 0xc408a30d, 0x58bc2acd, 0x7f0a2caa, 0x62adec59, 0x72e0bb5d
.word 0x468c293e, 0xc285ab41, 0xaf0d0224, 0x77811a21, 0xd9b862f0, 0xaf8cbaaf, 0x63c724dc, 0x71411dbd
.word 0x1c94b022, 0xeedda80f, 0xb753b05c, 0x9e66cfab, 0xd148f6f2, 0x5ffbc2d8, 0xf6b02dad, 0xfb9729f5
.word 0x10dbebae, 0x97230c53, 0x155650a9, 0xcd0db628, 0x15ec9b64, 0xc5a71023, 0x8e50b220, 0xb025b639
.word 0x3c68af69, 0x81d9c8f7, 0x8ac1ab25, 0xaa53f376, 0x0106de19, 0x32fe7b25, 0x1271e9cb, 0xc1200f5f
.word 0xa48c5d10, 0xb48722e1, 0x5016899b, 0x20399f7b, 0x1065d8cf, 0xc5ae68ef, 0x36709795, 0xe30d4959
.word 0xaf7e76d3, 0x8310912c, 0xb890bb99, 0x6b09a368, 0x77c31d63, 0x080d84fe, 0x0a511a3c, 0x083c7bd5
.word 0xfce2ec90, 0x2265e700, 0x44487741, 0x420db33a, 0xb9e070e5, 0xdb35cd2e, 0x92ed936e, 0x0de3e238
.word 0xe763bd76, 0xa245e873, 0xa4feb37f, 0x3cb3bda3, 0xb2dd6c9f, 0xfbe384f6, 0xee237f77, 0x48801a62
.word 0x38d4ce83, 0x6feec2a4, 0x1d16441c, 0x6090a92e, 0x87fdde52, 0x153cb9f3, 0xf7f42d90, 0x0d32ea76
.word 0x3512d3fc, 0x6181e95e, 0x8bc0fbeb, 0x20889061, 0x1f79e82a, 0x0a8e61d3, 0x6195b103, 0xe2c5470d
.word 0xd534dead, 0xf1c45d20, 0xeb48cd8f, 0x8e739dd4, 0x6ab695dd, 0x008f1d5a, 0x035b23c9, 0x719cc82f
.word 0xd0eee03f, 0x7f026d43, 0x6efa107c, 0xbf33f4ab, 0x4676b17e, 0x7b340b89, 0xf1b0dd70, 0x5eed4b58
.word 0xe7fb4b2f, 0x434daf03, 0xd6b7cd06, 0x120189b2, 0x030e5eea, 0xf48e44db, 0xef7ab6e9, 0xe1281dbb
.word 0xe9858e93, 0xaebdc5b1, 0x34106b13, 0x26a1840d, 0x83862693, 0xc3c0a434, 0x9220c1e4, 0x1bf4d720
.word 0x83353359, 0x6ec634cc, 0xc4f898d5, 0x24c8c597, 0x6139c9a7, 0x101b54b5, 0x6332f19b, 0x80e3d117
.word 0x27c2131c, 0x1e6bfb5d, 0x8390025a, 0x2adc131b, 0xdd76421b, 0x8f03743a, 0xd350fdcd, 0x3033fa6e
.word 0xac03c2ad, 0x7ceec9ad, 0x71bf9a60, 0xbe9942d0, 0x11789919, 0xa8512aef, 0xb9aad5ec, 0x6a890b58
.word 0xe30a8eb9, 0xdab329de, 0x75ab8736, 0x0d740351, 0x600163e8, 0xb91e4cf4, 0x9993c2d7, 0x54a4c723
.word 0x0966aba9, 0x7275423e, 0x9028194a, 0x786fb049, 0xa7df096a, 0x9a04cf22, 0xedb7794a, 0x156a136a
.word 0x71a1de25, 0xc367ef43, 0xc211adb6, 0xc3c48980, 0xd8c99ed1, 0x4c876868, 0xcd5da36d, 0x77fee192
.word 0x7869bae5, 0x6dbd2bc3, 0x62bb7950, 0xe823520d, 0x6c2e3ceb, 0xe6d0ce15, 0xccc7a063, 0x187a494a
.word 0x3f1a742d, 0xcefaf820, 0x50d45cb1, 0xbbe5bfc6, 0x0fc3b114, 0x9cb7f99c, 0x4d8655ef, 0x03fa33a5
.word 0x4fe1d086, 0x5b6326bf, 0xcbf94315, 0x834549f5, 0x9f8987d8, 0xa168e990, 0x0bc61d25, 0x3ea51b7b
.word 0x09218394, 0x92440180, 0x8924b703, 0x50b7cc2b, 0x3415c009, 0xf0e43248, 0x620c4cd0, 0x38cdb3ea
.word 0xf1dd1b72, 0xabe174cf, 0xe8c5b2e8, 0xd2935a81, 0x9c775daa, 0x6c257e7e, 0x73968ee9, 0xebdd68c6
.word 0xf3667f0b, 0xd60530c1, 0xd6c208e2, 0x85d25b43, 0x3beb3927, 0x7e5c1b21, 0xe0b2ce27, 0xe492996e
.word 0x1813b524, 0xd39b1425, 0x88e25f38, 0xaabdaf0c, 0xb630ebd8, 0x7afc5262, 0xc4eff954, 0x89443919
.word 0xe30ace3e, 0xfa734966, 0x9c434cbc, 0xc5f8a8d7, 0x98dc40fe, 0xd1b453d8, 0x81b9e465, 0xc2acba78
.word 0x55ca3aac, 0x7e53acf7, 0x4e57074d, 0x2f65abd9, 0x520362aa, 0x67dfecd3, 0x8916857d, 0xc2d33784
.word 0x6bcd6d80, 0x3b9c5672, 0xb9c9e359, 0xf142a013, 0xaae8bc8a, 0xf4022504, 0x83015538, 0xdf5589c0
.word 0x83ee0e22, 0x2a84a426, 0x3c484bb8, 0x3d5ea97f, 0x82117fdf, 0xcea1af64, 0x8272e9ae, 0x5d3d67b3
.word 0x901e99b7, 0x95b3ca6b, 0x14694fa6, 0x0b46b121, 0x0d4aafa3, 0xa3335a2b, 0x6585d27f, 0xa8c8d854
.word 0xa5bb5249, 0x05c42eae, 0x3dc581c3, 0xdcfb2e5a, 0xd6f204b3, 0x94c4d4cb, 0xac5ef6f5, 0x214ed83d
.word 0x72f067d2, 0x795e44cd, 0xb1b30a91, 0xe43a7b31, 0x64441a62, 0xdbc91dd0, 0x6727d518, 0x10d3dc6b
.word 0xacb340bd, 0xaa183e2c, 0xe3076c31, 0xd77c3768, 0x22f4793f, 0xb3d6ac4c, 0xcc70439d, 0xe2fd4279
.word 0xe1b9a51f, 0x119695e0, 0x8fe24210, 0x4176aa8a, 0xf728f85b, 0x21d1360f, 0xe1c006a3, 0x2c46552d
.word 0xdfa05933, 0x48d3f6ef, 0x2e7a39e8, 0x8af42605, 0xa56d6d1a, 0x359e647d, 0xb8d035cd, 0x53880593
.word 0x80279820, 0xda48298e, 0xea0257d8, 0xc2d22de6, 0x6498bac6, 0x0cba34df, 0x021a1049, 0xadb2ab64
.word 0xb183006a, 0x5be0fa06, 0x713a68a5, 0x30266519, 0x16c28c22, 0xbf7cc7af, 0x49ddaa5f, 0x1a7049df
.word 0x5d06d174, 0xd076fcdd, 0x4f00a826, 0x65d68511, 0x5e881166, 0x60f6b636, 0xefede110, 0x6c182ac2
.word 0x13cece2b, 0x68c561d3, 0xcd84877a, 0xe015698d, 0xf20ec7aa, 0x1cc03362, 0xf1a7736a, 0x530b4b54
.word 0x99d5d685, 0x1ed2f7a1, 0xb3cce1e8, 0x8b86eb72, 0xd19feab2, 0x45281549, 0xc3b2a1f7, 0xaae2a4d6
.word 0xf084eb8f, 0x197f10e3, 0x0cedf61e, 0x8de28eb7, 0x5b00f0b6, 0x64f95b57, 0x23d5ac25, 0xedaf1c75
.word 0xcedd8a29, 0x8ab6782f, 0xf494e1ed, 0x16754738, 0x235b67e2, 0xa64c78e6, 0xc2a06325, 0x0ad3df20
.word 0x3ae7f089, 0xc2b0cc66, 0xa8b3e978, 0x67e4d590, 0xc6a38116, 0x6bb1a159, 0x2ccc5383, 0x731faad9
.word 0xd9a7b144, 0x918b059d, 0xa519047e, 0x03341ecf, 0xd518280c, 0xaab19b05, 0x1095e73a, 0x21c0d740
.word 0x172c3c81, 0xb8e85416, 0xc913f4f7, 0xa4010202, 0x430dfcd2, 0x48043fc9, 0x08c628c8, 0x5359fa3c
.word 0xa0224cd6, 0x9cc0a8f2, 0x40101709, 0x149212a0, 0x9d84715a, 0xc7697c83, 0xd785826e, 0x7c91bdd3
.word 0xb3ab4e74, 0x7d08f135, 0x825286c0, 0x6d4ec428, 0x02d9a439, 0x5a864e72, 0xb5b60701, 0x9d270287
.word 0x794b0fd3, 0xdf5ebce8, 0xfdbbe2cd, 0x7a50ae8f, 0xa148337f, 0x5903b355, 0xc2e45ac2, 0xbb26a1a3
.word 0xb1f16b3b, 0x0d8c249c, 0x50af389b, 0x1c2b6300, 0x5cc608fb, 0x75c0633c, 0x01931c56, 0xbf27d75d
.word 0xc682d6e6, 0xbba17e36, 0x6ce0b171, 0x37a9c7d2, 0xe9cc09f1, 0xe594c06b, 0x3fe287c5, 0x5d79225c
.word 0xe3ab1e38, 0x88fb77e3, 0x99255e1e, 0x22e4c715, 0x80ca15e9, 0x06f37638, 0x1602ef02, 0x9d90a164
.word 0x4ca5327c, 0xeb774d80, 0x4e3c0f8c, 0xeaa668c1, 0xcb1954fb, 0xfe3db858, 0x529e08a6, 0x6e73f993
.word 0x12375086, 0xaa0a2954, 0xd570ed1c, 0xa27d4581, 0x011b9dbb, 0xc599ac4d, 0x7b2d9988, 0x3bf5e4e8
.word 0xbba79030, 0x6a31672b, 0x0324b277, 0x0fd48e59, 0x2b1c431e, 0x383a0fea, 0x90d8e94f, 0xaa42cd6d
.word 0x55e0da90, 0x1bc0961d, 0xc58baa9c, 0x2f2e575c, 0x9a8db7de, 0xda37c81c, 0xd4f170de, 0xe6c3c87a
.word 0x4a59b70f, 0x943737fa, 0xc60be380, 0x81f3812d, 0x486628be, 0xcd54c5f3, 0x7fe7fdda, 0xa113a15d
.word 0xb9ddc170, 0xae417f12, 0x584bcce2, 0xe8d45b95, 0x172f24fb, 0x667b6538, 0x2a81f625, 0x5aaf0c90
.word 0x22f7c3db, 0x2acbed8c, 0x5ba692bf, 0x4a665cf2, 0x52a2fd69, 0x74dee2ee, 0x13878689, 0x3ee992b4
.word 0x37ef1ac8, 0x883356f4, 0xfc4a1fdb, 0xf7a0616f, 0x5b01e18c, 0x051c35b8, 0x4dd6a8ee, 0x627d552a
.word 0xee590019, 0xcba4a56b, 0xca2e9c20, 0x0b1d6281, 0xd2dc0235, 0x60083e57, 0xf7f38f5b, 0x757d8217
.word 0xca453b98, 0x55028359, 0x5c8c82f1, 0x9e515cbf, 0x2385b818, 0x7b44881d, 0xc1b79b5a, 0x61e1cb83
.word 0xe15c8fe1, 0x2a54637e, 0x7b39bb57, 0x32b907b0, 0x22fbd96e, 0xe2c1ad62, 0x68fa8551, 0xca018980
.word 0xf78a03de, 0x157d1efc, 0x2c44dd1d, 0x835f0a9e, 0xbdc6a250, 0x224f8232, 0x9e793b7d, 0xfd665109
.word 0x4118cdd0, 0x23519011, 0x13e91427, 0x2af42a2e, 0x6800a394, 0x71d68d74, 0x6fda8a8d, 0xb7ed013b
.word 0x15d716b4, 0x8f5a34ee, 0x8341ccc7, 0x7ce097b0, 0x86974656, 0xbca8b7f6, 0x17cc9f3f, 0xbe273c3a
.word 0x9eb6d3b4, 0x4a1cc03a, 0x305c44ec, 0x14b34a3e, 0x832a8a0c, 0x6de43c5f, 0x03991c9e, 0x77b2a58e
.word 0x8b8acae2, 0x28f766da, 0x186fc0bc, 0xe711c71b, 0x06b6c7ae, 0xc586f94f, 0x7dc57c53, 0x5a3e2b86
.word 0x02944088, 0x245ed85c, 0x33dd3b47, 0x9dd72418, 0xf7044257, 0x8c08cec4, 0x74457f87, 0x275acb6b
.word 0x70507089, 0x702db9d7, 0x21c4a666, 0x9fb20c7a, 0x3d1cfa33, 0x5f0b758d, 0xc6720106, 0xc79e799f
.word 0x84ac11fb, 0x41aa9271, 0x5475f423, 0x31090351, 0x3262327a, 0x962cc6c7, 0x32207dbe, 0x4b3d87e9
.word 0x50d70394, 0x35794ecd, 0x7eb049e7, 0x5c5f60dd, 0x1468abec, 0xc0f33e81, 0x6225a59c, 0x7dd0c597
.word 0xee2f4df8, 0x83130ffd, 0x8802d801, 0xd75f5720, 0xf3808681, 0xae67f675, 0x256a44c6, 0x21fdfa59
.word 0xd53a829c, 0x9345c41c, 0x134bf514, 0xb75cc399, 0xddabbf50, 0x5ce0681e, 0x367132c3, 0xd5041f27
.word 0x69180237, 0xb3d9d5b3, 0x233e1abf, 0x1c86298e, 0x713d3409, 0xae353f1f, 0x6fc9f149, 0xb5f00192
.word 0xcd4b25e1, 0x5adbaa8f, 0x46747904, 0x7bae805f, 0xbd3a33ee, 0xb8ce1eeb, 0x87e9ecdc, 0x4d3743bf
.word 0x9589859b, 0xbebbe6eb, 0xe73576c5, 0xf19de325, 0x890fcc53, 0x0336da2c, 0xe1d90217, 0xadd26e7b
.word 0x43365732, 0x49138329, 0x6dd435c8, 0x2c8ae364, 0x14d86248, 0xe84d037e, 0x251716bc, 0xc9e01b55
.word 0x37da222a, 0x78fb7d5b, 0x0a87777a, 0xe48ff791, 0xc4d7a71d, 0xc06ecda5, 0x09f97c0c, 0x094ee2a9
.word 0x24b932c3, 0xfedeef5c, 0x04f8dc7c, 0xd7d7a9b7, 0x27c97fe9, 0x8ae49ea7, 0x3e392fa7, 0xe4aef8d3
.word 0xb3f413b1, 0xcdebc16c, 0x21ca9c0b, 0xa6e2cef5, 0x60f36cd4, 0x7c963de6, 0x050eacf7, 0x8aba9b5a
.word 0x51e7a7d4, 0x131e1360, 0x7956aa79, 0x7c1369e8, 0xbb1549b6, 0xb3d129c7, 0x8ce3e5e7, 0xc1ec4512
.word 0x96a6e184, 0xd78d41aa, 0x540c8e7c, 0xd3067e0d, 0x196a87f3, 0xd27156e1, 0x2ac9942e, 0xaf0522a4
.word 0x0054758b, 0xc7cc2edd, 0xb80b8432, 0x6ee79225, 0x75820620, 0x4575ed0c, 0x67c2b979, 0xfc204a68
.word 0xf808a184, 0x9bb57c9f, 0x473ec845, 0x7b15e7aa, 0x352cc6e4, 0xc33fa995, 0x3e460716, 0xb440b05d
.word 0x4748db9f, 0x282c1e8e, 0xb49c7e76, 0x869dea3a, 0xae0c9837, 0x39066209, 0x8c0d7512, 0xcd8ed11a
.word 0x207ff0ec, 0x951f5661, 0x0f4fa821, 0xa3f1a0ee, 0xa4d3223b, 0xe20ddb00, 0xe0f7010a, 0xc6017e5c
.word 0xa09a364f, 0xa5c5fc6c, 0x89e5a833, 0x9caebc67, 0xa3d77f87, 0xcfddf8f6, 0xe5b85059, 0x046271cb
.word 0xc17dd3bf, 0xe100c6f7, 0x7e0e437c, 0xafa6f188, 0xc558ac3f, 0x91a58049, 0xb61b36e6, 0x110e6149
.word 0x2ba484ca, 0xf96e6fbd, 0x8774fbb7, 0xd38745de, 0xf0d8ae49, 0x5c27631b, 0x3c079bde, 0x365ab3ce
.word 0xc8c5fccc, 0x414cab4d, 0xfeb3eede, 0x1758a6b5, 0x1c098e3d, 0x6fb3577b, 0x7a76c153, 0x32c1ecc3
.word 0x6cacc07a, 0xd9950472, 0xddbea2b4, 0x8e752abd, 0x82602f27, 0x9be60866, 0x96b4644f, 0x7a13f8ca
.word 0xd928d14d, 0x454d97c6, 0x379df694, 0xb1ccbf5a, 0x5f944567, 0x07278634, 0x11199e29, 0x0972cd69
.word 0xcbfc0529, 0xa366c052, 0x1252e88b, 0x86da3fe8, 0xb81ada9d, 0xe3b744c6, 0x9805f64e, 0x88393465
.word 0x80ad2a1f, 0x20ca438f, 0xa43ea0b0, 0x2f1b7c69, 0x480042a4, 0x65c6d102, 0xee971cb7, 0x55837fdd
.word 0x4797cd65, 0xbfdf1f27, 0xfb144a7d, 0xaa0cf7ca, 0xcb277ef4, 0xefd1a57a, 0x051d3f11, 0xbee1c434
.word 0x4c8c6a81, 0x3648ecef, 0x0c35aa8a, 0x12953359, 0xefdcd985, 0xe9c134a8, 0x5f9f1c8c, 0x62e51169
.word 0x4944e94f, 0x6c1c10ef, 0x6329a66d, 0x2f9de076, 0xbec7d4cb, 0xb425aa87, 0x4d24e6ea, 0xfc5e042b
.word 0x0e2d78ae, 0xdc37cccc, 0x5e2fed0b, 0xd718849b, 0xbe551a25, 0x5d8b9c30, 0x9d254dd1, 0xa23c9bc4
.word 0x2a6b151d, 0xf9adda87, 0x79823757, 0xb3870c93, 0xa90f46b0, 0xeef6bec2, 0x2b0a3513, 0x18151490
.word 0x89371d50, 0xdb6083bd, 0x7ffabf51, 0x39ca0436, 0x44d78e6e, 0x317343fc, 0x0848c769, 0xeacdf45e
.word 0xc0998994, 0x7d1a6ec5, 0xd569dc90, 0x49483eeb, 0xeb76c21f, 0x2874ec54, 0xb455513d, 0x55526a5b
.word 0xebed96cd, 0x005b25d8, 0xd15ffa7e, 0x16b441ea, 0x99964a31, 0x15bb285f, 0x9bc62a76, 0xc2495bb3
.word 0x4c74099c, 0xec146f0a, 0x4ad64f77, 0x532be82e, 0x3cba7265, 0xbcc516ec, 0x48dca28d, 0xb2395ecf
.word 0x779d6ebd, 0x59f7f1bc, 0x8179a099, 0xde60036a, 0x099d4031, 0x16fbd4b5, 0x94f28069, 0xaa415866
.word 0xd633f478, 0xe9db762c, 0x777bb864, 0x690f09d3, 0x9e0b3232, 0x3eecd306, 0x206a1488, 0x4dfc2abe
.word 0x143798d2, 0xbc818858, 0x4e4e9beb, 0xe908f229, 0x42be8c04, 0x13d27e00, 0x4be2e883, 0xc1208226
.word 0xc60e96c1, 0x8c584817, 0x2398bba1, 0x57611031, 0xb4969289, 0x54403d14, 0x0b8b6045, 0xb2ac4c10
.word 0x911142c8, 0x376b7143, 0x11388f5b, 0x39633f32, 0x8cde7c48, 0xa9d34abb, 0x5b227ac0, 0x4332e3cd
.section .kernel_stack,"aw",@progbits;
.align 2
kernel_stack_start:
.rept 4999
.4byte 0x0
.endr
kernel_stack_end:
.4byte 0x0
