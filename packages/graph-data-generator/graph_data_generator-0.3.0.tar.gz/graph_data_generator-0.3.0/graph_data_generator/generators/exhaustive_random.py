from random import shuffle

# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

    node_values = args
    if len(node_values) == 0:
        return (None, [])
    shuffle(node_values)
    choice = node_values.pop(0)
    return (choice, node_values)