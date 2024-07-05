import random

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class GrammarEncoder:
    def __init__(self):
        self.root = Node("<network>")
        self.vector = {
            "functions": ["LS", "HT", "SN", "GS", "LN", "HL", "LR"],
            "input_ids": ["i1", "i2", "i3"],
            "output_ids": ["o1", "o2", "o3"]
        }

    def generate_inputs(self):
        num_inputs = random.randint(1, 3)
        inputs = [f"i{random.randint(1, 3)}" for _ in range(num_inputs)]
        return ", ".join(inputs)

    def expand_network(self, node):
        hidden_neurons_node = Node("<hiddenNeurons>")
        output_neurons_node = Node("<outputNeurons>")
        node.add_child(hidden_neurons_node)
        node.add_child(output_neurons_node)
        self.expand_hidden_neurons(hidden_neurons_node)
        self.expand_output_neurons(output_neurons_node)

    def expand_hidden_neurons(self, node):
        production_choice = random.choice(["single", "multiple"])
        if production_choice == "single":
            self.expand_hidden_neuron(node)
        elif production_choice == "multiple":
            self.expand_hidden_neurons_multiple(node)

    def expand_hidden_neuron(self, node):
        func = random.choice(self.vector["functions"])
        weight = f"{random.choice(['+', '-'])}{random.randint(0,8)}.{random.randint(0,8)}"
        inputs = self.generate_inputs()
        node.add_child(Node(f"{func} : {weight} @i0, {inputs}#{inputs}"))

    def expand_hidden_neurons_multiple(self, node):
        self.expand_hidden_neuron(node)
        node.add_child(Node("_"))
        self.expand_hidden_neurons(node)

    def expand_output_neurons(self, node):
        func = random.choice(self.vector["functions"])
        weight1 = f"{random.choice(['+', '-'])}{random.randint(0,8)}.{random.randint(0,8)}"
        weight2 = f"{random.choice(['+', '-'])}{random.randint(0,8)}.{random.randint(0,8)}"
        output_id = random.choice(self.vector["output_ids"])
        node.add_child(Node(f"{func}: {weight1} @i0_.._{func}:{weight2}@{output_id}"))

    def generate_derivation_tree(self):
        self.expand_network(self.root)
        return self.root

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print(" " * level + node.value)
        for child in node.children:
            self.print_tree(child, level + 2)

    def encode_expressions(self):
        expressions = []
        def traverse(node):
            expressions.append(node.value)
            for child in node.children:
                traverse(child)
        traverse(self.root)
        return expressions

# Ejemplo de uso
encoder = GrammarEncoder()
tree = encoder.generate_derivation_tree()

print("Árbol de Derivación:")
encoder.print_tree()

expressions = encoder.encode_expressions()
print("\nExpresiones Generadas:")
for expr in expressions:
    print(expr)
