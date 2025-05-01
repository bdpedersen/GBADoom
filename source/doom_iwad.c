#if 0 // #ifndef WAD_CACHE
#pragma GCC optimize ("-O0")
#include "doom_iwad.h"

//Uncomment which edition you want to compile
#include "iwad/doom1.c"
//#include "iwad/doomu.c"
//#include "iwad/doom2.c"
//#include "iwad/tnt.c"
//#include "iwad/plutonia.c"
//#include "iwad/sigil.c"

const unsigned int doom_iwad_len = sizeof(doom_iwad);
#else
#include <stdint.h>
#include <stddef.h>
uint8_t *doom_iwad = NULL;
unsigned int doom_iwad_len = 0;
#endif