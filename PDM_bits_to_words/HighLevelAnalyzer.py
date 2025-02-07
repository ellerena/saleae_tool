# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    # List of settings that a user can set for this High Level Analyzer.
    channel = NumberSetting(min_value=0, max_value=1)
    bitspersample = NumberSetting(min_value=1, max_value=64)

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'mytype': {
            'format': 'Output type: {{type}}, Input type: {{data.input_type}}'
        }
    }

    def __init__(self):
        '''
        Initialize HLA.

        Settings can be accessed using the same name used above.
        '''
        global val, bitcount, maxsamples, samples

        val = 0
        bitcount = 0
        samples = 0
        maxsamples = 200

        print("channel:", self.channel)

    def decode(self, frame: AnalyzerFrame):
        global val, bitcount, maxsamples, samples
        '''
        Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.

        The type and data values in `frame` will depend on the input analyzer.
        '''

        if samples >= maxsamples:
            return

        if frame.type == 'data':
            if bitcount == 0:
                val = 0
            val = (val << 1) + frame.data['data']
            bitcount = bitcount + 1
            if bitcount == self.bitspersample:
                print(hex(val)[2:])
                bitcount = 0
                samples = samples + 1

        # Return the data frame itself
        return AnalyzerFrame('mytype', frame.start_time, frame.end_time, {
            'input_type': frame.type
        })
