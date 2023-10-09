for f in *; do
  # Move and rename files to user-friendly names
  echo -n "Renaming $f"
  abbr="${f:0:2}"
  cd ${abbr}
  for s in *-scale*; do
    echo -n ${s}
    mv -- "$s" "${s/-scale/}"
  done
  cd ../
  echo -n "."
done