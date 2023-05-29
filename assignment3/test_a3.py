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
        cls.assignment_scripts = [["script3_1.sh"], ["script3_2.sh"], ["script3_3.sh"],["script3_4.sh"]]
        
        #Create temp directory
        uidString = str(uuid.uuid4()) 
        cls.test_directory = "/tmp/Assignment3_"+uidString;
        os.mkdir(cls.test_directory)
        
        for file_lists in cls.assignment_scripts:
            for file in file_lists :
                #copy files, and set permissions
                if os.path.isfile(file) : 
                    shutil.copy(file,cls.test_directory)
                    new_filename = cls.test_directory + "/" + file;
                    os.system("chmod +x " + new_filename)
                else:
                    print("Setup failed, file " + file + "Does not exist")
                    assert("Setup failed, file " + file + "Does not exist")
        
        os.chdir(cls.test_directory) 
        
        
        
    @classmethod
    def tearDown(cls):
        #shutil.rmtree(cls.test_directory)
        pass

    def test_script3_1(self):
        print("Output for script3_1.sh")
        self.assertTrue(os.path.isfile(self.assignment_scripts[0][0]),"script3_1.sh file not found")
        
        test_dir = "p1_test"
        #create testing directory structure
        os.mkdir(test_dir)
        dirs = ["sub1", "sub2"]
        filelist = [["fan.txt", "fun.txt", "fern.txt","fit.txt"],["non.txt", "fin.txt", "fuun.txt"]]
        filelist2 = ["fan.txt", "fun.txt", "fern.txt","fit.txt"];
        for f in filelist2:
            cmd = "echo test > " + test_dir + "/" + f
            os.system(cmd)
            
        for i in range(len(dirs)) :
            if not dirs[i] == "." :
                os.mkdir(test_dir+"/"+dirs[i])
            for file in filelist[i]:
                cmd = "echo test > " + test_dir+"/"+dirs[i]+"/"+file
                os.system(cmd)
        
        output_filename = "out3_1.txt"
        pattern = "f*n.txt"
        
        cpi = subprocess.run([self.shell, self.assignment_scripts[0][0],test_dir, pattern, output_filename], capture_output=True, text=True)
        
        #check output file has been created
        self.assertTrue(os.path.isfile(output_filename),"Output file was not created by the script")
        #read the output file
        expectedFiles = ["p1_test/sub1/fan.txt","p1_test/sub1/fun.txt","p1_test/sub1/fern.txt", "p1_test/sub2/fin.txt", "p1_test/sub2/fuun.txt"]
        
        file_handle = open(output_filename,"r")
        text = file_handle.read();
        
        lines  = text.strip().split("\n")
        self.assertTrue(len(lines) == len(expectedFiles),"Incorrect number of files found")
        
        for line in lines:
            pair = line.split();
            idx = expectedFiles.index(pair[1])
            
            inum1 = os.stat(pair[1]).st_ino
            self.assertTrue(str(inum1) == pair[0],"one or more inode numbers are incorrect")
        
        print("End of run")
        file_handle.close()
        
    def test_script3_2(self):
        print("Output for script3_2.sh")
        self.assertTrue(os.path.isfile(self.assignment_scripts[1][0]),"script3_2.sh file not found")
        
        test_dir = "p2_test"
        os.mkdir(test_dir)
        
        dirs = ["sub1", "sub2"]
        filelist = [["fan.txt", "fun.txt", "fern.txt","fit.txt"],["non.txt", "fin.txt", "fuun.txt"]]
        
        for i in range(len(dirs)) :
            os.mkdir(test_dir+"/"+dirs[i])
            for file in filelist[i]:
                cmd = "echo test > " + test_dir+"/"+dirs[i]+"/"+file
                os.system(cmd)
        
        #add executable permissions to test file
        cmd1 = "chmod +x "+test_dir+"/sub1/fit.txt";
        cmd2 = "chmod +x "+test_dir+"/sub2/non.txt";
        os.system(cmd1)
        os.system(cmd2)
        
        pat = "*.txt"
        
        expectedFiles = [test_dir+"/sub1/fit.txt", test_dir+"/sub2/non.txt"]
        
        #create script
        script = "echo test $1"
        filename = "p2.sh"
        file = open(filename,"wt")
        file.write(script)
        file.close()
        os.system("chmod +x p2.sh")
        print("Running Script 2")
        
        cpi = subprocess.run([self.shell, self.assignment_scripts[1][0],test_dir, pat, filename], capture_output=True, text=True)
        lines = cpi.stdout.strip().split("\n")
        
        #check the results
        self.assertTrue(len(lines) == len(expectedFiles), "Incorrect number of results")
        
        for line in lines:
            tokens = line.split()
            self.assertTrue(tokens[0] == "test", "user script did not run")
            idx = expectedFiles.index(tokens[1])  #will assert, if not in list
            expectedFiles.remove(tokens[1])
        print("End of run")
        
    def test_script3_3(self):
        print("Output for script3_3.sh")
        self.assertTrue(os.path.isfile(self.assignment_scripts[2][0]),"script3_3.sh file not found")
        
        names = ["Brett", "Eddy"]
        answers = ["Brett is a member of twoset $(violin), he has perfect pitch. Brett has been playing the 'violin' for 10* years[ref 123], and he's known to have \"Perfect Pitch\",{ref 345}. Brett has played in Australian Orechestra*.",
                   "Eddy is a member of twoset $(violin), he has perfect pitch. Eddy has been playing the 'violin' for 10* years[ref 123], and he's known to have \"Perfect Pitch\",{ref 345}. Eddy has played in Australian Orechestra*."]
        for i in range(2):
            cpi = subprocess.run([self.shell, self.assignment_scripts[2][0],names[i]], capture_output=True, text=True)
            text = cpi.stdout.strip();
            
            print("Output for ./script3_3.sh " + names[i]);
            print(text)
            self.assertTrue(text == answers[i].strip(), "Incorrect output")
        print("End of run")
    def test_script3_4(self):
        print("Output for script3_4.sh")
        self.assertTrue(os.path.isfile(self.assignment_scripts[2][0]),"script3_4.sh file not found")
        
        test_dir = "p4_test"
        os.mkdir(test_dir)
        
        dirs = ["sub1", "sub2","sub1/inner1.txt"]
        filelist = [["fan.txt", "fun.txt", "fern.txt","fit.txt","sim.rat"],
                    ["nsn.txt", "fin.txt", "fuun.txt","lack.txt","txt.tack"],
                    ["outer.sub","inner.dub"]]

        for i in range(len(dirs)) :
            os.mkdir(test_dir+"/"+dirs[i])
            for file in filelist[i]:
                cmd = "echo test > " + test_dir+"/"+dirs[i]+"/"+file
                os.system(cmd)

        pat = "*.txt"
        expectedFiles = ["p4_test/sub1/fan.txt","p4_test/sub1/fun.txt","p4_test/sub1/fern.txt","p4_test/sub1/fit.txt",
                         "p4_test/sub2/nsn.txt","p4_test/sub2/fin.txt","p4_test/sub2/fuun.txt","p4_test/sub2/lack.txt"] 
        cpi = subprocess.run([self.shell, self.assignment_scripts[3][0],test_dir, pat], capture_output=True, text=True)
        print("stderr:\n" + cpi.stderr)
        print("stdout:\n" + cpi.stdout)
        
        lines = cpi.stdout.strip().split("\n")
        n = 3
        try:
            for line in lines[0:-1]:
                files = line.strip().split(" ")
                self.assertTrue(len(files) == n, "One of the printed lines does not contain 3 filenames")
                for file in files:
                    expectedFiles.remove(file.strip())
            lastlinefiles = lines[-1].strip().split(" ")
            for file in lastlinefiles:
                expectedFiles.remove(file)
        except:
            self.assertTrue(False,"File found that does not match pattern")
        self.assertTrue(len(expectedFiles) == 0, "Not all the expected files for the pattern were found")
        print("Done!")
        
        
if __name__ == '__main__':
    unittest.main()