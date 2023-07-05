working_file=/tmp/colondic
echo "" > /tmp/colondic

while read line
do
    [ -z "$line" ] && continue

    c35=$(echo "$line" | cut -c 35)
    c36=$(echo "$line" | cut -c 36)

    # sus entry in the dic 
    if [ "$c36" == " " ] || ([ "$c35" != " " ] && [ "$c36" != " " ])
    then
        words=($line)

        # iterate over indexes 
        for wordindex in "${!words[@]}"
        do
            word=${words[$wordindex]}
            # echo "$word"
            
            [ "$word" == "5%" ] && continue
            word=$(echo "$word" | cut -d\' -f 1 | cut -d, -f 1)
       
            # grep in dict 
            grep -q "^${word}$" "$2"
           
            # if we can't find the word in the dict ist german 
            if [ $? -eq 1 ]
            then
                # echo ""$word" is german in "$line""
                english=$(echo "$line" | cut -d" " -f 1-$wordindex)
                german=$(echo "$line" | cut -d" " -f $(expr $wordindex + 1)-)
                echo "${english}:${german}" >> $working_file
                break
            fi 
        done
    else
        # line not sus split at char 36
        english=$(echo "$line" | cut -c -34)
        german=$(echo "$line" | cut -c 36-)
        echo "${english}:${german}" >> $working_file
    fi
done < $1