import requests, json, types

server = 'https://api.blockmetro.io/v0/'

def check_errors(request_type: str, req: str, data: dict, headers: dict):
    try:
        if request_type == 'get':
            r = requests.get(f'{server}{req}', json=data, headers=headers)
        if request_type == 'post':
            r = requests.post(f'{server}{req}', json=data, headers=headers)
        if request_type == 'put':
            r = requests.put(f'{server}{req}', json=data, headers=headers)
        if request_type == 'delete':
            r = requests.delete(f'{server}{req}', json=data, headers=headers)
        return json.loads(r.text)
    except Exception as e:
        return {'error': {'message': 'ERROR: API Connection Error'} }

def get_request(api_key: str, req: str, data={}):
    headers = {'api-key': api_key}
    return check_errors('get', req, data, headers)

def post_request(api_key: str, req: str, data={}):
    headers = {'api-key': api_key}
    return check_errors('post', req, data, headers)

def put_request(api_key: str, req: str, data={}):
    headers = {'api-key': api_key}
    return check_errors('put', req, data, headers)

def delete_request(api_key: str, req: str, data={}):
    headers = {'api-key': api_key}
    return check_errors('delete', req, data, headers)

class Wallet:
    def __init__(self, api_key=''):
        self.api_key = api_key

    def retrieve(api_key: str):
        return get_request(api_key, 'wallet')

class Usage():
    def __init__(self, api_key: str):
        self.api_key = api_key

    def retrieve(api_key: str):
        return get_request(api_key, 'usage')

class Balance():
    def __init__(self, api_key=''):
        self.api_key = api_key

    def retrieve(api_key: str):
        return get_request(api_key, 'balance')

class Address():
    def __init__(self, api_key=''):
        self.api_key = api_key

    def retrieve(api_key: str, address: str):
        data = {'address': address}
        return get_request(api_key, 'addresses', data)

    def list(api_key: str, used='all', page=0):
        data = {'used': used, 'page': page}
        return get_request(api_key, 'addresses/list', data)

class StakePool():
    def __init__(self, api_key=''):
        self.api_key = api_key

    def retrieve(api_key: str):
        return get_request(api_key, 'stake-pools')

    def join(api_key: str, stake_pool_id: str):
        data = {'stake_pool_id': stake_pool_id}
        return put_request(api_key, 'stake-pools', data)

    def leave(api_key: str):
        return delete_request(api_key, 'stake-pools')

class Policy():
    def __init__(self, api_key=''):
        self.api_key = api_key

    def retrieve(api_key: str, policy_id: str):
        data = {'policy_id': policy_id}
        return get_request(api_key, 'policies', data)

    def create(api_key: str, name: str, active_until: int):
        data = {'name': name, 'active_until': active_until}
        return post_request(api_key, 'policies', data)

    def delete(api_key: str, policy_id: str):
        data = {'policy_id': policy_id}
        return delete_request(api_key, 'policies', data)

    def list(api_key: str, page=0):
        data = {'page': page}
        return get_request(api_key, 'policies/list', data)

class Transaction():
    def __init__(self, api_key=''):
        self.api_key = api_key

    def retrieve(api_key: str, transaction_id: str):
        data = {'transaction_id': transaction_id}
        return get_request(api_key, 'transactions', data)

    def create(api_key: str, payments: list):
        data = {'payments': payments}
        return post_request(api_key, 'transactions', data)

    def mint(api_key: str, address: str, policy_id: str, metadata: dict, amount=1, lovelace=0):
        data = {'address': address, 'policy_id': policy_id, 'metadata': metadata, 'amount': amount, 'lovelace': lovelace}
        return post_request(api_key, 'transactions/mint', data)

    def burn(api_key: str, policy_id: str, asset_name: str, amount=1):
        data = {'policy_id': policy_id, 'asset_name': asset_name, 'amount': amount}
        return post_request(api_key, 'transactions/burn', data)

    def list(api_key: str, direction='all', page=0):
        data = {'direction': direction, 'page': page}
        return get_request(api_key, 'transactions/list', data)

class Asset():
    def __init__(self, api_key=''):
        self.api_key = api_key

    def retrieve(api_key: str, policy_id: str, asset_name: str):
        data = {'policy_id': policy_id, 'asset_name': asset_name}
        return get_request(api_key, 'assets', data)

    def list(api_key: str, policy_id='', page=0):
        data = {'policy_id': policy_id, 'page': page}
        return get_request(api_key, 'assets/list', data)

