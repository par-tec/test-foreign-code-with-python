typedef struct element
{
    struct element *forward;
    struct element *backward;
    char *name;
} element;

typedef element* queue;
