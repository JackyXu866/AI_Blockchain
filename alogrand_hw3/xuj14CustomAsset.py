from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk.future.transaction import AssetConfigTxn, wait_for_confirmation


def create_asset(algod_client: algod.AlgodClient, mnemonic_phrase: str):
    params = algod_client.suggested_params()
    public_key = mnemonic.to_public_key(mnemonic_phrase)
    txn = AssetConfigTxn(
        sender=public_key,
        sp=params,
        total=100,
        default_frozen=False,
        unit_name="XUJ14",
        asset_name="xuj14",
        manager=public_key,
        reserve=public_key,
        freeze=public_key,
        clawback=public_key,
        url="https://github.com/JackyXu866", 
        decimals=0
    )
    stxn = txn.sign(mnemonic.to_private_key(mnemonic_phrase))
    txid = algod_client.send_transaction(stxn)
    print(txid)

    wait_for_confirmation(algod_client, txid)
    try:
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print("Asset ID:", asset_id)
    except Exception as e:
        print(e)



# purestake headers
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "fPMpB0SpZv3M4e9OTKAWC9NxBymUVSkj5IfwCuD0"
headers = {
"X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

mnemonic_phrase = input("Mnemonic: ").strip()
create_asset(algod_client, mnemonic_phrase)

# Asset ID: 118194452