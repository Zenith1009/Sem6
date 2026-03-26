# Makefile for 2-Pass 8085 Assembler

CC     = gcc
CFLAGS = -Wall -Wextra -g

# All source files
SRCS = main.c pass1.c pass2.c opcode_table.c symbol_table.c utils.c

# Object files
OBJS = $(SRCS:.c=.o)

TARGET = assembler

# Default target
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Compile each .c to .o
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Run on test file
run: $(TARGET)
	./$(TARGET) test.asm

# Clean build artifacts
clean:
	rm -f $(OBJS) $(TARGET) *.lst

.PHONY: all run clean
