#!/usr/bin/python

import ctypes as ct

# Maximal length of the string
CANCTRL_MAX_STRING_LEN = 25

CANCTRL_FIFOSIZE       = 65535

# Library thread priorities
CANCTRL_PRIORITY_LOW = 0
CANCTRL_PRIORITY_NORMAL = 1
CANCTRL_PRIORITY_HIGH = 2
CANCTRL_PRIORITY_RT = 3

# Controller modes
CANCTRL_MODE_LOOPBACK = 4
CANCTRL_MODE_LISTENONLY = 2
CANCTRL_MODE_NORMAL = 0

# Controller baudrates
CANCTRL_BAUDRATE_1000 = 1000
CANCTRL_BAUDRATE_500 = 500
CANCTRL_BAUDRATE_250 = 250
CANCTRL_BAUDRATE_125 = 125
CANCTRL_BAUDRATE_100 = 100
CANCTRL_BAUDRATE_83_3 = 83
CANCTRL_BAUDRATE_62_5 = 62
CANCTRL_BAUDRATE_50 = 50
CANCTRL_BAUDRATE_33_3 = 33
CANCTRL_BAUDRATE_20 = 20

# Can message frame info flags
CANCTRL_FRAME_NORET = 0x80
CANCTRL_FRAME_EXT = 0x20
CANCTRL_FRAME_STD = 0x00
CANCTRL_FRAME_RTR = 0x10
CANCTRL_FRAME_DLC = 0xF

# Library exceptions and return codes
USB2CAN_OK = 0
USB2CAN_USB_ERR = 1        # internal usb bus error  eg. ftdi device transfer timeout
USB2CAN_APP_ERR = 2        # internal application error eg. mutexes =  lists or thread error
USB2CAN_TX_FIFO_FULL = 3   # tx fifo full
USB2CAN_RX_FIFO_FULL = 4   # rx fifo full
USB2CAN_RX_FIFO_EMPTY = 5  # rx fifo empty
USB2CAN_FILTER_ERR = 6     # software filter error
USB2CAN_RESOURCE_ERR = 7   # insufficient resources  eg. malloc error
USB2CAN_PARAM_ERR = 8      # wrong parameter
USB2CAN_DEVICE_ERR = 9     # device error  eg. device not found
USB2CAN_HANDLE_ERR = 10    # internal library handle error eg. device not open =  ftd2xx.dll missing ?

# CAN message structure
class CanCtrlMsg(ct.Structure):
	_fields_ = [("id", ct.c_uint),
				("frameInfo", ct.c_ubyte),
				("data", ct.c_ubyte * 8),
				("timeStamp", ct.c_uint)]

	def __eq__(self, other):
		for field in self._fields_:
			attr_name = field[0]
			a, b = getattr(self, attr_name), getattr(other, attr_name)
			is_array = isinstance(a, ct.Array)
			if is_array and a[:] != b[:] or not is_array and a != b:
				print "is_array: " + str(is_array)
				print "a: " + str(a) + " b: " + str(b)
				return False
		return True

	def __ne__(self, other):
		for field in self._fields_:
			attr_name = field[0]
			a, b = getattr(self, attr_name), getattr(other, attr_name)
			is_array = isinstance(a, ct.Array)
			if is_array and a[:] != b[:] or not is_array and a != b:
				return True
		return False
