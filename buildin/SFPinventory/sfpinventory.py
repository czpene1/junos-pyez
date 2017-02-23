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
import getpass


def getxcvr_int(device):
    """
    :param device:  Directory describing device parameters i.e ip, hostname, credentials
    :return:       Instance of class XcvrTable and instance of class EthPortTable
    """
    router = Device(host=device["ip"], user=device["username"], password=device["password"], port=22)
    try:
        router.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return
    transceivers = (XcvrTable(router))
    transceivers.get()
    ports = (EthPortTable(router))
    ports.get()
    router.close()
    return [transceivers, ports]


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


def getdown(ethports):
    """
    :param device:  Instance of class EthPortTable
    :return:        List of interfaces which are down
    """
    l = []
    for port in ethports:
        if port.name.startswith("ge-") or port.name.startswith("xe-"):
            if port.admin == "down":
                l.append(str(port.name)[3:])
            elif port.oper == "down":
                l.append(str(port.name)[3:])
    return l



def main():
    # Login dialog
    ip = raw_input("IP: ")
    username = raw_input("Username[admin]: ") or "admin"
    password = getpass.getpass(prompt='Password: ', stream=None)


    dev_a = {"ip": ip, "username": username, "password": password}

    # Create the instances of XcvrTable and of EthPortTable
    sfp, interfaces = getxcvr_int(dev_a)

    # Print all transceivers
    print("\n=========== All transceivers ==============================")
    pprint(sfp.items())

    # Create and print the list of transceiver indexes
    transceivers = getsfpid(sfp.keys())
    print("\n=========== Slots where SFPs are found ====================")
    print(transceivers)


    # Get the list of interfaces which are down
    down = getdown(interfaces)

    stock = list(set(transceivers).intersection(down))

    print("\n=========== These SFPs are not in use  ====================")
    print("FPC  , PIC  , Xcvr   : SN     , Type")

    for i in range(len(stock)):
        # split into three parts by sign "/"
        m = 'FPC ' + (stock[i]).split('/')[0]
        n = 'PIC ' + (stock[i]).split('/')[1]
        o = 'Xcvr ' + (stock[i]).split('/')[2]
        # create XcvrTable key to list additional sfp parameters
        k = (m, n, o)
        print(m + ", " + n + ", " + o + ": " + sfp[k].sn + ", " + sfp[k].type)

if __name__ == "__main__":
        main()
