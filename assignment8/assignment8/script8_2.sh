while read site
do
    echo "E-mails for ${site}:"
    
    hach_tee_em_el=$(curl -s "$site")
    
    echo "$hach_tee_em_el" | sed -n "s/.*>\(.*@langara\.ca\).*/\1/gp"
    echo ""
done < "$1"