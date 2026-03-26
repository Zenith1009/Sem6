/*
 * opcode_table.c
 * Complete 8085 instruction set table.
 *
 * For register-encoded instructions (MOV, ADD, etc.), the 'opcode' field
 * stores the BASE opcode. The actual opcode is computed at Pass 2 by OR-ing
 * the appropriate register codes.
 *
 * Register codes: B=0, C=1, D=2, E=3, H=4, L=5, M=6, A=7
 * Register pair codes: B=0, D=1, H=2, SP=3 (for PUSH/POP: B=0,D=1,H=2,PSW=3)
 */

#include "assembler.h"
#include "opcode_table.h"

OpcodeEntry OPTAB[] = {
    /* ── Data Transfer Instructions ─────────────────────────────────── */
    { "MOV",   0x40, 1, IK_MOV    },  /* MOV r1,r2 → 0x40 | (dst<<3) | src */
    { "MVI",   0x06, 2, IK_MVI    },  /* MVI r,d8  → 0x06 | (r<<3)         */
    { "LXI",   0x01, 3, IK_LXI    },  /* LXI rp,d16                         */
    { "LDA",   0x3A, 3, IK_DIRECT },  /* LDA addr                            */
    { "STA",   0x32, 3, IK_DIRECT },  /* STA addr                            */
    { "LHLD",  0x2A, 3, IK_DIRECT },  /* LHLD addr                           */
    { "SHLD",  0x22, 3, IK_DIRECT },  /* SHLD addr                           */
    { "LDAX",  0x0A, 1, IK_REG    },  /* LDAX rp (B=0x0A, D=0x1A)           */
    { "STAX",  0x02, 1, IK_REG    },  /* STAX rp (B=0x02, D=0x12)           */
    { "XCHG",  0xEB, 1, IK_FIXED  },  /* XCHG                                */

    /* ── Arithmetic Instructions ─────────────────────────────────────── */
    { "ADD",   0x80, 1, IK_REG    },  /* ADD r  → 0x80 | reg                */
    { "ADI",   0xC6, 2, IK_MVI   },   /* ADI d8 (no register, just imm)     */
    { "ADC",   0x88, 1, IK_REG    },  /* ADC r  → 0x88 | reg                */
    { "ACI",   0xCE, 2, IK_MVI   },   /* ACI d8                              */
    { "SUB",   0x90, 1, IK_REG    },  /* SUB r  → 0x90 | reg                */
    { "SUI",   0xD6, 2, IK_MVI   },   /* SUI d8                              */
    { "SBB",   0x98, 1, IK_REG    },  /* SBB r  → 0x98 | reg                */
    { "SBI",   0xDE, 2, IK_MVI   },   /* SBI d8                              */
    { "INR",   0x04, 1, IK_INRDCR},  /* INR r  → 0x04 | (r<<3)             */
    { "DCR",   0x05, 1, IK_INRDCR},  /* DCR r  → 0x05 | (r<<3)             */
    { "INX",   0x03, 1, IK_REG    },  /* INX rp → 0x03 | (rp<<4)            */
    { "DCX",   0x0B, 1, IK_REG    },  /* DCX rp → 0x0B | (rp<<4)            */
    { "DAD",   0x09, 1, IK_REG    },  /* DAD rp → 0x09 | (rp<<4)            */
    { "DAA",   0x27, 1, IK_FIXED  },  /* DAA                                 */

    /* ── Logical Instructions ────────────────────────────────────────── */
    { "ANA",   0xA0, 1, IK_REG    },  /* ANA r  → 0xA0 | reg                */
    { "ANI",   0xE6, 2, IK_MVI   },   /* ANI d8                              */
    { "ORA",   0xB0, 1, IK_REG    },  /* ORA r  → 0xB0 | reg                */
    { "ORI",   0xF6, 2, IK_MVI   },   /* ORI d8                              */
    { "XRA",   0xA8, 1, IK_REG    },  /* XRA r  → 0xA8 | reg                */
    { "XRI",   0xEE, 2, IK_MVI   },   /* XRI d8                              */
    { "CMP",   0xB8, 1, IK_REG    },  /* CMP r  → 0xB8 | reg                */
    { "CPI",   0xFE, 2, IK_MVI   },   /* CPI d8                              */
    { "RLC",   0x07, 1, IK_FIXED  },  /* RLC                                 */
    { "RRC",   0x0F, 1, IK_FIXED  },  /* RRC                                 */
    { "RAL",   0x17, 1, IK_FIXED  },  /* RAL                                 */
    { "RAR",   0x1F, 1, IK_FIXED  },  /* RAR                                 */
    { "CMA",   0x2F, 1, IK_FIXED  },  /* CMA                                 */
    { "CMC",   0x3F, 1, IK_FIXED  },  /* CMC                                 */
    { "STC",   0x37, 1, IK_FIXED  },  /* STC                                 */

    /* ── Branch Instructions ─────────────────────────────────────────── */
    { "JMP",   0xC3, 3, IK_JUMP   },
    { "JZ",    0xCA, 3, IK_JUMP   },
    { "JNZ",   0xC2, 3, IK_JUMP   },
    { "JC",    0xDA, 3, IK_JUMP   },
    { "JNC",   0xD2, 3, IK_JUMP   },
    { "JPE",   0xEA, 3, IK_JUMP   },
    { "JPO",   0xE2, 3, IK_JUMP   },
    { "JM",    0xFA, 3, IK_JUMP   },
    { "JP",    0xF2, 3, IK_JUMP   },
    { "CALL",  0xCD, 3, IK_JUMP   },
    { "CZ",    0xCC, 3, IK_JUMP   },
    { "CNZ",   0xC4, 3, IK_JUMP   },
    { "CC",    0xDC, 3, IK_JUMP   },
    { "CNC",   0xD4, 3, IK_JUMP   },
    { "CPE",   0xEC, 3, IK_JUMP   },
    { "CPO",   0xE4, 3, IK_JUMP   },
    { "CM",    0xFC, 3, IK_JUMP   },
    { "CP",    0xF4, 3, IK_JUMP   },
    { "RET",   0xC9, 1, IK_FIXED  },
    { "RZ",    0xC8, 1, IK_FIXED  },
    { "RNZ",   0xC0, 1, IK_FIXED  },
    { "RC",    0xD8, 1, IK_FIXED  },
    { "RNC",   0xD0, 1, IK_FIXED  },
    { "RPE",   0xE8, 1, IK_FIXED  },
    { "RPO",   0xE0, 1, IK_FIXED  },
    { "RM",    0xF8, 1, IK_FIXED  },
    { "RP",    0xF0, 1, IK_FIXED  },
    { "PCHL",  0xE9, 1, IK_FIXED  },
    { "RST",   0xC7, 1, IK_RST    },  /* RST n → 0xC7 | (n<<3)              */

    /* ── Stack Instructions ──────────────────────────────────────────── */
    { "PUSH",  0xC5, 1, IK_PUSH_POP },
    { "POP",   0xC1, 1, IK_PUSH_POP },
    { "XTHL",  0xE3, 1, IK_FIXED   },
    { "SPHL",  0xF9, 1, IK_FIXED   },
    { "LHLD",  0x2A, 3, IK_DIRECT  },  /* (duplicate handled via lookup) */

    /* ── I/O & Machine Control ───────────────────────────────────────── */
    { "IN",    0xDB, 2, IK_IO     },
    { "OUT",   0xD3, 2, IK_IO     },
    { "HLT",   0x76, 1, IK_FIXED  },
    { "NOP",   0x00, 1, IK_FIXED  },
    { "EI",    0xFB, 1, IK_FIXED  },
    { "DI",    0xF3, 1, IK_FIXED  },
    { "RIM",   0x20, 1, IK_FIXED  },
    { "SIM",   0x30, 1, IK_FIXED  },

    /* ── Pseudo / Assembler Directives ───────────────────────────────── */
    { "ORG",   0x00, 0, IK_ORG    },
    { "DB",    0x00, 1, IK_DB     },
    { "DW",    0x00, 2, IK_DW     },
    { "END",   0x00, 0, IK_END    }
};

