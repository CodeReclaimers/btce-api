from HTMLParser import HTMLParser
import warnings
from common import makeRequest

class BTCEScraper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.messageId = None
        self.messageTime = None
        self.messageUser = None
        self.messageText = None
        self.messages = []        
        
        self.inMessageA = False
        self.inMessageSpan = False

    def handle_data(self, data):
        if self.inMessageA:
            self.messageUser = data.strip()
        elif self.inMessageSpan:
            self.messageText = data.strip()
        
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            messageId = None
            for k, v in attrs:
                if k == 'id':
                    if v[:3] != 'msg':
                        # this is not a chat message <p> tag, so do nothing
                        return
                    messageId = v
                if k == 'class' and v != 'chatmessage':
                    # this is not a chat message <p> tag, so do nothing
                    return
            
            if messageId is not None:
                self.messageId = messageId
        elif tag == 'a' and self.messageId is not None:
            self.inMessageA = True
            messageTime = None
            for k, v in attrs:
                if k == 'title':
                    messageTime = v
                if k == 'class' and v != 'chatmessage':
                    # this is not a chat message <p> tag, so do nothing
                    return
            self.messageTime = messageTime
        elif tag == 'span' and self.messageId is not None:
            self.inMessageSpan = True

    def handle_endtag(self, tag):
        if tag == 'p' and self.messageId is not None:
            # exiting from the message <p> tag
            
            # check for invalid message contents
            if self.messageId is None:
                warnings.warn("Missing message ID")
            if self.messageUser is None:
                warnings.warn("Missing message user")
            if self.messageTime is None:
                warnings.warn("Missing message time")
            if self.messageText is None:
                self.messageText = ''
                
            self.messages.append((self.messageId, self.messageUser, self.messageTime, self.messageText))
            self.messageId = None
            self.messageUser = None
            self.messageTime = None
            self.messageText = None            
        elif tag == 'a' and self.messageId is not None:
            self.inMessageA = False
        elif tag == 'span' and self.messageId is not None:
            self.inMessageSpan = False


def getChatMessages():            
    parser = BTCEScraper()
    parser.feed(makeRequest('/'))
    parser.close()
    return parser.messages
