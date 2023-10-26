import os
import shutil

logs = "logs"

log_directories = os.listdir(logs)
for log_dir in log_directories:
    structures = f"{logs}/{log_dir}/structures"
    codelets = f"{logs}/{log_dir}/codelets"
    shutil.rmtree(structures)
    shutil.rmtree(codelets)
