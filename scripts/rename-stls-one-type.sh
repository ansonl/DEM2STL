#!/bin/sh
# Run this inside the top level folder containing only one folder per state

for f in *; do
  # Move and rename files to user-friendly names
  echo -n "Moving $f"
  abbr="${f:0:2}"
  mkdir -p ${abbr}
  mv "${f}/${abbr}_tile_1_1.STL" "${abbr}/${abbr}-single-linear-scale-v2.stl"
  echo -n "."

  # Delete unneeded files and directories
  rm "${f}/logfile.txt"
  rmdir "${f}"
  echo "Done"
done