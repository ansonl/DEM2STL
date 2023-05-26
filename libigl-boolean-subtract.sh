echo Mesh boolean subtracting SC
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/SC-no-rivers/SC-hydro-patched_tile_1_1.STL ./state_stls_250m/SC/SC_tile_1_1.STL minus ./state_stls_250m/SC/SC_rivers.STL
echo SC result $?
echo Mesh boolean subtracting ME
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/ME-no-rivers/ME-hydro-patched_tile_1_1.STL ./state_stls_250m/ME/ME_tile_1_1.STL minus ./state_stls_250m/ME/ME_rivers.STL
echo ME result $?
