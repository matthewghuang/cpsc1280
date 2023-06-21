sorted=$(sort "$1" | sort -t: -k 1,2)
echo "$sorted" | sed -nE "s/^(.*):.*:.*/\1/p" | uniq > /tmp/pid
echo "$sorted" | sed -nE "s/.*space:(.*)/\1/p" > /tmp/space
echo "$sorted" | sed -nE "s/.*time:(.*)/\1/p" > /tmp/time
echo "$sorted" | sed -nE "s/.*total:(.*)/\1/p" > /tmp/total

echo "pid,space,time,total"
paste /tmp/pid /tmp/space /tmp/time /tmp/total -d,