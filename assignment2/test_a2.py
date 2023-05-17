import unittest
import uuid
import os
import shutil
import subprocess
import stat

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shell = "/usr/bin/bash"
        if not os.path.isfile(cls.shell):
            print("/usr/bin/bash not found, trying /bin/zsh for macs")
            cls.shell = "/bin/zsh"
    
        cls.test_files = [{"filename":"script2_1a.sh", "mode":"744"}, 
                          {"filename":"script2_1b.sh", "mode":"744"},
                          {"filename":"reference.txt", "mode":"664"},
                          {"filename":"part2_prep.sh", "mode":"744"},
                          {"filename":"script2_2a.sh", "mode":"744"},
                          {"filename":"script2_2b.sh", "mode":"744"},
                          {"filename":"script2_2c.sh", "mode":"744"}]
                          
        
        #Create working directory to execute script in 
        #a clean environment
        uidString = str(uuid.uuid4()) 
        cls.test_directory = "/tmp/Assignment2_"+uidString;
        os.mkdir(cls.test_directory)        
        print("Test ran in : " + cls.test_directory)
        for file in cls.test_files:
            if os.path.isfile(file["filename"]) :
                shutil.copy(file["filename"],cls.test_directory)
                new_filename = cls.test_directory + "/" + file["filename"];
                os.system("chmod "+ file["mode"]+" "+ new_filename)
            else:
                print("Setup failed, file " + file["filename"] + "Does not exist")
                assert("Setup failed, file " + file["filename"] + "Does not exist")
        os.chdir(cls.test_directory)        

    @classmethod
    def tearDown(cls):
        #uncomment in production
        #shutil.rmtree(cls.test_directory)
        pass
        
    def test_script2_1a(self):
        print("Output for Part 1")
        scriptIdx = 0
        items = [ ["question1/BTS","drwxrwxr-x"],
                        ["question1/BTS/file1.txt","-rw-rw-r--"],
                        ["question1/BTS/file2.txt","-rw-rw-r--"],
                        ["question1/BTS/file3.txt","-rw-rw-r--"],
                        ["question1/BTS/COLD_PLAY","dr-xr-xr-x"],
                        ["question1/BTS/COLD_PLAY/Universe","drwxrwxr-x"],
                        ["question1/BTS/COLD_PLAY/Universe/mars.txt","-rw-rw-r--"],
                        ["question1/BTS/COLD_PLAY/Universe/venus.txt","-rw-rw-r--"],
                        ["question1/BTS/COLD_PLAY/Universe/Jupiter.txt","-rw-rw-r--"],
                        ["question1/BTS/Idol","dr-xrwxr-x"],
                        ["question1/BTS/Idol/fileA.txt","-rw-rw-r--"],
                        ["question1/BTS/Idol/fileB.txt","-rw-rw-r--"],
                        ["question1/BTS/Idol/fileC.txt","-rw-rw-r--"],
                        ["question1/BTS/Dna","drwxr-xr-x"],
                        ["question1/BTS/Dna/fileA.txt","-rw-rw-r--"],
                        ["question1/BTS/Dna/fileB.txt","-rw-rw-r--"],
                        ["question1/BTS/Dna/fileC.txt","-rw-rw-r--"],
                        ["question1/BTS/Butter","drwxrwxr-x"],
                        ["question1/BTS/Butter/milk.txt","-rw-rw-r--"],
                        ["question1/BTS/Butter/fileC.txt","-rw-rw-r--"],
                        ["question1/BTS/Butter/oil.txt","-rw-rw-r--"],
                        ["question1/BTS/Dynamite","drwxrwxr-x"],
                        ["question1/BTS/Dynamite/coolshades.txt","-rw-rw-r--"],
                        ["question1/BTS/Dynamite/KingKong.txt","-rw-rw-r--"],
                        ["question1/RED_VELVET","drwxrwxr-x"],
                        ["question1/RED_VELVET/Rythm","drwxrwxr-x"],
                        ["question1/RED_VELVET/Rythm/hello.txt","-rw-rw-r--"],
                        ["question1/RED_VELVET/Psycho","drwxrwxr-x"],
                        ["question1/RED_VELVET/Psycho/hello.txt","-rw-rw-r--"],
                        ["question1/RED_VELVET/Queendom","drwxrwx---"],
                        ["question1/RED_VELVET/Queendom/Pose","drwxrwxr-x"],
                        ["question1/RED_VELVET/Queendom/Pose/strike.txt","-rw-rw-r--"],
                        ["question1/TXT","drwxrwxr-x"],
                        ["question1/TXT/song.txt","-rw-rw-r--"],
                        ["question1/Kep1er","drwx---r-x"],
                        ["question1/Kep1er/test.txt","-rw-rw-r--"]]
        self.assertTrue(os.path.isfile(self.test_files[scriptIdx]["filename"]),"Testing directory is not a directory or does not exist")
        cpi = subprocess.run([self.shell, self.test_files[scriptIdx]["filename"]], capture_output=True, text=True)
        print(cpi.stdout)
        
        #check if files and directories exist with the correct permissions
        for item in items:
            try:
                status = os.stat(item[0])
            except:    
                assert  False, "Script did not create all required directories or files"
            perms = stat.filemode(status.st_mode)
            assert perms == item[1], "Permission for " + item[0] + " not correct. perm =" + item[1] + ":" + perms
        file_pairs = [
            ["question1/BTS/Dna/fileA.txt", "question1/BTS/Dynamite/coolshades.txt"],
            ["question1/BTS/Dna/fileB.txt", "question1/RED_VELVET/Rythm/hello.txt"],
            ["question1/BTS/Dna/fileC.txt", "question1/RED_VELVET/Psycho/hello.txt"],
            ["question1/BTS/Dna/fileA.txt", "question1/BTS/Butter/oil.txt"],
            ["question1/BTS/COLD_PLAY/Universe/Jupiter.txt", "question1/BTS/Butter/milk.txt"]]
        
        #check if files are linked correctly
        for files in file_pairs:
            inum1 = os.stat(files[0]).st_ino
            inum2 = os.stat(files[1]).st_ino
            assert inum1 == inum2, "hard link for " + files[0] +" and " + files[1] + " do not match"
        
        file_sets = [["question1/BTS/Dna/fileA.txt", "question1/BTS/Dynamite/coolshades.txt","question1/BTS/Butter/oil.txt"],
                     ["question1/BTS/Dna/fileB.txt", "question1/RED_VELVET/Rythm/hello.txt"],
                     ["question1/BTS/Dna/fileC.txt", "question1/RED_VELVET/Psycho/hello.txt"],
                     ["question1/BTS/COLD_PLAY/Universe/Jupiter.txt", "question1/BTS/Butter/milk.txt"]]
        
        #check if files are linked incorrectly
        for fileset1 in file_sets:
            for fileset2 in file_sets:
                file1 = fileset1[0];
                file2 = fileset2[0];
                if file1 != file2:
                    inum1 = os.stat(file1).st_ino
                    inum2 = os.stat(file2).st_ino                    
                    assert inum1 != inum2, "hard link for " + file1 +" and " + file2 + " match but should not match"

                    
        
    def test_script2_2a(self):
        print("Output for Part 2a")
        scriptIdx = 4
        self.assertTrue(os.path.isfile(self.test_files[3]["filename"]),"Prep script not found")
        self.assertTrue(os.path.isfile(self.test_files[scriptIdx]["filename"]),"script2_2a.sh not found")
        subprocess.run([self.shell, self.test_files[3]["filename"]])
        cpi = subprocess.run([self.shell, self.test_files[scriptIdx]["filename"]], capture_output=True, text=True)
        files = cpi.stdout.strip().split("\n")
        files.sort()
        print(cpi.stdout)
        expected_files = [
            "q2_p2/location1/meat.txt",
            "q2_p2/location1/ommeui.txt",
            "q2_p2/location1/ommeuf.txt",
            "q2_p2/location1/oooome.txt",
            "q2_p2/location1/oooo.me",
            "q2_p2/location1/zebra/zero.tmef"]
        expected_files.sort()
        assert len(expected_files) == len(files), "File list is not correct"
        for i in range(len(expected_files)):
            assert expected_files[i] == files[i], "Files list is not correct"
        
    def test_script2_2b(self):
        print("Output for Part 2b")
        scriptIdx = 5
        self.assertTrue(os.path.isfile(self.test_files[3]["filename"]),"Prep script not found")
        self.assertTrue(os.path.isfile(self.test_files[scriptIdx]["filename"]),"script2_2b.sh not found")
        subprocess.run([self.shell, self.test_files[3]["filename"]])
        cpi = subprocess.run([self.shell, self.test_files[scriptIdx]["filename"]], capture_output=True, text=True)
        files = cpi.stdout.strip().split("\n")
        files.sort()
        expected_files = ["q2_p2/location1/oooo.mi",
                          "q2_p2/location2/orchard/zello/noether.ditto"]
        expected_files.sort()
        print(cpi.stdout)
        assert len(expected_files) == len(files), "File list is not correct"
        for i in range(len(expected_files)):
            assert expected_files[i] == files[i], "Files list is not correct"
        for file in expected_files:
            status = os.stat(file)
            assert status.st_mode & 0o002 == 0, "Write permission found on one of the listed files"
    
    def test_script2_2c(self):
        print("Output for Part 2c")
        scriptIdx = 6
        self.assertTrue(os.path.isfile(self.test_files[3]["filename"]),"Prep script not found")
        self.assertTrue(os.path.isfile(self.test_files[scriptIdx]["filename"]),"script2_2c.sh not found")
        subprocess.run([self.shell, self.test_files[3]["filename"]])
        cpi = subprocess.run([self.shell, self.test_files[scriptIdx]["filename"]], capture_output=True, text=True)
        files = cpi.stdout.strip().split("\n")
        files.sort()
        print(cpi.stdout)
        expected_files = [  "q2_p2/location1/zebra/zero.tmef",
                            "q2_p2/location1/zebra/zero",
                            "q2_p2/location1/zebra/zero.txt",
                            "q2_p2/location1/zany/topaz.txt",
                            "q2_p2/location2/orchard/zello/noether.ditto"]
        expected_files.sort()
        assert len(expected_files) == len(files), "File list is not correct"
        for i in range(len(expected_files)):
            assert expected_files[i] == files[i], "Files list is not correct"
        
if __name__ == '__main__':
    unittest.main()