import btceapi

mainPage = btceapi.scrapeMainPage()
for message in mainPage.messages:
    msgId, user, time, text = message
    print "%s %s: %s" % (time, user, text)
