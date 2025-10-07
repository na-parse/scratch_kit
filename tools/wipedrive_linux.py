import os
import json
import time
import datetime

## CHANGE ME
# Specify the /dev/XXX name
wipedev = 'sde'
## CHANGE ME



## Optional CHANGE MEs
wipeBlock = b'\x00' * 1024 * 1024
reportTime = 15

def get_disk_size(blockdev):
    sizeInBytes = int(open('/sys/block/{blockdev}/size'.format(**locals())).read())
    return sizeInBytes

def get_current_time():
  rightNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  return rightNow

def report_capacity(size_in_bytes):
    # function to report cap value in most convenient unit
    units = ['B','KiB','MiB','GiB','TiB','PiB','XiB']
    unitStep = 0
    while size_in_bytes > 1024 and unitStep < len(units):
        size_in_bytes = round(size_in_bytes / 1024,2)
        unitStep += 1
    reportValue = f'{size_in_bytes} {units[unitStep]}'
    return reportValue

def report_time(timeInSeconds):
    reportUnit = 's'
    reportValue = timeInSeconds
    # break limits
    changeSecondsToMinutes = 120 # two minutes
    changeMinutesToHours = 120 # two hours
    changeHoursToDays = 36 # 3 days
    if reportValue > changeSecondsToMinutes:
        reportValue = int(reportValue / 60)
        reportUnit = 'm'
    if reportValue > changeMinutesToHours:
        reportValue = int(reportValue/60)
        reportUnit = 'h'
    if reportValue > changeHoursToDays:
        reportValue = int(reportValue/24)
        reportUnit = 'd'
    return f'{reportValue}{reportUnit}'

try:
    print(f'!!!!! THIS WILL WIPE THE FOLLOWING DEVICE !!!!!')
    print(f'-- /dev/{wipedev}\n')
    response = input(f'Are you SURE? Enter \'confirm\' to proceed > ')
    if not response.upper() == 'CONFIRM':
      print(f'Aborting...')
      exit()
    else:
      print(f'!!! Proceeding to wipe /dev/{wipedev}')
    
    writtenBytes = 0
    startTime = time.time()
    diskSize = get_disk_size(wipedev)
    if not diskSize:
      print(f'ERROR: Unable to find disk size.')
      exit()
    
    lastReportTime = startTime
    with open(f'/dev/{wipedev}','wb+') as f:
        while True:
            writtenBytes += f.raw.write(wipeBlock)
            if (lastReportTime + reportTime) < time.time():
              remainingBytes = diskSize - writtenBytes
              writtenRate = int(writtenBytes / (time.time() - startTime))
              estimatedRemainingRate = int(remainingBytes / writtenRate)
              print(f'{get_current_time()} - Written {report_capacity(writtenBytes)} at {report_capacity(writtenRate)}/s - ({report_time(estimatedRemainingRate)} remaining)')
              
              lastReportTime = time.time()
except Exception as e:
    Exception(e)


