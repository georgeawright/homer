import graphviz

# dot_file_path = "logs/structures/spaces/ContextualSpace28/5000.dot"
dot_file_path = "logs/structures/concepts_and_frames/5000.dot"
# dot_file_path = "logs/structures/views/SimplexView8/4521.dot"
f = open(dot_file_path, "r")
dot_code = f.read()
src = graphviz.Source(dot_code)
src.render()
f.close()
