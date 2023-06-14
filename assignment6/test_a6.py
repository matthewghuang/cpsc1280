import unittest
import uuid
import os
import shutil
import subprocess
import stat

def copyFiles(destination, files_list, executable):
    for file in files_list:
        if os.path.isfile(file) : 
            shutil.copy(file,destination)
            if executable:
                new_filename = destination + "/" + file;
                os.system("chmod +x " + new_filename)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):                
        #Create temp directory
        uidString = str(uuid.uuid4()) 
        cls.test_directory = "/tmp/Assignment6_"+uidString;
        os.mkdir(cls.test_directory)
        
        cls.assignment_scripts = [["script6_1.sh"],["script6_2.sh"],["script6_3.sh"]]
        cls.auxillary_files = [["student_in_program.csv","ref6_1.txt","ref6_2.txt"],
                               ["dict_greek.txt","ref6_2a.txt","ref6_2b.txt","ref6_2c.txt","ref6_2d.txt"],
                               ["chambersdict.txt","ref6_3a.txt","ref6_3b.txt","ref6_3c.txt","ref6_3d.txt",
                                "ref6_3e.txt","ref6_3f.txt","ref6_3g.txt","ref6_3h.txt",
                                "ref6_3i.txt","ref6_3j.txt","ref6_3k.txt","ref6_3l.txt",
                                "ref6_3m.txt","ref6_3n.txt"]]
                                
        for files in cls.assignment_scripts:
            copyFiles(cls.test_directory, files, True)
        for files in cls.auxillary_files:
            copyFiles(cls.test_directory, files, False)
        
        os.chdir(cls.test_directory)
        
    def test_script6_1(self):
        print("Testing script6_1")
        tests = [{"year":"2015.2016", "school" : "Summit Learning Centre", "file" : "ref6_1.txt"},
                 {"year":"2014.2015", "school" : "Nelson Elementary", "file" : "ref6_2.txt"}]

        for test in tests:
            cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[0][0],self.auxillary_files[0][0],test["year"],test["school"]], capture_output=True, text=True)
            fid = open(test["file"],"r")
            data = fid.read().strip()
            fid.close()
            self.assertTrue(cpi.stdout.strip() == data, "Output does not match for entry :"+ test["diety"] + "\n Your output: \n" + cpi.stdout.strip() +
            "\nExpected:\n" + data)
            
    def test_script6_2(self):
        print("Testing script6_2")
        tests = [{"diety":"Zeus", "file" : "ref6_2a.txt"},
                 {"diety":"Zethus", "file" : "ref6_2b.txt"},
                 {"diety":"Vidor\.", "file" : "ref6_2c.txt"},
                 {"diety":"Sirens, The", "file" : "ref6_2d.txt"}]

        for test in tests:
            cpi = subprocess.run(["bash", self.assignment_scripts[1][0],self.auxillary_files[1][0],test["diety"]], capture_output=True, text=True)
            fid = open(test["file"],"r")
            data = fid.read().strip()
            fid.close()
            self.assertTrue(cpi.stdout.strip() == data, "Output does not match for entry :"+ test["diety"] + "\n Your output: \n" + cpi.stdout.strip() +
            "\nExpected:\n" + data)

    def test_script6_3(self):
        print("Testing script6_3")
        tests = [{"word":"AIDE-DE-CAMP","file":"ref6_3a.txt"},
                 {"word":"AERIE","file":"ref6_3b.txt"},
                 {"word":"AERIFY","file":"ref6_3c.txt"},
                 {"word":"ALOE","file":"ref6_3d.txt"},
                 {"word":"ALOES","file":"ref6_3e.txt"},
                 {"word":"AZYMOUS","file":"ref6_3f.txt"},
                 {"word":"BAA","file":"ref6_3g.txt"},
                 {"word":"DZIGGETAI","file":"ref6_3h.txt"},
                 {"word":"AHEM","file":"ref6_3i.txt"},
                 {"word":"AIERY","file":"ref6_3j.txt"},
                 {"word":"AHITHOPHEL","file":"ref6_3k.txt"},
                 {"word":"APRIL","file":"ref6_3l.txt"},
                 {"word":"A PRIORI","file":"ref6_3m.txt"},
                 {"word":"DEMESNE","file":"ref6_3n.txt"}]

        for test in tests:
            cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[2][0],self.auxillary_files[2][0],test["word"]], capture_output=True, text=True)
            fid = open(test["file"],"r")
            data = fid.read().strip()
            fid.close()
            self.assertTrue(cpi.stdout.strip() == data, "Output does not match for test case for term " + test["word"] +
            "\nYour output\n" + cpi.stdout.strip() + "\nExpected\n" + data)


if __name__ == '__main__':
    unittest.main()        