import os

log_directories = os.listdir("logs/")
log_directories.sort()
log_directory = "logs/" + log_directories[-1]

log_directory_contents = os.listdir(log_directory)
activity_logs = [
    file_name
    for file_name in log_directory_contents
    if "activity" in file_name and ".log" in file_name
]

with open(f"{log_directory}/focus_history.txt", "w") as history:
    for i in range(len(activity_logs)):
        file_name = "activity" + str(i + 1) + ".log"
        with open(f"{log_directory}/{file_name}", "r") as activity:
            time = ""
            previous_focus = ""
            focus = ""
            activity_lines = activity.readlines()
            for line in activity_lines:
                if line[0:6] == "Time: ":
                    time = line.split()[1]
                if line[0:7] == "Focus: ":
                    previous_focus = focus
                    focus = line[7:]
                    if focus != previous_focus:
                        history.write(f"{time} {focus}\n")
