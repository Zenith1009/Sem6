/* Assignment 4: RPC Simulation */

struct calc_input {
    double a;
    double b;
    int op; /* 1=ADD, 2=SUB, 3=MUL, 4=DIV */
};

typedef int int_array<>;

program ADD_PROG {
    version ADD_VERS {
        hyper FACTORIAL(int) = 1;
        double CALCULATE(calc_input) = 2;
        int IS_PRIME(int) = 3;
        string FIBONACCI(int) = 4;
        int MAX_IN_ARRAY(int_array) = 5;
    } = 1;
} = 0x4562877;
