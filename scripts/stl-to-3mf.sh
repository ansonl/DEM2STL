#AK stl to 3mf
stl-to-3mf AK-single.3mf ~/data/test.config AK-single "1,1,1,1|1,1,1,1|1,1,1,1|1,1,1,1" 1 1 1 AK-single.stl

stl-to-3mf AK-dual.3mf ~/data/test.config AK-dual-land-elevation "1,1,1,1|1,1,1,1|1,1,1,1|1,1,1,1" 1 1 1 AK-dual-land-elevation.stl AK-dual-hydrography "1,1,1,1|1,1,1,1|1,1,1,1|1,1,1,1" 1 1 1 AK-dual-hydrography.stl

stl-to-3mf AK-dual-transparent.3mf ~/data/test.config AK-dual-land-elevation-transparent "1,1,1,1|1,1,1,1|1,1,1,1|1,1,1,1" 1 1 1 AK-dual-land-elevation-transparent.stl AK-dual-hydrography-transparent "1,1,1,1|1,1,1,1|1,1,1,1|1,1,1,1" 1 1 1 AK-dual-hydrography-transparent.stl

#test
stl-to-3mf DC-single-test.3mf ~/data/test.config DC-single "1,0,0,0|0,1,0,0|0,0,1,0|0,0,0,1" 0 0 0 DC-single.stl

#new format
stl-to-3mf DC-single-test.3mf DC-single.stl