## Algorithm for **Pass 1 Assembler**

**Begin**

1. If a starting address is given,

   * Set `LOCCTR ← starting address`
2. Else

   * Set `LOCCTR ← 0`
3. While `OPCODE ≠ END` (or until EOF), do:

   * Read a line from the source program.
   * If there is a **label**:

     * If the label already exists in **SYMTAB**, then

       * Report an error (duplicate symbol).
     * Else

       * Insert `(label, LOCCTR)` into **SYMTAB**.
   * Search **OPTAB** for the opcode.
 
     * If found:

       * Increment `LOCCTR ← LOCCTR + N`
         (`N` = length of the instruction, e.g., 4 bytes for MIPS).
     * Else if the opcode is an **assembler directive**:

       * Update `LOCCTR` as directed.
     * Else:

       * Report an error (invalid opcode).
   * Write the line to the **intermediate file**.
4. Compute program length as:

   * `Program length = LOCCTR − starting address`

**End**

---

## Algorithm for Pass 2 Assembler

**Begin**

1. Read a line from the intermediate file.
2. If the opcode is `START`, then

   * Write the **header record**.
3. While opcode ≠ `END` (or until EOF), do:

   * Search **OPTAB** for the opcode.
   * If the opcode is found:

     * If the operand is a symbol, replace it with its address using **SYMTAB**.
     * Assemble the **object code**.
   * Else if the opcode is a defined **assembler directive**:

     * Convert it into the corresponding object code.
   * Add the generated object code to the **text record**.
   * Read the next line.
4. Write the **End record** to the text.
5. Output the complete object program.

**End**

---

### Note: Assume 8085 style for assembler

### What Pass 1 *really* does (conceptual clarity)

* Assigns addresses using `LOCCTR`
* Builds **SYMTAB**
* Produces an **intermediate file**
* Detects **syntax & symbol errors**
* Does **not** generate object code

### Pass-2 does **not** build tables. It **uses**:

* **SYMTAB** → for symbol addresses
* **OPTAB** → for opcode machine codes

Its only job is *translation*, not discovery. Think of it as the “execution phase” of the assembler’s thinking.
