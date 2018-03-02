try:
    import logging
except ImportError:
    print('Check if running virtual env')


class HeartData:
    """ Created HeartData class

    __init__ sets the attributes

    Main Attributes:
        mean_hr_bpm: estimated heart rate
        voltage_extremes: min/max lead voltages
        duration: total time
        num_beats: number of detected beats
        beats: times when a beat occurred
    """

    def __init__(self, files='test_data/test_data1.csv',
                 filetype='csv', time_unit='s'):
        logging.info('Initializing')
        self.files = files
        self.time_unit = time_unit
        self.data = None
        self.time = None
        self.voltage = None
        self.filetype = filetype

        self.beats = None
        self.mean_hr_bpm = None
        self.num_beats = None

        self.read_file()
        self.split_data(time_unit)
        self.duration = self.calc_duration()
        self.calc_mean_hr_bpm()
        self.voltage_extremes = self.calc_voltage_extremes()
        self.write_json()

    def read_file(self):  # Tried to make modular, but subscriptable error
        """ Reads data file

        :return: self.data
        """
        try:
            import pandas as pd
        except ImportError:
            logging.error('Check for pandas pkg')
        logging.info('Begin reading file')
        if self.filetype == 'csv':  # more elegant way of checking ext?
            self.data = pd.read_csv(self.files, delimiter=',', header=None)
        elif self.filetype == 'json':
            self.data = pd.read_json(self.files)

    def split_data(self, time_unit):
        # from loaddata import LoadData
        logging.info('Splitting data into time and voltage')
        try:
            df = self.data  # default is .csv
            df.columns = ['Time', 'Voltage']  # make interactive
            if time_unit == 'min':
                df['Time'] = df['Time'] / 60  # Will this break? Best practice?
                logging.info('Change units from min to s')
            elif time_unit == 'hr':
                df['Time'] = df['Time'] / 3600
                logging.info('Change units from min to s')
            self.time = df['Time'].tolist()
            self.voltage = df['Voltage'].tolist()
        except TypeError:
            logging.error('Check inputs')

    def calc_duration(self):
        duration = self.time[-1] - self.time[0]
        return duration

    def calc_mean_hr_bpm(self):
        import numpy as np
        import peakutils
        # from scipy import signal
        # import matplotlib.pyplot as plt
        avg_volt = np.mean(self.voltage)
        norm = self.voltage - avg_volt
        doub_autocorr = np.correlate(norm, norm, 'full')
        autocorr = doub_autocorr[len(doub_autocorr) // 2:]
        # peak = signal.find_peaks_cwt(autocorr, np.arange(0.1,1))
        # plt.plot(self.time, autocorr)
        # plt.show()
        # over-estimates peaks with find_peaks_cwt. Reference website:
        # https://blog.ytotech.com/2015/11/01/findpeaks-in-python/
        self.beats = peakutils.indexes(autocorr, thres=0.1, min_dist=100)
        self.num_beats = len(self.beats)
        dur_min = self.duration / 60  # b/c set-up for time to be in seconds
        self.mean_hr_bpm = self.num_beats / dur_min

    def calc_voltage_extremes(self):
        voltage_extremes = (min(self.voltage), max(self.voltage))
        return voltage_extremes

    def write_json(self):
        import pandas as pd
        my_dict = {'mean_hr_bpm': [self.mean_hr_bpm],
                   'voltage_extremes': [self.voltage_extremes],
                   'duration': [self.duration],
                   'num_beats': [self.num_beats],
                   'beats': [self.beats]}
        df = pd.DataFrame(data=my_dict)
        df.to_json(self.files + '.json', orient='records')
        print('{} converted'.format(self.files))
