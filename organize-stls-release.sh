#!/bin/sh
# Run this inside the top level folder containing all state folders

for f in *; do
  if [ ${#f} -eq 2 ]
  then
    # Move and rename files to user-friendly names
    echo -n "Moving $f"
    mv "${f}/${f}_rivers.STL" "${f}/${f}-dual-hydrography.stl"
    echo -n "."
    mv "${f}/${f}_tile_1_1.STL" "${f}/${f}-dual-land-elevation.stl"
    echo -n "."
    mv "${f}-single-print/${f}_tile_1_1.STL" "${f}/${f}-single.stl"
    echo -n "."

    # Delete unneeded files and directories
    rm "${f}/logfile.txt"
    rm "${f}-no-rivers/${f}_tile_1_1.STL"
    rm "${f}-no-rivers/logfile.txt"
    rmdir "${f}-no-rivers"
    rm "${f}-single-print/logfile.txt"
    rmdir "${f}-single-print"
    echo "Done"
  fi
done