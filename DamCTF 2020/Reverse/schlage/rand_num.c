#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

int main(int argc, char *argv[]){
	if(strcmp(argv[1], "5") == 0){
		srand(0x42424242);
		printf("%d", rand());
	} else if(strcmp(argv[1], "2") == 0){
		int seed;
		seed = atoi(argv[2]);
		srand(seed);
		printf("%d", rand());
	} else if(strcmp(argv[1], "4") == 0){
		int seed, garbage;
		seed = atoi(argv[2]);
		srand(seed);
		garbage = rand();
		printf("%d", rand());
	}
	return 0;
}