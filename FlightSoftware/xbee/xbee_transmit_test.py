import sys

# TODO: replace with the node identifier of your target device.
TARGET_NODE_ID = "RECEIVER"
MESSAGE = "Hello XBee!"

def find_device(node_id):
    import xbee
    """
    Finds the XBee device with the given node identifier in the network and
    returns it.

    :param node_id: Node identifier of the XBee device to find.

    :return: The XBee device with the given node identifier or ``None`` if it
        could not be found.
    """
    for dev in xbee.discover():
        if dev['node_id'] == node_id:
            return dev
    return None


print(" +--------------------------------------------+")
print(" | XBee MicroPython Transmit Data (NI) Sample |")
print(" +--------------------------------------------+\n")

import xbee
# Find the device with the configure node identifier.
device = find_device(TARGET_NODE_ID)
if not device:
    print("Could not find the device with node identifier '%s'" % TARGET_NODE_ID)
    sys.exit(-1)

addr16 = device['sender_nwk']
addr64 = device['sender_eui64']

print("Sending data to %s >> %s" % (TARGET_NODE_ID, MESSAGE))

try:
    # Some protocols do not have 16-bit address. In those cases, use the 64-bit one.
    xbee.transmit(addr16 if addr16 else addr64, MESSAGE)
    print("Data sent successfully")
except Exception as e:
    print("Transmit failure: %s" % str(e))