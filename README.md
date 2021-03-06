# blockchain-indexor

## Prerequisites to avoid sort errors
```sh
#.bashrc
export LC_ALL=C
```

## step 0
Uncompress data THEN you can tac and gzip again
```sh
$ nohup gunzip blockchain.DSC.gz 2> gunzip.err &
$ nohup tac blockchain.DSC | gzip -c > blockchain.ASC.gz &
```

## step1
```sh
$ zcat example.ASC.gz | python3 add_addresses.py | python3 make_list.py 2> step1.err | gzip -c > step1.gz
```

## step2
```sh
$ zcat example.ASC.gz | python3 add_addresses.py | python3 get_addresses.py 2> step2.err | sort -T. -S10g --parallel=24 -k1,1 -k2,2n | awk 'BEGIN{old="none";}{if ($1!=old) print $0; old=$1;}' | sort -T. -S 10g --parallel=24 -nk2,2 | awk '{print "-1",$1,NR-1;}' | gzip -c > step2.gz
```

## step3
```sh
$ zcat -c step1.gz step2.gz | sort -S 10g -T . -r -k2,3 --parallel=24 | gzip -c > step3.gz
```

## step4
```sh
$ zcat step3.gz | python3 list_translate.py 2> step4.err | gzip -c > step4.gz
```

## step5
```sh
$ zcat step4.gz | sort -S 10g -T . -nk1,1 --parallel=24 | gzip -c > step5.gz
```

## step6
```sh
$ zcat example.ASC.gz | python3 add_addresses.py | python3 json_translate.py --file step5.gz 2> step6.err | gzip -c > step6.gz
```
