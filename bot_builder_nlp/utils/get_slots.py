import re

from Levenshtein import distance


def is_alphanumeric(c):
    r = re.findall(r"[\u00C0-\u1FFF\u2C00-\uD7FF\w]", c)
    return len(r) > 0 and c != "_"


def get_word_positions(text: str):
    at_white_space = True
    last_index = 0
    current_index = 0
    result = []

    while current_index < len(text):
        if is_alphanumeric(text[current_index]):
            if at_white_space:
                last_index = current_index
                at_white_space = False
        elif at_white_space is False:
            result.append({"start": last_index, "end": current_index - 1})
            at_white_space = True
        current_index += 1

    if at_white_space is False:
        result.append({"start": last_index, "end": current_index - 1})

    return result


def get_best_substring(text1: str, text2: str):
    threshold = 0.8
    max_levenshtein = len(text2) * (1 - threshold)
    word_positions = get_word_positions(text1)
    result = []

    for i in range(len(word_positions)):
        for j in range(i, len(word_positions)):
            text3 = text1[word_positions[i]["start"] : word_positions[j]["end"] + 1]
            levenshtein = distance(text3, text2)
            accuracy = (len(text2) - levenshtein) / len(text2)

            if accuracy >= threshold:
                result.append(
                    {
                        "start": word_positions[i]["start"],
                        "end": word_positions[j]["end"],
                    }
                )

            if len(text3) - len(word_positions[0]) >= len(text2) + max_levenshtein:
                break

    return result


def get_slots(utterance: str, entities: list):
    result = {}

    for entity in entities:
        for option in entity["options"]:
            synonyms = option.get("synonyms", [])
            synonyms.append({"name": option["name"]})

            for synonym in synonyms:
                l = get_best_substring(utterance, synonym["name"])

                for pos in l:
                    result[entity["name"]] = utterance[pos["start"] : pos["end"] + 1]

    return result
