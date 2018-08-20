import commands
import time
import os
import re
import random
def sysdiskcheck(sdid):
    """
    Confirm whether device is a system disk"""


    try:
        re.compile('/dev/s[dg][a-z0-9]+$').match(sdid)
    except:
        raise Exception("sdid's Format is wrong:%s" %sdid)

    # if not sdid:
    #     raise Exception("sdid is none!")
    # elif "/dev/s" not in sdid
    #     raise Exception("sdid's Format is wrong:%s" %sdid)    
    cmd = "df | grep ' /$'"
    #result = exe_cmd(cmd)
    # result = commands.getoutput(r"df | grep ' /$'")
    # if not result:
    #     raise Exception("'df | grep ' /$' execute return none")`

    if sdid in exe_cmd(cmd):
        ret = True
    else:
        ret = False
    return ret


def exe_cmd(cmd=""):
    ret, output = commands.getstatusoutput(cmd)
    #print output
    if ret == 256:
        ret = 0
    if ret:
        
        raise Exception("Execute %s" %cmd)
        
    return output


def trim_disk(sdid):
    if not sdid:
        raise Exception("sdid is none!")
    cmd = "./Trim.py -d %s -all" %sdid
    return exe_cmd(cmd)
    #ret, output = commands.getstatusoutput("./Trim.py -d %s -all" %sdid) 

def Linux_set_partition(sdid, partition = 1):


    if sysdiskcheck(sdid):
        raise Exception("input sdid is system disk!")
    
    trim_disk(sdid)

    cmd = "hdparm -N %s | grep max | awk '{print $4}'| awk -F '/' '{print $1}'" %sdid
    
    max_sector_str = exe_cmd(cmd)
    try:
        max_sector = int(max_sector_str)
    except:
        raise Exception("max_sector is not a number: %s" %max_sector_str)
    
    partition_size = max_sector / partition
    partitionNameList=[]

    if partition <= 4:

        for cnt in range(1, partition):
            cmd = "echo -e 'n\np\n\n\n+%d\nw\n' | fdisk %s" %(partition_size, sdid)

            exe_cmd(cmd)
            partitionNameList.append("%s%d" %(sdid,cnt))
        
        cmd = "echo -e 'n\np\n\n\n\nw\n' | fdisk %s" %sdid
        exe_cmd(cmd)
        partitionNameList.append("%s%d" %(sdid,partition))
        
    elif partition > 4:

        for cnt in range(1, 4):
            cmd = "echo -e 'n\np\n\n\n+%d\nw\n' | fdisk %s" %(partition_size, sdid)
            exe_cmd(cmd)
            partitionNameList.append("%s%d" %(sdid,cnt))
        
        cmd = "echo -e 'n\ne\n\n\n\nw\n' | fdisk %s" %sdid
        exe_cmd(cmd)
        
        for cnt in range(4, partition):
            cmd = "echo -e 'n\n\n+%d\nw\n' | fdisk %s" %(partition_size, sdid)
            exe_cmd(cmd)
            partitionNameList.append("%s%d" %(sdid,(cnt+1)))

        cmd = "echo -e 'n\n\n\nw\n' | fdisk %s" %sdid

        exe_cmd(cmd)

        
        partitionNameList.append("%s%d" %(sdid,(partition+1)))
    return partitionNameList
    # for cnt in range(1, partition):
def mkfsANDmount(partition_name = "", filesystem = ""):
    
    sysdiskcheck(partition_name)

    FileSystemDict = {
        "ext2": "echo -e 'y\n'| mkfs -t ext2 ",
        "ext3": "echo -e 'y\n'| mkfs -t ext3 ",
        "ext4": "echo -e 'y\n'| mkfs -t ext4 ",
        "xfs": "mkfs -t xfs -f ",
        "ntfs": "mkfs -t ntfs -f ",
        "fat": "mkfs -t fat "
        }
        
    if FileSystemDict.get(filesystem):
        cmd_list = []

        if partition_name in exe_cmd("mount"):
            exe_cmd("umount %s" %partition_name)

        if os.path.exists('/mnt/%s' %partition_name.split("/")[-1]) is False:
            os.mkdir('/mnt/%s' %partition_name.split("/")[-1])

        cmd_list.append(FileSystemDict.get(filesystem) + partition_name)
        # cmd_list.append('rm -rf /mnt/%s' %partition_name.split("/")[-1])
        # cmd_list.append('mkdir /mnt/%s' %partition_name.split("/")[-1])
        cmd_list.append("mount %s /mnt/%s" %(partition_name,partition_name.split("/")[-1]))

        for cmd in cmd_list:
            #print cmd
            time.sleep(1)
            #print exe_cmd(cmd)
        return '/mnt/%s' %partition_name.split("/")[-1]




