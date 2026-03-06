#include "lab5.h"

#include <arpa/inet.h>
#include <math.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static CLIENT *create_udp_client(const char *host, int port)
{
    struct sockaddr_in server_addr;
    struct hostent *he;
    struct timeval timeout;
    int sock = RPC_ANYSOCK;

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons((unsigned short)port);

    if (inet_aton(host, &server_addr.sin_addr) == 0) {
        he = gethostbyname(host);
        if (he == NULL || he->h_addrtype != AF_INET || he->h_length != 4) {
            return NULL;
        }
        memcpy(&server_addr.sin_addr, he->h_addr_list[0], 4);
    }

    timeout.tv_sec = 5;
    timeout.tv_usec = 0;

    return clntudp_create(&server_addr, LAB5_PROG, LAB5_VERS, timeout, &sock);
}

#define MAX_BUF 1024

static void print_menu(void)
{
    printf("\n===== LAB 5 RPC MENU =====\n");
    printf("1. Check palindrome\n");
    printf("2. Check leap year\n");
    printf("3. Find GCD of two numbers\n");
    printf("4. Find square root\n");
    printf("5. Swap two variables without 3rd variable\n");
    printf("6. Max, Min, Average of array\n");
    printf("7. Compare two strings\n");
    printf("8. Check substring\n");
    printf("9. Concatenate two strings\n");
    printf("10. Reverse array elements\n");
    printf("11. Exit\n");
    printf("Enter choice: ");
}

static int parse_array(const char *line, int **arr, u_int *len)
{
    char buffer[MAX_BUF];
    char *tok;
    int *vals = NULL;
    u_int count = 0;

    strncpy(buffer, line, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';

    tok = strtok(buffer, ",");
    while (tok != NULL) {
        int *tmp = realloc(vals, (count + 1) * sizeof(int));
        if (tmp == NULL) {
            free(vals);
            return 0;
        }
        vals = tmp;
        vals[count++] = atoi(tok);
        tok = strtok(NULL, ",");
    }

    if (count == 0) {
        free(vals);
        return 0;
    }

    *arr = vals;
    *len = count;
    return 1;
}

int main(int argc, char *argv[])
{
    char *host;
    int port = 50051;
    CLIENT *clnt;

    if (argc < 2) {
        printf("usage: %s server_host [server_port]\n", argv[0]);
        return 1;
    }

    host = argv[1];
    if (argc >= 3) {
        port = atoi(argv[2]);
    }
    if (port <= 0 || port > 65535) {
        printf("Invalid port: %d\n", port);
        return 1;
    }

    clnt = create_udp_client(host, port);
    if (clnt == NULL) {
        clnt_pcreateerror("client create");
        return 1;
    }

    while (1) {
        int choice;
        print_menu();
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        if (choice == 11) {
            printf("Exiting client.\n");
            break;
        }

        if (choice == 1) {
            char str[MAX_BUF];
            int *res;
            printf("Enter string: ");
            scanf("%1023s", str);
            char *arg = str;
            res = is_palindrome_1(&arg, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else printf("Result: %s\n", (*res ? "Palindrome" : "Not Palindrome"));
        } else if (choice == 2) {
            int y;
            int *res;
            printf("Enter year: ");
            scanf("%d", &y);
            res = is_leap_year_1(&y, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else printf("Result: %s\n", (*res ? "Leap Year" : "Not Leap Year"));
        } else if (choice == 3) {
            int_pair p;
            int *res;
            printf("Enter first number: ");
            scanf("%d", &p.a);
            printf("Enter second number: ");
            scanf("%d", &p.b);
            res = gcd_1(&p, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else printf("Result: GCD = %d\n", *res);
        } else if (choice == 4) {
            double n;
            double *res;
            printf("Enter number: ");
            scanf("%lf", &n);
            res = square_root_1(&n, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else if (isnan(*res)) printf("Result: Invalid (negative number)\n");
            else printf("Result: %.6f\n", *res);
        } else if (choice == 5) {
            int_pair p;
            int_pair *res;
            printf("Enter first number: ");
            scanf("%d", &p.a);
            printf("Enter second number: ");
            scanf("%d", &p.b);
            res = swap_no_temp_1(&p, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else printf("Result after swap: a=%d, b=%d\n", res->a, res->b);
        } else if (choice == 6) {
            char line[MAX_BUF];
            int *arr = NULL;
            u_int len = 0;
            int_array rpc_arr;
            arr_stats *res;
            printf("Enter comma-separated array: ");
            scanf("%1023s", line);
            if (!parse_array(line, &arr, &len)) {
                printf("Invalid array input\n");
                continue;
            }
            rpc_arr.int_array_len = len;
            rpc_arr.int_array_val = arr;
            res = array_stats_1(&rpc_arr, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else printf("Result: max=%d, min=%d, avg=%.4f\n", res->max, res->min, res->avg);
            free(arr);
        } else if (choice == 7) {
            two_strings in;
            char s1[MAX_BUF], s2[MAX_BUF];
            int *res;
            printf("Enter first string: ");
            scanf("%1023s", s1);
            printf("Enter second string: ");
            scanf("%1023s", s2);
            in.s1 = s1;
            in.s2 = s2;
            res = compare_strings_1(&in, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else if (*res == 0) printf("Result: Strings are equal\n");
            else if (*res < 0) printf("Result: String 1 < String 2\n");
            else printf("Result: String 1 > String 2\n");
        } else if (choice == 8) {
            two_strings in;
            char s1[MAX_BUF], s2[MAX_BUF];
            int *res;
            printf("Enter main string: ");
            scanf("%1023s", s1);
            printf("Enter substring: ");
            scanf("%1023s", s2);
            in.s1 = s1;
            in.s2 = s2;
            res = is_substring_1(&in, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else printf("Result: %s\n", (*res ? "Substring exists" : "Substring does not exist"));
        } else if (choice == 9) {
            two_strings in;
            char s1[MAX_BUF], s2[MAX_BUF];
            char **res;
            printf("Enter first string: ");
            scanf("%1023s", s1);
            printf("Enter second string: ");
            scanf("%1023s", s2);
            in.s1 = s1;
            in.s2 = s2;
            res = concatenate_1(&in, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else printf("Result: %s\n", *res);
        } else if (choice == 10) {
            char line[MAX_BUF];
            int *arr = NULL;
            u_int len = 0;
            int_array rpc_arr;
            int_array *res;
            printf("Enter comma-separated array: ");
            scanf("%1023s", line);
            if (!parse_array(line, &arr, &len)) {
                printf("Invalid array input\n");
                continue;
            }
            rpc_arr.int_array_len = len;
            rpc_arr.int_array_val = arr;
            res = reverse_array_1(&rpc_arr, clnt);
            if (res == NULL) clnt_perror(clnt, "call failed");
            else {
                printf("Result: ");
                for (u_int i = 0; i < res->int_array_len; i++) {
                    if (i) printf(",");
                    printf("%d", res->int_array_val[i]);
                }
                printf("\n");
            }
            free(arr);
        } else {
            printf("Invalid choice\n");
        }
    }

    clnt_destroy(clnt);
    return 0;
}
