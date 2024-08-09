from numpy import argmax, ndarray
import pandas as pd
import torch
from datasets import Dataset, load_metric
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          Trainer, TrainingArguments)


INPUT_DATA_FILE = "train.txt"  # Veri setinin olduğu dosya
LABELS_FILE = "labels.txt"  # Etiketlenmiş verilerin olduğu dosya

tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-128k-uncased")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForTokenClassification.from_pretrained(
    "dbmdz/bert-base-turkish-128k-uncased", num_labels=len(tag2id)
).to(device)
metric = load_metric("seqeval") 


def load_and_label(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    sentences = []
    labels = []
    current_sentence = []
    current_labels = []

    for line in lines:
        if line := line.strip():
            word, label = line.split()
            current_sentence.append(word)
            current_labels.append(label)
        else:
            if current_sentence:
                sentences.append(current_sentence)
                labels.append(current_labels)
                current_sentence = []
                current_labels = []
        
    if current_sentence:
        sentences.append(current_sentence)
        labels.append(current_labels)

    return sentences, labels


def mask_aspects(text: str, aspects: list[str]) -> str:
    for aspect in aspects:
        text = text.replace(aspect, "[MASK]")
    return text


def check_label(labels: list[str]) -> bool:
    return any(label == "1" for label in labels)


def get_labels(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        return [i.rstrip() for i in file.readlines()]


def encode_tags(tags: list[str], tag2id: dict[str, int]) -> list[int]:
    return [tag2id[tag] for tag in tags]


def tokenize_and_align_labels(examples: dict):
    tokenized_inputs = tokenizer(
        examples["sentences"], padding="max_length", max_length=512, truncation=True, is_split_into_words=True
    )
    labels = []
    for i, label in enumerate(examples["labels"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            else:
                label_ids.append(label[word_idx])
        label_ids += [-100] * (512 - len(label_ids))
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


def compute_metrics(p: tuple[ndarray, ndarray]):
    predictions, labels = p
    predictions = argmax(predictions, axis=2)

    true_predictions = [
        [id2tag[p] for (p, l) in zip(prediction, label) if l != -100] for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [id2tag[l] for (p, l) in zip(prediction, label) if l != -100] for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


def main(*args):
    global tag2id, id2tag

    sentences, labels = load_and_label(INPUT_DATA_FILE)
    labels = get_labels(LABELS_FILE)

    data = pd.DataFrame({"sentences": sentences, "labels": labels})

    tag2id = {tag: id for id, tag in enumerate(labels)}
    id2tag = {id: tag for id, tag in enumerate(labels)}

    data["labels"] = data["labels"].apply(lambda x: encode_tags(x, tag2id))
    train_data = Dataset.from_pandas(data)

    tokenized_dataset = train_data.map(tokenize_and_align_labels, batched=True)

    train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
    tokenized_train_dataset = train_test_split["train"]
    tokenized_test_dataset = train_test_split["test"]

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_dataset,
        tokenizer=tokenizer,
        eval_dataset=tokenized_test_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.train()


if __name__ == "__main__":
    main()
