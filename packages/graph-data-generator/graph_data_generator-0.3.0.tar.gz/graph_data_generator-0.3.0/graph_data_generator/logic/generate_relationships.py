# Objectless relationship generation

from graph_data_generator.logic.generate_utils import preprocess_relationships
from graph_data_generator.logic.generate_count import count_generator_from
from graph_data_generator.logic.generate_assignment import assignment_generator_from
from graph_data_generator.logic.generate_values import generator_for_raw_property
from graph_data_generator.models.generator import Generator
from graph_data_generator.generators.ALL_GENERATORS import generators

def generate_relationship_properties(properties:dict) -> dict:
    """Generates a single relationship record.

    Args:
        input: Dictionary of relationship properties to process

    Returns:
        A dictionary of data representing relationship record.
    """
    if isinstance(properties, dict) == False:
        raise Exception(f'Expected properties to be a dictionary object. Instead got {properties}')

    # Insert a uuid so user does not need to assign a key
    properties["_uid"] = "{\"uuid\":[]}"
    
    # TODO: Sort properties so reference generators are last

    # Generate values for all properties
    output = {}
    for property_id, property in properties.items():
        # Skip any special COUNT identifier
        if property_id.lower() == "count":
            continue
        # Skip any special ASSIGNMENT identifier
        if property_id.lower() == "assignment":
            continue
        generator, args = generator_for_raw_property(property, generators)
        output[property_id] = generator.generate(args)
    return output

def generate_relationship_records(input: dict, nodes:dict) -> dict:
    """Generates a list of relationship records.

    Args:
        input: Dictionary defining relationship specification
        nodes: Nodes to connect

    Returns:
        A list of dictionaries of generated relationship records.
    """

    # Double check the node records match up with the relationship specifications
    from_node_id = input.get('fromId', None)
    if from_node_id is None:
        raise Exception(f'Expected "fromId" in relationship specification: {input}')
    to_node_id = input.get('toId', None)
    if to_node_id is None:
        raise Exception(f'Expected "toId" in relationship specification: {input}')
    from_nodes = nodes.get(from_node_id, None)
    if from_nodes is None:
        raise Exception(f'No from node records for node id {from_node_id} found in nodes arg: {nodes}')
    to_nodes = nodes.get(to_node_id, None)
    if to_nodes is None:
        raise Exception(f'No to node records for node id {to_node_id} found in nodes arg: {nodes}')
    to_nodes_copy = to_nodes[:]

    # Extract any count configuration from the properties
    properties = input.get('properties', {})
    assign_generator = assignment_generator_from(properties)

    # Generate relationship from each from node (if count > 0)
    output = []

    # Insert relationship type to record
    type = input.get('type', None)
        
    for f_node in from_nodes:
        fid = f_node.get('_uid', None)
        if fid is None:
            raise Exception(f'from node record is missing required _uid: {f_node}')
        # Number of relationships to generate out from node
        count_generator, args = count_generator_from(properties)
        count = count_generator.generate(args)
        for _ in range(count):
            if len(to_nodes_copy) == 0:
                # No more target nodes to attach to
                continue

            # Determine target node to connect to
            to_node, remaining_nodes = assign_generator.generate(to_nodes_copy)
            
            # Update target nodes if assignment generator pops/pass
            to_nodes_copy = remaining_nodes
            
            tid = to_node.get('_uid', None)
            if tid is None:
                raise Exception(f'Target node record is missing _uid: {to_node}')
            
            # Generate a single record _uid and prop values
            record = generate_relationship_properties(properties)

            # Insert from and to node _uids
            record["_from__uid"] = fid
            record["_to__uid"] = tid

            if type is not None:
                record['_type'] = type

            output.append(record)
    return output

def generate_relationships(input: list[dict], nodes: dict)-> list[dict]:
    """Generates a list of relationship records.

    Args:
        input: Dictionaries defining relationship specifications
        nodes: Dictionary of nodes for relationships to draw connections from

    Returns:
        A list of dictionaries of generated relationship records.
    """
    #  Sample Input
    # [
    #     {
    #     "id": "n0",
    #     "type": "LIVE_IN",
    #     "style": {},
    #     "properties": {
    #         "COUNT": "0-1"
    #     },
    #     "fromId": "n0",
    #     "toId": "n1"
    #     }
    # ]

    # Sample Nodes dict
    # {
    #     "n0":[
    #         {
    #             ...
    #         }
    #     ]
    # }

    if isinstance(input, list) == False:
        raise Exception(f'Expected a list of dictionary objects for input. Instead got {input}')

   # Purge improperly formatted objects and sort nodes using reference generators last
    cleaned_sorted_input = preprocess_relationships(input)

    # Using a dict as we generate nodes
    # node ids will be the keys, values will be a list of dictionaries representing individually created records
    output = {}

    # Run through each node type, generating nodes and properties for each based on the input configuration
    for spec in cleaned_sorted_input:
        id = spec.get('id', None)

        # Redundant as Id check should have already occurred in preprocess_nodes()
        if id is None:
            continue

        record = generate_relationship_records(spec, nodes)
        output[id] = record
    
    return output