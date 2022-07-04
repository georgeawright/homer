import graphviz

dot_file_path = "logs/1656929153.5948377/structures/concepts_and_frames/18000.dot"
f = open(dot_file_path, "r")
dot_code = f.read()
src = graphviz.Source(dot_code)
src.render()
f.close()
