from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.models.mapping import Mapping
from graph_data_generator.logger import ModuleLogger
import io 
import csv

def generate_csv_from_dictionaries(dict: dict) -> str:
    """Returns a csv data for dictionary of record data

    Args:
        dict: Single depth dictioary of key-value pairs representing generated node/relationship property data

    Returns:
        String csv data
    """    
    fieldnames = dict.keys()
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()

    for key, value in dict.items():
        try:
            writer.writerow(value)
        except Exception as e:
            raise Exception(f'Failed to write row for key: {key}: ERROR: {e}')
    return buffer.getvalue()

def generate_csvs_from_dictionaries(dicts: dict) -> dict[str, str]:
    """Returns a dictionary of filename : csv data string

    Args:
        dicts: Dictionary of records to be written to csv. Should contain 'nodes' and'relationships' keys with values being a list of dictionaries

    Returns:
        A dictionary of {filenames : csv strings}
    """
    # Prep result / return object
    output = {}

    # Process nodes
    nodes = dicts.get('nodes', None)
    if nodes is None:
        raise Exception(f'"nodes" key expected. Got {dicts}')
    
    for node_id, node_dict in nodes:
        csv = generate_csv_from_dictionaries(node_dict)
        output[node_id] = csv

    # Process optional relationships
    rels = dict.get('relationships', None)
    if rels is not None:
        for rel_id, rel_dict in rels:
            csv = generate_csv_from_dictionaries(rel_dict)
            output[rel_id] = csv

    return output


def generate_csv(element: BaseMapping) -> str:
    """Returns a csv data for generated data from a subclass of a BaseMapping object

    Args:
        element: A subclass of BaseMapping representing a node or relationship mapping

    Returns:
        Stringified csv data
    """    

    if isinstance(element, BaseMapping) == False:
        raise Exception(f'BaseMapping subclass expected. Got {element}')
    
    values : list[dict] = element.generated_values()
    
    # Generate csv from values
    if values is None or values == []:
        ModuleLogger().warning(f'No values generated for element {element}')

    fieldnames = values[0].keys()
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()

    for row in values:
        try:
            writer.writerow(row)
        except Exception as e:
            raise Exception(f'Failed to write row: {row}: ERROR: {e}')
    return buffer.getvalue()
    
def generate_csvs(mapping: Mapping) -> dict[str, str]:
    """Returns a dictionary of filename : csv data string. Will return the same data for a given Mapping object. To generate a new set of data, running the appropriate Mapping generate() function.

    Args:
        properties: Mapping object

    Returns:
        A dictionary of {filenames : csv strings}
    """   
    if mapping.did_generate_values() == False:
        mapping.generate_values()
    
    output = {}

    for nodeMapping in mapping.nodes.values():
        values = generate_csv(nodeMapping)
        filename = f'{nodeMapping.filename()}.csv'
        output[filename] = values
    
    for relMapping in mapping.relationships.values():
        values = generate_csv(relMapping)
        filename = f'{relMapping.filename()}.csv'
        output[filename] = values

    return output

