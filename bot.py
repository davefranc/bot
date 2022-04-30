from tinyman.v1.client import TinymanMainnetClient
from algosdk import mnemonic
import time
import sys
asset = int(sys.argv[1]) # asa id
amnts = int(sys.argv[2]) # amount of algo to spend

ADDRESS="your wallet"
MNEMONIC="your passphrase"
# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
account = {
    'address': '',
    'private_key': mnemonic.to_private_key(''),
}





client = TinymanMainnetClient(user_address=account['address'])


# Fetch our two assets of interest
TINYUSDC = client.fetch_asset(asset)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(TINYUSDC, ALGO)


# Always True
if 1 > 0:
    quote = pool.fetch_fixed_input_swap_bot(ALGO(1_000_000*amnts), slippage=1.00)

    # Prepare a transaction group
    transaction_group = pool.prepare_swap_transactions_from_quote(quote)
    # Sign the group with our key
    transaction_group.sign_with_private_key(account['address'], account['private_key'])
    # Submit transactions to the network and wait for confirmation
    result = client.submit(transaction_group, wait=True)
    print(f'Swapping {quote.amount_in} to {quote.amount_out}')

    # Check if any excess remaining after the swap
    excess = pool.fetch_excess_amounts()
    if TINYUSDC in excess:
        amount = excess[TINYUSDC]
        print(f'Excess: {amount}')
        # Leave the above print so other script knows hoe many tokens we bought
        if 2 > 1:
            transaction_group = pool.prepare_redeem_transactions(amount)
            transaction_group.sign_with_private_key(account['address'], account['private_key'])
            result = client.submit(transaction_group, wait=False)
