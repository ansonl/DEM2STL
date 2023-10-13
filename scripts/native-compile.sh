module use /usr/share/Modules/modulefiles
module load compile/gcc/12.2.0
module load openmpi/1.10.7

$PWD/../gcc-4.6.2/configure --prefix=$HOME/GCC-4.6.2 
make
make install

mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ 
make


#set new lib search path
export LD_LIBRARY_PATH=/share/spack/gcc-10.3.0/gcc-12.2.0-4dp/lib64:$LD_LIBRARY_PATH

#install 3mf addon
#manuall move 3mf to blender program files folder
bpy.ops.preferences.addon_enable(module='io_mesh_3mf')
bpy.ops.wm.save_userpref()


./blender -b -noaudio
./blender -b --python-console

