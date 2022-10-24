from base64 import b64encode
from algosdk.v2client import algod
from algosdk import mnemonic, encoding
from algosdk.future.transaction import wait_for_confirmation, AssetTransferTxn, PaymentTxn, calculate_group_id, LogicSigTransaction, LogicSig
import json


asset_id = 14035004

def opt_in(algod_client:algod.AlgodClient, mnem_B:str):
    params = algod_client.suggested_params()
    account_info = algod_client.account_info(mnemonic.to_public_key(mnem_B))
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1    
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

    if not holding:

        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=mnemonic.to_public_key(mnem_B),
            sp=params,
            receiver=mnemonic.to_public_key(mnem_B),
            amt=0,
            index=asset_id)
        stxn = txn.sign(mnemonic.to_private_key(mnem_B))
        txid = algod_client.send_transaction(stxn)
        print(txid)
        # Wait for the transaction to be confirmed
        wait_for_confirmation(algod_client, txid)


def transferAsset(algod_client:algod.AlgodClient, lsig: LogicSig, mnem_B:str):
    params = algod_client.suggested_params()
    txn_2 = PaymentTxn(
        mnemonic.to_public_key(mnem_B), 
        params, 
        "4O6BRAPVLX5ID23AZWV33TICD35TI6JWOHXVLPGO4VRJATO6MZZQRKC7RI", 
        4200000
    )

    txn_1 = AssetTransferTxn(
        sender="4O6BRAPVLX5ID23AZWV33TICD35TI6JWOHXVLPGO4VRJATO6MZZQRKC7RI",
        sp=params,
        receiver=mnemonic.to_public_key(mnem_B),
        amt=1,
        index=asset_id
    )


    # get group id and assign it to transactions
    gid = calculate_group_id([txn_2, txn_1])
    txn_2.group = gid
    txn_1.group = gid

    stxn_2 =  txn_2.sign(mnemonic.to_private_key(mnem_B))
    stxn_1 =  LogicSigTransaction(txn_1, lsig)
    
    group = [stxn_2, stxn_1]
    tx_id = algod_client.send_transactions(group)

    confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
    print("txID: {}".format(tx_id), " confirmed in round: {}".format(
    confirmed_txn.get("confirmed-round", 0)))   



# purestake headers
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "fPMpB0SpZv3M4e9OTKAWC9NxBymUVSkj5IfwCuD0"
headers = {
"X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

lsig = encoding.future_msgpack_decode(b64encode(open('SmartSignature.lsig', 'rb').read()))

mnemonic_A = input("Mnemonic A: ").strip()

opt_in(algod_client, mnemonic_A)
transferAsset(algod_client, lsig, mnemonic_A)

