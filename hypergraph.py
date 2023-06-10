import networkx as nx
import matplotlib.pyplot as plt
import time
import re

rule  = ""
invars = ""
outvars = ""

def plot_graph(edges):
	G = nx.Graph()
	G.add_edges_from(edges)
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

#relation: [[1, 2][1, 3]]
def substitution_test(relation):
	flat = list(set(relation[0]))
	#TODO: remove unique more generally
	if invars[0][0] != invars[0][1]:
		return True, relation[0]
	# if var names same, value cant be same
	if invars[0][0] == invars[0][1]:
		if relation[0][0] == relation[0][1]:
			return True, flat
		else:
			return False, []
	print("undefined substitution")
	exit(0)

def _generate_relation_substitution():
	code = "def relation_substition(a=0,b=0,c=0,d=0,e=0,f=0,g=0,h=0,i=0,j=0,k=0):\n"
	code +=	"	return " + str(outvars).replace("'", "") + "\n"
	print("\n" + code)
	exec(code, globals())

def _count_unique(list2d):
	unique_elements = set()
	for sublist in list2d:
		for elem in sublist:
			unique_elements.add(elem)
	return len(unique_elements)

def _generate_graph_substitution():
	new_amount = _count_unique(outvars) - _count_unique(invars)
	code = \
	"def graph_substitution(graph):\n" +\
	"	result = []\n" +\
	"	max_val = max(max(p) for p in graph) + 1\n" +\
	"	for i in range(len(graph)):\n"

	# TODO: generate nesting, "\t" * len(invars)
	if (len(invars) == 1):
		code +=\
		"		should_sub, flat = substitution_test([graph[i]])\n" +\
		"		if should_sub:\n" +\
		"			result += relation_substition(*flat, max_val + 0, max_val + 1, max_val + 2, max_val + 3, max_val + 4)\n" +\
		"			max_val += " + str(new_amount) + "\n" +\
		"		else:\n" +\
		"			result += [graph[i]]\n"
	else:
		print("undefined input width")
		exit(0)

	# elif (len(invars) == 2):
	# 	code +=\
	# 	"		for j in range(i + 1, len(graph)):\n" +\
	# 	"			flatted = graph[i] + graph[j]\n" +\
	# 	"			result += substitute(max_value, *flatted)\n" +\
	# 	"			max_value += " + str(new_amount) + "\n"

	code +=\
	"	return result\n"
	print(code)
	exec(code, globals())

def xyz_to_abc(rule):
	replacement_chars = 'abcdefghijklmnopqrstuvwxyz'
	mapping = {}
	output = ""
	index = 0
	for char in rule:
		if char.isalnum() and char not in mapping:
			mapping[char] = replacement_chars[index]
			index += 1
		output += mapping.get(char, char)
	print(output)
	return output

def parse_rule_arrays(string):
	res = []
	current_list = []
	for char in string:
		if char == '{':
			current_list = []
		elif char == '}':
			if current_list:
				res.append(current_list)
				current_list = []
		else:
			if char != ',' and char != ' ':
				current_list.append(char)
	return res

def parse_rule():
	global invars
	global outvars
	rules = xyz_to_abc(rule).split("->")
	invars = parse_rule_arrays(rules[0])
	outvars = parse_rule_arrays(rules[1])
	print(str(invars) + " -> " + str(outvars))
	_generate_relation_substitution()
	_generate_graph_substitution()

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
				graph = graph_substitution(graph)
			plt.clf()
			plot_graph(graph)
		plt.title(f"{rule}\nSteps: {current_step}")
		plt.pause(0.1)


# ui functions
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



# https://www.wolframphysics.org/technical-introduction/basic-form-of-models/
# 2.1 Basic structure
# graph = [[1, 2], [1, 3], [2, 3], [4, 1]]
# plot_graph(graph)
# plt.show()

# 2.2 First Example of a Rule
# rule = "{{x, y}} -> {{x, y}, {y, z}}"
# evolve_graph([[1, 2]], 4)

# 2.3 A Slightly Different Rule
# rule = "{{x, y}} -> {{z, y}, {y, x}}"
# evolve_graph([[1, 2]], 5)

# 2.4 Self-Loops (circle)
# rule = "{{x, y}} -> {{y, z}, {z, x}}"
# evolve_graph([[1, 1]], 6)

# 2.4.2 Binary tree
# rule = "{{x, x}} -> {{y, y}, {y, y}, {x, y}}"
# evolve_graph([[1, 1]], 6)

# 2.5 Multiedges
# rule = "{{x, y}} -> {{x, z}, {x, z}, {y, z}}"
# evolve_graph([[1, 1]], 6)

# 2.5.2 Multiedge after one step, but then destroys it
# rule = "{{x, y}} -> {{x, z}, {z, w}, {y, z}}"
# evolve_graph([[1, 1]], 4)

#TODO: ---------------------------------------------

# 2.6 Ternary self-loop
# rule = "{{x, y, z}} -> {{x, y, w}, {y, w, z}}"
# evolve_graph([[1, 1, 1]], 4)

# 2.7 More Than One Relation
# rule = "{{x, y}, {x, z}} -> {{x, y}, {x, w}, {y, w}, {z, w}}"
# evolve_graph([[1, 2], [1, 3]], 6)

# 2.8 Termination
# rule = "{{x, y, z}, {u, x}} -> {{x, u, v}, {z, y}, {z, u}}"
# evolve_graph([[0, 0, 0], [0, 0]], 6)

# 2.9 Connectedness
# rule = "{{x, y}} -> {{x, x}, {z, x}}"
# evolve_graph([[1, 2]], 4)



# 3.5 Rules Depending on a Single Binary Relation
# rule = "{{x, y}} -> {{x, z}, {y, z}, {z, z}}"
# evolve_graph([[1, 1]], 5)

# rule = "{{x, y}} -> {{x, y}, {y, z}, {z, x}}"
# evolve_graph([[1, 2]], 5)

# rule = "{{1, 2}} -> {{3, 4}, {4, 3}, {3, 1}, {3, 2}}"
# evolve_graph([[0, 0]], 5

# rule = "{{1, 2}} -> {{2, 3}, {2, 3}, {3, 1}, {3, 1}}"
# evolve_graph([[0, 0]], 5



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
