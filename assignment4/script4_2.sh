csv_file="$1"
rows_to_extract="$2"

data=$(tail "$csv_file" -n +2 | head -n $rows_to_extract)

echo "Activity Type Code,Cargo Type Code,Activity Period,Operating Airline"

activity_types=$(echo "$data" | cut -d , -f 8)
cargo_type_code=$(echo "$data" | cut -d , -f 9)
activity_period=$(echo "$data" | cut -d , -f 1)
operating_airline=$(echo "$data" | cut -d , -f 2)

paste_output=$(paste -d, <(echo "$activity_types") <(echo "$cargo_type_code") <(echo "$activity_period") <(echo "$operating_airline"))
sort <(echo "$paste_output") -t, -k 4 -f