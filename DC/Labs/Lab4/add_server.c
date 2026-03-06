#include "add.h"

#include <stdio.h>
#include <string.h>

quad_t *
factorial_1_svc(int *argp, struct svc_req *rqstp)
{
    static quad_t result;
    int n = *argp;

    (void)rqstp;

    if (n < 0) {
        result = -1;
        return &result;
    }

    result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }

    printf("FACTORIAL(%d) called, result = %lld\n", n, (long long)result);
    return &result;
}

double *
calculate_1_svc(calc_input *argp, struct svc_req *rqstp)
{
    static double result;

    (void)rqstp;

    switch (argp->op) {
    case 1:
        result = argp->a + argp->b;
        break;
    case 2:
        result = argp->a - argp->b;
        break;
    case 3:
        result = argp->a * argp->b;
        break;
    case 4:
        result = (argp->b == 0) ? (0.0 / 0.0) : (argp->a / argp->b);
        break;
    default:
        result = (0.0 / 0.0);
        break;
    }

    printf("CALCULATE(%.2f, %.2f, op=%d) called\n", argp->a, argp->b, argp->op);
    return &result;
}

int *
is_prime_1_svc(int *argp, struct svc_req *rqstp)
{
    static int result;
    int n = *argp;

    (void)rqstp;

    if (n <= 1) {
        result = 0;
    } else {
        result = 1;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                result = 0;
                break;
            }
        }
    }

    printf("IS_PRIME(%d) called, result = %d\n", n, result);
    return &result;
}

char **
fibonacci_1_svc(int *argp, struct svc_req *rqstp)
{
    static char response[2048];
    static char *result = response;
    int n = *argp;
    int a = 0;
    int b = 1;

    (void)rqstp;

    response[0] = '\0';

    if (n < 0) {
        strncpy(response, "Invalid input", sizeof(response) - 1);
        response[sizeof(response) - 1] = '\0';
        return &result;
    }

    while (a <= n) {
        char temp[64];
        snprintf(temp, sizeof(temp), "%d", a);

        if (response[0] != '\0') {
            strncat(response, ",", sizeof(response) - strlen(response) - 1);
        }
        strncat(response, temp, sizeof(response) - strlen(response) - 1);

        int next = a + b;
        a = b;
        b = next;
    }

    printf("FIBONACCI(%d) called\n", n);
    return &result;
}

int *
max_in_array_1_svc(int_array *argp, struct svc_req *rqstp)
{
    static int result;

    (void)rqstp;

    if (argp->int_array_len == 0) {
        result = 0;
        return &result;
    }

    result = argp->int_array_val[0];
    for (u_int i = 1; i < argp->int_array_len; i++) {
        if (argp->int_array_val[i] > result) {
            result = argp->int_array_val[i];
        }
    }

    printf("MAX_IN_ARRAY called on %u elements, result = %d\n", argp->int_array_len, result);
    return &result;
}
