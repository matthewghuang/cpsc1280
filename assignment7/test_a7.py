import unittest
import uuid
import os
import shutil
import subprocess
import stat
import datetime

def copyFiles(destination, files_list, executable=False):
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
        cls.test_directory = "/tmp/Assignment7_"+uidString;
        os.mkdir(cls.test_directory)
        
        cls.assignment_scripts = [["script7.sh"]]
        cls.auxillary_files = []
        for files in cls.assignment_scripts:
            copyFiles(cls.test_directory, files, True)
        for files in cls.auxillary_files:
            copyFiles(cls.test_directory, files, False)
                                
        os.chdir(cls.test_directory)

    def create_base_file(self,filename):
        data = "\"MachineID\",\"ItemA\",\"ItemB\",\"ItemC\",\"ItemD\",\"Last_Update\"\n" + "\"MA001\",100,200,100,100,2020-01-01\n"+"\"MA002\",300,400,100,200,2020-01-01\n"+"\"MA003\",200,250,500,100,2020-01-01\n"
        
        fid = open(filename,"w")
        fid.write(data)
        fid.close()

    def create_update_file(self,filename):
        data = "\"MachineID\",\"Item\",\"Operation\"\n" + \
        "\"MA004\",\"ItemA\",500\n"+ \
               "\"MA001\",\"ItemB\",+200\n"+ \
               "\"MA003\",\"ItemA\",-200\n" + \
               "\"MA004\",\"ItemA\",-200\n" + \
               "\"MA003\",\"ItemA\",+5\n" +  \
               "\"MA003\",\"ItemC\",66\n" + \
               "\"MA005\",\"ItemD\",100\n" 
        fid = open(filename,"w")
        fid.write(data)
        fid.close()        
        
    def test_script7(self):
        print("Test script7")
        filename_data = "data.file"
        filename_update = "update.file"
        self.create_base_file(filename_data)
        self.create_update_file(filename_update)
        cpi = subprocess.run(["/usr/bin/bash",self.assignment_scripts[0][0], filename_data,filename_update],capture_output=True, text=True)
        data = cpi.stdout.strip();
        print("STDERR:")
        print(cpi.stderr)
        print("Changing error")
        print("Your Output")
        print(data)
        dataTable = data.split("\n")
        today=datetime.datetime.now()
        date_str=today.strftime("%Y-%m-%d")
        expected_output= "\"MachineID\",\"ItemA\",\"ItemB\",\"ItemC\",\"ItemD\",\"Last_Update\"\n" + \
        f"\"MA001\",100,400,100,100,{date_str}\n" + \
        "\"MA002\",300,400,100,200,2020-01-01\n" + \
        f"\"MA003\",5,250,66,100,{date_str}\n" + \
        f"\"MA004\",300,0,0,0,{date_str}\n" + \
        f"\"MA005\",0,0,0,100,{date_str}\n" 
        expectedTable = expected_output.strip().split("\n")
        print("Expected table")
        print(expected_output)
        
        self.assertTrue(len(expectedTable) == len(dataTable), "Number of rows produced different than expected")
        
        for rowIdx in range(0,len(expectedTable)):
            row_data = dataTable[rowIdx].strip().split(",")
            row_expected = expectedTable[rowIdx].strip().split(",")
            self.assertTrue(len(row_data) == len(row_expected), "Number of fields in row do not match")
            for colIdx in range(0,len(row_expected)):
                self.assertTrue(row_data[colIdx].strip() == row_expected[colIdx].strip(), 
                "Data for row " + str(rowIdx) + " col " + str(colIdx) + " is incorrect")
        

if __name__ == '__main__':
    unittest.main()        