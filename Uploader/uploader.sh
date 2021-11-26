i=1
e=68

file=data_

i=1
while [ $i -lt $e ]; do 
    realfile=$file$i.json && i=$[$i+1];
    curl -H "Content-Type: application/json" -d "$(< $realfile )" -X POST http://localhost:4000/api/data
done