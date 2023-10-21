from graph_data_generator.models.generator import Generator, GeneratorType
from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logic.generate_values import generator_for_raw_property

def default_assignment_generator() -> Generator:
    generator = generators.get('exhaustive_random', None)
    return generator

def assignment_generator_from(properties:dict) -> Generator:
    """Returns an assignment generator for a relationship specification

    Args:
        properties: Specification dictionary

    Returns:
        Specified relationship assignment generator. Defaults to exhaustive_random if no other valid one specified 
    """
    assign = properties.get('ASSIGNMENT', None)

    # No explicit generator specified
    if assign is None:
        return default_assignment_generator()
    
    gen, _ = generator_for_raw_property(assign, generators)
    return gen
