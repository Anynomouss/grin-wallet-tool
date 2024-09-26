# -*- coding: utf-8 -*-
"""
@author: Anynomous
Licence: Apache v2.0.
Dislaimer: Software is provided as it without any waranty, use it at your own risk
WARNINGs: 
    -The use of brain wallets is inherently insecure since humans are
    not a good source of entropy. Use at your own risk!  
    -Brain wallet with BI39 passwords are more secure thanks to 2000 rounds of additional sha512 hardening. 
    -This tool is best used in a secure environment 
    -Always keep a backup of the software you use to generate wallets
    -When generating a Bip39 brain wallet, it is adviced to keep a non-digital 
    copy of the mnemonic that can be used with the BIP39 password to regain access to funds
    -Grin brain wallets can be used to share a message that leads to a shared wallet
    a shared wallet is not a replacement for normal transactions, does not generate
    payment proofs, cannot be used for dispute settlement and should only be 
    used to send funds to a receiver you want to have full control over send funds.
    
    -When receiving funds via a brain wallet, note that access is shared with the
    sender and funds are only safe when you send them to a wallet that you control

    HOW TO USE THIS TOOL:
    BEFORE YOU START, RUN GRIN NODE, INIT A WALLET AND ENABLE OWNER API:
    grin-wallet.exe init -r --here 
    grin-wallet.exe  --testnet owner_api --run_foreign    
    grin.exe --testnet
    
    
    ## Wallet types
    --type
    --normal-wallet
    --bip39-password-wallet
    --brain-bip39-password-wallet
    (either with one or two secrets)
    --voucher-wallet
    
    ## Action
    --new
    --load
     
    ## Input
    --mnemonic
    --brain-pasword
    --bip39-pasword
    --wallet-pasword

    ## Outputs
    --print-mnemonic
    --print-qr
    --create_wallet-file
    --create_qr-file
    
    ## API actions
    --deposit
    --swipe
    
    ## Extra options
    --secure=True
    
PROCEDURE:
    ITERATIVEY - for each wallets/vouchers, do the following:
1) Create a wallet using mimblewimble-py, 
2) Initiate a SRS transaction through the grin-wallet API -> grinmw library
3) Sign the transaction using the voucher wallet, - >  mimblewimble-py library
4) Sign with grin-wallet using the API (grinmw library) and finalize/broadcast the transaction
5) Create output wallet backup in the log file and generate the vouchers
    
USEFULL LINKS:
https://github.com/grinventions/mimblewimble-py
https://grincc.github.io/grin-wallet-api-tutorial/
https://docs.rs/grin_wallet_api/latest/grin_wallet_api/trait.OwnerRpc.html#required-methods
https://github.com/grincc/grin-wallet-api-tutorial
https://github.com/mimblewimble/grin-rfcs/blob/master/text/0007-node-api-v2.md#owner-api-endpoints



../../Python/Python311/python.exe grin-brainwallet.py
../../Python/Python311/python.exe test.py --passphrase='test'
"""



import argparse # pip install argparse
from mnemonic import Mnemonic # pip install mnemonic
from mimblewimble.wallet import Wallet # pip install mimblewimble
import hashlib # pip install hashlib, for SHA256 computation
import binascii
from grinmw.wallet_v3 import WalletV3
from pathlib import Path
from getpass import getpass
home = str(Path.home())

### Grin API's
import pprint, os
from grinmw.node_v2 import NodeV2
from grinmw.wallet_v3 import WalletV3
from pathlib import Path

def brain_wallet_bi39(passphrase1,passphrase2):
    bip39passphrase = passphrase
    mnemo =  Mnemonic("english")
    entropy = binascii.hexlify(passphrase1.encode('utf-8'))
    seed_bytes=entropy=hashlib.sha256(entropy.encode('utf-8')).digest()
    mnemonic = mnemo.to_mnemonic(entropy)
    master_seed = mnemo.to_seed(mnemonic, bip39passphrase.encode('utf-8').strip())
    w = Wallet(master_seed=master_seed)
    ##
    # instantiate the wallet
    # w = Wallet.fromSeedPhrase(recovery_phrase)
    
    # derive the slatepack address and the recovery phrase
    # path = 'm/0/1/0'
    # slatepack_address = w.getSlatepackAddress(path=path)
    return (w)
    


