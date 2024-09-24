# grin-wallet-tool:old_key:<br>
Grin wallet tool is a simple Python script that can be used to generate new or load existing
 1. normal wallets
 2. bip39 password protected wallets
 3. vaucher wallets
 4. brain-bip39 password protected wallets

In addition to generating various wallet types, this tool can be used to *load* or *swipe* grin funds to or from these wallets using the grin-wallet API. This is a tool for advanced users. In particular brain-wallets should not be used if you to not understand the risks. Brain wallets are convenient but considerd insecure since humans are bad at generating entropy. Perhaps first try this tool on testnet to familiarize yourself. 

## How are grin wallets generated?
Grin wallets are Hierarchically Deterministic (HD) wallets that use the BIP32 standard for deriving a master and children keys. The entropy to generate Grin wallet is normally randomly generate and can be represented as 12 word mnemonic (128 bits of entropy) or 12 word mnemonic (256 bits of entropy).  
This tool allows you to use any input string to replace that entropy that is sha256 hashed to create the entropy for a wallet. Any string that a human can think of is much less random than a regular 12 word mnemonic and is ill adviced to be used for main wallets. If you want to read more about Grin HD wallets, read this [[REF](https://anynomouss.github.io/grin-for-muggles/grin_for_muggles_and_aspiring_wizards.html)]


 1. normal wallets: <br>
    *seed_phrase (12-24 words) -> HD wallet*<br>
 2. bip39 password protected wallet: <br>
    *seed_phrase (12-24 words) ->  seed_entropy + password (2000 rounds of additional sha512) -> final entropy-> HD wallet*<br>
 3. vaucher wallets: <br>
    *seed_phrase (15 words) -> HD wallet*<br>
 4. brain-bip39 password protected wallets: <br>
    *password as seed (hex encode then sha256) -> seed_entropy + password (2000 rounds of additional sha512) -> final entropy-> HD wallet*<br>


## EXAMPLE USE CASES

### Why Brain wallets?
Charlie is an advanced crypto enthousias who assumes all his communication is monitored. He want to send a friend Grin via regular messages hidden in plain sight without it being obvious that is sending a transaction or mnemonic.  <br>
**Example 1:** Charlie can send the message "Hi Alice, smile for me:)" via a normal non encrypted messaging tool and she can input that into this tool and swipe the funds to her main wallet, withoutanyone suspecting a transaction took place.
**Example 2:** Charlie met Alice ones and gave her a second secret that is needed to recover funds from any brain wallet message he sends to alice. The second secret is *wimblemimble* and only he and Alice know this. 
Charlie can send the message *"Hi Alice, just grin"* and she can input this together with the BIP39 password *wimblemimble* in the tool to swipe the funds he sends her. Note that this second example is much more secure since it involves two secrets and thanks to 2000 rounds of additional sha512 hardening!
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
