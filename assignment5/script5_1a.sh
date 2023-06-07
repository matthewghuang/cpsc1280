filename="$1"

matches=$(grep -E "BELLEVILLE ST,.\*,[0-9]\+,([^0-6]|[[:digit:]][[:digit:]][[:digit:]]\*),[0-9]\+" "$filename")

echo "$matches"