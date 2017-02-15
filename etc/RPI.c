#include "RPI.h"
// Need 2837
struct bcm2835_peripheral gpio = {GPIO_BASE};
 
// Exposes the physical address defined in the passed structure using mmap on /dev/mem
int map_peripheral(struct bcm2835_peripheral *p)
{
	
   // Open /dev/mem
   if ((p->mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
      printf("Failed to open /dev/mem, try checking permissions.\n");
      return -1;
   }
 
   p->map = mmap(
      NULL,
      BLOCK_SIZE,
      PROT_READ|PROT_WRITE,
      MAP_SHARED,
      p->mem_fd,      // File descriptor to physical memory virtual file '/dev/mem'
      p->addr_p       // Address in physical map that we want this memory block to expose
   );
 
   if (p->map == MAP_FAILED) {
        perror("mmap");
        return -1;
   }
 
   p->addr = (volatile unsigned int *)p->map;
 
   return 0;
}
 
void unmap_peripheral(struct bcm2835_peripheral *p){
    munmap(p->map, BLOCK_SIZE);
    close(p->mem_fd);
}


int main (int argc, char *argv[]){
	printf("Start1\n");
	if(map_peripheral(&gpio) == -1) {
		printf("Failed to map the physical GPIO registers into the virtual memory space.\n");
		return -1;
	}
 
	// Define pin 7 as output
	INP_GPIO(4);
	OUT_GPIO(4);
	int lc=0;
	for (lc=0;lc<10;lc++){
		printf("lc: %d\n", lc);
		// Toggle pin 7 (blink a led!)
		GPIO_SET = 1 << 4;
		sleep(1);
		
		GPIO_CLR = 1 << 4;
		sleep(1);
		
	}
	
	/* Unmap the peripheral */
    unmap_peripheral(&gpio);
	return 0; 
}