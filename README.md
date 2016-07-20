# image-tiles
A simple script for breaking images into tiles.

```
usage: tile.py --image <image_path>
Chop up an image into tiles.

optional arguments:
  -i <path>, --image <path>
                        input image
  -r INIT_RESIZE, --init-resize INIT_RESIZE
                        resize image before processing (example: 500x500 or 500x to resize width to 500px 
                        keeping the aspect ratio)
  -t TILE_SIZE, --tile-size TILE_SIZE
                        tile size (default: 2x2)
  -m OVERLAP_MARGIN, --overlap-margin OVERLAP_MARGIN
                        tile margin (overlap size, default: 0)
  -o <path>, --output <path>
                        output directory
```
