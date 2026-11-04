#include <pthread.h>
#include <stdlib.h>
void *work(void *p){volatile unsigned long v=1;for(unsigned long i=0;i<10000000;i++)v=v*1664525+1013904223;return 0;}
int main(int argc,char**argv){int n=argc>1?atoi(argv[1]):1;pthread_t t[8];for(int i=0;i<n;i++)pthread_create(&t[i],0,work,0);for(int i=0;i<n;i++)pthread_join(t[i],0);return 0;}