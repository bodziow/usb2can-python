#!/usr/bin/python
# Example of handling procedure for USB2CAN device
# www.sygmi.canbus.pl

import ctypes as ct
import usb2can_types
import time

def main():

	# Load the USB2CAN library
	usb2can = ct.CDLL("usb2can.dll")
	if usb2can.Usb2Can_InitLib(None) != usb2can_types.USB2CAN_OK:
		print "Library error !!!"
		return

	libVer = ct.create_string_buffer(usb2can_types.CANCTRL_MAX_STRING_LEN)
	firmwareVer = ct.create_string_buffer(usb2can_types.CANCTRL_MAX_STRING_LEN)
	prodName = ct.create_string_buffer(usb2can_types.CANCTRL_MAX_STRING_LEN)

	usb2can.Usb2Can_GetLibVer(libVer)
	print "Library version: " + libVer.value

	# Open a CAN device in Loopback mode
	status = usb2can.Usb2Can_Open(usb2can_types.CANCTRL_BAUDRATE_100,
							usb2can_types.CANCTRL_MODE_LOOPBACK,
							usb2can_types.CANCTRL_PRIORITY_NORMAL,
							usb2can_types.CANCTRL_FIFOSIZE)
	if status != usb2can_types.USB2CAN_OK:
		print "Device error status: {} !!!".format(status)
		usb2can.Usb2Can_ReleaseLib();
		return

	print "Device opened in Loopback mode!"

	usb2can.Usb2Can_GetProduct(prodName)
	print "Product name: " + prodName.value
	usb2can.Usb2Can_GetFirmwareVer(firmwareVer)
	print "Firmware version: " + firmwareVer.value

	time.sleep(0.5)
	# Prepare a CAN message
	MSG_ID = 0x123;
	DLC = 8
	msg_tx = usb2can_types.CanCtrlMsg(MSG_ID, DLC)
	for i in range(0, DLC):
		msg_tx.data[i] = i

	# Send the CAN message
	status = usb2can.Usb2Can_Push(msg_tx)
	if status != usb2can_types.USB2CAN_OK:
		print "Usb2Can_Push failed with status: {} !!!".format(status)
		usb2can.Usb2Can_Close();
		usb2can.Usb2Can_ReleaseLib();
		return
	print "Sent -> CAN msg with ID = " + hex(msg_tx.id)
	time.sleep(0.2)

	# Read the CAN message
	msg_rx = usb2can_types.CanCtrlMsg()
	status = usb2can.Usb2Can_Pull(ct.byref(msg_rx))
	if status != usb2can_types.USB2CAN_OK:
		print "Usb2Can_Pull failed with status: {} !!!".format(status)
	print "Received <- CAN msg with ID = " + hex(msg_rx.id)

	# Compare TX and RX massages (should be the same)
	msg_rx.timeStamp = 0 # for comparasion purpose
	if msg_tx == msg_rx:
		print "Success. CAN RX and TX messages are the same."
	else:
		print "Failure. CAN RX and TX messages are different !!!"

	# Close CAN device and realease resources
	usb2can.Usb2Can_Close();
	usb2can.Usb2Can_ReleaseLib();

if __name__ == '__main__':
    main()