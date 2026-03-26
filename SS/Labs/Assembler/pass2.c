/*
 * pass2.c
 *
 * PASS 2 — Machine Code Generator
 *
 * Uses the intermediate lines and symbol table produced by Pass 1.
 * For each line:
 *   - Looks up opcode
 *   - Encodes operands (registers, immediates, addresses)
 *   - Resolves labels from symbol table (forward references handled)
 *   - Writes a listing file (.lst) with: address, hex bytes, source
 */
 
#include "assembler.h"
#include "utils.h"

/* ── Write bytes to listing file & stdout ─────────────── */
static void emit(FILE *out, int addr, unsigned char *bytes, int nbytes,
                 const char *label, const char *mnemonic, const char *operand) {
    int i;
    char hex[20] = "";
    char tmp[8];

    for (i = 0; i < nbytes; i++) {
        snprintf(tmp, sizeof(tmp), "%02X ", bytes[i]);
        strcat(hex, tmp);
    }

    /* Format: ADDR | HEX BYTES (padded) | LABEL : MNEMONIC OPERAND */
    if (label && label[0])
        fprintf(out, "%04X  %-12s  %s: %s %s\n", addr, hex, label, mnemonic, operand);
    else
        fprintf(out, "%04X  %-12s  %s %s\n", addr, hex, mnemonic, operand);

    /* Also print to stdout */
    if (label && label[0])
        printf("%04X  %-12s  %s: %s %s\n", addr, hex, label, mnemonic, operand);
    else
        printf("%04X  %-12s  %s %s\n", addr, hex, mnemonic, operand);
}

/* ── Resolve operand to an address (label or literal) ─── */
static int resolve_addr(const char *operand, SymbolTable *st) {
    int addr = symtab_lookup(st, operand);
    if (addr == -1) {
        /* Not a label — try parsing as a number */
        addr = parse_number(operand);
    }
    return addr;
}

