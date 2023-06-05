import unittest
import uuid
import os
import shutil
import subprocess
import stat
import grp
import time

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
        cls.test_directory = "/tmp/Assignment4_"+uidString;
        os.mkdir(cls.test_directory)
        print("The test directory is :" + cls.test_directory)
        cls.assignment_scripts = [["script4_1.sh"], ["script4_2.sh"], ["script4_3.sh"]]
        cls.auxillary_files = [[],["Air_Traffic.csv"],["start_process_tree.sh"]]
        for files in cls.assignment_scripts:
            copyFiles(cls.test_directory, files, True)
        for files in cls.auxillary_files:
            copyFiles(cls.test_directory, files, False)
        
        os.chdir(cls.test_directory)
    
    @classmethod
    def tearDown(cls):
        #shutil.rmtree(cls.test_directory)
        pass
    
    def setup_script4_1(self, test_dir_name):
        
        other_dirs = [test_dir_name+"/sub1",test_dir_name+"/sub2",test_dir_name+"/aub2" ]
        files = [{"file":test_dir_name+"/sub1/file1", "content":"something"},
                 {"file":test_dir_name+"/sub1/file2", "content":"something"},
                 {"file":test_dir_name+"/aub2/file3", "content":"something"},
                 {"file":test_dir_name+"/sub2/file4", "content":"something"}]
        os.mkdir(test_dir_name)
        for dir in other_dirs:
            os.mkdir(dir)
        for file in files:
            fid = open(file["file"],"w")
            fid.write(file["content"])
            fid.close()
        
        pass
    def test_script4_1(self):
        
        #check if scripts were copied correctly
        for script_file in self.assignment_scripts[0]:
            self.assertTrue(os.path.isfile(script_file),"Script not found")
        script = self.assignment_scripts[0][0]
        #create test
        test_dir_name = "script4_test"
        self.setup_script4_1(test_dir_name)
        
        #run script
        cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[0][0],test_dir_name], capture_output=True, text=True)
        print(cpi.stdout)
        username = os.getlogin() 
        group = os.geteuid()
        groupName = grp.getgrgid(group).gr_name
        expected = ["owner,group,filename,permissions",
                    f"{username},{groupName},script4_test/aub2/file3,-rw-rw-r--",
                    f"{username},{groupName},script4_test/sub1/file1,-rw-rw-r--",
                    f"{username},{groupName},script4_test/sub1/file2,-rw-rw-r--",
                    f"{username},{groupName},script4_test/sub2/file4,-rw-rw-r--"]
        output = cpi.stdout.strip().split("\n")
        self.assertTrue(len(expected) == len(output),"Output not the correct length")
        for line_num in range(len(output)):
            self.assertTrue(output[line_num] == expected[line_num], "output does not match expected output")
    
    def test_script4_2(self):
        
        lines = 7
        filename = "Air_Traffic.csv"
        expected=["Activity Type Code,Cargo Type Code,Activity Period,Operating Airline",
                  "Deplaned,Cargo,200507,ABX Air",
                  "Enplaned,Cargo,200507,ABX Air",
                  "Deplaned,Cargo,200507,Air Canada",
                  "Deplaned,Cargo,200507,ATA Airlines",
                  "Deplaned,Mail,200507,ATA Airlines",
                  "Enplaned,Cargo,200507,ATA Airlines",
                  "Enplaned,Mail,200507,ATA Airlines"]
                      
        for script_file in self.assignment_scripts[1]:
            self.assertTrue(os.path.isfile(script_file),"Script not found")
        for data_file in self.auxillary_files[1]:
            self.assertTrue(os.path.isfile(data_file),"Data file not found")
        
        cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[1][0],filename,str(lines)], capture_output=True, text=True)
        print(cpi.stdout)
        #remove date file, because it's very big.
        os.remove(filename)
        output = cpi.stdout.strip().split("\n")
        self.assertTrue(len(output) == len(expected),"Output length is wrong")
        
        for line_num in range(len(output)):
            self.assertTrue(output[line_num] == expected[line_num], "Output does not match expected output")

    def test_script4_3(self):
        print("testing script4_3.sh")
        for script_file in self.assignment_scripts[2]:
            self.assertTrue(os.path.isfile(script_file),"Script not found")
        for data_file in self.auxillary_files[2]:
            self.assertTrue(os.path.isfile(data_file),"Data file not found")
        
        #1.start background process
        running_script = subprocess.Popen(["bash","start_process_tree.sh"])
        parent_id = running_script.pid
        print("The parent id is:" + str(parent_id))
        #bad practice, but wait for 1 second before checking continueing.
        #otherwise next line runs before all processes are created.

        print("Sleeping for a second")
        time.sleep(1)
        
        #2.get list of backgroun processes
        #capture process id of children process.
        cpi = subprocess.run(["ps","-f","--ppid",str(parent_id)], capture_output=True, text=True)
        block = cpi.stdout.strip().split("\n")
        table = [];
        for line in block[1:]:
            row = line.split()
            id_idx = 1
            cmd_idx = 7
            arg1_idx = 8
            arg2_idx = 9
            if(len(row) > 9):
                row = [row[id_idx], row[cmd_idx]+ " " + row[arg1_idx] + " " + row[arg2_idx]]
                table.append(row);

        #run user script
        cpi = subprocess.run(["bash","script4_3.sh",str(parent_id)], capture_output=True, text=True);
        print("stdout:")
        user_output = cpi.stdout
        print(user_output)
        
        print("stderr:")
        print(cpi.stderr)
        #check if processes have been terminated
        for process in table:
            print("checking process " + process[0])
            output = subprocess.run(["ps", "--pid" , str(process[0]) ], capture_output = True, text = True)
            data = output.stdout.strip().split("\n")            
            self.assertTrue(len(data) == 1,"Process: " + str(process[0]) + " was not terminated for command " + process[1])
        
        #check if parent still exists
        parent = subprocess.run(["ps", "-l","--pid" , str(parent_id) ], capture_output = True, text = True)        
        rows = parent.stdout.strip().split("\n")
        self.assertTrue(len(rows) > 1,"Parent process was terminated")

        #check for zombie state
        data = rows[1].split(" ")
        self.assertTrue(data[1] != "Z", "Parent process was terminated")
        
        
        
        
        #check output
        lineTable = user_output.strip().split("\n")
        userTable = {} #look up table for process ids
        for line in lineTable:
            row = line.split(",")
            userTable[str(row[0]).strip()] = row
        
        for process in table:
            key = str(process[0]).strip() 
            if  key in userTable:
                self.assertTrue(len(userTable[key]) > 1 , "Something is wrong with the format of your table")
                self.assertTrue(userTable[key][1] == process[1],"Commands do not match for process." +
                "Your command: " + userTable[key][1] +". Expected: " + process[1])
            else:
                self.assertTrue(False,"Did not fine process id" + str(process[0]) + " in table for command" + process[1])
        
        
        running_script.kill()
        outs, errs = running_script.communicate()
        time.sleep(1)
if __name__ == '__main__':
    unittest.main()