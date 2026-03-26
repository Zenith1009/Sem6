; test.asm
; 2-Pass 8085 Assembler - Test Program
;
; This program demonstrates:
;   - ORG directive (start address)
;   - All major instruction types
;   - FORWARD REFERENCE: DONE and SUBR are used before they are defined
;   - Labels, jumps, data transfer, arithmetic, logical, stack, I/O

        ORG 2000H          ; Starting address

; --- Initialise registers ---
START:  MVI A, 05H         ; A = 05H
        MVI B, 03H         ; B = 03H
        LXI H, 3000H       ; HL = 3000H (data memory pointer)

; --- Store A to memory ---
        STA 3050H          ; Store A at address 3050H
        MOV M, A           ; Store A at address pointed by HL

; --- Arithmetic ---
        ADD B              ; A = A + B  (05 + 03 = 08)
        INR A              ; A = A + 1  (09)
        DCR B              ; B = B - 1  (02)
        DAD H              ; HL = HL + HL

; --- Logical ---
        ANI 0FH            ; A = A AND 0FH
        ORI 80H            ; A = A OR  80H
        XRA A              ; A = A XOR A = 0 (clears A)
        CPI 00H            ; Compare A with 00H

; --- FORWARD REFERENCE: DONE is defined BELOW this jump ---
        JZ  DONE           ; If A == 0, jump forward to DONE

; --- Stack operations ---
        PUSH B             ; Push BC onto stack
        PUSH H             ; Push HL onto stack
        POP  H             ; Pop into HL
        POP  B             ; Pop into BC

; --- Loop example ---
        MVI C, 04H         ; Loop counter = 4
LOOP:   DCR C              ; C = C - 1
        JNZ LOOP           ; Jump back to LOOP until C = 0

; --- I/O ---
        IN  01H            ; Read from port 01H into A
        OUT 02H            ; Write A to port 02H

; --- Subroutine call (forward reference) ---
        CALL SUBR          ; Call SUBR, defined below

; --- DONE: target of the forward-referenced JZ jump ---
DONE:   LDA 3050H          ; Load from address 3050H
        HLT                ; Halt

; --- Subroutine ---
SUBR:   MVI A, 0FFH        ; Load FFH into A
        STA 3051H          ; Store to 3051H
        RET                ; Return from subroutine

        END
