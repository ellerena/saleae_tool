# High Level Analyzer
# 
# Eddie Llerena
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting
import csv

# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    channl = NumberSetting(min_value=0, max_value=1)

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'mytype': {
            'format': 'Output type: {{type}}, Input type: {{data.input_type}}'
        }
    }

    def __init__(self):
        global i, num_shift, row, f
        i = 0
        row = ''
        num_shift = 14
        f = open("/Users/ellerena/Downloads/hlai2s.csv", 'w')
        print("cha:", self.channl)

    def decode(self, frame: AnalyzerFrame):
        global i, num_shift, row, f
        if frame.type == 'data':
            if frame.data['channel'] == self.channl:
                val = frame.data['data'] >> num_shift
                f.write(hex(val)[2:] + '\n')
                if (0 == i):
                    row = row + hex(val)
                    i = 15
                else:
                    row = row + ', ' + hex(val)
                    i = i - 1
                    if (0 == i):
                       	print (row)
                       	row = ''

        return
        
    def __del__(self):
        print ("done")
