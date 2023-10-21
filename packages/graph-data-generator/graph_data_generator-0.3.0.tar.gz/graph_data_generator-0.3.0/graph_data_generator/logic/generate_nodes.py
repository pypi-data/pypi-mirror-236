# Objectless process for creating Node data

from graph_data_generator.logic.generate_utils import preprocess_nodes
from graph_data_generator.logic.generate_count import count_generator_from
from graph_data_generator.logic.generate_values import generator_for_raw_property
from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logger import ModuleLogger

def generate_a_node_record(
        input: dict, 
        ) -> dict:
    """Generates a single node record.

    Args:
        input: List of dictionaries defining node specifications

    Returns:
        A dictionary with generated nodes records. Original node config ids as keys. Values are lists of dictionaries
    """
    output = {}
    properties = input.get('properties', {})

    # Insert a uuid so user does not need to assign a key
    properties["_uid"] = "{\"uuid\":[]}"

    # TODO: Sort properties so reference generators are last

    # Generate values for all properties
    for property_id, property in properties.items():
        # Skip the special COUNT identifier
        if property_id.lower() == "count":
            continue
        generator, args = generator_for_raw_property(
            property, 
            generators, 
            )
        output[property_id] = generator.generate(args)
    return output

def generate_node_records(
        input: dict,
        ) -> list[dict]:
    """Generates a list of node records}.

    Args:
        input: Dictionaries defining node specification

    Returns:
        A list of dictionaries of generated nodes records.
    """
    # Extract any count configuration from the properties
    properties = input.get('properties', None)
    count_generator, args = count_generator_from(properties)
    count = count_generator.generate(args)

    # Generate records
    output = []

    # Coalesce caption and labels into one list and add to records
    labels = input.get('labels', [])
    key_label = input.get('caption', None)
    if key_label is not None:
        labels.insert(0, key_label)

    for _ in range(count):
        # Generate a single node record
        node = generate_a_node_record(input)

        node["_labels"] = labels

        output.append(node)
    return output

def generate_nodes(input: list[dict]) -> dict:
    """Generates a dictionary of {node id: list of node records}.

    Args:
        input: List of node specification dictionaries

    Returns:
        A dictionary with generated nodes records. Each key is the id of the original node specification, value is a list of dictionary records generated
    """
    #   Sample input
    #   [
    #     {
    #       "id": "n0",
    #       "position": {
    #         "x": -154.38476542608726,
    #         "y": 210.7077534174155
    #       },
    #       "caption": "Person",
    #       "labels": [],
    #       "properties": {
    #         "name": "string",
    #         "COUNT": "3"
    #       },
    #       "style": {}
    #     }
    #   ]
    #  NOTE: position, labels, and the style key-values are unused by this function.

   # Purge improperly formatted objects and sort nodes using reference generators last
    cleaned_sorted_input = preprocess_nodes(input)

    # Using a dict as we generate nodes
    # node ids will be the keys, values will be a list of dictionaries representing individually created records
    output = {}

    # def callback(id: str) -> any:
    #     nonlocal cleaned_sorted_input

    # Run through each node type, generating nodes and properties for each based on the input configuration
    for node_spec in cleaned_sorted_input:
        id = node_spec.get('id', None)

        # Redundant as id check should have already occurred in preprocess_nodes()
        if id is None:
            continue

        # TODO: Support for cross node reference generators / pointers will likely go here
        node_records = generate_node_records(node_spec)

        output[id] = node_records
    
    return output