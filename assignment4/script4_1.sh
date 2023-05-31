dirname="$1"

# echo "owner,group,filename,permissions"
user=$(echo owner; find "$dirname" -maxdepth 1 -type f -printf "%u")
group=$(echo group; find "$dirname" -maxdepth 1 -type f -printf "%g")
name=$(echo filename; find "$dirname" -maxdepth 1 -type f -printf "%p")
perms=$(echo permissions; find "$dirname" -maxdepth 1 -type f -printf "%M")

paste_output=$(paste -d"," <(echo "$user") <(echo "$group") <(echo "$name") <(echo "$perms"))
sort <(echo "$paste_output") -t "," -k 3