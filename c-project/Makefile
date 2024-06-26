CC=gcc
CFLAGS=-fPIC -g -lc -lm -Wall

all: example libexample.so

example: example.o
	$(CC) -o example example.o $(CFLAGS)

example.o: example.c
	$(CC) -c example.c $(CFLAGS)

libexample.so: example.o
	$(CC) -shared -o libexample.so example.o

clean:
	rm -f example example.o example.so
	rm -f example example.o
