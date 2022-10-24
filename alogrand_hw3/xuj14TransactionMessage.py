import json
import base64
from algosdk.v2client import algod
from algosdk import mnemonic, constants
from algosdk.future import transaction


def transact(mnemonic_phrase):
    # purestake headers
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "fPMpB0SpZv3M4e9OTKAWC9NxBymUVSkj5IfwCuD0"
    headers = {
    "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    account = mnemonic.to_public_key(mnemonic_phrase)
    account_info = algod_client.account_info(account)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

    params = algod_client.suggested_params()

    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    note = "xuj14: Hello Assignment 03".encode()
    amount = 1
    send_to = "CHUGMLOF276225HD4EFKFQUR5YY3ZPED6XLR6ISPLMTKO56XHAHSSEML3M"
    unsigned_txn = transaction.PaymentTxn(account, params, send_to, amount, None, note)

    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(mnemonic_phrase))

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(account)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")


mnemonic_phrase = input("Mnemonic: ").strip()
transact(mnemonic_phrase)
