by_action=$(cat "$1" | sed -n -E "/$2/p")
by_ip=$(echo "$by_action" | sed -n -E "/$3/p") 
by_year=$(echo "$by_ip" | sed -n -E "/\[.*2022.*\]/p")
may_filter=$(echo "$by_year" | sed -n -E "/\[((1[5-9])|(2[0-9])|(3[0-1]))\/May.*\]/p")
jun_filter=$(echo "$by_year" | sed -n -E "/\[([0-9]|(1[0-9]?)|(2[0-1]))\/Jun.*\]/p")
format_output=$(echo -e "$may_filter\n$jun_filter" | sed -n -E "s/(.*) HOME - \[([0-9]+\/[A-Za-z]+\/[0-9]+):.*(\".*\") ([0-9]+)(.*)/\1,\2,\4,\3/p")

echo "User Address,Date,Return Code,Action"
echo "$format_output"