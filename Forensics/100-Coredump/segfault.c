#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <ctype.h>
#include <limits.h>


const char match[] = "t#hean;SW.er";


int main(int argc, char *argv[])
{
    char *line = NULL;
    size_t linecap = 0;
    ssize_t linelen;

    printf("password: ");
    fflush(stdout);

    linelen = getline(&line, &linecap, stdin);
    if (linelen < 0) {
        printf("No password!\n");
        exit(1);
    }

    if (line[linelen - 1] == '\n') {
        line[linelen - 1] = '\0';
    }

    char *password = malloc(linelen);
    strncpy(password, line, linelen);
    int password_len = strlen(password);

    for (int i = 0; i < password_len; i++) {
        password[i] = tolower(password[i]);
    }

    if (strncmp(password, match, password_len) == 0) {
        printf("Password is OK\n");
    }

    password[INT_MAX] = '\0';  // ...segfault.

    return 0;
}
