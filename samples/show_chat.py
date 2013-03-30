import btceapi

for message in btceapi.getChatMessages():
    msgId, user, time, text = message
    print "%s %s: %s" % (time, user, text)
