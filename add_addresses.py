import json
import sys
import gc

block_id = None
txid_index = 0
vout_index = 0
item_number = 0
# Blocks
for line in sys.stdin:
    block = json.loads(line)
    
    # Block order ASC assertion
    if block_id is None:
        assert(block["height"] == 0)
    else:
        assert(block["height"] == block_id + 1)
    block_id = block["height"]

    for tx in block["tx"]:
        for vout in tx["vout"]:
            # If pubkey: create "addresses" field and put the pubkey inside
            if vout["scriptPubKey"]["type"] == "pubkey":
                asm = vout["scriptPubKey"]["asm"].split(" ")
                pubKey = asm[0]
                vout["scriptPubKey"]["addresses"] = [pubKey]

            assert("scriptPubKey" in vout)
            assert("asm" in vout["scriptPubKey"])
    
    sys.stdout.write(json.dumps(block) + "\n")
