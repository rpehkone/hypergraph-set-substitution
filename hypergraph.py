import networkx as nx
import matplotlib.pyplot as plt
import time
import re

def plot_graph(edges):
	G = nx.Graph()
	for edge in edges:
		G.add_edges_from([tuple(edge)])
	if len(edges) < 40:
		# wolfram uses a proprietary force-directed graph layout algorithm
		# pos = nx.spectral_layout(G)
		pos = nx.spring_layout(G, seed=42)
		nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, node_shape='o', alpha=0.8)
		nx.draw_networkx_labels(G, pos, labels={node: node for node in G.nodes()}, font_size=10)
		nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True, arrowstyle="-|>", arrowsize=20, width=1.0, edge_color='black', alpha=1)
	else:
		iterations = max(1, int(80 - 0.05 * len(edges)))
		print(f"iterations = {iterations}")
		pos = nx.spring_layout(G, iterations=iterations)
		nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1.0, edge_color='black', alpha=1)
	plt.draw()

def _generate_substitution_function(outvars, invars):
	# code = f"""def substitute({', '.join(input_vars)}):
	code = "def substitute(x, y, z, w):\n"

	if invars[0] == invars[1]:
		code +=	"	if x != y:\n"+\
				"		return [(x, y)]\n"
		for i, v in enumerate(outvars):
			if v == "y":
				outvars[i] = 'z'
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

rule  = ""
def parse_rule():
	variables = re.findall(r"\b\w+\b", rule)
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

def on_window_close(event):
	exit(0)
fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_window_close)

auto_step = True
current_step = 0
def on_key_press(event):
	global current_step
	global auto_step

	if event.key == "right":
		current_step += 1
		auto_step = False
	elif event.key == "left":
		current_step -= 1
		auto_step = False
	elif event.key == "escape":
		exit(0)
	if current_step < 0:
		current_step = 0
plt.gcf().canvas.mpl_connect("key_press_event", on_key_press)

def evolve_graph(initial_graph, max_steps):
	parse_rule()

	global current_step
	global auto_step
	start_time = time.time()
	prev_solution = -1
	graph = []

	while True:
		if auto_step:
			if time.time() - start_time >= 2:
				start_time = time.time()
				current_step += 1
				if current_step == max_steps:
					auto_step = False
		if prev_solution != current_step:
			graph = initial_graph
			prev_solution = current_step
			for _ in range(current_step):
				graph = apply_rule(graph)
			plt.clf()
			plot_graph(graph)
		plt.title(f"{rule}\nSteps: {current_step}")
		plt.pause(0.1)

# https://www.wolframphysics.org/technical-introduction/basic-form-of-models/
# 2.1 Basic structure
# graph = [(1, 2), (1, 3), (2, 3), (4, 1)]
# plot_graph(graph)
# plt.show()

# 2.2 First Example of a Rule
# rule = "{{x, y}} -> {{x, y}, {y, z}}"
# evolve_graph([(1, 2)], 4)

# 2.3 A Slightly Different Rule
# rule = "{{x, y}} -> {{z, y}, {y, x}}"
# evolve_graph([(1, 2)], 5)

# 2.4 Self-Loops
# rule = "{{x, y}} -> {{y, z}, {z, x}}"
# evolve_graph([(1, 1)], 6)

# 2.4.2 Binary tree
# rule = "{{x, x}} -> {{y, y}, {y, y}, {x, y}}"
# evolve_graph([(1, 1)], 6)

# 2.5 Multiedges
# rule = "{{x, y}} -> {{x, z}, {x, z}, {y, z}}"
# evolve_graph([(1, 1)], 6)

# 2.5.2 Multiedge after one step, but then destroys it
# rule = "{{x, y}} -> {{x, z}, {z, w}, {y, z}}"
# evolve_graph([(1, 1)], 4)

#TODO: ---------------------------------------------

# 2.6 Ternary self-loop
# rule = "{{x, y, z}} -> {{x, y, w}, {y, w, z}}"
# evolve_graph([(1, 1, 1)], 4)

# 2.7 More Than One Relation
# rule = "{{x, y}, {x, z}} -> {{x, y}, {x, w}, {y, w}, {z, w}}"
# evolve_graph([(1, 2), (1, 3)], 6)

# 2.8 Termination
# rule = "{{x, y, z}, {u, x}} -> {{x, u, v}, {z, y}, {z, u}}"
# evolve_graph([(0, 0, 0), (0, 0)], 6)

# 2.9 Connectedness
# rule = "{{x, y}} -> {{x, x}, {z, x}}"
# evolve_graph([(1, 2)], 4)



# 3.5 Rules Depending on a Single Binary Relation
# rule = "{{x, y}} -> {{x, z}, {y, z}, {z, z}}"
# evolve_graph([{{1, 1}}, 5

# rule = "{{x, y}} -> {{x, y}, {y, z}, {z, x}}"
# evolve_graph([{{1, 2}}, 5

# rule = "{{1, 2}} -> {{3, 4}, {4, 3}, {3, 1}, {3, 2}}"
# evolve_graph([{{0, 0}}, 5

# rule = "{{1, 2}} -> {{2, 3}, {2, 3}, {3, 1}, {3, 1}}"
# evolve_graph([{{0, 0}}, 5



# 3.6 Rules Depending on One Ternary Relation
# rule = "{x, x, y} to {x, x}, {x, y}"
# evolve_graph([[0, 0, 0]], 6)

# rule = "{{x, x, y}} -> {{y, y, y}, {x, y, z}}"
# evolve_graph([[0, 0, 0]], 6)

# rule = "{{x, y, z}} -> {{x, u, v}, {z, v, w}, {y, w, u}}"
# evolve_graph([[1, 2, 3]], 5)



# 3.7 Rules Depending on More Than One Relation: The 22 -> 32 Case
# rule = "{{x, y}, {x, z}} -> {{x, w}, {y, w}, {z, w}}"
# evolve_graph([[0, 0], [0, 0]], 30)



# 3.8 Rules with Signature 22 -> 42
# rule = "{{x, y}, {x, z}} -> {{y, z}, {y, w}, {z, w}, {w, x}}"
# evolve_graph([[0, 0], [0, 0]], 10)

# rule = "{{x, y}, {y, z}} -> {{x, y}, {y, x}, {w, x}, {w, z}}"
# evolve_graph([[0, 0], [0, 0]], 10)

# rule = "{{x, y}, {y, z}} -> {{w, y}, {y, z}, {z, w}, {x, w}}"
# evolve_graph([[0, 0], [0, 0]], 10)



# 3.13 Multiple Transformation Rules
# {{{x, x}} -> {{y, x}, {x, z}}, {{x, y}, {y, z}} -> {{x, x}}}, {{0, 0}}, 7

# {{{1, 1}} -> {{2, 1}, {2, 1}, {3, 1}}, {{1, 2}, {3, 2}} -> {{2, 2}}}, {{1, 1}}, 20



# 3.14 Rules Involving Disconnected Pieces
# {{x, y}} -> {{y, z}, {y, z}}, {{0, 0}}, 5
# {{x, y}} -> {{x, x}, {y, z}}, {{0, 0}}, 5

#  {{x}, {y}} -> {{x, y}},
# initial = [[1]]
# for i in range(10):
# 	initial.append([i])
