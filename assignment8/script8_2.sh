while read site
do
    echo "E-mails for ${site}:"
    
    hach_tee_em_el=$(curl -s "$site")
    
    echo "$hach_tee_em_el" | sed -n -r "s/.*\b([a-zA-Z0-9_\.-]+@([a-zA-Z0-9\.-]+\.[a-zA-Z\.]{2,6})).*/\1/p"
    echo ""
done < "$1"