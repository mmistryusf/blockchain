from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware #Necessary for POA chains
import json
import sys
from pathlib import Path

source_chain = 'avax'
destination_chain = 'bsc'
contract_info = "contract_info.json"

def connectTo(chain):
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

    if chain == 'bsc':
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['avax','bsc']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getContractInfo(chain):
    """
        Load the contract_info file into a dictinary
        This function is used by the autograder and will likely be useful to you
    """
    p = Path(__file__).with_name(contract_info)
    try:
        with p.open('r')  as f:
            contracts = json.load(f)
    except Exception as e:
        print( "Failed to read contract info" )
        print( "Please contact your instructor" )
        print( e )
        sys.exit(1)

    return contracts[chain]



def scanBlocks(chain):
    """
        chain - (string) should be either "source" or "destination"
        Scan the last 5 blocks of the source and destination chains
        Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
        When Deposit events are found on the source chain, call the 'wrap' function the destination chain
        When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
    """

    if chain not in ['source','destination']:
        print( f"Invalid chain: {chain}" )
        return
    
    w3_src = connectTo('avax')
    w3_dst = connectTo('bsc')

    #contract_info = getContractInfo(chain)
    src_con_info = getContractInfo('source')
    dst_con_info = getContractInfo('destination')

    src_con = w3_src.eth.contract(address = src_con_info['address'], abi = src_con_info['abi'])
    dst_con = w3_dst.eth.contract(address = dst_con_info['address'], abi = dst_con_info['abi'])    

    end_block_src = w3_src.eth.get_block_number()
    end_block_dst = w3_dst.eth.get_block_number()
    
    start_block_src = end_block_src - 5 if end_block_src > 5 else 0
    start_block_dst = end_block_dst - 5 if end_block_dst > 5 else 0
    if chain == 'source':
        events_data = src_con.events.Deposit.create_filter(fromBlock=start_block_src, toBlock=end_block_src, argument_filters={}).get_all_entries()
        print(f"event count: {len(events_data)}")
        for event in events_data:
            token = event['args']['token']
            recipient = event['args']['recipient']
            amount = event['args']['amount']
            print(f"Detected Deposit event: {token}, {recipient}, {amount}")
            # call wrap function on the destinatino chain
            tx = dst_con.functions.wrap(token, recipient, amount).transact()
            #tx = dst_con.functions.wrap(token, recipient, amount).transact({'from':w3_dst.eth.accounts[0]})
            w3_dst.eth.wait_for_transaction_receipt(tx)
    else:
        events_data = dst_con.events.Unwrap.create_filter(fromBlock=start_block_dst, toBlock = end_block_dst, argument_filters={}).get_all_entries()
        
        for event in events_data:
            token = event['args']['wrapped_token']
            recipient = event['args']['recipient']
            amount = event['args']['amount']
            print(f"Detected Unwrap event: {token}, {recipient}, {amount}")
            # call wrap function on the destinatino chain
            tx = src_con.functions.withdraw(token, recipient, amount).transact()
            #tx = dst_con.functions.wrap(token, recipient, amount).transact({'from':w3_dst.eth.accounts[0]})
            w3_wrc.eth.wait_for_transaction_receipt(tx)
scanBlocks('source')
scanBlocks('destination')
