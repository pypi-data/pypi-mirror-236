import re
import nltk
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

try:
    nltk.data.find("corpora/stopwords.zip")
except:
    nltk.download("stopwords")
try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")
try:
    nltk.data.find("taggers/averaged_perceptron_tagger.zip")
    
except:
    nltk.download("averaged_perceptron_tagger")
    
from nltk.corpus import stopwords


def read_text(image_path, reader):
    """
    Read and extract text content from an image using OCR.

    Args:
        image_path (str): The path to the image file.
        reader: The OCR reader used to extract text from the image.

    Returns:
        str: The extracted text content from the image.
    """
    result = reader.ocr(image_path, cls=True)[0]
    text_ls = []
    for line in result:
        text_ls.append(line[1][0].lower())

    text = " ".join(text_ls)
    return text


def process_text(text):
    """
    Process and clean the input text.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: The cleaned and processed text.
    """

    
    stop_words = set(stopwords.words("english"))

    text = text.replace(".", " ")
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    tokens = nltk.word_tokenize(text)

    tokens = [token for token in tokens if token not in stop_words]

    cleaned_text = " ".join(tokens)

    return cleaned_text


def process_embedding(embeddings):
    """
    Process and reduce the dimensionality of the input embeddings.

    Args:
        embeddings: The input embeddings to be processed
                    and reduced in dimension.

    Returns:
        numpy.ndarray: The processed and reduced-dimensional embeddings.
    """
    # Perform Z-Score normalization
    embeddings = StandardScaler().fit_transform(embeddings)

    # Perform t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=2)
    encodings_2d = tsne.fit_transform(embeddings)

    return encodings_2d
