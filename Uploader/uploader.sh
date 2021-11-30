i=0
e=108

file=data/aerodata_flughafen_amsterdam_

i=1
while [ $i -lt $e ]; do 
    realfile=$file$i.json && i=$[$i+1];
    curl -H "Content-Type: application/json" -d "$(< $realfile )" -X POST http://localhost:4000/api/data
    echo $realfile uploaded.
done