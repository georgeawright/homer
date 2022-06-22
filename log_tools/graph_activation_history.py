import json
import os

log_directory = "logs/1655909355.8252764/structures/structures/SimplexView4/"
field = "activation"
log_files = os.listdir(log_directory)
log_files.sort(key=lambda x: int(x.split(".")[0]))

field_history_x = []
field_history_y = []

for log_file in log_files:
    field_history_x.append(log_file)
    file_name = f"{log_directory}{log_file}"
    with open(file_name, "r") as f:
        file_data = json.load(f)
        field_history_y.append(file_data[field])

print(field_history_x)
print()
print(field_history_y)
