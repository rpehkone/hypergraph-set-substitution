import networkx as nx
import matplotlib.pyplot as plt
import scipy #plot compiler
import re

def plot_graph(edges):
	G = nx.Graph()
	for edge in edges:
		G.add_edges_from([tuple(edge)])
	pos = nx.spring_layout(G, seed=42)
	nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=1000)
	plt.show()

#generate substitution function
def parse_rule(rule_str):
	variables = re.findall(r"\b\w+\b", rule_str)
	input_vars, output_vars = variables[:2], variables[2:]

	# Generate the function code
	# function_code = f"""def substitute({', '.join(input_vars)}):
	function_code =\
	f"""def substitute(x, y, z, w):
			return [({output_vars[0]}, {output_vars[1]}), ({output_vars[2]}, {output_vars[3]})]
	"""
	exec(function_code, globals())

def apply_rule(graph):
	result = []
	max_value = max(max(p) for p in graph) + 1
	for pair in graph:
		result += substitute(pair[0], pair[1], max_value, max_value + 1)
		max_res = max(max(p) for p in result) + 1
		max_value = max(max_res, max_value)
	return result

def evolve_graph(graph, steps, plot):
	for _ in range(steps):
		graph = apply_rule(graph)
		if plot:
			print(graph)
			plot_graph(graph)
	return graph

# https://www.wolframphysics.org/technical-introduction/basic-form-of-models/
# 2.1 Basic structure
# edges = [(1, 2), (1, 3), (2, 3), (4, 1)]
# plot_graph(edges)

# 2.2 Simple graph evolution
parse_rule("{{x, y}} -> {{x, y}, {y, z}}")
graph = [(1, 2)]
evolve_graph(graph, 4, True)
