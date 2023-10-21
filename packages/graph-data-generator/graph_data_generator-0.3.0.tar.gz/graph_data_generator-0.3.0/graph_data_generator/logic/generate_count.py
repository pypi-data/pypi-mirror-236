from graph_data_generator.models.generator import Generator, GeneratorType
from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logic.generate_values import generator_for_raw_property

def default_count_generator() -> (Generator, list):
    generator = generators.get('int_range', None)
    return generator, [1, 100] 

def count_generator_from(properties:dict) -> (Generator, list):
    """Returns a generator from a node or relationship specification dictionary.

    Args:
        properties: Dictionary defining specification

    Returns:
        Generator for property specifications. A random int generator will be returned if count not specified in properties arg.
    """
    
    count = properties.get('COUNT', None)

    # Was a COUNT explicitly specified?
    if count is None:
        return default_count_generator()
    
    # Find specified generator
    gen, arg = generator_for_raw_property(count, generators)

    # Invalidate if non-integer generator was specified
    if gen.type != GeneratorType.INT:
        return default_count_generator()
    
    # Return the retrieved int generator
    return gen, arg