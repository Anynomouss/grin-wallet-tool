# grin-wallet-tool:old_key:<br>
Grin-wallet-tool is a simple Python script that can be used to a) generate new or  b)load existing wallets and c) *load* or *swipe* grin funds to or from these wallets using the grin-wallet API. 
**Supported wallet types:**
 1. normal wallets
 2. bip39 password protected wallets
 3. voucher wallets
 4. brain-bip39 password protected wallets

 This tool is designed for advanced users who know how to use the command line and are familiar with the concept of [BIP39 wallets with extra password](https://bitcoin.stackexchange.com/questions/120215/how-is-an-hd-wallet-key-generatedhttps://bitcoin.stackexchange.com/questions/120215/how-is-an-hd-wallet-key-generated) and brain wallets. In particular brain-wallets require a good understanding of their risks. B

## How are grin wallets generated (BIP39, BIP32)?
Grin wallets use [BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md) word lists for mnemonic seed generation and [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032/derivation.pnghttps://github.com/bitcoin/bips/blob/master/bip-0032/derivation.png) standard for deriving Hierarchically Deterministic ([HD]((https://anynomouss.github.io/grin-for-muggles/grin_for_muggles_and_aspiring_wizards.html)])) wallet master and children keys. The entropy for a BIP39 mnemonnic seed phrase is normally randomly generate and can be represented as 12 word mnemonic (128 bits of entropy) or 24 word mnemonic (256 bits of entropy). BIP39 also allows inclusion of an extra password that is needed together with the mnemonic to derive a wallet. The advantage of using such an extra password is that if your mnemonic seed phrase is ever stolen, it cannot be used so easily since the attacker requirs to brute force or guess the extra BIP39 password. The downside of using an extra BIP39 password is that you require this tool to regenerate your wallet upon loss since it is not supported by any of the Grin wallet softwares. Also note that if you die, your relatives will need this extra password and might have a hard time recovering access to your Grin. 


## How are BIP39 brain wallets generated
Where normal wallets start with generating a mnemonic seed phrase from brain-bip39 wallets allows you to use any use one or two secret strings to generate a wallet. The particular implementation of brain-bip39 password protected wallets for Grin is a custom and includes the brain password as "_first secret_" to generate the initial seed entropy and optionally a "_second_secret_" as BIP39 password. The difference with traditional brain wallets is that this type of brain wallet is a) a HD wallet, reducing the chance of losing funds by missing kyes, and b) more secure since BIP39 includes an additional 2048 rounds of HMAC-SHA51 hashing for key stretching. Especially when using with two secrets, this is much more secure than traditional brain wallets. <br>
Having the option for two secrets allows more advanced use cases, such as sharing a first secret before hand and using a second secret that can consists of fairly simple messages send via a public channel to secure send funds between users.
  
:warning: **Warning** :warning:: Any string that a human can think of is much less random than a regular 12 word mnemonic. Unless you understand the inherent risk of using brain wallets and have a very reason to use them, it is ill adviced to them especially for wallets that hold large amounts of funds. 
To regenerate a brain wallet, you will need either to provide both secrets as arguments to this script or provide the mnmemonic and the second secret, e.g.:
```
secret1=myfirstpassword, secret2=mysecondpassword
OR
mnmemonic_in="some 12 or 14 word mnemonic", secret2=mysecondpassword
```

## Protocol explenation of how wallets are generated

 1. normal wallets: <br>
    ```
    seed_phrase 12-24 words (2048 rounds of HMAC-SHA512) ->  HD wallet*
    ```
 2. bip39 password protected wallet: <br>
    ```
    seed_phrase (12-24 words) + password (2048 rounds of HMAC-SHA512) ->  HD wallet
    ```
 3. vaucher wallets: <br>
    ```
    seed_phrase (15 words) -> (2048 rounds of HMAC-SHA512) ->  HD wallet
    ```
 4. brain-bip39 password protected wallets: <br>
    ```
    secret1 string (SHA256, add checksum) -> seed_phrase (12-24 words) + secret2   (2048 rounds of HMAC-SHA512) ->  HD wallet
    secret1 and secret2 are UTF8 encode strings
    ```


## EXAMPLE USE CASES

### Why Brain wallets?
Charlie is an advanced crypto enthousias who assumes all his communication is monitored. He want to send a friend Grin via regular messages hidden in plain sight without it being obvious that is sending a transaction or mnemonic.  <br>
**Example 1:** Charlie can send the message "Hi Alice, smile for me:)" via a normal non encrypted messaging tool and she can input that into this tool and swipe the funds to her main wallet, withoutanyone suspecting a transaction took place.
**Example 2:** Charlie met Alice ones and gave her a first secret that is needed to recover funds from any brain wallet message he sends to Alice. The first secret is *wimblemimble* and only he and Alice know this secet. 
Charlie can send the message *"Hi Alice, just grin"* and she can input *secret1="wimblemimble"* and *secret2="Hi Alice, just grin"* and argument *swipe=True* in the tool to swipe the funds from the brain wallet to her own wallet. Note that this second example is more secure than the first examplesince it involves two secrets and since BIP39 involves 2048 rounds of HMAC_SHA512 hardening!
**Example 3**: Charlie is aware that brain wallets are not very secure to be used for a main wallet but insists he knows two very good secrets.
He uses the last 8 words of the first sentence of his favorit book as first secret and uses his phone numer as second secret to generate his main wallet. He knows that this combination of two long secrets is reasonably secure and easy to remember without needing a physical backup but understands it is still less secure than a randomly generated wallet with a mnemonic

### Why use BIP39 wallets?
**Example 4:** Charlie played with brain wallets and realised that by using a random seed for the entropy together with a BIP39 password, he can generate a truly safe wallet backup since the seed cannot be guesed.   
For security he keeps two backup of the mnemonic, one in his house, one hidden in his parrents house. Even when a burgler breaks into his hous and finds the mnemonic, the thief will need expert help to recover the BIP39 password. Long before anyone can steal his funds Charlie recovers the wallet using the second backup at his parents place together with his BIP39 password. 

### Why use wallet vouchers?
Because they can be used to generate paper Grin wallets that can be shared in one interaction, basically by just giving someone the wallet to sweep funds from.  
**Example 5:** Bob wants to give Charlie grin for his birthday. He designs a cool custom card, creates a voucher wallet on which he deposits some grin, exports the wallet as a QR code which he puts on the custom card.  
Bob is very happy with this cool Grin birthday card. He scans the QR and "poof" he magically swipes all the funds without even needing to go through any interaction dance or with the risk of Bob's wallet not being online. 
**Example 6:**
Tom wants to create physical grin coins with a NFT chip that contain swipable grin wallets to sell to Harry. Tom simply generates vouchers wallets using this tool, loading them using the deposit command. 
The resulting voucher wallets will be stored on the NFT chip and optionally printed as QR on the back. Harry digs the coins and thinks Tom is a real wizard.
