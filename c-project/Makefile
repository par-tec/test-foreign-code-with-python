CC=gcc
CFLAGS=-fPIC -g

all: example example.so

example: example.o
	$(CC) -o example example.o $(CFLAGS)

example.o: example.c
	$(CC) -c example.c $(CFLAGS)

example.so: example.o
	$(CC) -shared -o example.so example.o

clean:
	rm -f example example.o example.so
	rm -f example example.o