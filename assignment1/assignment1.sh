dirs=("./A1/classical" "./A1/classical/bach" "./A1/classical/bach/Air on the G String" 
                       "./A1/classical/bach/Inventions and Sinfonias" "./A1/classical/bach/Mass in B minor" "./A1/classical/Beethoven" 
                       "./A1/classical/Beethoven/Piano Sonata No. 8" "./A1/classical/Beethoven/Symphony No.5" 
                       "./A1/classical/Beethoven/Symphony No.9" "./A1/classical/Chopin" "./A1/classical/Chopin/Etudes" 
                       "./A1/classical/Chopin/Minute Waltz" "./A1/classical/Chopin/Nocturne in E-flat major" 
                       "./A1/classical/Chopin/Preludes" "./A1/classical/Liszt" "./A1/classical/Liszt/Les preludes" 
                       "./A1/classical/Tchaikovsky" "./A1/classical/Vivaldi" "./A1/classical/Vivaldi/Four Seasons" 
                       "./A1/classical/Vivaldi/Violin concertos" "./A1/kpop" "./A1/kpop/AOA" "./A1/kpop/AOA/Excuse me" "./A1/kpop/AOA/Like a Cat" 
                       "./A1/kpop/AOA/Miniskirt" "./A1/kpop/BTS" 
                       "./A1/kpop/BTS/Dynamite" "./A1/kpop/BTS/fake love" 
                       "./A1/kpop/BTS/mic drop" "./A1/kpop/BTS/Permission to dance" 
                       "./A1/kpop/GirlsGeneration" "./A1/kpop/GirlsGeneration/Forever 1" "./A1/kpop/GirlsGeneration/Gee" 
                       "./A1/kpop/GirlsGeneration/Into the Future" "./A1/kpop/GirlsGeneration/oh!" 
                       "./A1/kpop/In the morning" "./A1/kpop/itzy" "./A1/kpop/LOCO" "./A1/kpop/newJeans" "./A1/kpop/Not-Shy" 
                       "./A1/kpop/purplekiss" "./A1/kpop/redvelvet" "./A1/kpop/redvelvet/Red Flavor" "./A1/kpop/redvelvet/Russian Roulette" 
                       "./A1/kpop/sneakers" "./A1/kpop/Twice" 
                       "./A1/kpop/Twice/Alcohol-Free" "./A1/kpop/Twice/Feel Special" "./A1/kpop/Twice/Set Me Free" 
                       "./A1/kpop/Twice/Talk that Talk" "./A1/kpop/Twice/TT" "./A1/rap" 
                       "./A1/rap/Anarchy" "./A1/rap/Bang Yong-guk" "./A1/rap/dok2" "./A1/rap/Hannya" "./A1/rap/rm" 
                       "./A1/rap/rm/life goes on" "./A1/rap/rm/love u hate u" 
                       "./A1/rap/so-yeon" "./A1/rap/so-yeon/Latata" "./A1/rap/so-yeon/My Bag" "./A1/rap/so-yeon/Tomboy" "./A1/rap/suga")

for str in ${dirs[@]}; do
    mkdir -p '$str'
done