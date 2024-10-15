# idtech_map_converter

This is a small piece of code that allow to convert original idtech 4 map (DOOM 3) files to idtech 7 map files.

You need to resave the converted map to a different map file to fix some issues with file structure.

Now converter supports:
- Brush geometry with scaling
- Materials creating for idtech 7
- Lights with correct output coordinates and params
- Static meshes (LWO)
- Some movable meshes (LWO with Havok class entity)
- Emitters (just scales and coordinates)

Sadly, patchDefs are not supported by idtech 7 so some geometry still missing. And it seems like forever ((

Enjoy!
