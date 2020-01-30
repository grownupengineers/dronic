
import sqlite3
from cryptography.fernet import Fernet

# TODO encrypt the values with some key, or not

DEFAULT_VAULT_PATH = '/opt/dronic/.vault'
DEFAULT_ENC_KEY = b'FSpcfyOFMwyyKylfkRFp3lFjfderv5J5HY1BQbz6K0s='

class Credentials(object):

    # maybe decide where the vault will be
    def __init__(self, vault: str = None, key: bytes = None):
        self._vault = vault is None ? DEFAULT_VAULT_PATH : vault
        self._fernet = Fernet(bytes is None ? DEFAULT_ENC_KEY : key)
        # this should be read-only, so we can keep multiple connections open
        self._conn = sqlite3.connect(self._vault)
        # TODO execute initialization script
        # init_fd = open('path/to/init_vault.sql')
        # self._conn.executescript(init_fd.read()).close()    # close cursor
        # init_fd.close()
    
    # to be callable
    # like in:
    #   credentials = Credentials()
    #   git_key = credentials('git-key')
    def __call__(self, cred_id):
        # get table from CredMap
        query = "SELECT table FROM CredMap WHERE cred_id=(?)"
        cursor = self._conn.cursor()
        cursor.execute(query, (cred_id,))
        row = cursor.fetchone()

        if row is None:
            # cred_id not found
            raise Exception("No credentials named '%s'" % cred_id)
        
        cursor.close()
        
        table = row[0]

        # now get the stuff
        cursor = self._conn.cursor()
        query = "SELECT * FROM (?) WHERE cred_id=(?)"
        cursor.execute(query, (table, cred_id))
        row = cursor.fetchone()
        if row is None:
            # this is not suppose to happen
            raise Exception("Unexpectedly, credential '%s' was not found")
        
        cursor.close()

        # we could trust sqlite3 that cred_id is the first element
        # and simply
        #return row[1:]
        # but...
        ret_val = []
        _del = True
        for val in row:
            if val == cred_id and _del:
                # only delete first time
                _del = False
                continue
            ret_val.append(
                self._fernet.decrypt(val).decode()
            )
        
        return tuple(ret_val)

