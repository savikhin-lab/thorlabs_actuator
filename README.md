# Thorlabs actuator

This package is a command line interface for controlling a Thorlabs Z812B actuator.

## Setup
Make sure you have the [Kinesis software](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control) installed.

**Next add the Kinesis folder to the `PATH` environment variable. This is critical. Without this step, the software will not be able to locate the DLLs used to communicate with the actuator.**

## Calibration
The motor is calibrated by storing `<wavelength>, <motor position>` pairs in a calibration file, and creating an environment variable that points to this file. You can use the Kinesis software to move the motor and record its position.

First create a calibration file somewhere, the location is not important. The file should have the following format:
```
<wavelength>,<motor position>
<wavelength>,<motor position>
<wavelength>,<motor position>
...
```

The last step is to create an environment variable `THORLABSMOTORCAL` and set it to the location of the calibration file.

## Installation
Clone the repository:
```
$ git clone https://github.com/savikhin-lab/thorlabs_actuator.git
```

Enter the `thorlabs_actuator` directory, then use `poetry` to build the package.
```
$ cd thorlabs_actuator
$ poetry build
```

Finally, use `pip` to install the package. The package will be called `etalon` since it is used to control the position of an etalon in our system.
```
$ python -m pip install --user dist/etalon-<version>-py3-none-any.whl
```

## Usage
Run `etalon --help` to see the available commands. You can see further help for individual commands via `etalon <cmd> --help`.
