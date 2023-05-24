dir=$1
pattern=$2
script=$3
find $dir -type f -executable -name $pattern -exec $script {} \;