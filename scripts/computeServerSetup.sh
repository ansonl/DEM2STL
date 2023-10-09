lsblk

sudo file -s /dev/nvme1n1
#Format device if no filesystem exists
#sudo mkfs -t xfs /dev/nvme1n1 

sudo mkdir /ebsData
sudo mount /dev/nvme1n1 /ebsData

sudo yum install git
sudo yum group install "Development Tools" "open-ssl-devel"

pip3 install ComplexHTTPServer #python3 -m ComplexHTTPServer XXXX

#7zip
#extract
7z x FILE.7z
#archive
7z a myzip ./FOLDER/*

#setup swap
sudo swapon -s
sudo mkswap /dev/nvme1n1
sudo swapon /dev/nvme1n1

#unmount
sudo umount -d /dev/nvme1n1


wget http://XXX:8727/usa-ak-combined.7z
~/7zz x usa-ak-combined.7z
#run script and log
./combined.sh |& tee output.log

#get tools
tar -xvf 7zip23.tar
chmod 777 ./7zz
chmod 777 ./7zzs
./7zz x amazon-linux-2-precompiled.7z


chmod 777 *.sh

#fetch data from s3

#run script and log
./meshBoolean-batch-combined-usa.sh |& tee usa-output.log

./meshBoolean-batch-combined-ak.sh |& tee ak-output.log