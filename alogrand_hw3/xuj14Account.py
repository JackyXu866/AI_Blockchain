from algosdk import account, mnemonic
from algosdk.v2client import algod

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "fPMpB0SpZv3M4e9OTKAWC9NxBymUVSkj5IfwCuD0"
headers = {
   "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)

generate_algorand_keypair()
generate_algorand_keypair()


# https://developer.algorand.org/docs/get-details/accounts/create/
