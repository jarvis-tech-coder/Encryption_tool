#include <stdio.h>
#include "../include/cipher.h"

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <filename> <password>\n", argv[0]);
        return 1;
    }

    // argv[2] ab poora string pass hoga, argv[2][0] nahi
    run_encryption(argv[1], argv[2]);
    
    return 0;
}