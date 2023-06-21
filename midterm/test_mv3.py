#!/usr/bin/python3
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
#takes a list of directories and attempts to create them
def makeDirectories(directories : list):
    for dir in directories:
        os.mkdir(dir)

def createFiles(files: list):
    for file in files:
        with open(file["name"], 'w') as outfile:
            outfile.write(file["content"])
            
        #insert code to add inode numbers.
    return files

def stringToTable(data_string: list):
    lines = data_string.strip().split("\n");
    table = []
    for line in lines:
        table.append(line.strip().split(","))
    return table
    
def unorderedTableCompare(table1:list, table2:list, sortkey):
    print("Comparing output table, with reference table.")
    #check dimensions
    assert len(table1) == len(table2), "Number of rows differ from expected output"
    
    #check headings
    headingA = table1[0].copy()
    headingB = table2[0].copy()
    assert len(headingA) == len(headingB), "Number of headings in tables differ"
    
    headingA.sort()
    headingB.sort()
    for i in range(len(headingA)):
        print("Comparing headings, heading in Table 1 :" + headingA[i] + " heading in Table2:" + headingB[i])
        assert headingA[i] == headingB[i], "Headings do not match"
    
    #compare data rows    
    #reset headings
    headingA = table1[0]
    headingB = table2[0]
    
    #change from rows to dictionary, so column order doesn't matter.
    table1Mod= []
    for i in range(len(table1)-1):
       row = {}
       assert len(table1[i+1]) == len(headingA),"Row " + str(i) + " does not have the correct number of columns in output table"
       for elementIdx in range(len(headingA)):
           row[headingA[elementIdx]] = table1[i+1][elementIdx]
           
       table1Mod.append(row)
    def getKey(row):
        return row[sortkey]
    
    table1Mod.sort(key=getKey)
    
    #change rows for table 1 to dictionary, so column order doesn't matter.
    table2Mod= []
    for i in range(len(table2)-1):
       row = {}
       assert len(table2[i+1]) == len(headingB),"Row " + str(i) + " does not have the correct number of columns in reference table"
       for elementIdx in range(len(headingB)):
           row[headingB[elementIdx]] = table2[i+1][elementIdx]
           
       table2Mod.append(row)
       
    table2Mod.sort(key=getKey)

    print("Sorted student table");
    print(table1Mod)
    print("Sorted reference table");
    print(table2Mod)
    #now actually compare elemnts of the table.
    print("Comparing sorted tables, sorted by column " + sortkey)
    for i in range(len(table1Mod)):
        for key in headingA:
            print("Checking row:" + str(i) + " column: " + key)
            print("Table1 value:" + str(table1Mod[i][key]) + " Table2 value:" + str(table2Mod[i][key]))
            assert table1Mod[i][key] == table2Mod[i][key], "found a value in the table that does not match"            

    return True

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):                
        #Create temp directory
        uidString = str(uuid.uuid4()) 
        cls.test_directory = "/tmp/midtermv3_"+uidString;
        os.mkdir(cls.test_directory)
        
        cls.assignment_scripts = [["scriptmv3_1.sh"],["scriptmv3_2.sh", "example.txt","ref1.csv"]]
                                
        for files in cls.assignment_scripts:
            copyFiles(cls.test_directory, files, True)
        
        os.chdir(cls.test_directory)

    def test_scriptmv3_1(self):
        print("Testing scriptmv3_1")
        student_script = self.assignment_scripts[0][0];
        test_cases = [{"dir_create":["dir1","dir2","dir1/sub1","dir1/sub1/hello","dir1/sub2",
                                     "dir2/sub1","dir2/sub1/hello",
                                     "dir2/sub1/tree","dir2/sub3"],
                        "file_create":[{"name" :"dir1/sub1/file2", "content" :"123"},
                                       {"name" : "dir2/sub1/file3", "content" :"456"},
                                       {"name" : "dir2/sub1/hello/goodbye", "content" : "789"}],
                        "file_link":[],
                       "stdout":["dir2/sub1/tree","dir2/sub3"], 
                       "dir_check":["dir1/sub1/tree","dir1/sub3"],
                       
                       "script_parameters":["/usr/bin/bash",student_script, "dir1", "dir2"]},
                       {"dir_create":["dir3","dir4","dir3/sub1","dir3/sub4","dir3/sub1/hello","dir3/sub2",
                                     "dir4/sub1","dir4/sub1/hello",
                                     "dir4/sub1/tree","dir4/sub3", "dir4/sub3/spider"],
                        "file_create":[{"name" :"dir3/sub1/file2", "content" :"12343"},
                                       {"name" : "dir4/sub1/file3", "content" :"45nn6"},
                                       {"name" : "dir4/sub1/hello/goodbye", "content" : "7dd89"}],
                        "file_link":[],
                       "stdout":["dir4/sub1/tree","dir4/sub3","dir4/sub3/spider"], 
                       "dir_check":["dir3/sub1/tree","dir3/sub3","dir3/sub3/spider"],
                       "script_parameters":["/usr/bin/bash",student_script, "dir3", "dir4"]},
                       ]
        
        for test in test_cases:
            print("Begin Test Case:")
            makeDirectories(test["dir_create"])
            test["file_create"] = createFiles(test["file_create"])            
            cpi = subprocess.run(test["script_parameters"],capture_output=True, text=True);
            print("Standard out:")
            print(cpi.stdout);
            print("Standard error:")
            print(cpi.stderr)
            
            #sort file lists to they are in the same over if they match
            test["stdout"].sort()
            userLines = cpi.stdout.strip().split()
            userLines.sort()
            self.assertTrue(len(userLines) == len(test["stdout"]), \
                   "Number of lines in output line is incorrect. Expected " + \
                   str(len(test["stdout"])) + " You had " + str(len(userLines)))
            #check output
            for i in range(len(userLines)):
                self.assertTrue(userLines[i] == test["stdout"][i], "A line in the output does not match the expected output:\nUser:" + userLines[i] 
                    +"\nExpected:"+test["stdout"][i])
                print("Matched:" +userLines[i])
            #check if directories are created
            for dir_to_check in test["dir_check"]:
                self.assertTrue(os.path.isdir(dir_to_check),dir_to_check + " has not been created")
                print(dir_to_check + " was created")
                
    def test_scriptmv3_2(self):
        student_script = self.assignment_scripts[1][0];
        datafile = self.assignment_scripts[1][1];
        test_cases = [{"script_parameters":["/usr/bin/bash",student_script, datafile],
                       "ref_table":self.assignment_scripts[1][2]}]
        
        for test in test_cases:
            print("Test case begin")
            cpi = subprocess.run(test["script_parameters"], capture_output=True, text=True)
            print("Stdout:")
            print(cpi.stdout)

            
            userTable = stringToTable(cpi.stdout)
            with open(test["ref_table"]) as datafile:
                dataString = datafile.read()
                print("Expected table")
                print(dataString)
                dataTable = stringToTable(dataString)

            print("Stderr:")
            print(cpi.stderr)
            #compare tables for output
            unorderedTableCompare(userTable, dataTable,"pid")
            
        
        
if __name__ == '__main__':
    unittest.main()        