def brain_wallet_two_secrets(passphrase,bip39_passphrasse):
    mnemo =  Mnemonic("english")
    entropy = passphrase
    seed_bytes=entropy=hashlib.sha256(entropy.encode('utf-8')).digest()
    mnemonic = mnemo.to_mnemonic(entropy)
    master_seed = mnemo.to_seed(mnemonic, bip39passphrase.strip())
    w = Wallet(master_seed=master_seed)
    ##
    # instantiate the wallet
    # w = Wallet.fromSeedPhrase(recovery_phrase)
    
    # derive the slatepack address and the recovery phrase
    # path = 'm/0/1/0'
    # slatepack_address = w.getSlatepackAddress(path=path)
    return (w)

def input_arguments_sanity_check(argumentss):
    ## SANITY checks and ask user for additional inputs in case secure=True
    valid_arguments=True
    
    ## Check only one wallet type command
    if sum([argument.normal-wallet, argument.bip39-pwd-walle,argument.brain-wallet, 
            argument.brain-wallet, argument.brain-bip39-pwd-wallet, 
            argument.voucher-wallet]) !=1:
        print("Error 1: You have to chose exactly one type of wallet: ")
        print("--normal-wallet=True")
        print("--bip39-pwd-wallet=True")
        print("--brain-bip39-pwd-wallet=True")
        print("--voucher-wallet=True")
        valid_arguments = False

        
    if sum([argument.new, argument.load]) !=1:
        print("Error 2: You have to chose exactly one of these two arguments: ")
        print("Use new co create a new wallet, use load to swipe funds from an existing wallet")
        print("--new=True")
        print("--load=True")
        
    
    if not valid_arguments:
       print("Status, cancelled because of invalid aruments, see error messages")    
            

###############################################################################
## Parse command line argument, check only possible combinations used
###############################################################################
if __name__ == '__main__':
    ###############################################################################
    ## 0A) Parse command line arguments using arparse
    ## Wallet types
    parser.add_argument("--normal-wallet", help = "Example: --normal-wallet=True", required = False, default = False, type=bool)
    parser.add_argument("--bip39-pwd-wallet", help = "Example: --bip39-pwd-wallet=True", required = False, default = False, type=bool)
    parser.add_argument("--brain-bip39-pwd-wallet", help = "Example: --brain-bip39-pwd-wallet=True", required = False, default = False, type=bool)
    parser.add_argument("--brain-wallet", help = "Example: --brain-wallet=True", required = False, default = False, type=bool)

    parser.add_argument("--voucher-wallet", help = "Example: --voucher=True", required = False, default = False, type=bool)
    ## Action
    parser.add_argument("--new", help = "Example: --new=True", required = False, default = False, type=bool)
    parser.add_argument("--load", help = "Example: --load=True", required = False, default = False, type=bool)
    ## Input
    parser.add_argument("--mnemonic", help = "Example: --mnemonicd='True'", required = False, default = False, type=bool)
    parser.add_argument("--bip39-password", help = "Example: --bip39-password=mysecondsecret", required = False, default = False, type=bool)
    parser.add_argument("--brain-password", help = "Example: --brain-password='myfirstsecret'", required = False, default = False, type=bool)
    ## Outputs
    parser.add_argument("--print-mnemonic", help = "Example: --wallet-password='password_for_wallet_out'", required = False, default = False, type=bool)
    parser.add_argument("--print-QR", help = "Example: ----print-QR=True", required = False, default = False, type=bool)
    parser.add_argument("--create_wallet-file", help = "Example: --create_wallet-file=True", required = False, default = 'False', type=str)
    parser.add_argument("--create_qr-file", help = "Example: --create_qr-file=True", required = False, default = 'False', type=str)
    ## API actions
    parser.add_argument("--deposit", help = "Example: --deposit=10.00", required = False, default = 0, type=int)
    parser.add_argument("--swipe", help = "Example: --swipe=True", required = False, default = False, type=bool)
    ## Extra options
    parser.add_argument("--secure", help = "Example: --secure=True", required = False, default = False, type=bool)

    
    
 
        

        if argument.new == True:
            passphrasse = getpass("Please enter your brain wallet secret passsphrase and press enter: ")     
        
    ## 1) Ask user for first secret/brainwallet password and if sepecified, also bii38 passpord 
    if argument.new == "True":
        passphrase = getpass("Passphrase: ")
    if argument.bip39passphrase == True:
        bip39passphrase = getpass("bip39 passphrase: ")    
    
    ## 2) Generate entropy for the brainwallet baseed on input password(s))
    if argument.bip39passphrase == "False":  

        
    if argument.bip39passphrase == True:     
        seed_bytes = mnemo.to_seed(mnemonic, passphrase=argument.bip39passphrase.strip())
        
    if argument.deposit:
        ## instantiate two wallets wallet, path is path for address generation for account zero
        voucher_path = 'm/0/1/0'
        voucher_wallet = Wallet.initialize()
        voucher_slatepack_address = voucher_wallet.getSlatepackAddress()
        
        


