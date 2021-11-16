
infile=`ls | grep *.in`
files=6
count=1

echo -e "[" > result.json
for file in `ls`
do
  ext="${file#*.}"
  if [ $ext == "in" ]
  then

    filename="${file%.*}"
    outfile=$filename.out
    for out in `ls`
    do
      if [ $out == $outfile ]
      then

        expected=$out
        actual=Actual$filename.out
        cat $file | python3 ../client.py 8080 > $actual
        diff=`diff $out $actual`
        if [[ $diff == "" ]]
        then

          if [ $count == $files ]
          then
            echo -e "  {\"$filename\": \"Passed\"}" >> result.json
            ((count++))
          else
            echo -e "  {\"$filename\": \"Passed\"}," >> result.json
            ((count++))
          fi
        else
          if [ $count == $files ]
          then
            echo -e "  {\"$filename\": \"Failed\"}" >> result.json
            ((count++))
          else
            echo -e "  {\"$filename\": \"Failed\"}," >> result.json
            ((count++))
          fi

        fi
      fi
    done
  fi

done

echo "]" >> result.json
PID=`ps | grep server.py | grep -v grep | awk '{print $1}'`
kill -9 $PID