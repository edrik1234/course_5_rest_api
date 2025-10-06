# Student Management System (Python + REST API + AWS):

A simple client–server project built in Python that manages student data via a REST API.  
The client interacts with a Flask-based server (running locally or on AWS EC2 via Docker) and supports full API'S of rest(get, post(write) , put(replace) , delete)

### 🔹 Features
- get, add, edit, and delete students  
- Connect locally or to a remote EC2 server  
- Restart Docker containers automatically via SSH (Paramiko)  
- Interactive CLI menu

### 🔹 Technologies and libraries
Python | Flask | Requests | Paramiko | Docker | AWS EC2 | ssh | paramiko | enum | subprocess

### 🔹 Files
- `lesson_5_middle_project.py` – main client menu & API logic  
- `SshToServer.py` – SSH helper for EC2  
- `server_side_on_ec2.py` – remote Docker restart script  

