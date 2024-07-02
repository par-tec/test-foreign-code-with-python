/**
 * A C file with a library function with a simple parsing funciton
 * based on sscanf
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FMT_BAD_NOSPACE "%d;%19s"   // %s stops at first whitespace.
#define FMT_GOOD "%d;%19[A-Za-z ]m" // Basic working format.

typedef struct person {
  int id;
  char name[20];
} Person;

/**
 * This function contains some errors that need to be fixed.
 */
int parse_person(char *line, Person *p) {
  int n = sscanf(line, FMT_GOOD, &p->id, p->name);
  if (n != 2) {
    return -1;
  }

  return n;
}

int main(int argc, char *argv[]) {
  char line[] = "42;John Doe";
  Person p;
  memset(&p, 0, sizeof(p));

  if (parse_person(line, &p) == 2) {
    printf("ID: %d\n", p.id);
    printf("Name: %s\n", p.name);
  } else {
    fprintf(stderr, "Parsing failed\n");
  }

  return 0;
}
