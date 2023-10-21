# Create .json file for Neo4j data importer use
from graph_data_generator.models.data_import import DataImporterJson
from graph_data_generator.models.mapping import Mapping
from graph_data_generator.logger import ModuleLogger
import json

def generate_data_import_json(mapping: Mapping) -> str:
    # generate data-importer.json
    dij = DataImporterJson()
    nodes = mapping.nodes
    dij.add_nodes(nodes)
    relationships = mapping.relationships
    dij.add_relationships(relationships)
    dij_dict = dij.to_dict()

    try:
        di_dump = json.dumps(dij_dict)
        return di_dump
    except Exception as e:
        ModuleLogger().error(f'Problem creating import model .json generation failed: {e}. Returning empty string')
        return ""