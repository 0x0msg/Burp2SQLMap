import subprocess
import os
import time
import sys
def save_request_to_file(request_data, filename="file.txt"):
    with open(filename, "w") as file:
        file.write(request_data)

def run_sqlmap_in_terminal(current_dir, filename="file.txt"):
    try:
        sqlmap_cmd = f'cd "{current_dir}"; sqlmap -r "{filename}"'

        process = subprocess.Popen(sqlmap_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("SQLMap is running...")

        # Read and print the SQLMap output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Wait for the SQLMap process to finish
        process.wait()

        # Print the final process return code
        print("SQLMap process exited with return code:", process.returncode)
    except Exception as e:
        print("Error running SQLMap in a new terminal:", e)

def monitor_sqlmap_progress():
    while True:
        time.sleep(1)
        if os.path.exists("file.txt"):
            with open("file.txt", "r") as file:
                request_data = file.read().strip()
                if request_data:
                    current_dir = sys.argv[1]
                    run_sqlmap_in_terminal(current_dir, "file.txt")
                    break
    print("SQLMap scan completed!")

if __name__ == '__main__':
    # For demonstration purposes, let's read the request from a file.txt
    with open("file.txt", "r") as file:
        request_data = file.read()
    save_request_to_file(request_data)
    monitor_sqlmap_progress()
