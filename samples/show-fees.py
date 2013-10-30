#!/usr/bin/python
import btceapi

print "Trading fees:"
connection = btceapi.BTCEConnection()
for pair in btceapi.all_pairs:
    fee = btceapi.getTradeFee(pair, connection)
    print "    %s %.3f %%" % (pair, fee)
