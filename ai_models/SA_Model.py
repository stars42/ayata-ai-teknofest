import pandas
import sklearn
import torch
from sklearn.preprocessing import LabelEncoder
from transformers import (AutoModelForTokenClassification,
                          BertForSequenceClassification, BertTokenizer,
                          Trainer, TrainingArguments)

INPUT_FILE = "data.csv"  # Promptların olduğu dosya
LABELS_FILE = "labels.txt"  # Etiketlenmiş verilerin olduğu dosya

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForTokenClassification.from_pretrained(
    "dbmdz/bert-base-turkish-128k-uncased", num_labels=3  # + - N
).to(device)

tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")
model = BertForSequenceClassification.from_pretrained("dbmdz/bert-base-turkish-cased", num_labels=3)


class ABSADataset(torch.utils.data.Dataset):
    def _init_(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def _getitem_(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def _len_(self):
        return len(self.labels)


def preprocess_data(df):
    inputs = []
    labels = []
    for _, row in df.iterrows():
        text = row["text"]
        aspect = row["aspect"]
        label = row["label_text"]

        combined_text = f"{text} [ASPECT] {aspect}"
        inputs.append(combined_text)
        labels.append(label)

    encodings = tokenizer(inputs, truncation=True, padding=True, max_length=512)
    return ABSADataset(encodings, labels)


def main(*args):
    data = pandas.read_csv(INPUT_FILE)

    label_encoder = LabelEncoder()
    data["label_text"] = label_encoder.fit_transform(data["label_text"])

    train_dataset, test_dataset = sklearn.model_selection.train_test_split(data, test_size=0.2)

    train_dataset = preprocess_data(train_dataset)
    test_dataset = preprocess_data(test_dataset)

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=100,
        per_device_eval_batch_size=100,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=test_dataset)

    trainer.train()


if __name__ == "__main__":
    main()
