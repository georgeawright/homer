from homer.homer import Homer

path_to_logs = "logs"
path_to_problem = "problems/temperature_problem_1.yaml"

homer = Homer.setup(path_to_logs, path_to_problem)
homer.run()
