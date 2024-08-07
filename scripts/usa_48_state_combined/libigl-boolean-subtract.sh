echo 2 Mesh boolean subtracting usa-48-log-low-poly
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_20m/usa-48-log-low-poly-no-rivers/usa-48-log-low-poly_tile_1_1.STL ./state_stls_20m/usa-48-log-low-poly/usa-48-log-low-poly_tile_1_1.STL minus ./state_stls_20m/usa-48-log-low-poly/usa-48-log-low-poly_rivers.STL
echo usa-48-log-low-poly result $?
echo 3 Mesh boolean subtracting usa-48-log-low-poly
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_20m/usa-48-log-low-poly-no-rivers/usa-48-log-low-poly_tile_1_1.STL ./state_stls_20m/usa-48-log-low-poly-thru-river-cutout-base/usa-48-log-low-poly_tile_1_1.STL minus ./state_stls_20m/usa-48-log-low-poly-thru-river-cutout-base/usa-48-log-low-poly_thru_rivers.STL
echo usa-48-log-low-poly result $?