int OPTAB_SIZE = sizeof(OPTAB) / sizeof(OPTAB[0]);

/* ── Lookup by mnemonic (case-insensitive) ──────────────── */
OpcodeEntry* lookup_opcode(const char *mnemonic) {
    int i;
    for (i = 0; i < OPTAB_SIZE; i++) {
        if (strcasecmp(mnemonic, OPTAB[i].mnemonic) == 0)
            return &OPTAB[i];
    }
    return NULL;
}

/*
 * get_reg_code: returns 3-bit register code for 8085 registers
 *   B=0, C=1, D=2, E=3, H=4, L=5, M=6, A=7
 * Returns -1 if invalid.
 */
int get_reg_code(const char *reg) {
    if (strcasecmp(reg, "B") == 0) return 0;
    if (strcasecmp(reg, "C") == 0) return 1;
    if (strcasecmp(reg, "D") == 0) return 2;
    if (strcasecmp(reg, "E") == 0) return 3;
    if (strcasecmp(reg, "H") == 0) return 4;
    if (strcasecmp(reg, "L") == 0) return 5;
    if (strcasecmp(reg, "M") == 0) return 6;
    if (strcasecmp(reg, "A") == 0) return 7;
    return -1;
}

/*
 * get_rp_code: returns 2-bit register pair code
 *   B=0, D=1, H=2, SP=3
 *   For PUSH/POP: B=0, D=1, H=2, PSW=3
 */
int get_rp_code(const char *rp) {
    if (strcasecmp(rp, "B")   == 0) return 0;
    if (strcasecmp(rp, "D")   == 0) return 1;
    if (strcasecmp(rp, "H")   == 0) return 2;
    if (strcasecmp(rp, "SP")  == 0) return 3;
    if (strcasecmp(rp, "PSW") == 0) return 3;
    return -1;
}
