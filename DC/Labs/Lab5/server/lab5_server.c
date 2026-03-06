#include "lab5.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int *is_palindrome_1_svc(char **argp, struct svc_req *rqstp)
{
    static int result;
    const char *s = *argp;
    int i = 0, j = (int)strlen(s) - 1;
    (void)rqstp;

    result = 1;
    while (i < j) {
        if (s[i++] != s[j--]) {
            result = 0;
            break;
        }
    }
    return &result;
}

int *is_leap_year_1_svc(int *argp, struct svc_req *rqstp)
{
    static int result;
    int y = *argp;
    (void)rqstp;

    result = ((y % 400 == 0) || ((y % 4 == 0) && (y % 100 != 0))) ? 1 : 0;
    return &result;
}

int *gcd_1_svc(int_pair *argp, struct svc_req *rqstp)
{
    static int result;
    int a = abs(argp->a), b = abs(argp->b);
    (void)rqstp;

    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    result = a;
    return &result;
}

double *square_root_1_svc(double *argp, struct svc_req *rqstp)
{
    static double result;
    (void)rqstp;

    result = (*argp < 0) ? (0.0 / 0.0) : sqrt(*argp);
    return &result;
}

int_pair *swap_no_temp_1_svc(int_pair *argp, struct svc_req *rqstp)
{
    static int_pair result;
    (void)rqstp;

    result = *argp;
    result.a = result.a + result.b;
    result.b = result.a - result.b;
    result.a = result.a - result.b;
    return &result;
}

arr_stats *array_stats_1_svc(int_array *argp, struct svc_req *rqstp)
{
    static arr_stats result;
    (void)rqstp;

    if (argp->int_array_len == 0) {
        result.max = result.min = 0;
        result.avg = 0.0;
        return &result;
    }

    result.max = result.min = argp->int_array_val[0];
    long long sum = argp->int_array_val[0];
    for (u_int i = 1; i < argp->int_array_len; i++) {
        int v = argp->int_array_val[i];
        if (v > result.max) result.max = v;
        if (v < result.min) result.min = v;
        sum += v;
    }
    result.avg = (double)sum / (double)argp->int_array_len;
    return &result;
}

int *compare_strings_1_svc(two_strings *argp, struct svc_req *rqstp)
{
    static int result;
    (void)rqstp;
    result = strcmp(argp->s1, argp->s2);
    return &result;
}

int *is_substring_1_svc(two_strings *argp, struct svc_req *rqstp)
{
    static int result;
    (void)rqstp;
    result = (strstr(argp->s1, argp->s2) != NULL) ? 1 : 0;
    return &result;
}

char **concatenate_1_svc(two_strings *argp, struct svc_req *rqstp)
{
    static char buffer[2048];
    static char *result = buffer;
    (void)rqstp;

    snprintf(buffer, sizeof(buffer), "%s%s", argp->s1, argp->s2);
    return &result;
}

int_array *reverse_array_1_svc(int_array *argp, struct svc_req *rqstp)
{
    static int_array result;
    static int *buf = NULL;
    static u_int cap = 0;
    (void)rqstp;

    if (argp->int_array_len > cap) {
        int *tmp = realloc(buf, argp->int_array_len * sizeof(int));
        if (tmp == NULL) {
            result.int_array_len = 0;
            result.int_array_val = NULL;
            return &result;
        }
        buf = tmp;
        cap = argp->int_array_len;
    }

    result.int_array_len = argp->int_array_len;
    result.int_array_val = buf;
    for (u_int i = 0; i < argp->int_array_len; i++) {
        buf[i] = argp->int_array_val[argp->int_array_len - 1 - i];
    }
    return &result;
}
