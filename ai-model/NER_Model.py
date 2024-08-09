import re
import unicodedata

import pandas as pd

INPUT_DATA_FILE = "data_combined.csv"
OUTPUT_CSV_FILE = "data_masked.csv"

normalize = lambda text: unicodedata.normalize("NFKD", text) \
                                    .encode("ascii", errors="ignore") \
                                    .decode("utf-8")


def load_data(csv_file: str):
    data = pd.read_csv(csv_file)
    texts = data["text"]
    aspects = data["aspect"]

    for index, item in enumerate(zip(texts, aspects)):
        text, aspect = item
        if normalize(text) != text or normalize(aspect) != aspect:
            data.drop(index, inplace=True)

    return data, texts, aspects


def create_tags(texts: list[str], aspects: list[str]) -> pd.DataFrame:
    """
    Bu fonksiyon verilen text ve aspect'lerden oluşan listeleri alır ve aspect'lerin içinde geçtiği kelimeleri bulur.
    """
    labels = []
    sentences = []

    for index, sentence in enumerate(texts):
        words = sentence.split()
        label = []
        wrong_aspect = []
        for word in words:
            # * Burada aspect'lerin içinde geçtiği kelimeleri buluyoruz.
            if re.search(re.escape(aspects[index]), word, flags=re.IGNORECASE):
                label.append("1")
            else:
                label.append("0")
        if check_label(label):
            labels.append(label)
            sentences.append(sentence)
        else:
            wrong_aspect.append(aspects[index])

    return pd.DataFrame({"Sentence": sentences, "Label": labels})


def mask_aspects(text: str, aspects: list[str]) -> str:
    for aspect in aspects:
        text = text.replace(aspect, "[MASK]")
    return text


def check_label(labels: list[str]) -> bool:
    return any(label == "1" for label in labels)


def main(*args):
    data, texts, aspects = load_data(INPUT_DATA_FILE)

    data["aspect"] = data["aspect"].apply(eval)
    data["text"] = data.apply(lambda row: mask_aspects(row["text"], row["aspect"]), axis=1)

    data.to_csv(OUTPUT_CSV_FILE, index=False)

    # TODO devamı Google Colab'da yazılacak
    labels = []
    result_df = create_tags(texts, aspects)


if __name__ == "__main__":
    main()
