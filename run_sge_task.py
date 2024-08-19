import os
import sys

import drmaa

job_name = sys.argv[1]
script_path = sys.argv[2]
script_args = sys.argv[3:]

if not os.path.isfile(script_path):
    print(f"Script \"{script_path}\" does not exist")
    sys.exit(1)

# Create a DRMAA session
with drmaa.Session() as s:
    jt = s.createJobTemplate()
    jt.remoteCommand = os.path.abspath(script_path)
    jt.args = script_args
    jt.joinFiles = True
    jt.nativeSpecification = "-l tmem=4G -l h_rt=19:00:00 -R y -l gpu=True -pe gpu 2 -l tscratch=50G"
    jt.jobName = job_name

    jt.workingDirectory = os.path.dirname(jt.remoteCommand)
    #jt.outputPath = ":" + os.path.join(jt.workingDirectory, f"{jt.jobName}.txt")

    # jt.outputPath = ':/dev/stdout'
    # jt.errorPath = ':/dev/stderr'

    job_id = s.runJob(jt)
    print(f"job \"{jt.jobName}\" scheduled with id: {job_id}", flush=True)

    # Wait for the job to complete and get the JobInfo
    job_info = s.wait(job_id, drmaa.Session.TIMEOUT_WAIT_FOREVER)

    # Check if the job finished normally and get the exit status
    if job_info.hasExited:
        exit_code = job_info.exitStatus
        print(f"Job {job_id} finished with exit code: {exit_code}")
        sys.exit(exit_code)
    else:
        print(f"Job {job_id} did not exit normally.")
        sys.exit(1)
