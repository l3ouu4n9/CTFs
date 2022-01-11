#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
	unsigned int v0; // eax

  	v0 = time(0);
  	srand(v0);
  	printf("%d", (unsigned int)(rand() % 0x100000));
}