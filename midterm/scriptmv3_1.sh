find "$1" -mindepth 1 -name "*" -type d | cut -d/ -f 2- > /tmp/sub1
find "$2" -mindepth 1 -name "*" -type d | cut -d/ -f 2- > /tmp/sub2
diffed=$(diff /tmp/sub1 /tmp/sub2 | sed -nE "/>/p" | sed -E "s/> (.*)/\1/")
echo "$diffed" | xargs -i echo "$2/{}"
echo "$diffed" | xargs  -i mkdir -p "$1/{}"
