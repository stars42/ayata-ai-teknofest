from scikit.learn.preprocessing import LabelEncoder
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          pipeline)

model_path = "./bert_ner"
ner_tokenizer = AutoTokenizer.from_pretrained(model_path)
ner = AutoModelForTokenClassification.from_pretrained(model_path)

model_path = "./bert_sa"
sa_tokenizer = AutoTokenizer.from_pretrained(model_path)
sa = AutoModelForTokenClassification.from_pretrained(model_path)

tags = ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]
tag2id = {tag: id for id, tag in enumerate(tags)}
id2tag = {id: tag for id, tag in enumerate(tags)}


def ner_predict_pip(sentence: str):
    ner = pipeline("ner", model=ner, tokenizer=ner_tokenizer)
    return ner(sentence)


def get_entities(ner_result: list):
    entities = []
    for entity in ner_result:
        if entity["entity"][0] == "B":
            entity_word = entity["word"]
            if ner_result.index(entity) + 1 < len(ner_result):
                next_entity = ner_result[ner_result.index(entity) + 1]
                if next_entity["entity"][0] == "I":
                    entity_word += " " + next_entity["word"]
                    i = ner_result.index(entity) + 2
                    while i < len(ner_result) and ner_result[i]["entity"][0] == "I":
                        entity_word += " " + ner_result[i]["word"]
                        i += 1
            entities.append(entity_word)
    return entities


def prepare_inputs(text: str, aspects: list):
    inputs = []
    for aspect in aspects:
        combined_text = f"{text} [ASPECT] {aspect}"
        inputs.append(combined_text)
    return inputs


def sa_predict(prompt: str, entities: list):
    prompt = prepare_inputs(prompt, entities)
    sa = pipeline("sentiment-analysis", model=sa, tokenizer=sa_tokenizer)
    return sa(prompt)


def predict(text_sentence: str):
    ner_result = ner_predict_pip(text_sentence)
    entities = get_entities(ner_result)
    data = sa_predict(text_sentence, entities)
    
    label_encoder = LabelEncoder()
    label_encoder.fit(data['label_text'])
    
    predicted_labels = label_encoder.inverse_transform(data.cpu().numpy())

    results = []
    for aspect, sentiment in zip(entities, predicted_labels):
        results.append({"entity": aspect, "sentiment": sentiment})

    return {
        "entity_list": entities,
        "results": results
    }


__all__ = ["predict"]