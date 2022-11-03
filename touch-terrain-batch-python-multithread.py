#Multi-thread launching touch terrain commands in previously generated batch file
#Run this file from geographic-data folder

# adapted from https://stackoverflow.com/a/14533902

from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call

import os
import datetime
first_time = datetime.datetime.now()

commands = []

# Run this file in geographic_data directory
os.chdir("./")

with open('./touch-terrain-batch.sh', 'r') as fp:
    for line in fp:
        commands.append(line)

pool = Pool(1) # 4 concurrent commands at a time
for i, returncode in enumerate(pool.imap(partial(call, shell=True), commands)):
    print(f'{i}: {commands[i]} done', flush=True)
    if returncode != 0:
       print("%d command failed: %d" % (i, returncode), flush=True)
       
later_time = datetime.datetime.now()
difference = later_time - first_time
seconds_in_day = 24 * 60 * 60
elapsed = divmod(difference.days * seconds_in_day + difference.seconds, 60)
print(str(elapsed[0]) + 'm ' + str(elapsed[1]) + 's elapsed')

os.chdir("./")