import csv
import random
from pathlib import Path
import re

import pandas as pd

from variables import (
    ACTION_NAMES,
    ADD_ATTRIBUTE_INTENT,
    ADD_METHOD_INTENT,
    ADD_RELATION_INTENT,
    ATTRIBUTE_NAMES,
    ATTRIBUTE_TYPES,
    CHANGE_DATATYPE_INTENT,
    CHANGE_NAME_INTENT,
    CHANGE_VISIBILITY_INTENT,
    CONTAINER_ABSTRACTIONS,
    CONTAINER_NAMES,
    CONTAINER_TYPES,
    CREATE_CONTAINER_INTENT,
    DATATYPES,
    DELETE_INTENT,
    DIRECTIONS,
    FOCUS_INTENT,
    METHOD_TYPES,
    MOVE_INTENT,
    RELATION_TYPES,
    TEMPLATE_QUERIES,
    UNDO_INTENT,
    VISIBILITIES,
)

NUMBER_QUERIES_PER_INTENT = 5000  # Adjust as needed
INTENTS = TEMPLATE_QUERIES.keys()
TRAINING_FILE_PATH = "./generated_queries/nlp_training_data.csv"
TEST_FILE_PATH = "./generated_queries/nlp_test_data.csv"


def remove_punctuation(text):
            # Define a regular expression pattern for punctuation
            pattern = r"[^\w\s]"  # This pattern matches anything that is not a word character or whitespace
            # Replace matched patterns with an empty string
            cleaned_text = re.sub(pattern, "", text)
            return re.sub(" +", " ", cleaned_text).strip()

def generate_create_container_sentence():
    template = random.choice(TEMPLATE_QUERIES[CREATE_CONTAINER_INTENT])
    container_abstraction = (
        random.choice(CONTAINER_ABSTRACTIONS) if random.random() < 0.2 else ""
    )
    element_type = random.choice(CONTAINER_TYPES)
    element_name = random.choice(CONTAINER_NAMES)

    sentence = template.format(
        container_abstraction=container_abstraction,
        element_type=element_type,
        element_name=element_name,
    )

    entities = {
        "container_abstraction": container_abstraction,
        "element_type": element_type,
        "element_name": element_name,
    }

    return {"text": sentence, "intent": CREATE_CONTAINER_INTENT, "entities": entities}


def generate_add_attribute_sentence():
    template = random.choice(TEMPLATE_QUERIES[ADD_ATTRIBUTE_INTENT])

    datatype = random.choice(DATATYPES)
    element_name = random.choice(ATTRIBUTE_NAMES)
    visibility = random.choice(VISIBILITIES) if random.random() < (0.5) else ""
    element_type = random.choice(ATTRIBUTE_TYPES)

    datatype_prefix = random.choice(
        ["of type ", "with datatype ", " with the type ", " with the datatype "]
    )

    datatype_str = datatype_prefix + datatype if random.random() < (0.7) else ""

    sentence = template.format(
        datatype=datatype_str,
        element_name=element_name,
        visibility=visibility,
        element_type=element_type,
    )

    entities = {
        "datatype": datatype if datatype_str != "" else "",
        "element_type": element_type,
        "element_name": element_name,
        "visibility": visibility,
    }

    return {
        "text": sentence,
        "intent": ADD_ATTRIBUTE_INTENT,
        "entities": entities,
    }


def generate_add_method_sentence():
    template = random.choice(TEMPLATE_QUERIES[ADD_METHOD_INTENT])

    element_name = random.choice(ACTION_NAMES)
    visibility = random.choice(VISIBILITIES) if random.random() < (0.5) else ""
    element_type = random.choice(METHOD_TYPES)

    sentence = template.format(
        element_name=element_name,
        visibility=visibility,
        element_type=element_type,
    )

    entities = {
        "element_name": element_name,
        "visibility": visibility,
        "element_type": element_type,
    }

    return {
        "text": sentence,
        "intent": ADD_METHOD_INTENT,
        "entities": entities,
    }


def generate_update_value_sentence(intent, target):
    template = random.choice(TEMPLATE_QUERIES[intent])

    new_value = random.choice(target)

    sentence = template.format(new_value=new_value)

    entities = {"new_value": new_value}

    return {"text": sentence, "intent": intent, "entities": entities}


def generate_add_relation_sentence():
    template = random.choice(TEMPLATE_QUERIES[ADD_RELATION_INTENT])

    class_name_from = random.choice(CONTAINER_NAMES)
    class_name_to = random.choice(CONTAINER_NAMES)
    relation_type = random.choice(RELATION_TYPES)
    element_name = random.choice(
        ATTRIBUTE_NAMES
    )  # todo check if attribute names represent actual values

    sentence = template.format(
        class_name_from=class_name_from,
        class_name_to=class_name_to,
        relation_type=relation_type,
        element_name=element_name,
    )

    entities = {
        "class_name_from": class_name_from,
        "class_name_to": class_name_to,
        "relation_type": relation_type,
        "element_name": element_name,
    }

    return {"text": sentence, "intent": ADD_RELATION_INTENT, "entities": entities}


