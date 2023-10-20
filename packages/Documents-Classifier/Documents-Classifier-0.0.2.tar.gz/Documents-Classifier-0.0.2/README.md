DocumentClassifier is a Python library that provides functionality for classifying documents based on images and text content. 

This library is designed to help you process and organize large sets of documents, making it useful for various applications such as image-based document classification and clustering.

## Usage
Prepare a folder of image documents

```python
import DocumentsClassifier as DC

# declare folder path
images_path = 'path/to/your/documents/folder'

# using function to classify
DC.classify(images_path)
 >> Clusterd successfully

```

After running the code, your images will be classified into subfolders in the root you declared:

## Some limitations
This package need to load some pretrained on [Huggingface](https://huggingface.co):

1. [SentenceTransformer](https://huggingface.co/sentence-transformers/all-mpnet-base-v2): Model for text embeddings.
2. [Classify Model](https://huggingface.co/fptinters/DocClass-classify-model): Our pretrained Beit for classifying images.
3. [Image Extractor](https://huggingface.co/fptinters/DocClass-image-model): Our pretrained Beit for extracting features.

And we also use [PaddleOCR](https://pypi.org/project/paddleocr/) for extracting texts so It maybe slow for the first time because It has to download pretrained.

We are in developing process so thanks for your patience.

##Updates
Version 0.0.2: Change text embedding method to SentenceTransformer


## License
This project is licensed under the MIT License - see the [LICENSE](https://choosealicense.com/licenses/mit/)
file for details.
## Contact & Contributing
If you have any questions or suggestions, please contact us at [hungdtse171849@fpt.edu.vn](hungdtse171849@fpt.edu.vn) or [phuongtnse161960@fpt.edu.vn](phuongtnse161960@fpt.edu.vn). 