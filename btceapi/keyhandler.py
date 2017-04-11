# Copyright (c) 2013-2017 CodeReclaimers, LLC


class InvalidNonceException(Exception):
    """Raised when an invalid nonce is set on a key."""
    pass


class KeyData(object):
    def __init__(self, secret, nonce):
        self.secret = secret
        self.nonce = nonce

    # BTC-e's API caps nonces' values
    MAX_NONCE_VALUE = 4294967294

    def setNonce(self, newNonce):
        if newNonce <= 0:
            raise InvalidNonceException('Nonces must be positive')
        if newNonce <= self.nonce:
            raise InvalidNonceException('Nonces must be strictly increasing')
        if newNonce > self.MAX_NONCE_VALUE:
            raise InvalidNonceException('Nonces cannot be greater than %d' %
                                        self.MAX_NONCE_VALUE)

        self.nonce = newNonce

        return self.nonce

    def incrementNonce(self):
        if self.nonce >= self.MAX_NONCE_VALUE:
            raise InvalidNonceException('Cannot increment nonce, already at'
                                        ' maximum value')

        self.nonce += 1

        return self.nonce


class AbstractKeyHandler(object):
    """AbstractKeyHandler handles the tedious task of managing nonces
    associated with BTC-e API key/secret pairs.
    The getNextNonce method is threadsafe, all others need not be."""
    def __init__(self):
        self._keys = {}
        self._loadKeys()

    @property
    def keys(self):
        if self._keys is None:
            raise Exception("Attempted to use a closed key handler.")

        return self._keys.keys()

    def _loadKeys(self):
        """ 
        Load the keys with their secrets and nonces from the datastore. 
        """
        raise NotImplementedError

    def _updateDatastore(self):
        """
        Should update the datastore with the latest data (newest nonces, and any
        keys that might have been added)
        """
        raise NotImplementedError

    def __del__(self):
        self.close()

    def close(self):
        self._updateDatastore()

        # By convention, if _keys is None the object is considered
        # closed and should not attempt to touch the underlying storage.
        self._keys = None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()

    def addKey(self, key, secret, next_nonce):
        if self._keys is None:
            raise Exception("Attempted to use a closed key handler.")

        self._keys[key] = KeyData(secret, next_nonce)
        return self

    def getNextNonce(self, key):
        return self.getKey(key).incrementNonce()

    def getSecret(self, key):
        return self.getKey(key).secret

    def setNextNonce(self, key, nextNonce):
        return self.getKey(key).setNonce(nextNonce)

    def getKey(self, key):
        if self._keys is None:
            raise Exception("Attempted to use a closed key handler.")

        data = self._keys.get(key)
        if data is None:
            raise KeyError("Key not found: %r" % key)

        return data


class KeyHandler(AbstractKeyHandler):
    """An implementation of AbstractKeyHandler using local files to store the
    data."""
    def __init__(self, filename=None, resaveOnDeletion=True):
        """The given file is assumed to be a text file with three lines
        (key, secret, nonce) per entry."""
        self.filename = filename
        self.resaveOnDeletion = resaveOnDeletion
        super(KeyHandler, self).__init__()

    def _loadKeys(self):
        if self.filename is not None:
            self._load()

    def _updateDatastore(self):
        if self.resaveOnDeletion and self.filename is not None:
            self._save()

    def _save(self):
        # Do nothing if the object has been closed.
        if self._keys is None:
            return

        with open(self.filename, 'wt') as f:
            for k, data in self._keys.items():
                f.write("%s\n%s\n%d\n" % (k, data.secret, data.nonce))

    def _load(self):
        with open(self.filename, 'rt') as input_file:
            while True:
                key = input_file.readline().strip()
                if not key:
                    break
                secret = input_file.readline().strip()
                nonce = int(input_file.readline().strip())
                self.addKey(key, secret, nonce)
