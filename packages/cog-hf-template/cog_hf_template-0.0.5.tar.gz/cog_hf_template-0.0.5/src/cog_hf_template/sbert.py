from pathlib import Path
from typing import Any

from cog import BasePredictor, Input

from .download_utils import Logger, maybe_pget_weights


class SentenceTransformersFeatureExtractionPredictor(BasePredictor):
    task = "feature-extraction"
    hf_model_id = "BAAI/bge-base-en"
    cache_dir = "./weights-cache"
    init_kwargs = {}
    encode_kwargs = {"normalize_embeddings": True}
    gcp_bucket_weights = None

    def setup(self):
        maybe_pget_weights(
            path=self.hf_model_id, remote_path=self.gcp_bucket_weights, remote_filenames=None, logger=Logger(__name__)
        )
        # os.environ["TRANSFORMERS_CACHE"] = self.cache_dir
        # os.environ["HF_HOME"] = self.cache_dir
        from sentence_transformers import SentenceTransformer

        cache_path = Path(self.cache_dir)

        if cache_path.exists() and len(list(cache_path.glob("**"))) > 1:
            self.hf_model_id = str(list(cache_path.glob("**"))[-2])

        self.model = SentenceTransformer(self.hf_model_id, cache_folder=self.cache_dir, **self.init_kwargs)

    def predict(self, text: str = Input(description="The text to embed")) -> Any:
        out = self.model.encode(text, **self.encode_kwargs)
        return out.tolist()
