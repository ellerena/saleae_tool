# High Level Analyzer - IIC Pattern Search and Color
# Description: given a slave address (search_dev), scans through the i2c
#               sequence, when a write/read to that slave is detected
#               the pattern is presented (or hidden depending on show_hide).
#               Used with data from i2c shared by multiple slave devices,
#               this generates a pattern that shpws when communication
#               with a specific slave address is occuring.
# Eddie Llerena
# https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

class Hla(HighLevelAnalyzer):
    #rejest = StringSetting()
    show_hide = ChoicesSetting(choices=('Show', 'Hide'))
    search_dev = NumberSetting(min_value=0, max_value=255)
    word_width = NumberSetting(min_value=1, max_value=4)

    result_types = {'newdev': {'format': '{{data.dev}}'}}

    # Initialize HLA
    def __init__(self):
        self.show = 0
        self.show_dev = self.show_hide
        self.search_dev_i = int(self.search_dev)
        self.byteCount = 0
        self.word_value = 0
        print("Slave:", hex(self.search_dev_i), " show/hide:", self.show_hide)

    # Process each input frame, optionally return a single or list of `AnalyzerFrame`
    def decode(self, frame: AnalyzerFrame):

        if frame.type == 'address':
            self.byteCount = int(self.word_width)
            dev_i2c_address = int.from_bytes(frame.data['address'], "big")

            if self.search_dev_i == dev_i2c_address:
                self.show = 1 if 'Show' == self.show_dev else 0
            else:
                self.show = 0 if 'Show' == self.show_dev else 1

            if self.show == 1:
                self.dev = frame.data['address'].hex()
                wr = "r" if frame.data['read'] else "w"
                print("\n" + wr, end = " ")
            else: # self.show == 0
                return

        elif frame.type == 'data' and self.show ==1:
            c = int.from_bytes(frame.data['data'], "big")

            if self.byteCount > 0:
                self.word_value = (self.word_value << 8) + c
                self.byteCount -=1

            if self.byteCount == 0:
                print('{:0{w}x}'.format(self.word_value, w = 2*int(self.word_width)), end = " ")
                self.dev = ''
                self.byteCount = int(self.word_width)
                self.word_value = 0

        # elif frame.type == 'stop':

        else: # handle start/stop
            return

        return AnalyzerFrame('newdev', frame.start_time, frame.end_time, {
            'dev': self.dev
        })
