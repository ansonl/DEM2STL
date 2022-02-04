#Multi-thread launching touch terrain commands in previously generated batch file
#Run this file from base project folder

# adapted from https://stackoverflow.com/a/14533902

from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call

import os
import datetime
first_time = datetime.datetime.now()

commands = []
completedCount = 0

# Run this file in root project directory
os.chdir(".")

with open('./gdalwarp-batch.sh', 'r') as fp:
    for line in fp:
        commands.append(line)

pool = Pool(6) # 6 concurrent commands at a time
for i, returncode in enumerate(pool.imap(partial(call, shell=True), commands)):
    completedCount += 1
    print(f'\r{completedCount}/{len(commands)} done', flush=True)
    if returncode != 0:
        print(f'command {i}: ' +commands[i], flush=True)
        print("command %d failed: %d" % (i, returncode), flush=True)
       
       
later_time = datetime.datetime.now()
difference = later_time - first_time
seconds_in_day = 24 * 60 * 60
elapsed = divmod(difference.days * seconds_in_day + difference.seconds, 60)
print(str(elapsed[0]) + 'm ' + str(elapsed[1]) + 's elapsed')


# Disable running of gdalcalc batch to retain truthfullness of below sea level elevations.
# Comment the system exit to depress BSL areas less and have a actual printed "bottom" for them instead of holes.
raise SystemExit(0)
# start calc batch

with open('./gdalcalc-batch.sh', 'r') as fp:
    for line in fp:
        commands.append(line)

pool = Pool(6) # 6 concurrent commands at a time
for i, returncode in enumerate(pool.imap(partial(call, shell=True), commands)):
    completedCount += 1
    print(f'\r{completedCount}/{len(commands)} done', flush=True)
    if returncode != 0:
        print(f'command {i}: ' +commands[i], flush=True)
        print("command %d failed: %d" % (i, returncode), flush=True)
       
       
later_time = datetime.datetime.now()
difference = later_time - first_time
seconds_in_day = 24 * 60 * 60
elapsed = divmod(difference.days * seconds_in_day + difference.seconds, 60)
print(str(elapsed[0]) + 'm ' + str(elapsed[1]) + 's elapsed')