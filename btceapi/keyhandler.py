

class KeyHandler:
    '''KeyHandler handles the tedious task of managing nonces associated
    with a BTC-e API key/secret pair.'''
    def __init__(self, filename = None):
        '''The given file is assumed to be a text file with three lines
        (key, secret, nonce) per entry.'''
        self.keys = {}
        if filename is not None:
            f = open(filename, "rt")
            while True:
                key = f.readline().strip()
                if not key:
                    break
                secret = f.readline().strip()
                nonce = int(f.readline().strip())
                self.keys[key] = (secret, nonce)
            
    def save(self, filename):
        f = open(filename, "wt")
        for k, (secret, nonce) in self.keys.items():
            f.write("%s\n%s\n%d\n" % (k, secret, nonce))
        
    def addKey(self, key, secret, next_nonce):
        self.keys[key] = (secret, next_nonce)

    def setNextNonce(self, key, next_nonce):
        data = self.keys.get(key)
        if data is None:
            raise Exception("Key not found: %r" % key)
        self.keys[key] = (data[0], next_nonce)
