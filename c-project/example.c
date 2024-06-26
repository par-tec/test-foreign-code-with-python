/**
 * A C file with a library function with a simple parsing funciton
 * based on sscanf
 */

#include <stdio.h>
#include <stdlib.h>

struct person
{
    int id;
    char name[20];
} person;

int parse_person(char *line, struct person *p)
{
    int n;

    // Beware! There is an error in the format string.
    // %s reads until the first whitespace character, so it won't work.
    n = sscanf(line, "%d;%19s", &p->id, p->name);
    if (n != 2)
    {
        return -1;
    }

    return 0;
}

int main(int argc, char *argv[])
{
    char line[] = "42;John Doe";
    struct person p;

    if (parse_person(line, &p) == 0)
    {
        printf("ID: %d\n", p.id);
        printf("Name: %s\n", p.name);
    }
    else
    {
        fprintf(stderr, "Parsing failed\n");
    }

    return 0;
}
