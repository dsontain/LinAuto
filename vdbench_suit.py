
class LogicDisk(object):
    def __init__(self):
        pass
    def storage_definition(self, sd=1, lun="", thread=32,**argv):
        sd = "sd=sd{} ".format(sd)
        lun = "lun={} ".format(lun)
        thread = "thread={}".format(thread)