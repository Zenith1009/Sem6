# Department of Computer Science and Engineering, S.V.N.I.T., Surat

**Supplementary Examination – July 2025**
**B.Tech – II (CSE) – 4th Semester**
**Microprocessor and Interfacing Techniques (CS202)**

**Date:** 17th July 2025
**Time:** 09:30 a.m. to 12:30 p.m.
**Max Marks:** 100

---

## Instructions

1. Assume any necessary data by giving proper justification.
2. Be precise and clear in answering the questions.
3. Figures to the right carry full marks of the respective question.

---

## Q1

### a)

Design and draw complete memory interfacing circuit with 8085 to interface **24K ROM** using **06 × 8K × 8 IC** and **4K RAM** using **2K × 4 IC** and I/O interfacing with **two 8255s** using a **single 3-to-8 decoder** with suitable start addresses.
**(06 Marks)**

### b)

Discuss with example **PUSH**, **HLHD**, and **CALL** in 8085.
**(03 Marks)**

### c)

Draw and explain timing diagram for **LHLD instruction**.
**(03 Marks)**

---

## Q2

### a)

Enlist addressing modes of 8085 instructions and explain with example **any three addressing modes**.
**(06 Marks)**

### b)

Explain complete **interrupt vector table of 8085**. Discuss clearly **priority, input, vector location**, etc.
**(05 Marks)**

### c)

Explain with diagram **bidirectional communication between two computers using the 8255A**.
**(04 Marks)**

---

## Q3

### a)

Draw and explain hardware circuit to implement **RST-3 in 8085**.
Discuss **SIM instruction of 8085**.
**(05 Marks)**

### b)

Explain the following instructions in 8085 with example and their effect on flag:

* **LDAX**
* **SPHL**
* **XTHL**
  **(06 Marks)**

### c)

Explain with neat diagram **mode-0 and mode-2 of 8253**.
**(04 Marks)**

---

## Q4

### a) Answer the following (with suitable justifications / calculations):

#### i)

Explain the type of numbers that can be displayed at the output port.

```asm
MVI A, 91H
ORA A
JP OUTPRT
XRA A
OUTPRT: OUT F2H
HLT
```

#### ii)

Explain the function of the following program.

```asm
MVI A, BYTE1
ORA A
JM OUTPRT
OUT 01H
HLT
OUTPRT: CMA
ADI 01H
OUT 01H
HLT
```

**(04 Marks)**

---

### b)

Design and explain **Multiplexed Scan Display** for displaying **2025** using **8085 and 8255**.
Assume suitable port addresses and write complete routine for the same.
**(04 Marks)**

### c)

Design a **delay routine in 8085 for 1 second delay**.
Show clear calculations for 1 second time delay.
Assume **2.5 MHz clock frequency**.
**(05 Marks)**

### d)

Explain **Interrupt response of 8085 with 8259 programmable interrupt controller (PIC)**.
Discuss **ICW1 and OCW1 of 8259**.
**(05 Marks)**

---

## Q5

Write an **8085 Assembly Language Programme (ALP)** for the following:

### a)

Design an I/O interfacing circuit to have **counter 0 address as FCH** and write 8085 ALP to generate **square wave of 1 ms time period** using **counter 1 of 8253** for input frequency of **1 MHz**.
**(05 Marks)**

### b)

Write an 8085 ALP to implement **RST 4 breakpoint routine** which will cause **4 LEDs connected via D3–D0** to flash **10 times** with delay of **1 second**, when **RST 6** is executed.
Assume clock frequency of **2 MHz** to implement delay routine of 1 second.
**(05 Marks)**

### c)

A string of readings in bytes is stored in memory locations starting at **XX40H**, and the end of string is indicated by the byte **0DH**.

* Write an 8085 ALP to check each byte in the string
* Save the bytes in the range **F0H to FAH (both inclusive)** in memory locations starting from **XX90H**
* Perform addition of all saved numbers and store the result (which may be **16 bits**) at **XXF0H onwards**

**(05 Marks)**

---

## Q6 (For 8086)

### a)

What will happen when the following two interrupt requests (in 8086) occur at the same time?

1. **Single Step Mode and INTR**
2. **NMI and INTO**
   Discuss in detail.
   **(04 Marks)**

### b)

Explain the following instructions in 8086 with example and their effect on flag:

* **AAM**
* **SAR**
* **STOS**
* **RET**
  **(06 Marks)**

### c)

Write an **8086 Assembly Language Program (ALP)** for the following:

#### i)

To check for **palindrome** for the given line through keyboard.

* Implement macro to take line input through keyboard
* Implement procedures:

  * (i) Generate reverse of the given line input
  * (ii) Check for palindrome
* Display output message(s) using macro

#### ii)

Write an 8086 ALP that prompts the user to type some text consisting of words separated by blanks, ending with carriage return, and display the text in the **same word order**, but with the **letters in each word reversed**.
Use macro for input and procedure to perform the task.

**(12 Marks)**
