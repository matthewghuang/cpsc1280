find "$1" -name "$2" -printf "%i %p\n" -maxdepth 0  | tee "$3"