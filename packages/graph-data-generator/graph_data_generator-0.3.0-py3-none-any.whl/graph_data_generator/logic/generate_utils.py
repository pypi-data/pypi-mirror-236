import json
from graph_data_generator.generators.ALL_GENERATORS import generators_json
from graph_data_generator.logger import ModuleLogger

reference_generator_names_only = [name for name, specs in generators_json.items() if specs.get('type', '').lower() == 'reference']

# What happens when an objective-c dev becomes a python dev ;D
def properties_contain_a_reference_generator(obj: dict) -> bool:
    # Node or Relationship 'properties' value should be a dictionary.
    # Check each key-value pair, looking for a value that specifies a reference generator.
    # If found in any of the pairs, return True.
    for _, value in obj.items():
        if property_contains_reference_generator(value):
            return True
    return False

def property_contains_reference_generator(obj: str) -> bool:
    # Values with generator specifications will look like: "{\"reference\": [\"\"]}"
    
    if isinstance(obj, str) == False:
        # Not even the right object type to contain reference generator specification
        return False
    
    # Try to convert json object, this is slow but if unsuccessful that automatically it's not a reference generator
    try:
        spec = json.loads(obj)
        keys = [*spec]
        if len(keys) != 1:
            # Not sure what was passed in as a value
            ModuleLogger().error(f'ERROR: Invalid value passed to reference generator: {obj}')
            return False
        if keys[0] not in reference_generator_names_only:
            ModuleLogger().warning(f'Value passed to property is not a reference generator: {obj}')
            return False
        return True
    except:
        return False

def preprocess_nodes(json: list[dict]) -> list[dict]:
    # Filter out dicts without required keys
    # Sample dict list
    #   [
    #     {
    #       "id": "n0",
    #       "caption": "Person",
    #       "labels": [],
    #       "properties": {
    #         "name": "string",
    #         "COUNT": "3"
    #       }
    #     }
    #   ]

    filtered_list = [obj for obj in json if 'properties' in obj and 'id' in obj and 'caption' in obj]
    filtered_list.sort(key=lambda x: properties_contain_a_reference_generator(x['properties'])) 
    return filtered_list

def preprocess_relationships(json: list[dict]) -> list[dict]:
    # Filter out dicts without required keys
    # Sample dict list
    # [
    #     {
    #     "id": "n3",
    #     "fromId": "n4",
    #     "toId": "n1",
    #     "type": "IN",
    #     "properties": {
    #         "Distance": "km"
    #     }
    #     }
    # ]

    filtered_list = [obj for obj in json if 'properties' in obj and 'id' in obj and 'fromId' in obj and 'toId' in obj and 'type'in obj]
    filtered_list.sort(key=lambda x: properties_contain_a_reference_generator(x['properties'])) 
    return filtered_list

def convert_dicts_to_csv(filename: str, dicts: list[dict])-> (str, str):
    """Converts a dictionary of {ids: list[dict]} to a filename, CSV string tuple

    Args:
        filename: filename for the csv file.
        dict: Source dictionary of data to convert to .csvs. The keys, meant for faster updating earlier, are ignored by this function

    Returns:
        A list of tuples containing (filename, csv string) or None if an exception is caught
    """
    import csv
    from io import StringIO

    fieldnames = dicts[0].keys()

    csv_buffer = StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    
    # Write header row
    csv_writer.writeheader()

    # Write rows
    for row_dict in dicts:
        csv_writer.writerow(row_dict)

    return (filename, csv_buffer.getvalue())
    