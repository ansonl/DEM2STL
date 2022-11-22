echo Mesh boolean subtracting LA
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/LA-no-rivers/LA-hydro-patched_tile_1_1.STL ./state_stls/LA/LA-blender.STL minus ./state_stls/LA/LA_rivers.STL
echo LA result $?
echo Mesh boolean subtracting WA
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/WA-no-rivers/WA-hydro-patched_tile_1_1.STL ./state_stls/WA/WA-blender.STL minus ./state_stls/WA/WA_rivers.STL
echo WA result $?
echo Mesh boolean subtracting NC
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/NC-no-rivers/NC-hydro-patched-blender.STL ./state_stls/NC/NC-blender.STL minus ./state_stls/NC/NC_rivers.STL
echo NC result $?
echo Mesh boolean subtracting FL
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/FL-no-rivers/FL-hydro-patched-blender.STL ./state_stls/FL/FL-blender.STL minus ./state_stls/FL/FL_rivers.STL
echo FL result $?
echo Mesh boolean subtracting CA
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/CA-no-rivers/CA-hydro-patched-blender.STL ./state_stls/CA/CA-blender.STL minus ./state_stls/CA/CA_rivers.STL
echo CA result $?