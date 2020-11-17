import os
import sys
import time
import click
import numpy as np
from ctypes import c_short, c_int, c_char_p
from pathlib import Path
from scipy.interpolate import interp1d
from . import actuator_low_level as actuator


class Actuator:
    def __init__(self, serial_num=27004957, poll_millis=10):
        """A high-level wrapper around a Thorlabs KDC101 and Z812B.
        """
        self._serial = c_char_p(bytes(str(serial_num), "utf-8"))
        cal_file_path = os.environ["THORLABSMOTORCAL"]
        if cal_file_path is None:
            print("THORLABSMOTORCAL environment variable not found.")
            sys.exit(-1)
        cal_file_path = Path(cal_file_path)
        self.cal_data = np.loadtxt(cal_file_path, delimiter=",")
        self._wl_interp = interp1d(self.cal_data[:, 0], self.cal_data[:, 1], kind="linear")
        res = actuator.TLI_BuildDeviceList()
        if res != 0:
            sys.exit(f"Actuator failed to build device list. Error: {res}")
        res = actuator.CC_Open(self._serial)
        if res != 0:
            sys.exit(f"Failed to connect to actuator. Error: {res}")
        millis = c_int(poll_millis)
        actuator.CC_StartPolling(self._serial, millis)
        time.sleep(0.1)

    def close(self):
        """Close the connection to the actuator.
        """
        actuator.CC_StopPolling(self._serial)
        actuator.CC_Close(self._serial)

    def pos(self):
        """Get the current position in device units.
        """
        actuator.CC_ClearMessageQueue(self._serial)
        return int(actuator.CC_GetPosition(self._serial))

    def home(self):
        """Send the actuator to the home position if necessary

        Homing the device is not just the process of sending the device to the home
        position, it also establishes the reference position of the motor. If the motor
        doesn't need to re-establish that reference position then it won't move.

        If the device was recently powered off, then it will start up thinking that it's at
        position 0, which is not correct. It will also tell you that the device can move
        without homing, but all of the position will be relative to this power-on position
        rather than the actual 0 position.
        """
        actuator.CC_ClearMessageQueue(self._serial)
        if not actuator.CC_CanHome(self._serial):
            sys.exit("Can't home actuator")
        actuator.CC_Home(self._serial)
        # The motor needs time to move and poll its location, otherwise it will just
        # return its old (stale) position.
        time.sleep(1)
        pos = -1
        while pos != 0:
            pos = actuator.CC_GetPosition(self._serial)
            time.sleep(0.01)
        # Sometimes the motor just hangs in the "homing" state even though it's
        # reached the home position, so you have to manually stop it. If you don't
        # issue this stop command then it may hang and become unresponsive.
        actuator.CC_StopProfiled(self._serial)

    def move(self, pos):
        """Move to a position given in device units.
        """
        actuator.CC_ClearMessageQueue(self._serial)
        res = actuator.CC_SetMoveAbsolutePosition(self._serial, pos)
        if res != 0:
            sys.exit(f"Failed to set move position. Error: {res}")
        actuator.CC_MoveAbsolute(self._serial)
        while actuator.CC_GetPosition(self._serial) != pos:
            time.sleep(0.01)

    def move_wl(self, wl):
        """Move to a specific wavelength.
        """
        actuator.CC_ClearMessageQueue(self._serial)
        pos = int(np.floor(self._wl_interp(wl)))
        click.echo(pos)
        res = actuator.CC_SetMoveAbsolutePosition(self._serial, pos)
        if res != 0:
            sys.exit(f"Failed to set move position. Error: {res}")
        actuator.CC_MoveAbsolute(self._serial)
        curr_pos = actuator.CC_GetPosition(self._serial)
        while curr_pos != pos:
            time.sleep(0.05)
            curr_pos = actuator.CC_GetPosition(self._serial)
