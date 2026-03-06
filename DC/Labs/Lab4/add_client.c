#include "add.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 1024

static void print_menu(void)
{
    printf("\n===== RPC MENU =====\n");
    printf("1. Find factorial\n");
    printf("2. Calculator (basic operations)\n");
    printf("3. Prime check\n");
    printf("4. Fibonacci series up to n\n");
    printf("5. Maximum in integer array\n");
    printf("6. Exit\n");
    printf("Enter your choice: ");
}

static int parse_int_array(const char *line, int **arr, u_int *len)
{
    char buffer[MAX_LINE];
    char *token;
    int *values = NULL;
    u_int count = 0;

    strncpy(buffer, line, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';

    token = strtok(buffer, ",");
    while (token != NULL) {
        int *tmp = realloc(values, (count + 1) * sizeof(int));
        if (tmp == NULL) {
            free(values);
            return 0;
        }
        values = tmp;
        values[count++] = atoi(token);
        token = strtok(NULL, ",");
    }

    if (count == 0) {
        free(values);
        return 0;
    }

    *arr = values;
    *len = count;
    return 1;
}

int
main(int argc, char *argv[])
{
    char *host;
    CLIENT *clnt;

    if (argc < 2) {
        printf("usage: %s server_host\n", argv[0]);
        return 1;
    }

    host = argv[1];
    clnt = clnt_create(host, ADD_PROG, ADD_VERS, "udp");
    if (clnt == NULL) {
        clnt_pcreateerror(host);
        return 1;
    }

    while (1) {
        int choice;
        print_menu();

        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        if (choice == 6) {
            printf("Exiting client.\n");
            break;
        }

        if (choice == 1) {
            int n;
            quad_t *res;
            printf("Enter number: ");
            scanf("%d", &n);
            res = factorial_1(&n, clnt);
            if (res == NULL) {
                clnt_perror(clnt, "call failed");
            } else if (*res < 0) {
                printf("Factorial is not defined for negative numbers.\n");
            } else {
                printf("Result: %lld\n", (long long)*res);
            }
        } else if (choice == 2) {
            calc_input input;
            double *res;
            printf("Enter first number: ");
            scanf("%lf", &input.a);
            printf("Enter second number: ");
            scanf("%lf", &input.b);
            printf("Operation (1=ADD, 2=SUB, 3=MUL, 4=DIV): ");
            scanf("%d", &input.op);

            res = calculate_1(&input, clnt);
            if (res == NULL) {
                clnt_perror(clnt, "call failed");
            } else if (isnan(*res)) {
                printf("Invalid operation (division by zero or bad operator).\n");
            } else {
                printf("Result: %.4f\n", *res);
            }
        } else if (choice == 3) {
            int n;
            int *res;
            printf("Enter number: ");
            scanf("%d", &n);
            res = is_prime_1(&n, clnt);
            if (res == NULL) {
                clnt_perror(clnt, "call failed");
            } else {
                printf("Result: %s\n", (*res == 1) ? "Prime" : "Not Prime");
            }
        } else if (choice == 4) {
            int n;
            char **res;
            printf("Enter upper limit: ");
            scanf("%d", &n);
            res = fibonacci_1(&n, clnt);
            if (res == NULL) {
                clnt_perror(clnt, "call failed");
            } else {
                printf("Result: %s\n", *res);
            }
        } else if (choice == 5) {
            char line[MAX_LINE];
            int *arr = NULL;
            u_int len = 0;
            int_array rpc_arr;
            int *res;

            printf("Enter comma-separated integers: ");
            scanf("%s", line);

            if (!parse_int_array(line, &arr, &len)) {
                printf("Invalid array input.\n");
                continue;
            }

            rpc_arr.int_array_len = len;
            rpc_arr.int_array_val = arr;
            res = max_in_array_1(&rpc_arr, clnt);

            if (res == NULL) {
                clnt_perror(clnt, "call failed");
            } else {
                printf("Result: %d\n", *res);
            }

            free(arr);
        } else {
            printf("Invalid choice.\n");
        }
    }

    clnt_destroy(clnt);
    return 0;
}
