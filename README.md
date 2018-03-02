# bme590hrm
Heart Rate Monitor

[![Build Status](https://travis-ci.org/ttw6/bme590hrm.svg?branch=master)](https://travis-ci.org/ttw6/bme590hrm)

## Overview

The class HeartData was created to have the following attributes:
* mean_hr_bpm
* voltage_extremes
* duration
* num_beats
* beats

In the main code, the user will need to change the path and file name manually, which will then call on the HeartData class. Path refers to the subfolder that contains all the ECG data. In addition, decorators were not successfully set up, so user will need to run HeartData.run_fn(time_unit = 's') if he or she skips initialiation. 
Apologies for the inconvenience, but v2.0.0 will focus on improving automation and stress-testing the code.