###############################################################################
## Wallet actions
## Dependencies, not on linux use pip3 to istall for Python 3
## https://github.com/grinfans/grinmw.py/tree/main
###############################################################################



## Setup API's
home = str(Path.home())
wallet_api_url = 'http://localhost:3420/v3/owner'
node_api_url = 'http://localhost:3420/v3/owner'
pp = pprint.PrettyPrinter(indent=4)

# change to your grin node owner_api sercret file
node_api_secret_file = '/home/ubuntu/.grin/main/.owner_api_secret'
wallet_api_user = 'grin'
wallet_api_password = open(node_api_secret_file).read().strip()
wallet = WalletV3(wallet_api_url, wallet_api_user, wallet_api_password)
wallet.init_secure_api()

# change to you wallet password
wallet_password = '123'

wallet.open_wallet(None, wallet_password)
pp.pprint(wallet.node_height())
pp.pprint(wallet.get_slatepack_address())


#########Examples
# change to you wallet password
wallet_password = '123'

wallet.open_wallet(None, wallet_password)
pp.pprint(wallet.node_height())
pp.pprint(wallet.get_slatepack_address())
##############################################################################

        
        #######################################################################
        ## 2 Initiate an SRS transaction via the wallet owner API
        #######################################################################
        
        ## The path assumes you innitiated the sender wallet with grin-wallet --here
        pp = pprint.PrettyPrinter(indent=4)
        api_url = 'http://localhost:3420/v3/owner'
        
        ## change to your grin owner_api sercret file
        api_sercet_file = 'settings/.owner_api_secret'
        api_user = 'grin'
        api_password = open(api_sercet_file).read().strip()
        wallet = WalletV3(api_url, api_user, api_password)
        wallet.init_secure_api()
        
        ## change to you wallet password
        wallet_password = 'Test123' 
        wallet.open_wallet(None, wallet_password)
        ## pp.pprint(wallet.get_slatepack_address())
        
        ## send transaction, example from gate.io
        send_args = {
            'src_acct_name': None,
            'amount': int(argument.value * 1000000000),
            'minimum_confirmations': 10,
            'max_outputs': 500,
            'num_change_outputs': 1,
            'selection_strategy_is_use_all': False,
            'target_slate_version': None,
            'payment_proof_recipient_address': voucher_slatepack_address, 
            'ttl_blocks': None,
            'send_args': {
                "dest": 'grin1n26np6apy0757asdfads6qx6yz4qayuwxcpjvl87a2mjv3jpk6mnyz8y4vq65ahjm',
                "post_tx": True,
                "fluff": True,
                "skip_tor": True,
                "amount_includes_fee":argument.feesindcluded
            }
        }
        
        results = wallet.init_send_tx(send_args)
        print(results)
        