# def set_common_fs_and_partition(sdid, partition = 1,fs= 'ext4'):

#     for k in Linux_set_partition(sdid, partition):
#         mkfsANDmount(k, fs)












class VdbenchFileSystemConfig(object):




    def create_fsd(self,fsd="",anchor="",depth=1,width=1,files=1,size="(4k,50,1m,10,256k,10,512k,20,64k,10)"):
    

        fsd_str = 'fsd=%s,anchor=%s,depth=%s,width=%s,files=%s,size=%s,openflags=o_direct'\
        %(fsd,anchor,depth,width,files,size)
        return fsd_str

    def create_fwd(self,fwd="fwd1",fsd="fsd*"):

        fwd_str = 'fwd=%s,fsd=%s,fileio=random\n' %(fwd, fsd)
        return fwd_str


    def create_rd(self,rd='rd1', fwd='fwd*', forxfersize="4k",rdpct ="10",threads="32" ,elapsed="300"):

        rd_str = 'rd=%s,fwd=%s,fwdrate=max,format=yes,interval=1,\
elapsed=%s,forrdpct=(%s),forthreads=(%s),forxfersize=(%s),foroperation=(read)\n'\
        %(rd, fwd,elapsed,rdpct,threads,forxfersize)
        return rd_str


    def getFSDs(self,anchorlist=["/mnt/sdd1","/mnt/sdd2"],pathsize=10):
        fsd_list = ""
        depth = random.randint(2,5)
        width = random.randint(1,6)
        files = pathsize*1024/(depth**width)/2

        for k in anchorlist:
            fsd = "fsd%d" %anchorlist.index(k)
            anchor = k
            fsd_list = fsd_list + self.create_fsd(fsd,anchor,depth,width,files,size="(4k,50,1m,10,256k,10,512k,20,64k,10)") +'\n'
        return fsd_list

    def getRDs(self,rdlist=[["4k","10","32","300"],["5k","10","32","300"]]):
        
        rd_str = ''
        
        for k in rdlist:
            rd = "rd%d" %rdlist.index(k)
            fwd = 'fwd*'
            forxfersize=k[0]
            rdpct =k[1]
            threads=k[2]
            elapsed=k[3]
            
            rd_str = rd_str + self.create_rd(rd, fwd, forxfersize,rdpct ,threads,elapsed)
        return rd_str


    def getRDs2(self,rdlist=["4k/10/32/300","4k/10/32/300"]):
        
        rd_str = ''
        
        for k in rdlist:

            if len(k.split('/')) != 4:
                raise Exception("Wrong Rd str:%s" %k)

            rd = "rd%d" %rdlist.index(k)
            fwd = 'fwd*'
            forxfersize=k.split("/")[0]
            rdpct =k.split("/")[1]
            threads=k.split("/")[2]
            elapsed=k.split("/")[3]
            
            rd_str = rd_str + self.create_rd(rd, fwd, forxfersize,rdpct ,threads,elapsed)
        return rd_str
        
    def standcfg1(self,mntpath=["/mnt/sdd1"],rdlist=[],runtime=300):

        if not rdlist:
            rdlist = [str(2**x)+"k/"+ str(y) +"/32/"+str(runtime) for x in range(2,12) for y in [0,50,100]]

        return self.getFSDs(mntpath)+ self.create_fwd() + self.getRDs2(rdlist)
    def save_cfg(self,context='',filename = "test.cfg"):
        with open(filename,"w") as f:
            f.write(context)
if __name__ == "__main__":
    # sdid = raw_input("sdid:")
    # partcnt = input("part:")
    # filesystem = raw_input("fs:")
    # sysdiskcheck(sdid)
    # trim_disk(sdid)
    # for k in Linux_set_partition(sdid, partcnt):
    #     mkfsANDmount(k,filesystem)
    # t = VdbenchFileSystemConfig()
    # print t.getRDs()
    #print [str(2**x)+"k/100/"+str(y)+"/60" for x in range(2,12) for y in [1,32]]
    # t = VdbenchFileSystemConfig()
    # #print t.getFSDs(["/mnt/sdd1","/mnt/sdd2"]) + t.create_fwd() + t.getRDs2([str(2**x)+"k/100/32/60" for x in range(2,12)])
    
    # t.save_cfg(t.standcfg1())
    t = VdbenchFileSystemConfig()
    print t.getFSDs(["/mnt/sdd1","/mnt/sdd2"]) + t.create_fwd() + t.getRDs2([str(2**x)+"k/100/32/60" for x in range(2,12)]