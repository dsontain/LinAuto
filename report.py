import re
import sys


class VdbenchResult(object):

    def __init__(self, report=r"C:\Users\zc\Desktop\output\sd1.html"):
        
        with open (report, "r") as f:
            self.report = f.read()

    def __call__(self):

        zeros = self.check_zero()
        valid_lines = self.simplify()

        if zeros:
            print("Total valid lines :    {}".format(len(valid_lines)))
            print("IO slow down to 0 :    {}".format(len(zeros)))
            print("Total / IO to 0   :    {} %".format(((len(zeros)) / len(valid_lines)) * 100))
            for k, j in self.continuous_to_0().items():
                print("{}:     {}".format(k, j))
            return False
        else:
            print("No IO to 0 \nTotal valid lines :    {}".format(len(valid_lines)))
            return True

    def simplify(self):
        pattern = r"\d{2}:\d{2}:\d{2}.\d{3} +\d+ +\d+.\d+ +\d+.\d+ +\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+"
        return re.compile(pattern, flags=0).findall(self.report)

    def check_zero(self):
        pattern = r"\d{2}:\d{2}:\d{2}.\d{3} +\d+ +0+.0+ +0+.0+ +\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+ +\d+.\d+"
        return re.compile(pattern, flags=0).findall(self.report)

    def continuous_to_0(self):
        zero_distribution = {
            "Last 1 s": 0,
            "Last 2 s": 0,
            "Last 3 s": 0,
            "Last 4 s": 0,
            "Last 5 s": 0,
            "Last 6 s": 0,
            "Last 7 s": 0,
            "Last 8 s": 0,
            "Last 9 s": 0,
            "Last 10 s": 0,
            "Last more than 10 s" : 0
        }

        zero_lines = self.check_zero()
        out_list = []
        tmp_list = [zero_lines[0]]

        for k in zero_lines[1:]:
            if int(k.split()[1]) - int(zero_lines[zero_lines.index(k) - 1].split()[1]) == 1 :
                tmp_list.append(k)
            else:
                out_list.append(tmp_list)
                tmp_list = []
        

        for n in out_list:
            if len(n) == 1: 
                zero_distribution["Last 1 s"] = zero_distribution["Last 1 s"] + 1
            elif len(n) == 2: 
                zero_distribution["Last 2 s"] = zero_distribution["Last 2 s"] + 1
            elif len(n) == 3: 
                zero_distribution["Last 3 s"] = zero_distribution["Last 3 s"] + 1
            elif len(n) == 4: 
                zero_distribution["Last 4 s"] = zero_distribution["Last 4 s"] + 1
            elif len(n) == 5: 
                zero_distribution["Last 5 s"] = zero_distribution["Last 5 s"] + 1
            elif len(n) == 6: 
                zero_distribution["Last 6 s"] = zero_distribution["Last 6 s"] + 1
            elif len(n) == 7: 
                zero_distribution["Last 7 s"] = zero_distribution["Last 7 s"] + 1
            elif len(n) == 8: 
                zero_distribution["Last 8 s"] = zero_distribution["Last 8 s"] + 1
            elif len(n) == 9: 
                zero_distribution["Last 9 s"] = zero_distribution["Last 9 s"] + 1
            elif len(n) == 10: 
                zero_distribution["Last 10 s"] = zero_distribution["Last 10 s"] + 1
            elif len(n) > 10:
                  zero_distribution["Last more than 10 s"] = zero_distribution["Last more than 10 s"] + 1              

        return zero_distribution

    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        VdbenchResult(sys.argv[1])()
        
    else:
         VdbenchResult()()
