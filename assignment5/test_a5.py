import unittest
import uuid
import os
import shutil
import subprocess
import stat

def asciify(input_String):
    output = ""
    for i in range(len(input_String)):
        if (input_String[i] >= "A" and input_String[i] <="Z") or \
           (input_String[i] >= "a" and input_String[i] <="z") or \
           (input_String[i] >= "0" and input_String[i] <="9") or \
           input_String[i] == " " or input_String[i] == "." or input_String[i] == "," :
           output += input_String[i]
    return output
def remove_quotes(old_string):
    return old_string.replace("\"","")
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
        cls.test_directory = "/tmp/Assignment5_"+uidString;
        os.mkdir(cls.test_directory)
        
        cls.assignment_scripts = [["script5_1a.sh","script5_1b.sh","script5_1c.sh","script5_1d.sh"], 
                                  ["script5_2.sh"], ["script5_3.sh"],["script5_4.sh"]]
        cls.auxillary_files = [["Tree_Species_mod.csv"],[],["wines_SPA.csv"]]
        for files in cls.assignment_scripts:
            copyFiles(cls.test_directory, files, True)
        for files in cls.auxillary_files:
            copyFiles(cls.test_directory, files, False)
        
        os.chdir(cls.test_directory)
        master_data_file = cls.auxillary_files[0][0]
        ref_file = open(master_data_file,"r")
        
        cls.header = ref_file.readline()
        cls.data = ref_file.readlines()
        ref_file.close()
        cls.headings = cls.header.strip().split(",")
        
        #Create look up table from row to headings.
        cls.idx_dict ={}
        for i in range(0,len(cls.headings)) :
            cls.idx_dict.update({cls.headings[i] : i})

            
    def test_script5_1a(self):
        print("running script5_1a")
        self.assertTrue(os.path.isfile(self.assignment_scripts[0][0]), "Script not found")
        self.assertTrue(os.path.isfile(self.auxillary_files[0][0]), "Datafile not found")
        os.path.isfile(self.auxillary_files[0][0])
        
        street_key = "Street"
        script_conditions = {street_key:"BELLEVILLE ST","Height":7 }
        print("opening file")
        
        #perform search on master data
        species_idx = self.idx_dict[street_key]
        height_idx = self.idx_dict["Height"]
        
        row_count = 0;
        for row in self.data:
            fields = row.split(",")
            try:
                f_height = float(fields[height_idx].strip())
            except:
                f_height = float('-inf')
            if fields[species_idx].strip() == script_conditions[street_key] and \
               f_height >= script_conditions["Height"] :
                row_count += 1
        print("Total rows : " + str(row_count))
        
        #run student script, number of rows should equal to row_count
        cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[0][0],
                                                  self.auxillary_files[0][0]], 
                             timeout=10,capture_output=True, text=True)
        print("stderr:")
        print(cpi.stderr)
        student_output = cpi.stdout.strip().split("\n")
        
        #check headings
        s_heading = student_output[0].split(",")
        if len(s_heading) == len(self.headings) :
            for i in range(len(s_heading)):
                if asciify(s_heading[i].strip()) != asciify(self.headings[i].strip()) :
                    print("Your Headings:" + student_output[0])
                    print("My Headings:" + self.header)
                    print("First difference at column " + str(i))
                    self.assertTrue(False,"Error in headings")        
                    
        else:
            print("Your Headings:" + student_output[0])
            print("My Headings:" + self.header)
            self.assertTrue(False,"Number of headings do not match")
        print("Headings match")
       
        count = 0
        for row in student_output[1:]:
            fields = row.split(",")
            try:
                f_height = float(fields[height_idx].strip())
            except:
                f_height = float('-inf')
            if not (fields[species_idx].strip() == script_conditions[street_key] and \
               f_height >= script_conditions["Height"]) :
                self.assertTrue(False,"Found row that does not match question requirements\n" + row)
            else:
                count += 1
        self.assertTrue(row_count == count,"Number of rows found different than expected")                
        print("Test passed")
        return
    
    def test_script5_1b(self):
        print("running script5_1b")
        self.assertTrue(os.path.isfile(self.assignment_scripts[0][1]), "Script not found")
        self.assertTrue(os.path.isfile(self.auxillary_files[0][0]), "Datafile not found")
        self.master_data_file = self.auxillary_files[0][0]
        
        species_key = "Species"
        category_key = "TreeCategory"
        tests = [{"Species":"Abies grandis","TreeCategory":"Park Trees","file":"ref5_1b1.csv"},
                {"Species":"Cedrus deodara","TreeCategory":"Park Frontage Trees","file":"ref5_1b2.csv"}]
                

        #perform search on master data
        species_idx = self.idx_dict[species_key]
        category_idx = self.idx_dict[category_key]
        
        
        row_counts = []
        for test in tests:
            count = 0
            for row in self.data:
                fields = row.split(",")
                if fields[species_idx].strip() == test[species_key] and \
                    test[category_key] == fields[category_idx] :
                    count += 1
            row_counts.append(count)
        print(row_counts)
        
        for i in range(len(tests)):
            test = tests[i]
            print(f"Test case {test[species_key]} and {test[category_key]} ")
            #run student script, number of rows should equal to row_count
            cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[0][1], self.auxillary_files[0][0], \
                                 test[species_key],test[category_key]], timeout=10,capture_output=True, text=True)
            print("stderr:")
            print(cpi.stderr)
            student_output = cpi.stdout.strip().split("\n")
        
            #check headings
            s_heading = student_output[0].split(",")
            if len(s_heading) == len(self.headings) :
                for j in range(len(s_heading)):
                    if asciify(s_heading[j].strip()) != asciify(self.headings[j].strip()) :
                        print("Your Headings:" + student_output[0])
                        print("My Headings:" + self.header)
                        print("First difference at column " + str(i))
                        self.assertTrue(False,"Error in headings")        
                    
            else:
                print("Your Headings:" + student_output[0])
                print("My Headings:" + self.header)
                self.assertTrue(False,"Number of headings do not match")
            print("Headings match")
       
            
            for row in student_output[1:]:
                fields = row.split(",")
                if not (fields[species_idx].strip() == test[species_key] and \
                    test[category_key] == fields[category_idx]) :
                    print("Row with incorrect column values:")
                    print("First incorrect row")
                    print(row)
                    self.assertTrue(False,"Row that does not match search condition found")

            self.assertTrue(row_counts[i] == (len(student_output)-1),"Incorrect number of rows found")    
            
        print("Test passed")
        return        
    def test_script5_1c(self):
        print("running script5_1c")
        self.assertTrue(os.path.isfile(self.assignment_scripts[0][2]), "Script not found")
        self.assertTrue(os.path.isfile(self.auxillary_files[0][0]), "Datafile not found")
        
        
        species_key = "Species"
        tests = [{"species1":"Wildlife snag","species2":"Pinus nigra"},
                 {"species1":"Aesculus carnea","species2":"Pinus sylvestris"}]
        
        
        #perform search on master data
        species_idx = self.idx_dict[species_key]
        row_counts = []
        for test in tests:
            count = 0
            for row in self.data:
                fields = row.split(",")
                if fields[species_idx].strip() == test["species1"] or \
                   fields[species_idx].strip() == test["species2"] :
                    count += 1
            row_counts.append(count)
        print(row_counts)
        
        for i in range(len(tests)):
            test = tests[i]
            print(f"Test case {test['species1']} and {test['species2']} ")
            #run student script, number of rows should equal to row_count
            cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[0][2], self.auxillary_files[0][0], \
                                 test["species1"],test["species2"]], timeout=10,capture_output=True, text=True)
            print("stderr:")
            print(cpi.stderr)
            student_output = cpi.stdout.strip().split("\n")
            for row in student_output:
                fields = row.split(",")
                if not (fields[species_idx] == test["species1"] or
                        fields[species_idx] == test["species2"] ) :
                    print("Row with incorrect column values:")
                    print("First incorrect row")
                    print(row)
                    self.assertTrue(False,"Row that does not match search condition found")

            self.assertTrue(len(student_output) == row_counts[i], "Number of rows do not match")
        print("Test passed")

    def test_script5_1d(self):
        print("running script5_1d") 
        self.assertTrue(os.path.isfile(self.assignment_scripts[0][3]), "Script not found")
        self.assertTrue(os.path.isfile(self.auxillary_files[0][0]), "Datafile not found")
        
        height_key = "Height"
        tests = [{"min":15,"max":30}]
        
        #perform search on master data
        height_idx = self.idx_dict[height_key]
        print("height index " +  str(height_idx))
        row_counts = []
        for test in tests:
            count = 0
            for row in self.data:
                fields = row.split(",")
                try:
                    t_height=float(fields[height_idx].strip())
                except:
                    t_height = float("-inf")
                if t_height <= test["max"] and \
                   t_height >= test["min"] :
                    count += 1
            row_counts.append(count)
        print(row_counts)
        
        for i in range(len(tests)):
            test = tests[i]
            print(f"Test case min = {test['min']} and max = {test['max']} ")
            #run student script, number of rows should equal to row_count
            cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[0][3], self.auxillary_files[0][0]], timeout=10,capture_output=True, text=True)
            print("stderr:")
            print(cpi.stderr)
            student_output = cpi.stdout.strip().split("\n")
            print(len(student_output))
            for row in student_output:
                fields = row.split(",")
                try:
                    t_height=float(fields[hight_idx].strip())
                except:
                    t_height = float("-inf")
                if t_height <= test["max"] and \
                   t_height >= test["min"] :
                    print("Row with incorrect column values:")
                    print("First incorrect row")
                    print(row)
                    self.assertTrue(False,"Row that does not match search condition found")

            self.assertTrue(len(student_output) == row_counts[i], "Number of rows do not match")
        print("Test passed")
        
    def create_data5_2(self, test_dir):
        os.mkdir(test_dir+"/sub1")
        os.mkdir(test_dir+"/sub2")
        os.mkdir(test_dir+"/sub3")
        files = [{"file":test_dir+"/sub1/file1", "content":"Snake Eyes\n"},
                 {"file":test_dir+"/sub2/file2", "content":"Speed"},
                 {"file":test_dir+"/sub2/file3", "content":"Running Snake echo \n"},
                 {"file":test_dir+"/sub1/non", "content":"Running Snake echo \n"}]
        
        print("files")
        print(files)
        for file in files:
            fid = open(file["file"],"w")
            fid.write(file["content"])
            fid.close()                 
        pass
    
    def test_script5_2(self):
        print("Testing script5_2")
        self.assertTrue(os.path.isfile(self.assignment_scripts[1][0]), "Script not found")
        test_dir = "test5_2"
        os.mkdir(test_dir)
        self.create_data5_2(test_dir)
        
        expected = ["test5_2/sub1/file1", "test5_2/sub2/file3"]
        expected.sort()
        file_pat = "file?"
        regex_pat = "Sn.k[ea]"
        print(f" filename pattern {file_pat} regex pattern {regex_pat}")
        print(f"expected results:")
        print(expected)
        cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[1][0],test_dir,file_pat, regex_pat], capture_output=True, text=True)
        print("script stderr")
        print(cpi.stderr)
        print("script stdout")
        print(cpi.stdout)
        lines = cpi.stdout.strip().split("\n")
        lines.sort()
        self.assertTrue(len(lines) == len(expected),"Incorrect output length")
        for i in range(len(lines)):
            self.assertTrue(lines[i]==expected[i],"Unexpected output you had\n" + lines[i] + "\nI expected \n" + expected[i])
    
    def test_script5_3(self):
        print("Testing script5_3")
        self.assertTrue(os.path.isfile(self.assignment_scripts[2][0]), "Script not found")
        self.assertTrue(os.path.isfile(self.auxillary_files[2][0]), "Datafile not found")
        
        tests = [{"winery" :"Emilio Moro"},
                 {"winery" :"Bodegas Mauro"}]
        winery_idx = 0
        rating_idx = 3
        year_idx = 2
        
        ref_file = open(self.auxillary_files[2][0],"r")
        heading = ref_file.readline()
        data = ref_file.readlines()
        ref_file.close()
    
        results = []
        for test in tests:
            record = {}
            ratings = []
            for row in data:
                fields = row.split(",")
                if remove_quotes(fields[winery_idx]) == test["winery"]:
                    ratings.append(float(fields[rating_idx]))
            
            record.update({"max" : max(ratings)})
            max_rating = max(ratings)
            
            years = []
            for row in data:
                fields = row.split(",")
                
                if remove_quotes(fields[winery_idx]) == test["winery"] and \
                    fields[rating_idx] == str(max_rating):
                    years.append(int(remove_quotes(fields[year_idx])))
            years.sort(reverse=True)
            year_list = list(set(years))
            year_list.sort(reverse=True)
            
            record.update({"years" : year_list})
            results.append(record)
        print(results)    
        
        #run student code
        for k in range(len(tests)):
            test = tests[k]
            print(f"Test case winery = {test['winery']}")
            print(f"Expected max = {results[k]['max']}")
            
            cpi = cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[2][0],
                                        self.auxillary_files[2][0],test["winery"]], timeout=5,capture_output=True, text=True)
            print("stderr")
            print(cpi.stderr)
            student_data = cpi.stdout.strip().split("\n")
            print(student_data[0])
            self.assertTrue(float(student_data[0])==results[k]["max"], "Maximum rating is incorrect")
            self.assertTrue(len(student_data[1:])==len(results[k]["years"]), "Different number of years found")
            years = results[k]["years"]
            for l in range(len(years)):
                self.assertTrue(years[l] == float(student_data[l+1]),"Incorect year found:" + str(student_data[l+1]))
            
        print("Test Passed")
            
    def create5_4_data(self, filename):
        fid = open(filename,"w")
        fid.write("Dog Cat Mouse Dog\nHorse Tree Cat \n Dog Dog Dog Dig\n")
        fid.close()
        
    def test_script5_4(self):
        print("Testing script5_4")
        self.assertTrue(os.path.isfile(self.assignment_scripts[3][0]), "Script not found")
        filename = "test5_4.txt"
        self.create5_4_data(filename)
        pat ="D.g"
        expected = 6
        print(f"Pattern = {pat} expected count = {expected}")
        cpi = subprocess.run(["/usr/bin/bash", self.assignment_scripts[3][0],filename,pat], capture_output=True, text=True)
        self.assertTrue(cpi.stdout.strip() == str(expected),"Incorrect answer")
        print("Test Passed")
if __name__ == '__main__':
    unittest.main()        