import logging
import os

from promptmanager.runtime.flow import PMNodeOutput
from promptmanager.script.embeddings.huggingface_embeddings import PMHuggingFaceEmbeddings

logger = logging.getLogger('pm_log')


def run(params: dict, inputs: dict, outputs: dict) -> PMNodeOutput:
    logger.info("Welcome to Use HuggingFace Embeddings!")

    logger.info("This is params info:")
    logger.info(params)
    logger.info("This is inputs info:")
    logger.info(inputs)
    logger.info("This is outputs info:")
    logger.info(outputs)

    embeddings = PMHuggingFaceEmbeddings()
    results = embeddings

    output = PMNodeOutput()
    for output_name in outputs.keys():
        output.add_output(output_name, results)

    return output
