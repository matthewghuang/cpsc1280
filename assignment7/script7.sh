# update
tail -n +2 "$2" > /tmp/update_data
# make a temporary working file
cat "$1" > /tmp/workingass

while read update_row
do
	machine_id_to_update=$(echo "$update_row" | sed -ne "s/\(.*\),\(.*\),\(.*\)/\1/p")
	item_to_update=$(echo "$update_row" | sed -ne "s/\(.*\),\(.*\),\(.*\)/\2/p")
	operation_to_update=$(echo "$update_row" | sed -ne "s/\(.*\),\(.*\),\(.*\)/\3/p")

	headings=($(head -n 1 /tmp/workingass | sed -e "s/,/ /g"))
	
	row=$(grep $machine_id_to_update /tmp/workingass)

	# find/make the appropriate data row to update
	if [ $? -eq 1 ] # row doesn't exist
	then
    	# copy an existing row
	    row=$(tail -n +2 /tmp/workingass | head -n 1)
    	cells=($(echo "$row" | sed -e "s/,/ /g"))
    	
    	index=0
    
        # set all cells to 0	
    	for cell in "${cells[@]}"
    	do
            cells[$index]=0
            
            index=$(expr $index + 1)
        done
       
        # set the machine id cell so we can identify it 
    	cells[0]=$machine_id_to_update
	else # row does exist
    	cells=($(echo "$row" | sed -e "s/,/ /g"))
	fi
	
	index=0

	for cell in "${cells[@]}"
	do
		heading=${headings[index]}
		
		if [ "$heading" == "$item_to_update" ]
		then
	        echo "$operation_to_update" | grep -Eq "^[+-]"
	        
	        if [ $? -eq 0 ] # is an add or sub operation
	        then
	            cells[index]=$(echo "$cell $operation_to_update" | bc)
	        else # is a set operation
	            cells[index]=$operation_to_update
	        fi
	    elif [ "$heading" == "\"Last_Update\"" ]
	    then
	        # update the date
	        cells[index]=$(date +%F)
		fi

		index=$(expr $index + 1)
	done
	
	
    # delete the existing row and append the updated one to the tmp working file
    sed -i -e /$machine_id_to_update/d /tmp/workingass
    # turn array into comma separated row
    echo "${cells[@]}" | sed -e "s/ /,/g" >> /tmp/workingass
done < /tmp/update_data

head -n 1 /tmp/workingass && tail -n +2 /tmp/workingass | sort
