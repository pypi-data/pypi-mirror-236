import cv2
import os
from paddleocr import PaddleOCR
import torch
import torch.nn.functional as F
from PIL import Image

from .utils import read_text, process_text


class EmbeddingDataset:
    """
    A class for embedding images and text and combining them into a dataset.

    Attributes:
        image_model: The image model used for image feature extraction.
        feature_extractor: The feature extractor for image processing.
        text_model: The text model used for text embedding.

    Methods:
        image_embedding(image_path):
            Extract image embeddings from the specified image file.
        text_embedding(image_path, reader):
            Embed text content extracted from an image using OCR.
        embedding_img(image_path, reader):
            Extract both image and text embeddings from an image.
        __call__(images_root, images_paths, img_weight=0.8, txt_weight=0.2):
            Embed images and text from a list of
            image paths and combine them into a dataset.
    """

    def __init__(self, image_model, feature_extractor, text_model):
        """
        Initialize the EmbeddingDataset with image and text models.

        Args:
            image_model: The image model used for image feature extraction.
            feature_extractor: The feature extractor for image processing.
            text_model: The text model used for text embedding.
        """
        self.feature_extractor = feature_extractor
        self.image_model = image_model
        self.text_model = text_model

    def image_embedding(self, image_path):
        """
        Extract image embeddings from the specified image file.

        Args:
            image_path (str): The path to the image file.

        Returns:
            torch.Tensor: The extracted image embeddings.
        """
        with torch.no_grad():
            image = Image.open(image_path).convert("RGB")

            inputs = self.feature_extractor(images=image, return_tensors="pt")
            outputs = self.image_model(**inputs)

            last_hidden_states = outputs.last_hidden_state

            cls_embedding = last_hidden_states[:, 0, :]

        return cls_embedding

    def text_embedding(self, image_path, reader):
        """
        Embed text content extracted from an image using OCR.

        Args:
            image_path (str): The path to the image file.
            reader: The OCR reader used to extract text from the image.

        Returns:
            torch.Tensor: The embedded text content.
        """
        text = read_text(image_path, reader)
        cleaned_text = process_text(text)
        with torch.no_grad():
            embedding = self.text_model.encode(cleaned_text, convert_to_tensor=True)
            embedding_rs = torch.reshape(embedding, [1,768])

        return embedding_rs

    def embedding_img(self, image_path, reader):
        """
        Extract both image and text embeddings from an image.

        Args:
            image_path (str): The path to the image file.
            reader: The OCR reader used to extract text from the image.

        Returns:
            tuple: A tuple containing the image and text embeddings.
        """
        img_embedding = self.image_embedding(image_path)
        txt_embedding = self.text_embedding(image_path, reader)

        return img_embedding, txt_embedding

    def __call__(self, images_root, images_paths,
                 img_weight=0.8, txt_weight=0.2):
        """
        Embed images and text from a list of image paths
        and combine them into a dataset.

        Args:
            images_root (str): The root directory of image files.
            images_paths (list): A list of image file paths to be embedded.
            img_weight (float): Weight for image embeddings (default is 0.8).
            txt_weight (float): Weight for text embeddings (default is 0.2).

        Returns:
            torch.Tensor: The combined dataset embeddings.
        """
        reader = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
        img_embedding_list = []
        txt_embedding_list = []

        for image_path in images_paths:
            image_path = os.path.join(images_root, image_path)
            img_embedding, txt_embedding = self.embedding_img(image_path,
                                                              reader)

            img_embedding_list.append(img_embedding)
            txt_embedding_list.append(txt_embedding)

        img_embedding_tensor = torch.cat(img_embedding_list, dim=0)
        txt_embedding_tensor = torch.cat(txt_embedding_list, dim=0)

        img_embedding_nml = F.normalize(img_embedding_tensor, dim=1)
        txt_embedding_nml = F.normalize(txt_embedding_tensor, dim=1)

        dataset_embedding = torch.cat(
            (img_embedding_nml * img_weight,
             txt_embedding_nml * txt_weight), dim=1
        )

        return dataset_embedding