def generate_focus_or_delete_sentence(intent, element_types, target):
    template = random.choice(TEMPLATE_QUERIES[intent])

    element_name = random.choice(target)
    element_type = random.choice(element_types) if random.random() < (0.5) else ""

    sentence = template.format(
        element_type=element_type,
        element_name=element_name,
    )

    entities = {
        "element_type": element_type,
        "element_name": element_name,
    }

    return {"text": sentence, "intent": intent, "entities": entities}


def generate_move_sentence():
    template = random.choice(TEMPLATE_QUERIES[MOVE_INTENT])

    direction = random.choice(DIRECTIONS)
    element_type = "class"
    element_name = random.choice(CONTAINER_NAMES)

    sentence = template.format(
        direction=direction, element_type=element_type, element_name=element_name
    )

    entities = {
        "direction": direction,
        "element_type": element_type,
        "element_name": element_name,
    }

    return {"text": sentence, "intent": MOVE_INTENT, "entities": entities}


def generate_undo_sentence():
    sentence = random.choice(TEMPLATE_QUERIES[UNDO_INTENT])

    return {"text": sentence, "intent": UNDO_INTENT, "entities": {}}


def generate_sentence(intent) -> list:
    retVal = []
    if intent == CREATE_CONTAINER_INTENT:
        retVal.append(generate_create_container_sentence())
    elif intent == ADD_ATTRIBUTE_INTENT:
        retVal.append(generate_add_attribute_sentence())
    elif intent == ADD_METHOD_INTENT:
        retVal.append(generate_add_method_sentence())
    elif intent == CHANGE_NAME_INTENT:
        retVal.append(
            generate_update_value_sentence(CHANGE_NAME_INTENT, CONTAINER_NAMES)
        )
        retVal.append(generate_update_value_sentence(CHANGE_NAME_INTENT, ACTION_NAMES))
        retVal.append(
            generate_update_value_sentence(CHANGE_NAME_INTENT, ATTRIBUTE_NAMES)
        )
    elif intent == CHANGE_VISIBILITY_INTENT:
        retVal.append(
            generate_update_value_sentence(CHANGE_VISIBILITY_INTENT, VISIBILITIES)
        )
    elif intent == CHANGE_DATATYPE_INTENT:
        retVal.append(generate_update_value_sentence(CHANGE_DATATYPE_INTENT, DATATYPES))
    elif intent == DELETE_INTENT:
        retVal.append(
            generate_focus_or_delete_sentence(
                DELETE_INTENT, CONTAINER_TYPES, CONTAINER_NAMES
            )
        )
        retVal.append(
            generate_focus_or_delete_sentence(
                DELETE_INTENT, ATTRIBUTE_TYPES, ATTRIBUTE_NAMES
            )
        )
        retVal.append(
            generate_focus_or_delete_sentence(DELETE_INTENT, METHOD_TYPES, ACTION_NAMES)
        )
    elif intent == ADD_RELATION_INTENT:
        retVal.append(generate_add_relation_sentence())
    elif intent == FOCUS_INTENT:
        retVal.append(
            generate_focus_or_delete_sentence(
                FOCUS_INTENT, CONTAINER_TYPES, CONTAINER_NAMES
            )
        )
        retVal.append(
            generate_focus_or_delete_sentence(
                FOCUS_INTENT, ATTRIBUTE_TYPES, ATTRIBUTE_NAMES
            )
        )
        retVal.append(
            generate_focus_or_delete_sentence(FOCUS_INTENT, METHOD_TYPES, ACTION_NAMES)
        )
    elif intent == MOVE_INTENT:
        retVal.append(generate_move_sentence())
    elif intent == UNDO_INTENT:
        retVal.append(generate_undo_sentence())
    else:
        raise NotImplementedError()
    for s in retVal:
        s["text"] = remove_punctuation(s["text"])

    return retVal


if __name__ == "__main__":
    training_data = []
    test_data = []

    for _ in range(NUMBER_QUERIES_PER_INTENT):
        for curr_intent in INTENTS:
            training_data.extend(generate_sentence(curr_intent))
            test_data.extend(generate_sentence(curr_intent))

    df_training = pd.DataFrame(training_data)
    df_test = pd.DataFrame(test_data)

    Path(TRAINING_FILE_PATH).parent.mkdir(parents=True, exist_ok=True)

    df_training.to_csv(
        TRAINING_FILE_PATH,
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
    )
    df_test.to_csv(
        TEST_FILE_PATH,
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
    )

    print(f"Generated data at: \n\t {TRAINING_FILE_PATH} \n\t {TEST_FILE_PATH}")
