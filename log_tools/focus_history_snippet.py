import os

log_directories = os.listdir("logs/")
log_directories.sort()
print(log_directories)
log_directory = log_directories[-1]

with open(f"logs/{log_directory}/activity.log", "r") as activity, open(
    f"logs/{log_directory}/focus_history.txt", "w"
) as history:
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
