import subprocess
import sys
import time
from multiprocessing import Manager, Process

from library import get_file_paths


# run JS script
def start_process(shared_data, path):
    cmd = ['node', path]

    # Start the process
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    while True:
        # Read one line of output
        line = process.stdout.readline()
        if not line:
            break  # No more output
        # Decode line (from bytes to string) and process it
        step_number = line.decode('utf-8').strip()
        # with shared_data.get_lock():  # Ensure thread-safe operations on shared data
        #I think since we are only writing to each index from the single porcess we can raw dog it.
        shared_data[path] = step_number

    # Wait for the process to finish and get the exit code
    shared_data[path] = "complete"
    process.wait()


if __name__ == '__main__':

    with Manager() as manager:
        shared_data = manager.dict()
        processes = []
        # if len(sys.argv) > 1:
        #     arg1 = sys.argv[1]
        # else:
        #     raise "need to pass an argument to run the scraping process. this argument is the name of the event type"
        # paths = get_file_paths(f'scripts/{arg1}')
        paths = ['pipescript1.js', 'pipescript2.js', 'pipescript3.js']

        totat_progress = 100 * len(paths)

        # Start multiple processes
        for path in paths:
            p = Process(target=start_process, args=(shared_data, path))
            processes.append(p)
            p.start()

        all_done = False
        while not all_done:
            time.sleep(0.2)

            # Check if all processes have completed
            all_done = all(shared_data.get(path) == "complete" for path in paths)


            # Log the progress from the shared dictionary
            prog = 0
            for process_id, progress in shared_data.items():
                if progress == "complete":
                    prog += 100
                else:
                    prog += int(progress)
            #the calling proccess can consume this to track progress
            print(f"{int(prog/totat_progress * 100)}")
            #without this output is buffered and not consumed until the end. No idea why i need it here adn not above
            sys.stdout.flush()

        # Wait for all processes to finish
        for p in processes:
            p.join()

        # At this point, all processes have finished
        print("done")


