import networkx as nx
import matplotlib.pyplot as plt
import scipy #plot compiler
import re

def plot_graph(edges):
	G = nx.Graph()
	for edge in edges:
		G.add_edges_from([tuple(edge)])
	# wolfram uses a proprietary force-directed graph layout algorithm
	pos = nx.spring_layout(G, seed=42)
	# pos = nx.spectral_layout(G)
	nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, node_shape='o', alpha=0.8)
	nx.draw_networkx_labels(G, pos, labels={node: node for node in G.nodes()}, font_size=10)
	nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True, arrowstyle="-|>", arrowsize=20, width=1.0, edge_color='black', alpha=1)
	plt.show()

def _generate_substitution_function(outvars, invars):
	# code = f"""def substitute({', '.join(input_vars)}):
	code = "def substitute(x, y, z, w):\n"

	if invars[0] == invars[1]:
		code +=	"	if x != y:\n"+\
				"		return [(x, y)]\n"
		for i, v in enumerate(outvars):
			if v == "y":
				outvars[i] = 'z'
		#makes more sense
		# outvars[1] = chr(ord(outvars[1]) + 1)
		# parse_rule("{{x, x}} -> {{z, z}, {z, z}, {x, z}}")

	code +=	"	return ["
	i = 0
	while i < len(outvars):
			code += "(" + outvars[i] + ", " + outvars[i + 1] + ")"
			i += 2
			if i < len(outvars):
				code += ", "
	code += "]"
	print(code)
	exec(code, globals())

def parse_rule(rule_str):
	variables = re.findall(r"\b\w+\b", rule_str)
	input_vars, output_vars = variables[:2], variables[2:]
	_generate_substitution_function(output_vars, input_vars)

def apply_rule(graph):
	result = []
	max_value = max(max(p) for p in graph)
	for pair in graph:
		result += substitute(pair[0], pair[1], max_value + 1, max_value + 2)
		max_res = max(max(p) for p in result)
		max_value = max(max_res, max_value)
	return result

def evolve_graph(graph, steps, plot):
	for _ in range(steps):
		graph = apply_rule(graph)
		if (len(graph) <= 15):
			print(graph)
		if plot:
			plot_graph(graph)
	return graph

# https://www.wolframphysics.org/technical-introduction/basic-form-of-models/
# 2.1 Basic structure
# graph = [(1, 2), (1, 3), (2, 3), (4, 1)]
# plot_graph(graph)

# 2.2 First Example of a Rule
# parse_rule("{{x, y}} -> {{x, y}, {y, z}}")
# evolve_graph([(1, 2)], 4, True)

# 2.3 A Slightly Different Rule
# parse_rule("{{x, y}} -> {{z, y}, {y, x}}")
# evolve_graph([(1, 2)], 4, True)

# 2.4 Self-Loops
# parse_rule("{{x, y}} -> {{y, z}, {z, x}}")
# evolve_graph([(1, 1)], 6, True)

# 2.4.2 Binary tree
# parse_rule("{{x, x}} -> {{y, y}, {y, y}, {x, y}}")
# evolve_graph([(1, 1)], 6, True)

# 2.5 Multiedges
# parse_rule("{{x, y}} -> {{x, z}, {x, z}, {y, z}}")
# evolve_graph([(1, 1)], 6, True)

# 2.5.2 multiedge after one step, but then destroys it
# parse_rule("{{x, y}} -> {{x, z}, {z, w}, {y, z}}")
# evolve_graph([(1, 1)], 4, True)



# 3.6
#TODO: convert input {x, x, y} to {x, x}, {x, y}
