mkdir -p question1/BTS/COLD_PLAY/Universe
mkdir -p question1/BTS/Idol
mkdir -p question1/BTS/Dna
mkdir -p question1/BTS/Butter
mkdir -p question1/BTS/Dynamite
mkdir -p question1/RED_VELVET/Rythm
mkdir -p question1/RED_VELVET/Psycho
mkdir -p question1/RED_VELVET/Queendom/Pose
mkdir -p question1/TXT
mkdir -p question1/Kep1er

>question1/BTS/file1.txt
>question1/BTS/file2.txt
>question1/BTS/file3.txt
>question1/BTS/COLD_PLAY/Universe/mars.txt
>question1/BTS/COLD_PLAY/Universe/venus.txt
>question1/BTS/COLD_PLAY/Universe/Jupiter.txt
>question1/BTS/Idol/fileA.txt
>question1/BTS/Idol/fileB.txt
>question1/BTS/Idol/fileC.txt
>question1/BTS/Dna/fileA.txt
>question1/BTS/Dna/fileB.txt
>question1/BTS/Dna/fileC.txt
>question1/BTS/Butter/milk.txt
>question1/BTS/Butter/fileC.txt
>question1/BTS/Butter/oil.txt
>question1/BTS/Dynamite/coolshades.txt
>question1/BTS/Dynamite/KingKong.txt
>question1/RED_VELVET/Rythm/hello.txt
>question1/RED_VELVET/Psycho/hello.txt
>question1/RED_VELVET/Queendom/Pose/strike.txt
>question1/TXT/song.txt
>question1/Kep1er/test.txt

chmod ug=rw,o=r question1/BTS/*
chmod a=rx question1/BTS/COLD_PLAY
chmod ug=rwx,o=rx question1/BTS/COLD_PLAY/Universe
chmod ug=rw,o=r question1/BTS/COLD_PLAY/Universe/*
chmod uo=rx,g=rwx question1/BTS/Idol
chmod ug=rw,o=r question1/BTS/Idol/*
chmod u=rwx,go=rx question1/BTS/Dna
chmod ug=rw,o=r question1/BTS/Dna/*
chmod ug=rwx,o=rx question1/BTS/Butter
chmod ug=rw,o=r question1/BTS/Butter/*
chmod ug=rwx,o=rx question1/BTS/Dynamite
chmod ug=rw,o=r question1/BTS/Dynamite/*
chmod ug=rwx,o=rx question1/RED_VELVET
chmod ug=rwx,o=rx question1/RED_VELVET/Rythm
chmod ug=rw,o=r question1/RED_VELVET/Rythm/*
chmod ug=rwx,o=rx question1/RED_VELVET/Psycho
chmod ug=rw,o=r question1/RED_VELVET/Psycho/*
chmod ug=rwx,o-rwx question1/RED_VELVET/Queendom
chmod ug=rwx,o=rx question1/RED_VELVET/Queendom/Pose
chmod ug=rw,o=r question1/RED_VELVET/Queendom/Pose/*
chmod ug=rwx,o=rx question1/TXT
chmod ug=rw,o=r question1/TXT/song.txt
chmod u=rwx,g-rwx,o=rx question1/Kep1er
chmod ug=rw,o=r question1/Kep1er/test.txt