parent_id="$1"

ps_output=$(ps --ppid "$parent_id" --format pid,cmd --no-headers)
ppid=$(echo "$ps_output" | cut -d" " -f 2)
rest=$(echo "$ps_output" | cut -d" " -f 3-)

pasted=$(paste -d , <(echo "$ppid") <(echo "$rest"))
echo "$pasted"

echo "$ppid" | xargs kill -s SIGINT