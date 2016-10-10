#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>


#define PWD_LEN 56


void create_password(char *dst, size_t len)
{
    srandom(time(NULL));

    for (size_t i = 0; i < len - 1; i++) {
        dst[i] = 'A' + random() % ('Z' - 'A');
    }

    dst[len - 1] = '\0';
}


int main(int argc, char *argv[])
{
    char password[PWD_LEN];

    create_password(password, PWD_LEN);
    printf("%s\n", password);

    return 0;
}