/* ── Main Pass 2 Function ─────────────────────────────── */
int pass2(Pass1Result *result, const char *out_file) {
    FILE         *fp;
    int           i, error = 0;
    unsigned char bytes[3];

    fp = fopen(out_file, "w");
    if (!fp) {
        fprintf(stderr, "Error: Cannot open output file '%s'\n", out_file);
        return -1;
    }

    fprintf(fp, "%-4s  %-12s  %-30s\n", "ADDR", "HEX CODE", "SOURCE");
    fprintf(fp, "-------------------------------------------------------\n");
    printf("\n%-4s  %-12s  %-30s\n", "ADDR", "HEX CODE", "SOURCE");
    printf("-------------------------------------------------------\n");

    for (i = 0; i < result->line_count; i++) {
        Line       *ln  = &result->lines[i];
        OpcodeEntry *op  = lookup_opcode(ln->mnemonic);
        int          addr = ln->address;

        char op1[MAX_OPERAND], op2[MAX_OPERAND];
        split_operands(ln->operand, op1, op2);

        /* ── Pseudo / Directive Lines ──────────────────── */
        if (strcmp(ln->mnemonic, "ORG") == 0 ||
            strcmp(ln->mnemonic, "END") == 0) {
            /* Just print, no bytes */
            fprintf(fp, "      %-12s  %s %s\n", "", ln->mnemonic, ln->operand);
            printf("      %-12s  %s %s\n", "", ln->mnemonic, ln->operand);
            continue;
        }

        if (strcmp(ln->mnemonic, "DB") == 0) {
            bytes[0] = (unsigned char)(parse_number(op1) & 0xFF);
            emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
            continue;
        }

        if (strcmp(ln->mnemonic, "DW") == 0) {
            int val = parse_number(op1);
            bytes[0] = (unsigned char)(val & 0xFF);        /* Low byte first */
            bytes[1] = (unsigned char)((val >> 8) & 0xFF); /* High byte      */
            emit(fp, addr, bytes, 2, ln->label, ln->mnemonic, ln->operand);
            continue;
        }

        if (!op) {
            fprintf(stderr, "Error (line %d): Unknown mnemonic '%s'\n",
                    ln->line_no, ln->mnemonic);
            error = 1;
            continue;
        }

        /* ── Encode By Instruction Kind ────────────────── */
        switch (op->kind) {

        /* Fixed: single-byte, no operand */
        case IK_FIXED:
            bytes[0] = op->opcode;
            emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
            break;

        /* MOV r1, r2 — opcode = 0x40 | (dst<<3) | src */
        case IK_MOV: {
            int dst = get_reg_code(op1);
            int src = get_reg_code(op2);
            if (dst < 0 || src < 0) {
                fprintf(stderr, "Error (line %d): Invalid register in MOV '%s'\n",
                        ln->line_no, ln->operand);
                error = 1; break;
            }
            /* HLT has same encoding as MOV M,M — guard */
            if (dst == 6 && src == 6) {
                fprintf(stderr, "Error (line %d): MOV M,M is illegal\n", ln->line_no);
                error = 1; break;
            }
            bytes[0] = (unsigned char)(0x40 | (dst << 3) | src);
            emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /*
         * MVI r, d8     — opcode = base | (r<<3), then d8
         * Also used for immediate-only instructions like ADI, SUI, ANI, etc.
         * where op1 is the immediate (no register shift).
         */
        case IK_MVI: {
            /* Check if this is a register + immediate (like MVI A, 05H)
               or immediate-only (like ADI 05H, ANI 0FH, CPI 10H etc.) */
            int reg = get_reg_code(op1);
            if (reg >= 0 && op2[0] != '\0') {
                /* Register + immediate (MVI) */
                bytes[0] = (unsigned char)(op->opcode | (reg << 3));
                bytes[1] = (unsigned char)(parse_number(op2) & 0xFF);
            } else {
                /* Immediate only (ADI, ANI, SUI, CPI, ORI, XRI etc.) */
                bytes[0] = op->opcode;
                bytes[1] = (unsigned char)(parse_number(op1) & 0xFF);
            }
            emit(fp, addr, bytes, 2, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /* LXI rp, d16 — opcode = 0x01 | (rp<<4), then d16 little-endian */
        case IK_LXI: {
            int rp = get_rp_code(op1);
            if (rp < 0) {
                fprintf(stderr, "Error (line %d): Invalid register pair '%s'\n",
                        ln->line_no, op1);
                error = 1; break;
            }
            int val = parse_number(op2);
            bytes[0] = (unsigned char)(0x01 | (rp << 4));
            bytes[1] = (unsigned char)(val & 0xFF);
            bytes[2] = (unsigned char)((val >> 8) & 0xFF);
            emit(fp, addr, bytes, 3, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /*
         * IK_REG — used for: ADD, ADC, SUB, SBB, ANA, ORA, XRA, CMP
         *                     LDAX, STAX, INX, DCX, DAD
         * All single-register or register-pair ops with single operand.
         */
        case IK_REG: {
            /* LDAX / STAX use register pair (B or D), encoded differently */
            if (strcmp(ln->mnemonic, "LDAX") == 0 ||
                strcmp(ln->mnemonic, "STAX") == 0) {
                int rp = get_rp_code(op1);
                if (rp < 0 || rp > 1) {
                    fprintf(stderr, "Error (line %d): LDAX/STAX only use B or D\n",
                            ln->line_no);
                    error = 1; break;
                }
                bytes[0] = (unsigned char)(op->opcode | (rp << 4));
                emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
                break;
            }
            /* INX, DCX, DAD — register pair ops */
            if (strcmp(ln->mnemonic, "INX") == 0 ||
                strcmp(ln->mnemonic, "DCX") == 0 ||
                strcmp(ln->mnemonic, "DAD") == 0) {
                int rp = get_rp_code(op1);
                if (rp < 0) {
                    fprintf(stderr, "Error (line %d): Invalid register pair '%s'\n",
                            ln->line_no, op1);
                    error = 1; break;
                }
                bytes[0] = (unsigned char)(op->opcode | (rp << 4));
                emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
                break;
            }
            /* ADD, ADC, SUB, SBB, ANA, ORA, XRA, CMP — register ops */
            {
                int reg = get_reg_code(op1);
                if (reg < 0) {
                    fprintf(stderr, "Error (line %d): Invalid register '%s'\n",
                            ln->line_no, op1);
                    error = 1; break;
                }
                bytes[0] = (unsigned char)(op->opcode | reg);
                emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
            }
            break;
        }

        /* INR r / DCR r — opcode = base | (r<<3) */
        case IK_INRDCR: {
            int reg = get_reg_code(op1);
            if (reg < 0) {
                fprintf(stderr, "Error (line %d): Invalid register '%s'\n",
                        ln->line_no, op1);
                error = 1; break;
            }
            bytes[0] = (unsigned char)(op->opcode | (reg << 3));
            emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /* LDA, STA, LHLD, SHLD — opcode + 16-bit direct address */
        case IK_DIRECT: {
            int val = resolve_addr(op1, &result->symtab);
            bytes[0] = op->opcode;
            bytes[1] = (unsigned char)(val & 0xFF);
            bytes[2] = (unsigned char)((val >> 8) & 0xFF);
            emit(fp, addr, bytes, 3, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /* JMP, CALL, Jcond, Ccond — opcode + 16-bit address (label or literal) */
        case IK_JUMP: {
            int target = resolve_addr(op1, &result->symtab);
            if (target == -1) {
                fprintf(stderr, "Error (line %d): Undefined label '%s'\n",
                        ln->line_no, op1);
                error = 1; break;
            }
            bytes[0] = op->opcode;
            bytes[1] = (unsigned char)(target & 0xFF);
            bytes[2] = (unsigned char)((target >> 8) & 0xFF);
            emit(fp, addr, bytes, 3, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /* PUSH / POP rp — opcode = base | (rp<<4) */
        case IK_PUSH_POP: {
            int rp = get_rp_code(op1);
            if (rp < 0) {
                fprintf(stderr, "Error (line %d): Invalid register pair '%s'\n",
                        ln->line_no, op1);
                error = 1; break;
            }
            bytes[0] = (unsigned char)(op->opcode | (rp << 4));
            emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /* IN port / OUT port — opcode + 8-bit port number */
        case IK_IO: {
            int port = parse_number(op1) & 0xFF;
            bytes[0] = op->opcode;
            bytes[1] = (unsigned char)port;
            emit(fp, addr, bytes, 2, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        /* RST n — opcode = 0xC7 | (n<<3) */
        case IK_RST: {
            int n = parse_number(op1) & 0x07;
            bytes[0] = (unsigned char)(0xC7 | (n << 3));
            emit(fp, addr, bytes, 1, ln->label, ln->mnemonic, ln->operand);
            break;
        }

        default:
            fprintf(stderr, "Error (line %d): Unhandled instruction kind\n",
                    ln->line_no);
            error = 1;
            break;
        }
    }

    fclose(fp);
    return error ? -1 : 0;
}
