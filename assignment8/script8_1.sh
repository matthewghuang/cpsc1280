while read line
do
    # for some reason -z was not working for this so i googled it
    if [[ ! $line =~ [^[:space:]] ]] # https://stackoverflow.com/questions/2578116/how-can-i-test-if-line-is-empty-in-shell-script
    then
        echo ""
        continue
    fi
    
    c35=$(echo "$line" | cut -c 35)
    c36=$(echo "$line" | cut -c 36)
   
    # check for overflow 
    if [ "$c36" == " " ] || ([ "$c35" != " " ] && [ "$c36" != " " ])
    then
        words=($line)
        
        for wordindex in "${!words[@]}"
        do
            word=${words[$wordindex]}
          
            # remove apostrophes and commas so it can be find in the dict 
            word=$(echo "$word" | cut -d\' -f 1 | cut -d, -f 1)
       
            # grep in dict 
            grep -q "^${word}$" "$2"
           
            # if we can't find the word in the dict it's probably german
            if [ $? -eq 1 ]
            then
                # check if the next word is german as well
                nextword=${words[$(expr $wordindex + 1)]}
                grep -q "^${nextword}$" "$2"
               
                # sanity check, if the next word is english continue (for 5% edge case)
                if [ $? -eq 0 ]
                then
                    continue 
                fi
                
                # echo ""$word" is german in "$line""
                english=$(echo "${words[@]}" | cut -d" " -f 1-$wordindex)
                german=$(echo "${words[@]}" | cut -d" " -f $(expr $wordindex + 1)-)
                echo "${english}: ${german}"
                break
            fi 
        done
    else
        english=$(echo "$line" | cut -c -34)
        german=$(echo "$line" | cut -c 36-)
        echo "${english}:${german}"
    fi
done < $1