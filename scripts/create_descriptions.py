# Replace REGION_NAME and REGION_ABBR in description

# python3 create_descriptions.py REGIONFILE DESCRIPTIONFILE OUTPUTDIR

# run from top level dir
# python ./scripts/create_descriptions.py ./references/usa_regions.json ./templates/description.md ./descriptions

import sys
import json

if (len(sys.argv) < 4):
  print("not enough args")
  sys.exit()

with open(sys.argv[2], 'r', encoding="utf-8") as descFile:
  global desc
  desc = descFile.read()

with open(sys.argv[1]) as regionsFile:
  global regions
  regions = json.load(regionsFile)

for abbr in regions:
  dPath = f"{sys.argv[3]}/{abbr}.md"
  f = open(dPath, 'w', encoding="utf-8")
  abbrDesc = desc.replace('REGION_NAME', f"{regions[abbr]}, USA").replace('REGION_ABBR', abbr)
  f.write(abbrDesc)
  print(f"Wrote {dPath}")
  f.close()

print(f"Finished creating descriptions in {sys.argv[3]}")