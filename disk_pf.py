
import win32com.client as client

import time
import copy

com = client.Dispatch("WbemScripting.SWbemRefresher")
obj = client.GetObject("winmgmts:\\root\cimv2")
diskitems = com.AddEnum(obj, "Win32_PerfFormattedData_PerfDisk_LogicalDisk").objectSet
    #time.sleep(1)

diskitems = com.AddEnum(obj, "Win32_PerfRawData_PerfDisk_PhysicalDisk").objectSet



com.Refresh()


for k in diskitems:
    print(k.name)



start = diskitems[0].DiskReadsPerSec




class DiskAttribuce(obj):
    def __init__(self, disk):
        self.CurrentDiskQueueLength = disk.CurrentDiskQueueLength
        self.DiskBytesPerSec = disk.CurrentDiskQueueLength
        self.DiskReadBytesPerSec = disk.CurrentDiskQueueLength
        self.DiskReadsPerSec = disk.CurrentDiskQueueLength
        self.DiskTransfersPerSec = disk.CurrentDiskQueueLength
        self.DiskWriteBytesPerSec = disk.CurrentDiskQueueLength
        self.DiskWritesPerSec = disk.CurrentDiskQueueLength


class DiskItem(object):
    def __init__(self):

        self.com = client.Dispatch("WbemScripting.SWbemRefresher")
        obj = client.GetObject("winmgmts:\\root\cimv2")
#diskitems = com.AddEnum(obj, "Win32_PerfFormattedData_PerfDisk_LogicalDisk").objectSet
    #time.sleep(1)

        self.diskitems = self.com.AddEnum(obj, "Win32_PerfRawData_PerfDisk_PhysicalDisk").objectSet

        self.com.Refresh()

        # self.CurrentDiskQueueLength = 0
        # self.Description = 0
        # self.DiskBytesPerSec = 0
        # self.DiskReadBytesPerSec = 0
        # self.DiskReadsPerSec = 0
        # self.DiskTransfersPerSec =0
        # self.DiskWriteBytesPerSec = 0
        # self.DiskWritesPerSec = 0


    def get_attribute(self, disknum = 0):
        self.com.Refresh()


        
        disk = self.diskitems[disknum]
        dict_attribute = {
        "CurrentDiskQueueLength" :disk.CurrentDiskQueueLength,
        #"Description" : disk.Description,
        "DiskBytesPerSec" : disk.DiskBytesPerSec,
        "DiskReadBytesPerSec" : disk.DiskReadBytesPerSec,
        "DiskReadsPerSec" : disk.DiskReadsPerSec,
        "DiskTransfersPerSec" : disk.DiskTransfersPerSec,
        "DiskWriteBytesPerSec" : disk.DiskWriteBytesPerSec,
        "DiskWritesPerSec" : disk.DiskWritesPerSec
        }
        return dict_attribute

    def per_sec_performance(self, disknum = 0):
      
        
        init = self.get_attribute(disknum)
        time.sleep(1)
        print(init["DiskTransfersPerSec"])
        while True:
            start = time.time()
            current = self.get_attribute(disknum)
            dict_performance = {
            "CurrentDiskQueueLength" :current["CurrentDiskQueueLength"],
            #"Description" : disk.Description,
            "DiskBytesPerSec" : int(current["DiskBytesPerSec"]) - int(init["DiskBytesPerSec"]),
            "DiskReadBytesPerSec" : int(current["DiskReadBytesPerSec"]) - int(init["DiskReadBytesPerSec"]),
            "DiskReadsPerSec" : current["DiskReadsPerSec"] - init["DiskReadsPerSec"],
            "DiskTransfersPerSec" : current["DiskTransfersPerSec"] - init["DiskTransfersPerSec"],
            "DiskWriteBytesPerSec" : int(current["DiskWriteBytesPerSec"]) - int(init["DiskWriteBytesPerSec"]),
            "DiskWritesPerSec" : int(current["DiskWritesPerSec"]) - int(init["DiskWritesPerSec"])
            }
            print(dict_performance)
            init = current
            while  time.time() - start < 1:
                time.sleep(0.000001)
                continue
            #print(time.time() - start)
a = DiskItem()

a.per_sec_performance()


# while True:

#     t_1=time.time()

#     # print(a.get_attribute(0))
#     a.per_sec_performance(0)
#     t_2 = time.time()
#     print(t_2 - t_1)
#     time.sleep(1)



# for item in diskitems:
#     print(item.Name)
#     # for a in item.
#     #     print(a)
#     #print(float(item.DiskReadsPerSec))
#     # if item.Name in data_dict:
#     #     data_dict[item.Name]['io_stat'] = {}
#     #     data_dict[item.Name]['io_stat']['r/s'] = {'volume':float(item.DiskReadsPerSec), 'unit':''}
#     #     data_dict[item.Name]['io_stat']['w/s'] = {'volume':float(item.DiskWritesPerSec), 'unit':''}
#     #     data_dict[item.Name]['io_stat']['rkB/s'] = {'volume':(float(item.DiskReadBytesPerSec) / 1024), 'unit':'KB/s'}
#     #     data_dict[item.Name]['io_stat']['wkB/s'] = {'volume':(float(item.DiskWriteBytesPerSec) / 1024), 'unit':'KB/s'}
# print(data_dict)



# class Win32_PerfRawData_PerfDisk_PhysicalDisk : Win32_PerfRawData
# {
#   uint64 AvgDiskBytesPerRead;
#   uint32 AvgDiskBytesPerRead_Base;
#   uint64 AvgDiskBytesPerTransfer;
#   uint64 AvgDiskBytesPerTransfer_Base;
#   uint64 AvgDiskBytesPerWrite;
#   uint64 AvgDiskBytesPerWrite_Base;
#   uint64 AvgDiskQueueLength;
#   uint64 AvgDiskReadQueueLength;
#   uint32 AvgDiskSecPerRead;
#   uint32 AvgDiskSecPerRead_Base;
#   uint32 AvgDiskSecPerTransfer;
#   uint32 AvgDiskSecPerTransfer_Base;
#   uint32 AvgDiskSecPerWrite;
#   uint32 AvgDiskSecPerWrite_Base;
#   uint64 AvgDiskWriteQueueLength;
#   string Caption;
#   uint32 CurrentDiskQueueLength;
#   string Description;
#   uint64 DiskBytesPerSec;
#   uint64 DiskReadBytesPerSec;
#   uint32 DiskReadsPerSec;
#   uint32 DiskTransfersPerSec;
#   uint64 DiskWriteBytesPerSec;
#   uint32 DiskWritesPerSec;
#   uint64 Frequency_Object;
#   uint64 Frequency_PerfTime;
#   uint64 Frequency_Sys100NS;
#   string Name;
#   uint64 PercentDiskReadTime;
#   uint64 PercentDiskReadTime_Base;
#   uint64 PercentDiskTime;
#   uint64 PercentDiskTime_Base;
#   uint64 PercentDiskWriteTime;
#   uint64 PercentDiskWriteTime_Base;
#   uint64 PercentIdleTime;
#   uint64 PercentIdleTime_Base;
#   uint32 SplitIOPerSec;
#   uint64 Timestamp_Object;
#   uint64 Timestamp_PerfTime;
#   uint64 Timestamp_Sys100NS;
# };