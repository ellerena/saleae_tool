# import math
# import numpy

from saleae.range_measurements import DigitalMeasurer

HWVAD_TRIGG = 'hwvadTrigg'
PREROLL_EMPTY = 'prerollEmpty'
WW_DETECTED = 'wwDetect'


class MyDigitalMeasurer(DigitalMeasurer):
    supported_measurements = [HWVAD_TRIGG, PREROLL_EMPTY, WW_DETECTED]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        self.hwvad_trigg = None
        self.preroll_empty = None
        self.ww_detected = None
        self.state = 0

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get transitions in the form of pairs of `Time`, Bitstate (`True` for high, `False` for low)
    # `Time` currently only allows taking a difference with another `Time`, to produce a `float` number of seconds
    def process_data(self, data):
        for t, bitstate in data:
            if self.hwvad_trigg == None:
                self.hwvad_trigg = t
            elif self.preroll_empty == None:
                self.preroll_empty = t - self.hwvad_trigg
            elif self.ww_detected == None:
                self.ww_detected = t - self.hwvad_trigg
        # pass

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}

        if HWVAD_TRIGG in self.requested_measurements:
            values[HWVAD_TRIGG] = 0

        if PREROLL_EMPTY in self.requested_measurements:
            values[PREROLL_EMPTY] = self.preroll_empty

        if WW_DETECTED in self.requested_measurements:
            values[WW_DETECTED] = self.ww_detected

        return values
