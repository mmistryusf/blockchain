from web3 import Web3
import eth_account
import os

def get_keys(challenge,keyId = 0, filename = "eth_mnemonic.txt"):
    """
    Generate a stable private key
    challenge - byte string
    keyId (integer) - which key to use
    filename - filename to read and store mnemonics

    Each mnemonic is stored on a separate line
    If fewer than (keyId+1) mnemonics have been generated, generate a new one and return that
    """

    w3 = Web3()

    msg = eth_account.messages.encode_defunct(challenge)

	#YOUR CODE HERE
    sk = "58ba79907fc0bf103b89d9cd25a52ffc1a73112dae7bd01784670627541464d9"
    private_key =hex(int(sk, 16)) 
    #eth_addr = account.address
    eth_addr = "0xeccB3980559C4476Bb5F1f9e572930e8AB683e09"

    sig = w3.eth.account.sign_message(msg, private_key=private_key)
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
