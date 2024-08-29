from datetime import datetime
import os
import sys

import drmaa


def _copy_file_to_stdout(file_path):
  with open(file_path, 'rb') as file:
    file_fd = file.fileno()
    stdout_fd = sys.stdout.fileno()
    file_size = os.path.getsize(file_path)
    os.sendfile(stdout_fd, file_fd, 0, file_size)


job_name = sys.argv[1]
native_specs = sys.argv[2]
script_path = sys.argv[3]
script_args = sys.argv[4:]

if not os.path.isfile(script_path):
    print(f"Script \"{script_path}\" does not exist")
    sys.exit(1)

# Create a DRMAA session
with drmaa.Session() as s:
    jt = s.createJobTemplate()
    jt.remoteCommand = os.path.abspath(script_path)
    jt.args = script_args
    jt.joinFiles = True
    jt.nativeSpecification = native_specs
    jt.jobName = job_name

    jt.workingDirectory = os.path.dirname(jt.remoteCommand)

    ts = datetime.now().strftime("%y%m%d_%H%M%S")
    log_path = os.path.join(jt.workingDirectory, f"{jt.jobName}_{ts}.txt")

    jt.outputPath = ":" + log_path

    # jt.outputPath = ':/dev/stdout'
    # jt.errorPath = ':/dev/stderr'

    job_id = s.runJob(jt)
    print(f"Job \"{jt.jobName}\" scheduled with id: {job_id}", flush=True)
    print(f"Log file: {log_path}", flush=True)

    # Wait for the job to complete and get the JobInfo
    job_info = s.wait(job_id, drmaa.Session.TIMEOUT_WAIT_FOREVER)

    _copy_file_to_stdout(log_path)
    os.remove(log_path)

    # Check if the job finished normally and get the exit status
    if job_info.hasExited:
        exit_code = job_info.exitStatus
        print(f"Job {job_id} finished with exit code: {exit_code}")
        sys.exit(exit_code)
    else:
        print(f"Job {job_id} did not exit normally.")
        sys.exit(1)
