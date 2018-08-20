import wmi
# myWmi = wmi.WMI()
# for cls in myWmi.classes:
#     print(cls)

c = wmi.WMI()

tmplist = []
for physical_disk in c.Win32_DiskDrive():
    tmpdict ={}
    print(physical_disk)
    tmpdict["Caption"] = physical_disk.Caption
    tmpdict["Size"] = int(physical_disk.Size)/1024/1024/1024
    tmplist.append(tmpdict)
print(tmplist)




# import wmi

# import os

# import sys

# import platform

# import time

# import win32com.client as client

# import json

# class DataPollster(object):

 

#     def get_cpu(self):

#         # Initilization

#         c = wmi.WMI()

#         data_dict = {}

#         for cpu in c.Win32_Processor():

#             device = cpu.DeviceID.lower()

 

#             # Get cpu_usage

#             data_dict[device] = {'volume':float(cpu.LoadPercentage), 'unit':'%'}

#         return data_dict




# def get_disk():

#     c = wmi.WMI ()



#     data_dict = {}

#     data_dict['total_available'] = 0

#     data_dict['total_capacity'] = 0

#     data_dict['total_free'] = 0

#     #  DriveType=3 : "Local Disk",

#     for disk in c.Win32_LogicalDisk (DriveType=3):

#         data_dict['total_available'] += round(float(disk.FreeSpace) / (1024*1024*1024), 2)
#         data_dict['total_capacity'] += round(float(disk.Size) / (1024*1024*1024), 2)
#         data_dict['total_free'] += round(float(disk.FreeSpace) / (1024*1024*1024), 2)



#         dev_tmp = {}

#         dev_tmp['dev'] = disk.DeviceID

#         dev_tmp['available'] = {'volume':round(float(disk.FreeSpace) / (1024*1024*1024), 2), 'unit':'GB'}

#         dev_tmp['capacity'] = {'volume':round(float(disk.Size) / (1024*1024*1024), 2), 'unit':'GB'}

#         dev_tmp['free'] = {'volume':round(float(disk.FreeSpace) / (1024*1024*1024), 2), 'unit':'GB'}

#         dev_tmp['fstype'] = disk.FileSystem

#         dev_tmp['mnt'] = ''

#         #dev_tmp['used'] = round(long(disk.FreeSpace) / long(disk.Size), 2)



#         data_dict[disk.DeviceID] = dev_tmp



#     com = client.Dispatch("WbemScripting.SWbemRefresher")

#     obj = client.GetObject("winmgmts:\\root\cimv2")

#     diskitems = com.AddEnum(obj, "Win32_PerfFormattedData_PerfDisk_LogicalDisk").objectSet

    
#     com.Refresh()

#     for item in diskitems:

#         if item.Name in data_dict:

#             data_dict[item.Name]['io_stat'] = {}

#             data_dict[item.Name]['io_stat']['r/s'] = {'volume':float(item.DiskReadsPerSec), 'unit':''}

#             data_dict[item.Name]['io_stat']['w/s'] = {'volume':float(item.DiskWritesPerSec), 'unit':''}

#             data_dict[item.Name]['io_stat']['rkB/s'] = {'volume':(float(item.DiskReadBytesPerSec) / 1024), 'unit':'KB/s'}

#             data_dict[item.Name]['io_stat']['wkB/s'] = {'volume':(float(item.DiskWriteBytesPerSec) / 1024), 'unit':'KB/s'}

#     return {'data':data_dict, 'timestamp':time.asctime(time.localtime())}




# print(get_disk())


# # for k in c.Win32_LogicalDisk():
# #     print(k)
