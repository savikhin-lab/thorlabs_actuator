from ctypes import cdll, c_short, POINTER, c_char, c_int, c_bool, CDLL, CFUNCTYPE


def bind(lib, fn_name, argtypes=None, restypes=None):
    """Create a Python wrapper around a C function."""
    _func = getattr(lib, fn_name)
    _func.argtypes = argtypes
    _func.restypes = restypes
    return _func


lib = cdll.LoadLibrary(
    "C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.KCube.DCServo.dll"
)

# Setup and teardown
TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
CC_Open = bind(lib, "CC_Open", [POINTER(c_char)], c_short)
CC_Close = bind(lib, "CC_Close", [POINTER(c_char)])
CC_ClearMessageQueue = bind(lib, "CC_ClearMessageQueue", [POINTER(c_char)])
CC_StartPolling = bind(lib, "CC_StartPolling", [POINTER(c_char), c_int], c_bool)
CC_StopPolling = bind(lib, "CC_StopPolling", [POINTER(c_char)])

# Homing
CC_CanHome = bind(lib, "CC_CanHome", [POINTER(c_char)], c_bool)
CC_NeedsHoming = bind(lib, "CC_NeedsHoming", [POINTER(c_char)], c_bool)
CC_CanMoveWithoutHomingFirst = bind(
    lib, "CC_CanMoveWithoutHomingFirst", [POINTER(c_char)], c_bool
)
CC_Home = bind(lib, "CC_Home", [POINTER(c_char)], c_short)

# Motion
CC_GetPosition = bind(lib, "CC_GetPosition", [POINTER(c_char)], c_int)
CC_MoveRelative = bind(lib, "CC_MoveRelative", [POINTER(c_char), c_int], c_short)
CC_SetMoveAbsolutePosition = bind(
    lib, "CC_SetMoveAbsolutePosition", [POINTER(c_char), c_int], c_short
)
CC_MoveAbsolute = bind(lib, "CC_MoveAbsolute", [POINTER(c_char)], c_short)
CC_StopImmediate = bind(lib, "CC_StopImmediate", [POINTER(c_char)], c_short)
CC_StopProfiled = bind(lib, "CC_StopProfiled", [POINTER(c_char)], c_short)
