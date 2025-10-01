import requests
from enum import Enum, auto
from SshToServer  import SshToServer
import subprocess


server_address = "55.20.33.15"
server_port = 5000


def run_local_command(command):
    try:
        # Run the command
        result = subprocess.run(command, shell = True, check = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        if result.stdout:
            return result.stdout
        else:
            return result.stderr

    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}")
        print(f"Error output: {e.stderr}")


class Menu_Options(Enum):
    get_students_full_list = auto()
    get_specific_student_information  = auto()
    save_a_new_student  = auto()
    change_student_name = auto()
    change_student_age = auto()
    delete_specific_student = auto()
    exit = auto()


def input_parameters_function():
    port = int(input("please enter the port: "))
    host_address = input("please enter host_address: ")
    if host_address == "51.20.55.87":
        restart_container_on_ec2()
        return host_address, port
    else:
        restart_container()
        return host_address, port


def restart_container_on_ec2():
    my_ssh = SshToServer(r"C:\Users\edrik_cgifjkr\Desktop\Course_4_CLOUD_TECHNOLOGY\my_key_pair.pem", "51.20.55.87", "ubuntu")
    my_ssh.result_of_command("sudo python3 server_side_on_ec2.py")


def restart_container():
    docker_container_id = run_local_command(f'docker ps -a -q -f "status=exited"').strip()
    run_local_command(f'docker restart {docker_container_id}')


def print_all_students(all_students):
    print(all_students)


def print_specified_student(student):
    print(f"student_id:     {student["id"]}")
    print(f"student_name:   {student["name"]} ")
    print(f"student_age:    {student["age"]}")


def get_students_full_url():
    return server_url + "/" + students_api


def get_students_full_list(option_value):
    response = requests.get(get_students_full_url())
    if response.status_code == 200:
        students = response.json()["students"]
        if option_value == 1:
            print_all_students(students)
        else:
            return students
    else:
        print(f"error {response.status_code}")
        return None


def get_specific_student_information(option_value) -> dict:
    id_input = int(input("please enter an id to find the specific student: "))
    response = requests.get(get_students_full_url() + "/" + str(id_input))
    if response.status_code == 200:
        student = response.json()
        if option_value == 2:
            print_specified_student(student)
        else:
            return student
    elif response.status_code == 404:
        print(f"error status code id is not in dictionary {response.status_code}")
        return None
    else:
        print(f"error {response.status_code}")
        return None


def save_a_new_student():
    name_student = input("please enter student name: ")
    age_student = int((input("please enter student age: ")))
    data = {
        "name": name_student, "age": age_student
    }
    response = requests.post(get_students_full_url(), json = data)
    if response.status_code == 201:
        students = get_students_full_list(0)
        i = len(students)
        print(f"student created successfully")
        print(f"id: {i}")
        print(f"name: {name_student}")
        print(f"age: {age_student}")
    else:
        print(f"invalid status code error {response.status_code}")        


def change_student_name():
    name = input("enter which name you want to change to: ")
    student = get_specific_student_information(0)
    student["name"] = name
    response = requests.put(get_students_full_url() + "/" + str(student["id"]) , json = student )
    if response.status_code == 200:
        print("students name updated successfully")
    else:
        print(f"error {response.status_code}")


def change_student_age():
    age = int(input("enter which age you want to change to: "))
    student = get_specific_student_information(0)
    student["age"] = age
    response = requests.put(get_students_full_url() + "/" + str(student["id"]), json = student )
    if response.status_code == 200:
        print("students age updated successfully")
    else:
        print(f"error {response.status_code}")


def delete_specific_student():
    id_student = int(input("please enter the student's id you want to delete: "))
    response = requests.delete(get_students_full_url() + "/" + str(id_student))
    if response.status_code == 200:
        print("student deleted successfully ")
    else:
        print(f"error deletion failed {response.status_code}")  

def print_menu():
    for item in Menu_Options:
        print(f"{item.value}. {item.name.replace('_', ' ').title()}")


def run_main():
    while True:
        try:
            print_menu() 
            choice = int(input("please choose an option: "))
            option = Menu_Options(choice)
            if option == Menu_Options.exit:
                if input("Are you sure? (y/n): ").lower() == "y":
                    break
            else:
                func_name = option.name
                func = globals().get(func_name)
                if func and func_name ==  "get_students_full_list":
                    func(1)
                elif func and func_name == "get_specific_student_information":
                    func(2)
                elif func:
                    func()
                else:
                    print("Function not implemented:", func_name)
        except(ValueError) as e:
            print(f"value error {e}")
        except(KeyboardInterrupt) as e:
            print(f"keybord interrupt error {e}")

        
                

server_address, server_port = input_parameters_function()
server_url = f"http://{server_address}:" + str(server_port)
students_api = "students"
run_main()
