from .download_utils import resolve_task_name
from .hf import (
    FeatureExtractionPredictor,
    ImageClassificationPredictor,
    TextClassificationPredictor,
)
from .sbert import SentenceTransformersFeatureExtractionPredictor
from .text_generation import TextGenerationPredictor


task2predictor = {
    "text-generation": TextGenerationPredictor,
    "text-classification": TextClassificationPredictor,
    "image-classification": ImageClassificationPredictor,
    "feature-extraction": FeatureExtractionPredictor,
    "sentence-transformers-feature-extraction": SentenceTransformersFeatureExtractionPredictor,
}


def get_predictor(task: str = None, **kwargs):
    task = task or resolve_task_name(kwargs["hf_model_id"])
    klass = task2predictor[task]
    for k, v in kwargs.items():
        setattr(klass, k, v)
    return klass
