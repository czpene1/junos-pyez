""""
#########################################################################################################

   Author:         Petr Nemec
   Description:    This script searches for unused transceivers which may be taken to stock
   Date:           2017-02-20

#########################################################################################################
"""

from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable
from jnpr.junos.op.xcvr import XcvrTable
from pprint import pprint


def getxcvr(device):
    """
    :param device:  Directory describing device parameters i.e ip, hostname, credentials
    :return:       Instance of class XcvrTable
    """
    router = Device(host=device["ip"], user=device["username"], password=device["password"])
    try:
        router.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return
    transceivers = (XcvrTable(router))
    transceivers.get()
    router.close()
    return transceivers


def getsfpid(listofkeys):
    """
    :param list:   keys of the table XcvrTable
    :return:       list of interface IDs
    """
    l = []
    for i in range(len(listofkeys)):
        id = ""
        for j in range(3):
            aux = ""
            # remove leading "FPC"
            if str(listofkeys[i][j]).startswith("FPC "):
                aux = listofkeys[i][j][4:] + "/"
            # remove leading "PIC"
            if str(listofkeys[i][j]).startswith("PIC "):
                aux = listofkeys[i][j][4:] + "/"
            # remove leading "Xcvr"
            if str(listofkeys[i][j]).startswith("Xcvr "):
                aux = listofkeys[i][j][5:]
                # sfp_list[i] = sfp_list[i] + "/" + str(listofkeys[i][j])[2:]
            id = id + aux
        l.append(id)
    return l


def getintf(device):
    """
    :param device:  Directory describing device parameters i.e ip, hostname, credentials
    :return:        Instance of class EthPortTable
    """
    router = Device(host=device["ip"], user=device["username"], password=device["password"])
    try:
        router.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return
    ports = (EthPortTable(router))
    ports.get()
    router.close()
    return ports


def getdown(ethports):
    """
    :param device:  Instance of class EthPortTable
    :return:        List of interfaces which are down
    """
    l = []
    for port in ethports:
        if (port.name.startswith("ge-") or port.name.startswith("xe-")):
            if port.admin == "down":
                l.append(str(port.name)[3:])
            elif port.oper == "down":
                l.append(str(port.name)[3:])
    return l


# Device credentials
dev_a = {"name": "router-a", "ip": "1.1.1.1",
         "username": "joe", "password": "smith", }


def main():
    # Create instances of XcvrTable
    sfp = getxcvr(dev_a)

    # Print all transceivers
    pprint(sfp.items())

    # Create and print the list of transceiver indexes
    transceivers = getsfpid(sfp.keys())
    print("\n=========== SFPs identified in these slots ====================")
    print(transceivers)

    # Create an instance of EthPortTable
    interfaces = getintf(dev_a)

    # Print all interfaces
    # pprint(interfaces.items())

    # Get the list of interfaces which are down
    down = getdown(interfaces)

    stock = list(set(transceivers).intersection(down))

    print("\n=========== These SFPs are not in use  ====================")
    print(stock)

    for i in range(len(stock)):
        # split into three parts by sign "/"
        m = "FPC " + (stock[i]).split('/')[0]
        n = "PIC " + (stock[i]).split('/')[1]
        o = "Xcvr " + (stock[i]).split('/')[2]
        # create XcvrTable key to list additional sfp parameters
        k = (m + ', ' + n + ', ' + o)
        print sfp[k].ver
        print sfp[k].pn
        print sfp[k].sn
        print sfp[k].type


if __name__ == "__main__":
        main()
