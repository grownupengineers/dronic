
DEFAULT_VAULT_PATH = '/opt/dronic/.vault'

class Credentials(object):

    # maybe decide where the vault will be
    def __init__(self, vault: str = None):
        self._vault = vault is None ? DEFAULT_VAULT_PATH : vault
    
    # to be callable
    # like in:
    #   credentials = Credentials()
    #   git_key = credentials('git-key')
    def __call__(self, cred_id):
        # TODO look in the vault for the credentials
        return "fuck off"
