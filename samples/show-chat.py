#!/usr/bin/python
import btceapi

mainPage = btceapi.scrapeMainPage()
for message in mainPage.messages:
    msgId, user, time, text = message
    print "%s %s: %s" % (time, user, text)

print
print "24change reserves: %d USD" % mainPage.reserves24change
print "ALFAcashier reserves: %d USD" % mainPage.reservesALFAcashier
print "%d users online" % mainPage.usersOnline
print "%d bots online" % mainPage.botsOnline
print "dev online: %s" % ('yes' if mainPage.devOnline else 'no')
print "support online: %s" % ('yes' if mainPage.supportOnline else 'no')
print "admin online: %s" % ('yes' if mainPage.adminOnline else 'no')