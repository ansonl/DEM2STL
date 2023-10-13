./batch-usa-linear.sh |& tee usa-linear-output.log
./batch-usa-sqrt.sh |& tee usa-sqrt-output.log
./batch-ak-linear.sh |& tee ak-linear-output.log
./batch-ak-sqrt.sh |& tee ak-sqrt-output.log
./batch-cn-linear.sh |& tee cn-linear-output.log

#zip up
find ./state_stls -name '*.stl' -not -path "*/250-0-1res/*" | xargs 7zzs a -mmt8 -mx9 usa-ak-cn-flat-stl.7z

find ./state_stls -name '*.3mf'| xargs 7zzs a -mmt256 -mx9 usa-ak-cn-flat-output.7z
#can't have ./ in front of passed files path for 7z to keep relative path
find state_stls -name '*.3mf'| xargs 7zzs a -mmt256 -mx9 usa-ak-cn-output.7z

7zzs a -mmt256 -mx9 usa-ak-cn-output.7z ./usa-individual-states-linear/250/PA/PA-linear-dual-transparent-v2.3mf ./usa-individual-states-linear/250/PA/PA-linear-dual-v2.3mf
