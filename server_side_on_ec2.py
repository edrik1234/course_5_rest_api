import subprocess


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




docker_container_id = run_local_command(f'docker ps -a -q -f "status=exited"').strip()
run_local_command(f'docker restart {docker_container_id}')

