from defsent import DefSent
from sentence_transformers import SentenceTransformer
import os
import yaml
import shutil

from transformers import AutoImageProcessor, AutoModelForImageClassification
from transformers import BeitFeatureExtractor, BeitModel

from .classification import get_cluster


class DocumentClassifier:
    """
    A class for document classification and clustering.

    Attributes:
        configs (dict): Configuration parameters for document classification.

    Methods:
        get_config():
            Load configuration parameters from a YAML file.
        classify():
            Perform document classification and clustering.
        divide_folders(clusters):
            Organize clustered images into separate folders.
    """

    def __init__(self):
        """
        Initialize the DocumentClassifier.
        """
        self.configs = self.get_config()

    def get_config(self):
        """
        Load configuration parameters from a YAML file.

        Returns:
            dict: Configuration parameters.
        """

        base_dir = os.path.dirname(__file__)
        config_path = os.path.join(base_dir, 'config.yml')
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)

        configs = {}
        configs["classify_model"] = config["models"]["classify_model"]
        configs["image_model"] = config["models"]["image_model"]
        configs["text_model"] = config["models"]["text_model"]
        configs["feature_extractor"] = config["models"]["feature_extractor"]

        configs["images_root"] = config["dataset"]

        configs["img_weight"] = config["parameters"]["img_weight"]
        configs["txt_weight"] = config["parameters"]["txt_weight"]
        configs["epsilon_dbscan"] = config["parameters"]["epsilon_dbscan"]
        configs["min_samples"] = config["parameters"]["min_samples"]

        return configs

    def classify(self):
        """
        Perform document classification and clustering.

        Returns:
            dict: Clustered images.
        """
        processor = AutoImageProcessor.from_pretrained(self.configs["classify_model"])
        classify_model = AutoModelForImageClassification.from_pretrained(self.configs["classify_model"])

        feature_extractor = BeitFeatureExtractor.from_pretrained(self.configs["feature_extractor"])
        image_model = BeitModel.from_pretrained(self.configs["image_model"])

        text_model = SentenceTransformer(self.configs["text_model"])
        text_model.max_seq_length = 100000

        result = get_cluster(
            self.configs["images_root"],
            image_model,
            classify_model,
            processor,
            text_model,
            feature_extractor,
            self.configs["epsilon_dbscan"],
            self.configs["min_samples"],
            self.configs["img_weight"],
            self.configs["txt_weight"],
        )

        return result

    def divide_folders(self, clusters):
        """
        Organize clustered images into separate folders.

        Args:
            clusters (dict): Clustered images.
        """
        for i, (k, v) in enumerate(clusters.items()):
            folder_path = os.path.join(self.configs["images_root"], str(i))
            os.mkdir(folder_path)
            for image in v:
                image_path = os.path.join(self.configs["images_root"], image)
                shutil.move(image_path, folder_path)

    def __call__(self, data_path):
        """
        Perform document classification, clustering, and folder organization.

        Args:
            data_path (str): The root directory of images to be processed.
        """
        self.configs["images_root"] = data_path

        clusters = self.classify()

        self.divide_folders(clusters)

        print("Clustered successfully")
