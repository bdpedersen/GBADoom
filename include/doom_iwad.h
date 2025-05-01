#ifndef DOOM_IWAD_H
#define DOOM_IWAD_H
#include <stdint.h>

#if 1 // #ifdef WAD_CACHE
extern uint8_t *doom_iwad;
#else
extern const unsigned  char doom_iwad[]; 
#endif 

extern unsigned int doom_iwad_len;


#endif // DOOM_IWAD_H
