from functions import get_files_info
from functions import get_file_content
from functions import write_file
from functions import run_file

def main():
    working_directory = "calculator"
    directory = "."
    # print(write_file.write_file(working_directory,"garbage.txt","Hello World"))
    # print(run_file.run_file(working_directory,"tests.py"))
    print(run_file.run_file(working_directory,"main.py",["14 + 8"]))
    # print(write_file.write_file(working_directory,"/tmp/temp.txt","Hello World this is garbage"))


    

main()