import os
import numpy as np
from PIL import Image
from sklearn.cluster import DBSCAN

from .utils import process_embedding
from .embeddings import EmbeddingDataset


class ClassifyDataset:
    """
    A class to classify dataset

    Attributes:
        classify_model: Model for classifying documents.
        processor: Image processor for preprocessing images.
        text_model: Model for embedding texts.
        feature_extractor: Image feature extractor.

    Methods:
        first_stage_classify: Classify documents and cards as a
                            first stage for subsequent clustering.
        __call__: clustering cards after classifying
    """

    def __init__(self, classify_model, processor,
                 text_model, feature_extractor):
        """
        Constructs all the necessary attributes for the classify object
        """

        self.classify_model = classify_model
        self.processor = processor
        self.text_model = text_model
        self.feature_extractor = feature_extractor

    def first_stage_classify(self, images_root):
        """
        Classify documents into groups and cards in the first stage.

        Args:
            images_root (str): Root of the images folder to be classified.

        Returns:
            dict: A dictionary of classified classes.
        """
        images = [image for image in os.listdir(images_root)]

        class_to_images = {}

        for image_file in images:
            if image_file == ".DS_Store":
                continue
            image_path = os.path.join(images_root, image_file)
            image = Image.open(image_path).convert("RGB")

            inputs = self.processor(images=image, return_tensors="pt")
            outputs = self.classify_model(**inputs)
            logits = outputs.logits

            # Predicted class index
            predicted_class_idx = logits.argmax(-1).item()

            # Map the predicted class index to the class label
            cl_name = self.classify_model.config.id2label[predicted_class_idx]

            # Group images by class label
            if cl_name not in class_to_images:
                class_to_images[cl_name] = []
            class_to_images[cl_name].append(image_file)

        return class_to_images

    def __call__(self, images_root, image_model,
                 epsilons, min_spl, img_w, txt_w):
        """
        Perform clustering of cards after classifying.

        Args:
            images_root (str): Root of the images folder.
            image_model: Pre-trained image model.
            epsilons (float): DBSCAN epsilon parameter.
            min_samples (int): DBSCAN min_samples parameter.
            img_w (float): Weight for image embeddings.
            txt_w (float): Weight for text embeddings.

        Returns:
            (dict): A dictionary mapping cluster labels
                     to lists of image filenames.
        """
        classification = self.first_stage_classify(images_root)
        card_paths = classification["card"]
        del classification["card"]

        embedder = EmbeddingDataset(
            image_model, self.feature_extractor, self.text_model
        )

        embeddings = embedder(images_root, card_paths, img_w, txt_w)
        processed_embeddings = process_embedding(embeddings)

        dbscan = DBSCAN(eps=epsilons, min_samples=min_spl, metric="cosine")
        clusters = dbscan.fit_predict(processed_embeddings)

        unique_clusters = set(clusters)
        for cluster in unique_clusters:
            classification[cluster] = [
                card_paths[i] for i in range(len(clusters)) if clusters[i] == cluster
            ]

        return classification


def get_cluster(
    images_root,
    image_model,
    classify_model,
    processor,
    text_model,
    feature_extractor,
    eps,
    min_samples,
    img_w,
    txt_w,
):
    """
    Classify and cluster images in a dataset.

    Returns:
        dict: A dictionary containing the results of the clustering process.
              Keys represent cluster labels, and values are lists
              of image filenames belonging to each cluster.
    """
    classifier = ClassifyDataset(
        classify_model, processor, text_model, feature_extractor
    )

    result = classifier(images_root, image_model,
                        eps, min_samples, img_w, txt_w)

    return result