class BlockMetro():
    def __init__(self, api_key):
        self.api_key = api_key
        self.load_wallet(api_key)
        self.load_usage(api_key)
        self.load_balance(api_key)
        self.load_address(api_key)
        self.load_stake_pool(api_key)
        self.load_policy(api_key)
        self.load_transaction(api_key)
        self.load_asset(api_key)

    def load_wallet(self, api_key):
        wallet = Wallet(api_key)

        def new_retrieve(self):
            return get_request(self.api_key, 'wallet')

        wallet.retrieve = types.MethodType(new_retrieve, wallet)
        self.Wallet = wallet

    def load_usage(self, api_key):
        usage = Usage(api_key)

        def new_retrieve(self):
            return get_request(self.api_key, 'usage')

        usage.retrieve = types.MethodType(new_retrieve, usage)
        self.Usage = usage

    def load_balance(self, api_key):
        balance = Balance(api_key)

        def new_retrieve(self):
            return get_request(self.api_key, 'balance')

        balance.retrieve = types.MethodType(new_retrieve, balance)
        self.Balance = balance

    def load_address(self, api_key):
        address = Address(api_key)

        def new_retrieve(self, address: str):
            data = {'address': address}
            return get_request(self.api_key, 'addresses', data)

        def new_list(api_key: str, used='all', page=0):
            data = {'used': used, 'page': page}
            return get_request(self.api_key, 'addresses/list', data)

        address.retrieve = types.MethodType(new_retrieve, address)
        address.list = types.MethodType(new_list, address)
        self.Address = address

    def load_stake_pool(self, api_key):
        stake_pool = StakePool(api_key)

        def new_retrieve(self):
            return get_request(self.api_key, 'stake-pools')

        def new_join(self, stake_pool_id: str):
            data = {'stake_pool_id': stake_pool_id}
            return put_request(self.api_key, 'stake-pools', data)

        def new_leave(self):
            return delete_request(self.api_key, 'stake-pools')

        stake_pool.retrieve = types.MethodType(new_retrieve, stake_pool)
        stake_pool.join = types.MethodType(new_join, stake_pool)
        stake_pool.leave = types.MethodType(new_leave, stake_pool)
        self.StakePool = stake_pool

    def load_policy(self, api_key):
        policy = Policy(api_key)

        def new_retrieve(self, policy_id: str):
            data = {'policy_id': policy_id}
            return get_request(self.api_key, 'policies', data)

        def new_create(self, name: str, active_until: int):
            data = {'name': name, 'active_until': active_until}
            return post_request(self.api_key, 'policies', data)

        def new_delete(self, policy_id: str):
            data = {'policy_id': policy_id}
            return delete_request(self.api_key, 'policies', data)

        def new_list(self, page=0):
            data = {'page': page}
            return get_request(self.api_key, 'policies/list', data)

        policy.retrieve = types.MethodType(new_retrieve, policy)
        policy.create = types.MethodType(new_create, policy)
        policy.delete = types.MethodType(new_delete, policy)
        policy.list = types.MethodType(new_list, policy)

        self.Policy = policy

    def load_transaction(self, api_key):
        transaction = Transaction(api_key)

        def new_retrieve(self, transaction_id: str):
            data = {'transaction_id': transaction_id}
            return get_request(self.api_key, 'transactions', data)

        def new_create(self, payments: list):
            data = {'payments': payments}
            return post_request(self.api_key, 'transactions', data)

        def new_mint(self, address: str, policy_id: str, metadata: dict, amount=1, lovelace=0):
            data = {'address': address, 'policy_id': policy_id, 'metadata': metadata, 'amount': amount, 'lovelace': lovelace}
            return post_request(self.api_key, 'transactions/mint', data)

        def new_burn(self, policy_id: str, asset_name: str, amount=1):
            data = {'policy_id': policy_id, 'asset_name': asset_name, 'amount': amount}
            return post_request(self.api_key, 'transactions/burn', data)

        def new_list(self, direction='all', page=0):
            data = {'direction': direction, 'page': page}
            return get_request(self.api_key, 'transactions/list', data)

        transaction.retrieve = types.MethodType(new_retrieve, transaction)
        transaction.create = types.MethodType(new_create, transaction)
        transaction.mint = types.MethodType(new_mint, transaction)
        transaction.burn = types.MethodType(new_burn, transaction)
        transaction.list = types.MethodType(new_list, transaction)

        self.Transaction = transaction

    def load_asset(self, api_key):
        asset = Asset(api_key)

        def new_retrieve(self, policy_id: str, asset_name: str):
            data = {'policy_id': policy_id, 'asset_name': asset_name}
            return get_request(self.api_key, 'assets', data)

        def new_list(self, policy_id='', page=0):
            data = {'policy_id': policy_id, 'page': page}
            return get_request(self.api_key, 'assets/list', data)

        asset.retrieve = types.MethodType(new_retrieve, asset)
        asset.list = types.MethodType(new_list, asset)
        self.Asset = asset
