from homer.homer import Homer

path_to_logs = "logs"
path_to_problem = "problems/temperature_problem_1.yaml"

homer = Homer.setup(path_to_logs, path_to_problem)

homer.run()

homer.logger.graph_concepts(
    [
        "label",
        "label-evaluation",
        "group",
        "group-evaluation",
        "group-selection",
        "group-label",
        "group-label-evaluation",
        "group-label-selection",
        "correspondence",
        "correspondence-evaluation",
        "correspondence-label",
        "correspondence-selection",
        "textlet",
    ],
    "perceptlet_types",
)

# homer.logger.graph_codelets("codelets_family_tree")
homer.logger.graph_coderack("coderack_population")
homer.logger.graph_concepts(["satisfaction"], "satisfaction_concept")

homer.logger.graph_processes("processes")
homer.logger.graph_codelet_types("codelets_by_type")
