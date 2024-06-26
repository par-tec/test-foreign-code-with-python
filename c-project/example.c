/**
 * A C file with a library function that appends a buffer to a linked list.
 */

#include <stdlib.h>
#include <string.h>

#include <search.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "example.h"


static element *
new_element(void)
{
    element *e;

    e = malloc(sizeof(*e));
    if (e == NULL)
    {
        fprintf(stderr, "malloc() failed\n");
        exit(EXIT_FAILURE);
    }

    return e;
}



element* append(queue *q, char *name) {
    element *elem, *prev;

    if (!q) return NULL; // Check if the queue pointer itself is NULL

    elem = new_element();
    if (!elem) return NULL; // Check if memory allocation failed

    elem->name = name; // Assuming name is properly allocated and managed outside this function

    if (!*q) {
        // If the queue is empty, insert the new element at the beginning
        *q = elem;
    } else {
        // Find the last element in the queue
        for (prev = *q; prev->forward != NULL; prev = prev->forward)
            ;
        // Insert the new element at the end of the queue
    }
    insque(elem, prev);

    return elem;
}


int main(int argc, char *argv[])
{
    element *first, *elem, *prev;
    queue *q = malloc(sizeof(queue));

    elem = append(q, "1");


    printf("Traversing completed list:\n");
    elem = first;
    do
    {
        printf("    %s\n", elem->name);
        elem = elem->forward;
    } while (elem != NULL && elem != first);

    if (elem == first)
        printf("That was a circular list\n");

    exit(EXIT_SUCCESS);
}
