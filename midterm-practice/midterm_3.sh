cleaned=$(cat "$1" | sed -nE "/^[A-Za-z ]{34} /p")
extracted=$(echo "$cleaned" | sed -nE "/^$2/p" | sed -E "/^$2.*( ).*[A-Za-z].*( |\t){2,}/d")
definitions=$(echo "$extracted" | sed -nE "s/(^$2)[ ]+(.*)/\2/p")

echo "$definitions"