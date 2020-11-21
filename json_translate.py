import sys
import json
import gzip
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, help="Specify index file", required=True)
args = parser.parse_args()

index_file = gzip.open(args.file,"r")
previous_occurrence = None

def next_index():
    global previous_occurrence
    l = index_file.readline().strip().split()
    assert(len(l)==2)
    occurrence,index = int(l[0]),int(l[1])
    if previous_occurrence != None:
        assert(occurrence==previous_occurrence+1)
    previous_occurrence = occurrence
    return(index)

item_number = 0
for line in sys.stdin:
    block = json.loads(line)
    for tx in block["tx"]:
        tx["index"] = next_index()
        item_number += 1
        for vin in tx["vin"]:
            if "txid" in vin:
                vin["txid_index"] = next_index()
                item_number += 1
                vin["index"] = next_index()
                item_number += 1
        for vout in tx["vout"]:
            vout["index"] = next_index()
            item_number += 1
            if "addresses" in vout["scriptPubKey"]:
                address_indexes = []
                for address in vout["scriptPubKey"]["addresses"]:
                    address_indexes.append(next_index())
                    item_number += 1
                vout["scriptPubKey"]["address_indexes"] = address_indexes

    sys.stdout.write(json.dumps(block) + "\n")
    sys.stderr.write("block " + str(block["height"]) + ", " + str(item_number) + " items\n")
    sys.stderr.flush()

