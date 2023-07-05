echo 2 Mesh boolean subtracting DC
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/DC-no-rivers/DC_tile_1_1.STL ./state_stls_250m/DC/DC_tile_1_1.STL minus ./state_stls_250m/DC/DC_rivers.STL
echo DC result $?
echo 3 Mesh boolean subtracting DC
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/DC-no-rivers/DC_tile_1_1.STL ./state_stls_250m/DC-thru-river-cutout-base/DC_tile_1_1.STL minus ./state_stls_250m/DC-thru-river-cutout-base/DC_thru_rivers.STL
echo DC result $?
echo 6 Mesh boolean subtracting RI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/RI-no-rivers/RI_tile_1_1.STL ./state_stls_250m/RI/RI_tile_1_1.STL minus ./state_stls_250m/RI/RI_rivers.STL
echo RI result $?
echo 7 Mesh boolean subtracting RI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/RI-no-rivers/RI_tile_1_1.STL ./state_stls_250m/RI-thru-river-cutout-base/RI_tile_1_1.STL minus ./state_stls_250m/RI-thru-river-cutout-base/RI_thru_rivers.STL
echo RI result $?
echo 10 Mesh boolean subtracting VI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/VI-no-rivers/VI_tile_1_1.STL ./state_stls_250m/VI/VI_tile_1_1.STL minus ./state_stls_250m/VI/VI_rivers.STL
echo VI result $?
echo 11 Mesh boolean subtracting VI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/VI-no-rivers/VI_tile_1_1.STL ./state_stls_250m/VI-thru-river-cutout-base/VI_tile_1_1.STL minus ./state_stls_250m/VI-thru-river-cutout-base/VI_thru_rivers.STL
echo VI result $?
echo 14 Mesh boolean subtracting DE
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/DE-no-rivers/DE_tile_1_1.STL ./state_stls_250m/DE/DE_tile_1_1.STL minus ./state_stls_250m/DE/DE_rivers.STL
echo DE result $?
echo 15 Mesh boolean subtracting DE
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/DE-no-rivers/DE_tile_1_1.STL ./state_stls_250m/DE-thru-river-cutout-base/DE_tile_1_1.STL minus ./state_stls_250m/DE-thru-river-cutout-base/DE_thru_rivers.STL
echo DE result $?
echo 18 Mesh boolean subtracting CT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/CT-no-rivers/CT_tile_1_1.STL ./state_stls_250m/CT/CT_tile_1_1.STL minus ./state_stls_250m/CT/CT_rivers.STL
echo CT result $?
echo 19 Mesh boolean subtracting CT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/CT-no-rivers/CT_tile_1_1.STL ./state_stls_250m/CT-thru-river-cutout-base/CT_tile_1_1.STL minus ./state_stls_250m/CT-thru-river-cutout-base/CT_thru_rivers.STL
echo CT result $?
echo 22 Mesh boolean subtracting NJ
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NJ-no-rivers/NJ_tile_1_1.STL ./state_stls_250m/NJ/NJ_tile_1_1.STL minus ./state_stls_250m/NJ/NJ_rivers.STL
echo NJ result $?
echo 23 Mesh boolean subtracting NJ
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NJ-no-rivers/NJ_tile_1_1.STL ./state_stls_250m/NJ-thru-river-cutout-base/NJ_tile_1_1.STL minus ./state_stls_250m/NJ-thru-river-cutout-base/NJ_thru_rivers.STL
echo NJ result $?
echo 26 Mesh boolean subtracting PR
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/PR-no-rivers/PR_tile_1_1.STL ./state_stls_250m/PR/PR_tile_1_1.STL minus ./state_stls_250m/PR/PR_rivers.STL
echo PR result $?
echo 27 Mesh boolean subtracting PR
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/PR-no-rivers/PR_tile_1_1.STL ./state_stls_250m/PR-thru-river-cutout-base/PR_tile_1_1.STL minus ./state_stls_250m/PR-thru-river-cutout-base/PR_thru_rivers.STL
echo PR result $?
echo 30 Mesh boolean subtracting VT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/VT-no-rivers/VT_tile_1_1.STL ./state_stls_250m/VT/VT_tile_1_1.STL minus ./state_stls_250m/VT/VT_rivers.STL
echo VT result $?
echo 31 Mesh boolean subtracting VT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/VT-no-rivers/VT_tile_1_1.STL ./state_stls_250m/VT-thru-river-cutout-base/VT_tile_1_1.STL minus ./state_stls_250m/VT-thru-river-cutout-base/VT_thru_rivers.STL
echo VT result $?
echo 34 Mesh boolean subtracting NH
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NH-no-rivers/NH_tile_1_1.STL ./state_stls_250m/NH/NH_tile_1_1.STL minus ./state_stls_250m/NH/NH_rivers.STL
echo NH result $?
echo 35 Mesh boolean subtracting NH
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NH-no-rivers/NH_tile_1_1.STL ./state_stls_250m/NH-thru-river-cutout-base/NH_tile_1_1.STL minus ./state_stls_250m/NH-thru-river-cutout-base/NH_thru_rivers.STL
echo NH result $?
echo 38 Mesh boolean subtracting MA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MA-no-rivers/MA_tile_1_1.STL ./state_stls_250m/MA/MA_tile_1_1.STL minus ./state_stls_250m/MA/MA_rivers.STL
echo MA result $?
echo 39 Mesh boolean subtracting MA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MA-no-rivers/MA_tile_1_1.STL ./state_stls_250m/MA-thru-river-cutout-base/MA_tile_1_1.STL minus ./state_stls_250m/MA-thru-river-cutout-base/MA_thru_rivers.STL
echo MA result $?
echo 42 Mesh boolean subtracting MD
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MD-no-rivers/MD_tile_1_1.STL ./state_stls_250m/MD/MD_tile_1_1.STL minus ./state_stls_250m/MD/MD_rivers.STL
echo MD result $?
echo 43 Mesh boolean subtracting MD
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MD-no-rivers/MD_tile_1_1.STL ./state_stls_250m/MD-thru-river-cutout-base/MD_tile_1_1.STL minus ./state_stls_250m/MD-thru-river-cutout-base/MD_thru_rivers.STL
echo MD result $?
echo 46 Mesh boolean subtracting IN
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/IN-no-rivers/IN_tile_1_1.STL ./state_stls_250m/IN/IN_tile_1_1.STL minus ./state_stls_250m/IN/IN_rivers.STL
echo IN result $?
echo 47 Mesh boolean subtracting IN
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/IN-no-rivers/IN_tile_1_1.STL ./state_stls_250m/IN-thru-river-cutout-base/IN_tile_1_1.STL minus ./state_stls_250m/IN-thru-river-cutout-base/IN_thru_rivers.STL
echo IN result $?
echo 50 Mesh boolean subtracting WV
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WV-no-rivers/WV_tile_1_1.STL ./state_stls_250m/WV/WV_tile_1_1.STL minus ./state_stls_250m/WV/WV_rivers.STL
echo WV result $?
echo 51 Mesh boolean subtracting WV
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WV-no-rivers/WV_tile_1_1.STL ./state_stls_250m/WV-thru-river-cutout-base/WV_tile_1_1.STL minus ./state_stls_250m/WV-thru-river-cutout-base/WV_thru_rivers.STL
echo WV result $?
echo 54 Mesh boolean subtracting SC
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/SC-no-rivers/SC_tile_1_1.STL ./state_stls_250m/SC/SC_tile_1_1.STL minus ./state_stls_250m/SC/SC_rivers.STL
echo SC result $?
echo 55 Mesh boolean subtracting SC
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/SC-no-rivers/SC_tile_1_1.STL ./state_stls_250m/SC-thru-river-cutout-base/SC_tile_1_1.STL minus ./state_stls_250m/SC-thru-river-cutout-base/SC_thru_rivers.STL
echo SC result $?
echo 58 Mesh boolean subtracting OH
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/OH-no-rivers/OH_tile_1_1.STL ./state_stls_250m/OH/OH_tile_1_1.STL minus ./state_stls_250m/OH/OH_rivers.STL
echo OH result $?
echo 59 Mesh boolean subtracting OH
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/OH-no-rivers/OH_tile_1_1.STL ./state_stls_250m/OH-thru-river-cutout-base/OH_tile_1_1.STL minus ./state_stls_250m/OH-thru-river-cutout-base/OH_thru_rivers.STL
echo OH result $?
echo 62 Mesh boolean subtracting PA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/PA-no-rivers/PA_tile_1_1.STL ./state_stls_250m/PA/PA_tile_1_1.STL minus ./state_stls_250m/PA/PA_rivers.STL
echo PA result $?
echo 63 Mesh boolean subtracting PA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/PA-no-rivers/PA_tile_1_1.STL ./state_stls_250m/PA-thru-river-cutout-base/PA_tile_1_1.STL minus ./state_stls_250m/PA-thru-river-cutout-base/PA_thru_rivers.STL
echo PA result $?
echo 66 Mesh boolean subtracting ME
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/ME-no-rivers/ME_tile_1_1.STL ./state_stls_250m/ME/ME_tile_1_1.STL minus ./state_stls_250m/ME/ME_rivers.STL
echo ME result $?
echo 67 Mesh boolean subtracting ME
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/ME-no-rivers/ME_tile_1_1.STL ./state_stls_250m/ME-thru-river-cutout-base/ME_tile_1_1.STL minus ./state_stls_250m/ME-thru-river-cutout-base/ME_thru_rivers.STL
echo ME result $?
echo 70 Mesh boolean subtracting MS
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MS-no-rivers/MS_tile_1_1.STL ./state_stls_250m/MS/MS_tile_1_1.STL minus ./state_stls_250m/MS/MS_rivers.STL
echo MS result $?
echo 71 Mesh boolean subtracting MS
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MS-no-rivers/MS_tile_1_1.STL ./state_stls_250m/MS-thru-river-cutout-base/MS_tile_1_1.STL minus ./state_stls_250m/MS-thru-river-cutout-base/MS_thru_rivers.STL
echo MS result $?
echo 74 Mesh boolean subtracting AR
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/AR-no-rivers/AR_tile_1_1.STL ./state_stls_250m/AR/AR_tile_1_1.STL minus ./state_stls_250m/AR/AR_rivers.STL
echo AR result $?
echo 75 Mesh boolean subtracting AR
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/AR-no-rivers/AR_tile_1_1.STL ./state_stls_250m/AR-thru-river-cutout-base/AR_tile_1_1.STL minus ./state_stls_250m/AR-thru-river-cutout-base/AR_thru_rivers.STL
echo AR result $?
echo 78 Mesh boolean subtracting IA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/IA-no-rivers/IA_tile_1_1.STL ./state_stls_250m/IA/IA_tile_1_1.STL minus ./state_stls_250m/IA/IA_rivers.STL
echo IA result $?
echo 79 Mesh boolean subtracting IA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/IA-no-rivers/IA_tile_1_1.STL ./state_stls_250m/IA-thru-river-cutout-base/IA_tile_1_1.STL minus ./state_stls_250m/IA-thru-river-cutout-base/IA_thru_rivers.STL
echo IA result $?
echo 82 Mesh boolean subtracting AL
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/AL-no-rivers/AL_tile_1_1.STL ./state_stls_250m/AL/AL_tile_1_1.STL minus ./state_stls_250m/AL/AL_rivers.STL
echo AL result $?
echo 83 Mesh boolean subtracting AL
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/AL-no-rivers/AL_tile_1_1.STL ./state_stls_250m/AL-thru-river-cutout-base/AL_tile_1_1.STL minus ./state_stls_250m/AL-thru-river-cutout-base/AL_thru_rivers.STL
echo AL result $?
echo 86 Mesh boolean subtracting TN
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/TN-no-rivers/TN_tile_1_1.STL ./state_stls_250m/TN/TN_tile_1_1.STL minus ./state_stls_250m/TN/TN_rivers.STL
echo TN result $?
echo 87 Mesh boolean subtracting TN
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/TN-no-rivers/TN_tile_1_1.STL ./state_stls_250m/TN-thru-river-cutout-base/TN_tile_1_1.STL minus ./state_stls_250m/TN-thru-river-cutout-base/TN_thru_rivers.STL
echo TN result $?
echo 90 Mesh boolean subtracting ND
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/ND-no-rivers/ND_tile_1_1.STL ./state_stls_250m/ND/ND_tile_1_1.STL minus ./state_stls_250m/ND/ND_rivers.STL
echo ND result $?
echo 91 Mesh boolean subtracting ND
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/ND-no-rivers/ND_tile_1_1.STL ./state_stls_250m/ND-thru-river-cutout-base/ND_tile_1_1.STL minus ./state_stls_250m/ND-thru-river-cutout-base/ND_thru_rivers.STL
echo ND result $?
echo 94 Mesh boolean subtracting KY
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/KY-no-rivers/KY_tile_1_1.STL ./state_stls_250m/KY/KY_tile_1_1.STL minus ./state_stls_250m/KY/KY_rivers.STL
echo KY result $?
echo 95 Mesh boolean subtracting KY
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/KY-no-rivers/KY_tile_1_1.STL ./state_stls_250m/KY-thru-river-cutout-base/KY_tile_1_1.STL minus ./state_stls_250m/KY-thru-river-cutout-base/KY_thru_rivers.STL
echo KY result $?
echo 98 Mesh boolean subtracting IL
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/IL-no-rivers/IL_tile_1_1.STL ./state_stls_250m/IL/IL_tile_1_1.STL minus ./state_stls_250m/IL/IL_rivers.STL
echo IL result $?
echo 99 Mesh boolean subtracting IL
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/IL-no-rivers/IL_tile_1_1.STL ./state_stls_250m/IL-thru-river-cutout-base/IL_tile_1_1.STL minus ./state_stls_250m/IL-thru-river-cutout-base/IL_thru_rivers.STL
echo IL result $?
echo 102 Mesh boolean subtracting KS
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/KS-no-rivers/KS_tile_1_1.STL ./state_stls_250m/KS/KS_tile_1_1.STL minus ./state_stls_250m/KS/KS_rivers.STL
echo KS result $?
echo 103 Mesh boolean subtracting KS
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/KS-no-rivers/KS_tile_1_1.STL ./state_stls_250m/KS-thru-river-cutout-base/KS_tile_1_1.STL minus ./state_stls_250m/KS-thru-river-cutout-base/KS_thru_rivers.STL
echo KS result $?
echo 106 Mesh boolean subtracting LA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/LA-no-rivers/LA_tile_1_1.STL ./state_stls_250m/LA/LA_tile_1_1.STL minus ./state_stls_250m/LA/LA_rivers.STL
echo LA result $?
echo 107 Mesh boolean subtracting LA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/LA-no-rivers/LA_tile_1_1.STL ./state_stls_250m/LA-thru-river-cutout-base/LA_tile_1_1.STL minus ./state_stls_250m/LA-thru-river-cutout-base/LA_thru_rivers.STL
echo LA result $?
echo 110 Mesh boolean subtracting GA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/GA-no-rivers/GA_tile_1_1.STL ./state_stls_250m/GA/GA_tile_1_1.STL minus ./state_stls_250m/GA/GA_rivers.STL
echo GA result $?
echo 111 Mesh boolean subtracting GA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/GA-no-rivers/GA_tile_1_1.STL ./state_stls_250m/GA-thru-river-cutout-base/GA_tile_1_1.STL minus ./state_stls_250m/GA-thru-river-cutout-base/GA_thru_rivers.STL
echo GA result $?
echo 114 Mesh boolean subtracting SD
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/SD-no-rivers/SD_tile_1_1.STL ./state_stls_250m/SD/SD_tile_1_1.STL minus ./state_stls_250m/SD/SD_rivers.STL
echo SD result $?
echo 115 Mesh boolean subtracting SD
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/SD-no-rivers/SD_tile_1_1.STL ./state_stls_250m/SD-thru-river-cutout-base/SD_tile_1_1.STL minus ./state_stls_250m/SD-thru-river-cutout-base/SD_thru_rivers.STL
echo SD result $?
echo 118 Mesh boolean subtracting NE
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NE-no-rivers/NE_tile_1_1.STL ./state_stls_250m/NE/NE_tile_1_1.STL minus ./state_stls_250m/NE/NE_rivers.STL
echo NE result $?
echo 119 Mesh boolean subtracting NE
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NE-no-rivers/NE_tile_1_1.STL ./state_stls_250m/NE-thru-river-cutout-base/NE_tile_1_1.STL minus ./state_stls_250m/NE-thru-river-cutout-base/NE_thru_rivers.STL
echo NE result $?
echo 122 Mesh boolean subtracting WA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WA-no-rivers/WA_tile_1_1.STL ./state_stls_250m/WA/WA_tile_1_1.STL minus ./state_stls_250m/WA/WA_rivers.STL
echo WA result $?
echo 123 Mesh boolean subtracting WA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WA-no-rivers/WA_tile_1_1.STL ./state_stls_250m/WA-thru-river-cutout-base/WA_tile_1_1.STL minus ./state_stls_250m/WA-thru-river-cutout-base/WA_thru_rivers.STL
echo WA result $?
echo 126 Mesh boolean subtracting NC
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NC-no-rivers/NC_tile_1_1.STL ./state_stls_250m/NC/NC_tile_1_1.STL minus ./state_stls_250m/NC/NC_rivers.STL
echo NC result $?
echo 127 Mesh boolean subtracting NC
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NC-no-rivers/NC_tile_1_1.STL ./state_stls_250m/NC-thru-river-cutout-base/NC_tile_1_1.STL minus ./state_stls_250m/NC-thru-river-cutout-base/NC_thru_rivers.STL
echo NC result $?
echo 130 Mesh boolean subtracting VA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/VA-no-rivers/VA_tile_1_1.STL ./state_stls_250m/VA/VA_tile_1_1.STL minus ./state_stls_250m/VA/VA_rivers.STL
echo VA result $?
echo 131 Mesh boolean subtracting VA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/VA-no-rivers/VA_tile_1_1.STL ./state_stls_250m/VA-thru-river-cutout-base/VA_tile_1_1.STL minus ./state_stls_250m/VA-thru-river-cutout-base/VA_thru_rivers.STL
echo VA result $?
echo 134 Mesh boolean subtracting WI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WI-no-rivers/WI_tile_1_1.STL ./state_stls_250m/WI/WI_tile_1_1.STL minus ./state_stls_250m/WI/WI_rivers.STL
echo WI result $?
echo 135 Mesh boolean subtracting WI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WI-no-rivers/WI_tile_1_1.STL ./state_stls_250m/WI-thru-river-cutout-base/WI_tile_1_1.STL minus ./state_stls_250m/WI-thru-river-cutout-base/WI_thru_rivers.STL
echo WI result $?
echo 138 Mesh boolean subtracting MO
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MO-no-rivers/MO_tile_1_1.STL ./state_stls_250m/MO/MO_tile_1_1.STL minus ./state_stls_250m/MO/MO_rivers.STL
echo MO result $?
echo 139 Mesh boolean subtracting MO
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MO-no-rivers/MO_tile_1_1.STL ./state_stls_250m/MO-thru-river-cutout-base/MO_tile_1_1.STL minus ./state_stls_250m/MO-thru-river-cutout-base/MO_thru_rivers.STL
echo MO result $?
echo 142 Mesh boolean subtracting OK
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/OK-no-rivers/OK_tile_1_1.STL ./state_stls_250m/OK/OK_tile_1_1.STL minus ./state_stls_250m/OK/OK_rivers.STL
echo OK result $?
echo 143 Mesh boolean subtracting OK
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/OK-no-rivers/OK_tile_1_1.STL ./state_stls_250m/OK-thru-river-cutout-base/OK_tile_1_1.STL minus ./state_stls_250m/OK-thru-river-cutout-base/OK_thru_rivers.STL
echo OK result $?
echo 146 Mesh boolean subtracting UT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/UT-no-rivers/UT_tile_1_1.STL ./state_stls_250m/UT/UT_tile_1_1.STL minus ./state_stls_250m/UT/UT_rivers.STL
echo UT result $?
echo 147 Mesh boolean subtracting UT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/UT-no-rivers/UT_tile_1_1.STL ./state_stls_250m/UT-thru-river-cutout-base/UT_tile_1_1.STL minus ./state_stls_250m/UT-thru-river-cutout-base/UT_thru_rivers.STL
echo UT result $?
echo 150 Mesh boolean subtracting WY
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WY-no-rivers/WY_tile_1_1.STL ./state_stls_250m/WY/WY_tile_1_1.STL minus ./state_stls_250m/WY/WY_rivers.STL
echo WY result $?
echo 151 Mesh boolean subtracting WY
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/WY-no-rivers/WY_tile_1_1.STL ./state_stls_250m/WY-thru-river-cutout-base/WY_tile_1_1.STL minus ./state_stls_250m/WY-thru-river-cutout-base/WY_thru_rivers.STL
echo WY result $?
echo 154 Mesh boolean subtracting CO
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/CO-no-rivers/CO_tile_1_1.STL ./state_stls_250m/CO/CO_tile_1_1.STL minus ./state_stls_250m/CO/CO_rivers.STL
echo CO result $?
echo 155 Mesh boolean subtracting CO
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/CO-no-rivers/CO_tile_1_1.STL ./state_stls_250m/CO-thru-river-cutout-base/CO_tile_1_1.STL minus ./state_stls_250m/CO-thru-river-cutout-base/CO_thru_rivers.STL
echo CO result $?
echo 158 Mesh boolean subtracting NY
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NY-no-rivers/NY_tile_1_1.STL ./state_stls_250m/NY/NY_tile_1_1.STL minus ./state_stls_250m/NY/NY_rivers.STL
echo NY result $?
echo 159 Mesh boolean subtracting NY
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NY-no-rivers/NY_tile_1_1.STL ./state_stls_250m/NY-thru-river-cutout-base/NY_tile_1_1.STL minus ./state_stls_250m/NY-thru-river-cutout-base/NY_thru_rivers.STL
echo NY result $?
echo 162 Mesh boolean subtracting MN
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MN-no-rivers/MN_tile_1_1.STL ./state_stls_250m/MN/MN_tile_1_1.STL minus ./state_stls_250m/MN/MN_rivers.STL
echo MN result $?
echo 163 Mesh boolean subtracting MN
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MN-no-rivers/MN_tile_1_1.STL ./state_stls_250m/MN-thru-river-cutout-base/MN_tile_1_1.STL minus ./state_stls_250m/MN-thru-river-cutout-base/MN_thru_rivers.STL
echo MN result $?
echo 166 Mesh boolean subtracting NM
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NM-no-rivers/NM_tile_1_1.STL ./state_stls_250m/NM/NM_tile_1_1.STL minus ./state_stls_250m/NM/NM_rivers.STL
echo NM result $?
echo 167 Mesh boolean subtracting NM
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NM-no-rivers/NM_tile_1_1.STL ./state_stls_250m/NM-thru-river-cutout-base/NM_tile_1_1.STL minus ./state_stls_250m/NM-thru-river-cutout-base/NM_thru_rivers.STL
echo NM result $?
echo 170 Mesh boolean subtracting AZ
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/AZ-no-rivers/AZ_tile_1_1.STL ./state_stls_250m/AZ/AZ_tile_1_1.STL minus ./state_stls_250m/AZ/AZ_rivers.STL
echo AZ result $?
echo 171 Mesh boolean subtracting AZ
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/AZ-no-rivers/AZ_tile_1_1.STL ./state_stls_250m/AZ-thru-river-cutout-base/AZ_tile_1_1.STL minus ./state_stls_250m/AZ-thru-river-cutout-base/AZ_thru_rivers.STL
echo AZ result $?
echo 174 Mesh boolean subtracting OR
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/OR-no-rivers/OR_tile_1_1.STL ./state_stls_250m/OR/OR_tile_1_1.STL minus ./state_stls_250m/OR/OR_rivers.STL
echo OR result $?
echo 175 Mesh boolean subtracting OR
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/OR-no-rivers/OR_tile_1_1.STL ./state_stls_250m/OR-thru-river-cutout-base/OR_tile_1_1.STL minus ./state_stls_250m/OR-thru-river-cutout-base/OR_thru_rivers.STL
echo OR result $?
echo 178 Mesh boolean subtracting ID
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/ID-no-rivers/ID_tile_1_1.STL ./state_stls_250m/ID/ID_tile_1_1.STL minus ./state_stls_250m/ID/ID_rivers.STL
echo ID result $?
echo 179 Mesh boolean subtracting ID
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/ID-no-rivers/ID_tile_1_1.STL ./state_stls_250m/ID-thru-river-cutout-base/ID_tile_1_1.STL minus ./state_stls_250m/ID-thru-river-cutout-base/ID_thru_rivers.STL
echo ID result $?
echo 182 Mesh boolean subtracting NV
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NV-no-rivers/NV_tile_1_1.STL ./state_stls_250m/NV/NV_tile_1_1.STL minus ./state_stls_250m/NV/NV_rivers.STL
echo NV result $?
echo 183 Mesh boolean subtracting NV
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/NV-no-rivers/NV_tile_1_1.STL ./state_stls_250m/NV-thru-river-cutout-base/NV_tile_1_1.STL minus ./state_stls_250m/NV-thru-river-cutout-base/NV_thru_rivers.STL
echo NV result $?
echo 186 Mesh boolean subtracting MI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MI-no-rivers/MI_tile_1_1.STL ./state_stls_250m/MI/MI_tile_1_1.STL minus ./state_stls_250m/MI/MI_rivers.STL
echo MI result $?
echo 187 Mesh boolean subtracting MI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MI-no-rivers/MI_tile_1_1.STL ./state_stls_250m/MI-thru-river-cutout-base/MI_tile_1_1.STL minus ./state_stls_250m/MI-thru-river-cutout-base/MI_thru_rivers.STL
echo MI result $?
echo 190 Mesh boolean subtracting MT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MT-no-rivers/MT_tile_1_1.STL ./state_stls_250m/MT/MT_tile_1_1.STL minus ./state_stls_250m/MT/MT_rivers.STL
echo MT result $?
echo 191 Mesh boolean subtracting MT
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/MT-no-rivers/MT_tile_1_1.STL ./state_stls_250m/MT-thru-river-cutout-base/MT_tile_1_1.STL minus ./state_stls_250m/MT-thru-river-cutout-base/MT_thru_rivers.STL
echo MT result $?
echo 194 Mesh boolean subtracting FL
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/FL-no-rivers/FL_tile_1_1.STL ./state_stls_250m/FL/FL_tile_1_1.STL minus ./state_stls_250m/FL/FL_rivers.STL
echo FL result $?
echo 195 Mesh boolean subtracting FL
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/FL-no-rivers/FL_tile_1_1.STL ./state_stls_250m/FL-thru-river-cutout-base/FL_tile_1_1.STL minus ./state_stls_250m/FL-thru-river-cutout-base/FL_thru_rivers.STL
echo FL result $?
echo 198 Mesh boolean subtracting CA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/CA-no-rivers/CA_tile_1_1.STL ./state_stls_250m/CA/CA_tile_1_1.STL minus ./state_stls_250m/CA/CA_rivers.STL
echo CA result $?
echo 199 Mesh boolean subtracting CA
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/CA-no-rivers/CA_tile_1_1.STL ./state_stls_250m/CA-thru-river-cutout-base/CA_tile_1_1.STL minus ./state_stls_250m/CA-thru-river-cutout-base/CA_thru_rivers.STL
echo CA result $?
echo 202 Mesh boolean subtracting TX
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/TX-no-rivers/TX_tile_1_1.STL ./state_stls_250m/TX/TX_tile_1_1.STL minus ./state_stls_250m/TX/TX_rivers.STL
echo TX result $?
echo 203 Mesh boolean subtracting TX
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/TX-no-rivers/TX_tile_1_1.STL ./state_stls_250m/TX-thru-river-cutout-base/TX_tile_1_1.STL minus ./state_stls_250m/TX-thru-river-cutout-base/TX_thru_rivers.STL
echo TX result $?
