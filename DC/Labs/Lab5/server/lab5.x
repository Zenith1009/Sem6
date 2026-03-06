/* Lab 5 RPC IDL - server package */

struct int_pair {
    int a;
    int b;
};

struct two_strings {
    string s1<>;
    string s2<>;
};

typedef int int_array<>;

struct arr_stats {
    int max;
    int min;
    double avg;
};

program LAB5_PROG {
    version LAB5_VERS {
        int IS_PALINDROME(string) = 1;
        int IS_LEAP_YEAR(int) = 2;
        int GCD(int_pair) = 3;
        double SQUARE_ROOT(double) = 4;
        int_pair SWAP_NO_TEMP(int_pair) = 5;
        arr_stats ARRAY_STATS(int_array) = 6;
        int COMPARE_STRINGS(two_strings) = 7;
        int IS_SUBSTRING(two_strings) = 8;
        string CONCATENATE(two_strings) = 9;
        int_array REVERSE_ARRAY(int_array) = 10;
    } = 1;
} = 0x31230055;
