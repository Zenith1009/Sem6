/*
 * utils.h
 */
#ifndef UTILS_H
#define UTILS_H

void str_trim(char *s);
void str_upper(char *s);
void strip_comment(char *s);
int  parse_number(const char *s);
int  is_valid_label(const char *s);
void split_operands(const char *operand, char *op1, char *op2);

#endif
