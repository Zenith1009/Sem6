#include "lab5.h"

#include <arpa/inet.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static void lab5_prog_1(struct svc_req *rqstp, SVCXPRT *transp)
{
    union {
        char *is_palindrome_1_arg;
        int is_leap_year_1_arg;
        int_pair gcd_1_arg;
        double square_root_1_arg;
        int_pair swap_no_temp_1_arg;
        int_array array_stats_1_arg;
        two_strings compare_strings_1_arg;
        two_strings is_substring_1_arg;
        two_strings concatenate_1_arg;
        int_array reverse_array_1_arg;
    } argument;

    char *result;
    xdrproc_t xdr_argument;
    xdrproc_t xdr_result;
    char *(*local)(char *, struct svc_req *);

    switch (rqstp->rq_proc) {
    case NULLPROC:
        (void)svc_sendreply(transp, (xdrproc_t)xdr_void, (char *)NULL);
        return;

    case IS_PALINDROME:
        xdr_argument = (xdrproc_t)xdr_wrapstring;
        xdr_result = (xdrproc_t)xdr_int;
        local = (char *(*)(char *, struct svc_req *))is_palindrome_1_svc;
        break;

    case IS_LEAP_YEAR:
        xdr_argument = (xdrproc_t)xdr_int;
        xdr_result = (xdrproc_t)xdr_int;
        local = (char *(*)(char *, struct svc_req *))is_leap_year_1_svc;
        break;

    case GCD:
        xdr_argument = (xdrproc_t)xdr_int_pair;
        xdr_result = (xdrproc_t)xdr_int;
        local = (char *(*)(char *, struct svc_req *))gcd_1_svc;
        break;

    case SQUARE_ROOT:
        xdr_argument = (xdrproc_t)xdr_double;
        xdr_result = (xdrproc_t)xdr_double;
        local = (char *(*)(char *, struct svc_req *))square_root_1_svc;
        break;

    case SWAP_NO_TEMP:
        xdr_argument = (xdrproc_t)xdr_int_pair;
        xdr_result = (xdrproc_t)xdr_int_pair;
        local = (char *(*)(char *, struct svc_req *))swap_no_temp_1_svc;
        break;

    case ARRAY_STATS:
        xdr_argument = (xdrproc_t)xdr_int_array;
        xdr_result = (xdrproc_t)xdr_arr_stats;
        local = (char *(*)(char *, struct svc_req *))array_stats_1_svc;
        break;

    case COMPARE_STRINGS:
        xdr_argument = (xdrproc_t)xdr_two_strings;
        xdr_result = (xdrproc_t)xdr_int;
        local = (char *(*)(char *, struct svc_req *))compare_strings_1_svc;
        break;

    case IS_SUBSTRING:
        xdr_argument = (xdrproc_t)xdr_two_strings;
        xdr_result = (xdrproc_t)xdr_int;
        local = (char *(*)(char *, struct svc_req *))is_substring_1_svc;
        break;

    case CONCATENATE:
        xdr_argument = (xdrproc_t)xdr_two_strings;
        xdr_result = (xdrproc_t)xdr_wrapstring;
        local = (char *(*)(char *, struct svc_req *))concatenate_1_svc;
        break;

    case REVERSE_ARRAY:
        xdr_argument = (xdrproc_t)xdr_int_array;
        xdr_result = (xdrproc_t)xdr_int_array;
        local = (char *(*)(char *, struct svc_req *))reverse_array_1_svc;
        break;

    default:
        svcerr_noproc(transp);
        return;
    }

    (void)memset((char *)&argument, 0, sizeof(argument));
    if (!svc_getargs(transp, xdr_argument, (caddr_t)&argument)) {
        svcerr_decode(transp);
        return;
    }

    result = (*local)((char *)&argument, rqstp);
    if (result != NULL && !svc_sendreply(transp, xdr_result, result)) {
        svcerr_systemerr(transp);
    }

    if (!svc_freeargs(transp, xdr_argument, (caddr_t)&argument)) {
        fprintf(stderr, "unable to free arguments\n");
        exit(1);
    }
}

int main(int argc, char *argv[])
{
    int port = 50051;
    int sock;
    struct sockaddr_in addr;
    SVCXPRT *transp;

    if (argc >= 2) {
        port = atoi(argv[1]);
    }
    if (port <= 0 || port > 65535) {
        fprintf(stderr, "Invalid port: %d\n", port);
        return 1;
    }

    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons((unsigned short)port);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind");
        close(sock);
        return 1;
    }

    transp = svcudp_create(sock);
    if (transp == NULL) {
        fprintf(stderr, "cannot create udp service\n");
        close(sock);
        return 1;
    }

    if (!svc_register(transp, LAB5_PROG, LAB5_VERS, lab5_prog_1, 0)) {
        fprintf(stderr, "unable to register LAB5 service\n");
        return 1;
    }

    printf("LAB5 RPC server listening on UDP port %d\n", port);
    fflush(stdout);
    svc_run();

    fprintf(stderr, "svc_run returned unexpectedly\n");
    return 1;
}
