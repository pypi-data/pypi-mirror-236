import os
from pathlib import Path
from typing import Any

import cog
from cog import Input
from PIL import Image
from PIL.ImageFile import ImageFile

from .download_utils import Logger, maybe_pget_weights


class HuggingFacePipelinePredictor(cog.BasePredictor):
    task = None
    hf_model_id = None
    pipeline_kwargs = {}
    cache_dir = "./weights-cache"

    # URL to a tar file of the weights. If specified, will download the weights to cache_dir if it doesn't exist.
    name = None

    def setup(self):
        maybe_pget_weights(
            path=self.hf_model_id, remote_path=self.name, remote_filenames=None, logger=Logger(__name__)
        )

        os.environ["TRANSFORMERS_CACHE"] = self.cache_dir
        cache_path = Path(self.cache_dir)
        # if cache dir exists, figure out where snapshot is and set that as hf_model_id
        if cache_path.exists() and any(cache_path.glob("**/snapshots")):
            self.hf_model_id = str(list(cache_path.glob("**/snapshots/**"))[-1])

        # NOTE - TRANSFORMERS_CACHE dir will get created when transformers is imported,
        # so it's important we do the logic above first.
        from transformers import pipeline

        self.pipe = pipeline(self.task, self.hf_model_id, **self.pipeline_kwargs)


class TextClassificationPredictor(HuggingFacePipelinePredictor):
    task = "text-classification"
    hf_model_id = "distilbert-base-uncased-finetuned-sst-2-english"

    def predict(self, text: str = Input(description="Input text to classify")) -> Any:
        result = self.pipe(text)
        return result[0]


class ImageClassificationPredictor(HuggingFacePipelinePredictor):
    task = "image-classification"
    hf_model_id = "microsoft/resnet-18"

    def predict(
        self,
        image: cog.Path = Input(description="Path of image to classify"),
    ) -> Any:
        if not isinstance(image, ImageFile) and not str(image).startswith("http"):
            image = Image.open(str(image))
        result = self.pipe(image)
        return result[0]


class FeatureExtractionPredictor(HuggingFacePipelinePredictor):
    # TODO - this pipeline outputs all layers, so you'd have to pool yourself.
    # See sbert.py to use sentence-transformers instead if that's easier/better.
    task = "feature-extraction"
    hf_model_id = "BAAI/bge-base-en"

    def predict(self, text: str = Input(description="Input text to embed")) -> Any:
        # This is a tensor of shape [1, sequence_lenth, hidden_dimension] representing the input string.
        result = self.pipe(text)
        return result[0]
