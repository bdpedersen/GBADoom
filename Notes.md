- All graphics looks to be cached when accessed so can be evicted at any time

- Map data is NOT cached. Hence it is assumed to be resident in the cache until a new version of the data is loaded.
- THINGS is loaded in P_LoadThings in p_setup.c:173. Data does not leak out of this function so THINGS can be evicted.
- LINEDEFS is loaded in P_LoadLineData in p_setup.c:214. A pointer is transfered 
  to _g->lines which is used in :
  - AM_drawWalls
  - P_BlockLinesIterator
  - P_GroupLines
  - P_FindLineFromLineTag
  - P_SpawnScrollers
  - EV_SilentLineTeleport
  - R_RenderMaskedSegRange
  - R_StoreWallRange
  - R_AddLine
  - P_CrossSubsector
- SIDEDEFS is loaded in P_LoadSideDefs in p_setup.c:250 and in P_LoadSideDefs2 in :260. No pointer is taken so this can be evicted.
- VERTEXES is loaded by P_LoadVertexes in p_setup.c:60. A pointer is transfered to _g->vertexes which is used in
  - AM_FindMinMaxBoundaries
  However this is only used on initialization so vertexes can be evicted as soon as this is done. To avoid fragmentation, this should be 
  loaded last, which should be OK.
- SEGS is loaded by P_LoadSegs in p_setup.c:76. A pointer is stored in _g->segs which is used in
  - P_GroupLines
  - R_Subsector
  - P_CrossSubsector
- SSECTORS is loaded in P_LoadSubsectors in p_setup.c:90. No pointer is taken so this can be evicted
- NODES is held by nodes, which is defined in r_hotpath.iwram.c and loaded in p_setup.c:153. Functions that use it:
    - R_PointInSubSector
    - R_RenderBSPNode
    - P_CrossBSPNode
- SECTORS is loaded in P_LoadSectors in p_setup.c:115. Data is not leaking out so this can be evicted
- REJECT is loaded in P_LoadReject in p_setup.c:349. A pointer is leaked to _g->rejectmatrix which is used in:
  - P_CheckSight
- BLOCKMAP is loaded in P_LoadBlockMap in p_setup.c:322. A pointer is leaked to _g->blockmaplump which is used in
  - P_BlockLinesIterator
  
In reality all that can not be evicted must stay resident until flushed. Others (including vertexes) can be treated as normal assets that are loaded on demand. Then the more memory the merrier. During setup the cache should have an "evict early" policy to make sure that locked items are in the beginning of the cache. That way fragmentation will be easier to handle in the end.

The allocation system allows a purgeable pointer type that will evicted on OOM. This can be used for caching. Will have to experiment with cache size and free up as much PMEM as possible.

Demos can be omitted and thereby we can save 20k. This must be done in d_main

If we allow tearing, we can share framebuffer and rasterbuffer to save a frame buffer (39k) and raster buffer (29k) and move the frame buffer to PMEM

Last we should be looking at stack depth. We can fit a number of smaller variables in the stack areas and there is potentially 9-15K found there.

The lump cache is 18k - we could choose to cache the lump indices also and just have a lump index cache of maybe 32 entires that can be held at any given point in time. We would then still have a hash table with the index and then a doubly linked list array to hold the LRU. To save space these entries should reflect what we have in the actual cache so we could have a cache pointer array also of the same number of entries. The locked entities would then just be evicted from the index but not from the cache when time comes...

Last but not least - put tables in PMEM