echo Mesh boolean subtracting LA
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_500m/LA-no-rivers/LA-hydro-patched_tile_1_1.STL ./state_stls_500m/LA/LA_blender_fixed.STL minus ./state_stls_500m/LA/LA_rivers.STL
echo LA result $?
echo Mesh boolean subtracting WA
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_500m/WA-no-rivers/WA-hydro-patched_tile_1_1.STL ./state_stls_500m/WA/WA_blender_fixed.STL minus ./state_stls_500m/WA/WA_rivers.STL
echo WA result $?
echo Mesh boolean subtracting NC
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_500m/NC-no-rivers/NC-hydro-patched_blender_fixed.STL ./state_stls_500m/NC/NC_blender_fixed.STL minus ./state_stls_500m/NC/NC_rivers.STL
echo NC result $?
echo Mesh boolean subtracting FL
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_500m/FL-no-rivers/FL-hydro-patched_blender_fixed.STL ./state_stls_500m/FL/FL_blender_fixed.STL minus ./state_stls_500m/FL/FL_rivers.STL
echo FL result $?
echo Mesh boolean subtracting CA
time ./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_500m/CA-no-rivers/CA-hydro-patched_blender_fixed.STL ./state_stls_500m/CA/CA_blender_fixed.STL minus ./state_stls_500m/CA/CA_rivers.STL
echo CA result $?