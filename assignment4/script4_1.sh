dirname="$1"

echo "owner,group,filename,permissions"
# user=$(echo owner; find "$dirname" -maxdepth 1 -type f -printf "%u")
user=$(ls -l "$dirname" | tail -n +2 | cut -d " " -f 3)
group=$(ls -l "$dirname" | tail -n +2 | cut -d " " -f 4)
name=$(printf "$dirname/"; ls -l "$dirname" | tail -n +2 | cut -d " " -f 10)
perms=$(ls -l "$dirname" | tail -n +2 | cut -d " " -f 1)

paste_output=$(paste -d"," <(echo "$user") <(echo "$group") <(echo "$name") <(echo "$perms"))
sort <(echo "$paste_output") -t "," -k 3