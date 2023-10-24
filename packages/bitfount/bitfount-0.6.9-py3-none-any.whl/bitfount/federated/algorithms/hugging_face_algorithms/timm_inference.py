"""Hugging Face TIMM inference Algorithm.

Adapted from: https://github.com/huggingface/api-inference-community/
"""
import os
from typing import Any, ClassVar, Dict, Mapping, Optional, Union

from PIL import Image
from marshmallow import fields
import pandas as pd
import timm
from timm.data import (
    CustomDatasetInfo,
    ImageNetInfo,
    create_transform,
    infer_imagenet_subset,
    resolve_model_data_config,
)
import torch

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import delegates

logger = _get_federated_logger(__name__)


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the TIMMInference algorithm."""

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, Any]) -> Dict[str, Any]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the TIMMInference algorithm."""

    def __init__(
        self,
        model_id: str,
        image_column_name: str,
        num_classes: int,
        checkpoint_path: Optional[Union[os.PathLike, str]],
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = f"hf_hub:{model_id}"
        self.image_column_name = image_column_name
        self.num_classes = num_classes
        self.checkpoint_path = checkpoint_path

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Primarily initialises the model with the checkpoint file.

        Also initialises the transformations.
        """
        # TODO: [BIT-3097] Resolve initialise without DP
        if pod_dp:
            logger.warning("The use of DP is not supported, ignoring set `pod_dp`.")

        self.initialise_data(datasource=datasource)
        self.model = timm.create_model(
            self.model_id,
            num_classes=self.num_classes,
            checkpoint_path=self.checkpoint_path or "",
        )
        self.transform = create_transform(
            **resolve_model_data_config(self.model, use_test_size=True)
        )
        self.model.eval()

        dataset_info = None
        label_names = self.model.pretrained_cfg.get("label_names", None)
        label_descriptions = self.model.pretrained_cfg.get("label_descriptions", None)

        if label_names is None:
            # if no labels added to config, use imagenet labeller in timm
            imagenet_subset = infer_imagenet_subset(self.model)
            if imagenet_subset:
                dataset_info = ImageNetInfo(imagenet_subset)
            else:
                # fallback label names
                label_names = [f"LABEL_{i}" for i in range(self.model.num_classes)]

        if dataset_info is None:
            dataset_info = CustomDatasetInfo(
                label_names=label_names,
                label_descriptions=label_descriptions,
            )

        self.dataset_info = dataset_info

    def run(self) -> pd.DataFrame:
        """Runs the inference on the images in the datasource.

        Returns:
            A dataframe with the predictions where each row is an image and each column
            is a class.
        """
        image_column = self.datasource.get_column(self.image_column_name).tolist()
        dataframe_records = []
        for image_path in image_column:
            image = Image.open(image_path)
            image = self.transform(image.convert("RGB")).unsqueeze(0)

            with torch.no_grad():
                out = self.model(image)

            probabilities = out.squeeze(0).softmax(dim=0)
            values, indices = torch.topk(probabilities, self.model.num_classes)

            labels = {
                self.dataset_info.index_to_description(i, detailed=True): v.item()
                for i, v in zip(indices, values)
            }

            dataframe_records.append(labels)

        df = pd.DataFrame.from_records(dataframe_records)
        df = df.reindex(sorted(df.columns), axis=1)
        return df


@delegates()
class TIMMInference(BaseAlgorithmFactory):
    """HuggingFace TIMM Inference Algorithm..

    Args:
        model_id: The model id to use from the Hugging Face Hub.
        image_column_name: The column name of the image paths.
        num_classes: The number of classes in the model.
        checkpoint_path: The path to a checkpoint file local to the Pod. Defaults to
            None.

    Attributes:
        model_id: The model id to use from the Hugging Face Hub.
        image_column_name: The column name of the image paths.
        num_classes: The number of classes in the model.
        checkpoint_path: The path to a checkpoint file local to the Pod. Defaults to
            None.
    """

    def __init__(
        self,
        model_id: str,
        image_column_name: str,
        num_classes: int,
        checkpoint_path: Optional[Union[os.PathLike, str]] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.image_column_name = image_column_name
        self.num_classes = num_classes
        self.checkpoint_path = checkpoint_path

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_id": fields.String(required=True),
        "image_column_name": fields.String(required=True),
        "num_classes": fields.Integer(required=True),
        "checkpoint_path": fields.String(required=False, allow_none=True),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the TIMMInference algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the TIMMInference algorithm."""
        return _WorkerSide(
            model_id=self.model_id,
            image_column_name=self.image_column_name,
            num_classes=self.num_classes,
            checkpoint_path=self.checkpoint_path,
            **kwargs,
        )
