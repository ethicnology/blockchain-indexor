# blockchain-indexor

## Prerequisites to avoid sort errors
export LC_ALL=C

## step 0
$ zcat fichier.gz | tac | gzip -c > fichier.ASC.gz

## step1
$ zcat demo.ASC.gz | python3 add_addresses.py | python3 make_list.py 2> step1.err | gzip -c > step1.gz


## step2
$ zcat demo.ASC.gz | python3 add_addresses.py | python3 get_addresses.py 2> step2.err | sort -T. -S10g --parallel=24 -k1,1 -k2,2n | awk 'BEGIN{old="none";}{if ($1!=old) print $0; old=$1;}' | sort -T. -S10g --parallel=24 -nk2,2 | awk '{print "-",$1,NR-1;}' | gzip -c > step2.gz


## step3
zcat -c step1.gz step2.gz | sort -S 200g -T . -r -k2,3 --parallel=24 | cut -d" " -f1,3 | gzip -c > step3.gz

## step4
zcat step3.gz | python3 list_translate.py 2> step4.err | gzip -c > step4.gz

## step5
zcat step4.gz | sort -S 200g -T . -nk1,1 --parallel=24 | gzip -c > step5.gz

## step6
zcat fichier.ASC.gz | python3 json_translate.py 2> step6.err | gzip -c > fichier.ASC.indexed.gz
