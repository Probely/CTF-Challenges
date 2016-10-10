#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>


#define PWD_LEN 56


void create_password(char *dst, size_t len, unsigned int seed)
{
    // srand()/rand() isn't consistent across platforms
    srandom(seed);

    for (size_t i = 0; i < len - 1; i++) {
        dst[i] = 'A' + random() % ('Z' - 'A');
    }

    dst[len - 1] = '\0';
}


int main(int argc, char *argv[])
{
    if (argc <= 1) {
        printf("USAGE: %s <timestamp>\n", argv[0]);
        exit(1);
    }

    char password[PWD_LEN];
    unsigned int seed = atol(argv[1]);

    create_password(password, PWD_LEN, seed);
    printf("%u %s\n", seed, password);

    return 0;
}
