#extract
7zzs x -mmt256 -mx9 

./batch-usa-linear.sh |& tee usa-linear-output.log
./batch-usa-sqrt.sh |& tee usa-sqrt-output.log
./batch-ak-linear.sh |& tee ak-linear-output.log
./batch-ak-sqrt.sh |& tee ak-sqrt-output.log
./batch-cn-linear.sh |& tee cn-linear-output.log

#go to top level folder with all subregion directories
../../../organize-stls-release.sh

~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/usa-individual-states-linear/250/ linear v2 \#C5F178FF \#2AE3FFFF
~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/usa-individual-states-sqrt/250/ sqrt v1 \#FFE066FF \#2AE3FFFF
~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/ak-na-conformal-conic-linear/250/ linear v1 \#C5F178FF \#2AE3FFFF
~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/ak-na-conformal-conic-sqrt/250/ sqrt v1 \#FFE066FF \#2AE3FFFF
~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/cn-asia-conformal-conic-linear/1000/ linear v1 \#C5F178FF \#2AE3FFFF
~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/cn-asia-conformal-conic-sqrt/1000/ sqrt v1 \#FFE066FF \#2AE3FFFF

~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/williamstown-ma-usa-linear/3.6/ linear v1 \#C5F178FF \#2AE3FFFF


#zip up
find ./state_stls -name '*.stl' -not -path "*/250-0-1res/*" | xargs 7zzs a -mmt8 -mx9 usa-ak-cn-flat-stl.7z

find ./state_stls -name '*.3mf' -not -path "*/250-0-1res/*" | xargs 7zzs a -mmt8 -mx9 usa-ak-cn-flat-3mf.7z

find ./state_stls -name '*.3mf'| xargs 7zzs a -mmt256 -mx9 usa-ak-cn-flat-3mf.7z
#can't have ./ in front of passed files path for 7z to keep relative path
find state_stls -name '*.3mf'| xargs 7zzs a -mmt256 -mx9 usa-ak-cn-output.7z