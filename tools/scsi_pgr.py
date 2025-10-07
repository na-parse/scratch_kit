import os
import fcntl
import struct

# Constants for SCSI commands and IOCTL
SG_IO = 0x2285  # SG_IO ioctl code for SCSI generic devices
READ_RESERVATION_CMD = b'\x5E\x00\x00\x00\x00\x00\x00\x00\x18\x00'  # Persistent Reserve In
RESERVE_CMD = b'\x5F\x01\x00\x00\x00\x00\x00\x00\x18\x00'  # Persistent Reserve Out (Reserve)
RELEASE_CMD = b'\x5F\x02\x00\x00\x00\x00\x00\x00\x18\x00'  # Persistent Reserve Out (Release)
BUFFER_SIZE = 256

# SCSI IO structure
SG_IO_STRUCT = struct.Struct("=QIIIIIIII16s")

def scsi_command(device, cmd, direction="in", buffer_size=BUFFER_SIZE):
    """
    Sends a SCSI command to the specified device.
    :param device: Path to the SCSI device (e.g., /dev/sdX)
    :param cmd: SCSI Command Descriptor Block (CDB)
    :param direction: "in" for reading, "out" for writing
    :param buffer_size: Size of the data buffer
    :return: Data from the command execution
    """
    try:
        with open(device, "rb+") as dev:
            buffer = bytearray(buffer_size)
            sg_io_hdr = SG_IO_STRUCT.pack(
                id(buffer),  # Address of buffer
                len(buffer),  # Input/output data length
                0 if direction == "in" else len(buffer),  # DXFER_FROM_DEV or DXFER_TO_DEV
                0,  # Timeout (set as needed)
                0, 0, 0,  # Flags, Pack ID, and Reserved
                len(cmd),  # Command length
                cmd  # Command Descriptor Block (CDB)
            )
            # Perform IOCTL operation
            fcntl.ioctl(dev, SG_IO, sg_io_hdr)
            return bytes(buffer)
    except Exception as e:
        print(f"Error: {e}")
        return None

def view_reservation(device):
    print("Viewing Reservation:")
    data = scsi_command(device, READ_RESERVATION_CMD)
    if data:
        print(data.hex())

def set_reservation(device, key):
    print("Setting Reservation:")
    # Add the reservation key to the CDB (bytes 2-9 are the service action reservation key)
    cmd = RESERVE_CMD[:2] + key.to_bytes(8, 'big') + RESERVE_CMD[10:]
    scsi_command(device, cmd, direction="out")

def release_reservation(device, key):
    print("Releasing Reservation:")
    # Add the reservation key to the CDB (bytes 2-9 are the service action reservation key)
    cmd = RELEASE_CMD[:2] + key.to_bytes(8, 'big') + RELEASE_CMD[10:]
    scsi_command(device, cmd, direction="out")

# Example usage
device_path = "/dev/sdX"  # Replace with the actual device path
reservation_key = 0x123456789ABCDEF0  # Replace with the desired reservation key

view_reservation(device_path)
set_reservation(device_path, reservation_key)
release_reservation(device_path, reservation_key)
