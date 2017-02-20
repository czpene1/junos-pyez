""""
#########################################################################################

   Author:         Petr Nemec
   Description:    This script reads prefix list configuration from two routers
                   and identifies missing routes
   Date:           2017-02-20

#########################################################################################
"""

from jnpr.junos import Device
from jnpr.junos.exception import *
from pprint import pprint
from deepdiff import DeepDiff
from CfgPrefList import CfgPlTable


def getpreflistcfg(device):
    """
    :param device:  Directory describing device parameters i.e ip, hostname, credentials
    :return:       Instance of class CfgPlTable
    """
    router = Device(host=device["ip"], user=device["username"], password=device["password"])
    try:
        router.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return
    pf_list = (CfgPlTable(router))
    pf_list.get()
    router.close()
    return pf_list


def pl_table_to_dict(table):
    """
    :param table: Instance of class CfgPlTable
    :return:      directory  with structure { pref-list : [ 'prefix1', 'prefix2'...]}
    """
    plist_dir = {}
    for plist in table:
        plist_dir[plist.key] = plist.plitem
    return plist_dir


dev_a = {"name": "router-a", "ip": "1.1.1.1",
         "username": "joe", "password": "smith", }

dev_b = {"name": "router-b", "ip": "2.2.2.2",
         "username": "joe", "password": "smith", }



def main():
    # Create instances of CfgPlTable
    pref_list_a = getpreflistcfg(dev_a)
    pref_list_b = getpreflistcfg(dev_b)

    # Convert the instances of class CfgPlTable class into dictionaries
    first = pl_table_to_dict(pref_list_a)
    second = pl_table_to_dict(pref_list_b)


    # Test if the dictionaries and the items are the same
    ddiff = (DeepDiff(second, first, ignore_order=True))
    if not ddiff:
        print "The static routes defined on both routers are identical"
        print "=============================\n"
    else:
        if ddiff.get('dictionary_item_added'):
            print "This prefix-lists are missing on router B:"
            pprint(ddiff['dictionary_item_added'])
            print "=============================\n"
        if ddiff.get('dictionary_item_removed'):
            print "This prefix-lists are missing on router A:"
            pprint(ddiff['dictionary_item_removed'])
            print "=============================\n"
        if ddiff.get('iterable_item_added'):
            print "This prefixes are missing on router B:"
            pprint(ddiff['iterable_item_added'])
            print "=============================\n"
        if ddiff.get('iterable_item_removed'):
            print "This prefixes are missing on Router A:"
            pprint(ddiff['iterable_item_removed'])
            print "=============================\n"


if __name__ == "__main__":
        main()
