# grin-wallet-tool:old_key:<br>
Grin-wallet-tool is a Python command line tool that can be used to a) generate new wallets, b) load  existing wallets and c) *load* or *swipe* grin funds to or from  a wallet or voucher using the grin-wallet API. 
**Supported wallet types:**
 1. regular-wallet
 2. bip39-password-wallet
 3. voucher-wallet
 4. brain-bip39-wallet

 This tool is designed for advanced users who know how to use the command line and are familiar with the concept of [BIP39 wallets with extra password](https://bitcoin.stackexchange.com/questions/120215/how-is-an-hd-wallet-key-generated) and brain wallets, and entropy. In particular brain-wallets require a good understanding of their inherent risks.

## How are grin wallets generated (BIP39, BIP32)?
Grin wallets use [BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md) word lists for mnemonic seed generation and [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032/derivation.pnghttps://github.com/bitcoin/bips/blob/master/bip-0032/derivation.png) standard for deriving Hierarchically Deterministic ([HD]((https://anynomouss.github.io/grin-for-muggles/grin_for_muggles_and_aspiring_wizards.html)])) wallet master and children keys. The entropy for a BIP39 mnemonnic seed phrase is randomly generate and can be represented as 12 word mnemonic (128 bits of entropy + checksum) or 24 word mnemonic (256 bits + checksum). BIP39 also allows inclusion of an extra password that is needed together with the mnemonic to derive a wallet. The advantage of using such an extra password is that if your mnemonic seed phrase is ever stolen, it cannot be used so easily since the attacker requirs to brute force or guess the extra BIP39 password. The disadvantage of using an extra BIP39 password is that you require that you need to remember the password and that you require this tool to regenerate your wallet since extra passwords are currently not supported by any of the main Grin wallet softwares. Note that if you die, your relatives will need this extra password and detailed instruction to regain access to your Grin wallet. Security and ease (recoverability) are often inversely correlated.

## How are BIP39 brain wallets generated
Regular wallets start with generating random entropy which together with a checksum can be presented as a mnemonic seed phrase. The difference with brain-bip39 wallets is that they allow you to use any one secret (*secret1*) to replace the innitial seed entropy from which the mnemonic is generated, and optionally allows for a second secret (*secret2*) to be used a a bip39 password for extra security. The particular implementation of brain-bip39 password protected wallets for Grin is a custom and more secure than traditional brain wallets. Note that nothing stops you from using the same password for *secret1* and *secret2* although this does reduce the security and might be confusing since you might later on think you only used it for *secret1*. Grin brainwallets still use BIP39 to generate a mnemonic based on *secret1* and BIP32 adds additional security since it includes an additional 2048 rounds of HMAC-SHA251 hashing for key stretching. The resulting wallets is a regular HD wallet. When using two secrets, this type of brain wallets is much more secure than traditional brain wallets. <br>
Having the option for two secrets also allows for more advanced use cases, such as sharing a strong secret before hand and using each time a new second secret, that can consists of fairly simple text messages send via a public channel, to send funds between users. See the heading "Use Cases" for some examples.
 
:warning: **Warning** :warning:: Any string that a human can think of is much less random than a regular 12 word mnemonic. Unless you understand the inherent risk of using brain wallets and have a good reason to use them, this auther not to use them, particullarly do not use them to hold large amounts of funds for a longer time. 
To regenerate a brain wallet, you will need either to provide both secrets as arguments to this script or provide the mnmemonic and the second secret, e.g.:
```
secret1="myfirstpassword", secret2="mysecondpassword"
    OR
mnmemonic_in="some 12 or 24 word mnemonic", secret2="mysecondpassword"
```

## Protocol explenation of how wallets are generated

 1. wallet-type="regular-wallet": <br>
    ```nocolor
    entropy+checksum -> seed_phrase 12-24 words (2048 rounds of HMAC-SHA512) ->  HD wallet*
    ```
 2. wallet-type="bip39-wallet": <br>
    ```nocolor
    entropy+checksum -> seed_phrase (12-24 words) + password (2048 rounds of HMAC-SHA512) ->  HD wallet
    ```
 3. wallet-type="voucher-wallet": <br>
    ```nocolor
    entropy+checksum -> seed_phrase (15 words) -> (2048 rounds of HMAC-SHA512) ->  HD wallet
    ```
 4. wallet-type="brain-bip39-wallet": <br>
    ```nocolor
    SHA256(secret1*)+checksum -> seed_phrase (24 words) + secret2*   (2048 rounds of HMAC-SHA512) ->  HD wallet
    *secret1 and secret2 are UTF16 encode string and as such do support Chinese charcters
    ```


## EXAMPLES

### Why Brain wallets?
Charlie is an advanced crypto enthousiast who assumes all his communication is monitored. He want to send a friend Grin via regular messages hidden in plain sight without it being obvious that he is sending Grin.  <br>
**Example 1:** Charlie can send the message "Hi Alice, smile for me:)" via a non encrypted messaging tool and she can input that into this tool and swipe the funds to her main wallet, without anyone ever suspecting a transaction of sorts took place. <br>
Before sending the messssage, Charlie generated a wallet and deposited funds in a brain wallet, Alice swipes them after reseaving the message
 ```nocolor
## Charlie:
python grin-wallet-tool.py --new=True --wallet-type="brain-bip39-wallet" secret1="Hi Alice, just grin" deposit=100 
## Alice:
python grin-wallet-tool.py --load=True --wallet-type="brain-bip39-wallet" secret1="Hi Alice, just grin" swipe=True 
 ```
**Example 2:** Charlie met Alice ones and gave her a first secret that is needed to recover funds from any brain wallet message he sends to Alice. The first secret is *wimblemimble* and only he and Alice know this secet. 
Charlie can send the message *"Hi Alice, just grin"* and she can input both secrets in the tool to load the wallet and swipe the funds. Note that this example is more secure than the first example since it involves two secrets.
 ```nocolor
## Charlie:
python grin-wallet-tool.py --new=True --wallet-type="brain-bip39-wallet" secret1="Hi Alice, just grin" secret2="wimblemimble" deposit=100 
## Alice:
python grin-wallet-tool.py --load=True --wallet-type="brain-bip39-wallet" secret1="Hi Alice, just grin" secret2="wimblemimble" swipe=True 
 ```
**Example 3**: Charlie is aware that brain wallets are not very secure to be used for a main wallet but insists he knows two very good secrets.
He uses the last 8 words of the first sentence of his favorit book as first secret and uses his phone numer as second secret to generate his main wallet. He knows that this combination of two long secrets is reasonably secure and easy to remember without needing a physical backup but understands it is still less secure than a randomly generated wallet with a mnemonic.

### Why use BIP39 wallets?
**Example 4:** Charlie played with brain wallets and realised that by using a random seed for the entropy together with a BIP39 password, he can generate a truly safe wallet backup since the seed cannot be guessed. He generates an output wallet file:
 ```nocolor
python grin-wallet-tool.py --load=1000 --wallet-type="bip39-wallet" bip39-password="proteG0"  
wallet-file="bip39password_protected_wallet.json" 
 ```

**Example 5:** 
For security he keeps two backup of the mnemonic, one in his house, one hidden in his parents house. Even when a burgler breaks into his hous and finds the mnemonic, the thief will need expert help to recover the BIP39 password which takes time and expertise. Long before the thief can access his funds, Charlie recovers the wallet using the second backup at his parents place together with his BIP39 password and sends the funds to a new wallet. 
**Example 6:** 

### Why use wallet vouchers?
Grin voucher wallets can be shared as paper wallet with a QR code or as a mnemonic seed phrase, or as a wallet file. The receiver of a grinvoucher basically gets shared access to the wallet and can sweep funds into a wallet only they control. Note that grin vouchers are not a replacement for regular transactions since they generate payments proofs and shared access to a wallet means there is no proper way to settle disputes if one of the parties cheats. For example, selling a voucher where the creator sweeps the funds before the buyer can. Be aware of these risks.  
**Example 7:** Bob wants to give Charlie grin for his birthday.  He creates a voucher wallet on which he deposits some grin funds and uses the *qr-file="birthday-QR-code"* command to output a QR code for the voucher wallet which he can incorporate into a cool grin birhtday card design.  
Bob is very happy with his gift, knowing he gets to own a small piece of a very elegant crypto project that is designed for the decades to come. He scans the QR and "poof" he magically swipes all the funds into his mobile Grim wallet without even needing to go through any interaction dance or need to worry whether Bob's wallet is online. 
**Example 8:**
Tom wants to create physical grin coins with a NFC chip that contain swipable grin wallets to sell to Harry. Tom generates vouchers wallets using this tool using the "wallet-out="NFC-coin-wallet1", loading them with a 100 grin using the argument *deposit=100*. 
The resulting voucher wallets will be stored on the NFT chip and optionally printed as QR on the back. Harry digs the coins and thinks Tom is a real wizard.
## Alice:
 ```nocolor
## Tom:  
python grin-wallet-tool.py --new=True --deposit=100 --wallet-type="voucher-wallet" qr-file="birthday-QR-code.png" 
## Harry:
python grin-wallet-tool.py --load=True --swipe=True --wallet-type="voucher-wallet"  *qr-file="birthday-QR-code.png"*
 ```
