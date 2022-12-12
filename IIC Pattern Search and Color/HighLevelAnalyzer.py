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

    result_types = {'newdev': {'format': '{{data.dev}}'}}

    # Initialize HLA
    def __init__(self):
        global show, search_dev_i, show_dev
        show = 0
        show_dev = self.show_hide
        search_dev_i = int(self.search_dev)
        print("Slave:", hex(search_dev_i), " show/hide:", self.show_hide)

    # Process each input frame, optionally return a single or list of `AnalyzerFrame`
    def decode(self, frame: AnalyzerFrame):

        # globals to persist across frames
        global dev, show, search_dev_i, show_dev

        if frame.type == 'address':
            devi = int.from_bytes(frame.data['address'], "big")

            if search_dev_i == devi:
                show = 1 if 'Show' == show_dev else 0
            else:
                show = 0 if 'Show' == show_dev else 1

            if show == 1:
                dev = frame.data['address'].hex()
                wr = "r" if frame.data['read'] else "w"
                # print("\n" + dev + " " + wr, end = " ")
                print("\n" + wr, end = " ")
            else: # show == 0
                return

        elif frame.type == 'data' and show ==1:
            print("{:02x}".format(int.from_bytes(frame.data['data'], "big")), end = " ")
            dev = ''

        # elif frame.type == 'stop':

        else: # handle start/stop
            return

        return AnalyzerFrame('newdev', frame.start_time, frame.end_time, {
            'dev': dev
        })
