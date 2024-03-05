#!!!!RUN ALL SCRIPTS AND DELETE PREVIOUS DATA!!!!
import subprocess

from library import clean_path, get_file_paths


def run_js_scripts(file_paths):
    processes = []
    total_proccesses = len(file_paths)
    for path in file_paths:
        # Form the command to execute 'node' with the file path
        command = ['node', path]
        
        # Spawn a new process for each command
        process = subprocess.Popen(command)
        
        # Append the process to the list of processes
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.wait()
        
    print("All processes have completed.")
    return 0

paths = get_file_paths('scripts/rugby_union')
clean_path('data/rugby_union')
run_js_scripts(paths)
