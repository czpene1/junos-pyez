""""
#########################################################################################################

   Author:         Petr Nemec
   Description:    This script reads static route configuration defined under VRFs from two routers
                   and identifies missing routes
   Date:           2017-02-11

#########################################################################################################
"""

from jnpr.junos import Device
from jnpr.junos.exception import *
from pprint import pprint
from deepdiff import DeepDiff
from CfgStatRoute import CfgStaticRouteTable


def getstaticcfg(device):
    """
    :param device:  Directory describing device parameters i.e ip, hostname, credentials
    :return:       Instance of class CfgStaticRouteTable
    """
    router = Device(host=device["ip"], user=device["username"], password=device["password"])
    try:
        router.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return
    stat_routes = (CfgStaticRouteTable(router))
    stat_routes.get()
    router.close()
    return stat_routes


def table_to_dict(table):
    """
    :param table: Instance of class CfgStaticRouteTable
    :return:      directory  with structure { instance : { route : next-hop }}
    """
    stat_dir = {}
    for route in table:
        if route.instance not in stat_dir:
            stat_dir[route.instance] = {}
            stat_dir[route.instance][route.key] = route.nh
        else:
            stat_dir[route.instance][route.key] = route.nh
    return stat_dir



dev_a = {"name": "router-a", "ip": "1.1.1.1",
         "username": "joe", "password": "smith", }

dev_b = {"name": "router-b", "ip": "2.2.2.2",
         "username": "joe", "password": "smith", }



def main():
    # Create instances of CfgStaticRouteTable
    stat_routes_a = getstaticcfg(dev_a)
    stat_routes_b = getstaticcfg(dev_b)

    # Convert the instances of class CfgStaticRouteTable class into dictionaries
    first = table_to_dict(stat_routes_a)
    second = table_to_dict(stat_routes_b)


    # Test if the dictionaries are the same
    ddiff = (DeepDiff(second, first, ignore_order=True))
    if not ddiff:
        print "The static routes defined on both routers are identical"
        print "=============================\n"
    else:
        if ddiff.get('dictionary_item_added'):
            print "This routes are missing on router B:"
            pprint(ddiff['dictionary_item_added'])
            print "=============================\n"
        if ddiff.get('dictionary_item_removed'):
            print "This routes are missing on router A:"
            pprint(ddiff['dictionary_item_removed'])
            print "=============================\n"
        if ddiff.get('values_changed'):
            print "This routes have different next-hops:"
            pprint(ddiff['values_changed'])


if __name__ == "__main__":
        main()
