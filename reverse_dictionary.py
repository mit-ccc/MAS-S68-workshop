#!/usr/bin/env python3

"""
Code for the MAS.S68 (Generative AI for Constructive Communication) programming workshop

Reverse dictionary (description-to-word guesser) using the OpenAI GPT-3 API

Prompts and evaluation data are in data/train.jsonl and data/test.jsonl respectively
and were produced by ./pull_rd_data.py
"""

import json
import os
import openai
import re

# The number of examples from data/train.jsonl to include in the prompt.  If 0, use a separate 0-shot prompt
_NUM_FEW_SHOT_EXAMPLES = 5

# The OpenAI model to use
_MODEL = "text-curie-001"
# _MODEL = "text-davinci-003"  # Uncomment to use the highest-powered model

# Don't forget to set your OPENAI_API_KEY environment variable.
# Or set it here directly (but don't check it into a git repo.)
openai.api_key = os.getenv("OPENAI_API_KEY")


def call_gpt3_api(prompt, model="text-davinci-003"):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response


def definition_to_zero_shot_prompt(definition):
    return 'What are some words that mean "%s"?\n\n' % (definition)


def definition_to_few_shot_prompt(definition, examples):
    instructions = "Please find words that mean the same thing as the given definition.  For example:\n\n"
    target = {
        "definition": definition,
        "word": "",
    }  # placeholder for the word we're looking for
    # Format the example text as a bulleted list
    example_text = "\n".join(
        [
            '- "%s": %s' % (example["definition"], example["word"])
            for example in examples + [target]
        ]
    )
    return instructions + example_text


def response_to_completion_text(openai_response):
    return openai_response["choices"][0]["text"]


def completion_text_to_first_word(s):
    words = re.sub("[^A-Za-z]", " ", s.strip()).split()
    if words:
        return words[0]
    else:
        # Return empty string if it produces no answer
        return ""


def get_best_word_for_definition(definition, examples_to_use=None):
    if not examples_to_use:
        prompt = definition_to_zero_shot_prompt(definition)
    else:
        prompt = definition_to_few_shot_prompt(definition, examples_to_use)

    openai_response = call_gpt3_api(prompt, model=_MODEL)
    completion = response_to_completion_text(openai_response)
    first_word = completion_text_to_first_word(completion)
    return first_word


def read_batch_of_queries(filename):
    """Reads a set of reverse dictionary train/test records as a list of dictionaries."""
    return [json.loads(line) for line in open(filename, "r").read().strip().split("\n")]


def get_example_queries_for_prompt(filename):
    return read_batch_of_queries(filename)[:_NUM_FEW_SHOT_EXAMPLES]


def run_batch_of_queries(evaluation_queries_filename, prompt_example_queries_filename):
    evaluation_queries = read_batch_of_queries(evaluation_queries_filename)
    if _NUM_FEW_SHOT_EXAMPLES > 0:
        prompt_example_queries = get_example_queries_for_prompt(
            prompt_example_queries_filename
        )
    else:
        prompt_example_queries = None
    num_correct = 0
    for record in evaluation_queries:
        definition = record["definition"]
        record["gpt3_best_word"] = get_best_word_for_definition(
            definition, examples_to_use=prompt_example_queries
        )
        record["gpt3_is_correct"] = (
            record["gpt3_best_word"].lower() == record["word"].lower()
        )
        if record["gpt3_is_correct"]:
            num_correct += 1
        print(json.dumps(record))
    print(
        "Accuracy = %d / %d = %f"
        % (num_correct, len(evaluation_queries), num_correct / len(evaluation_queries))
    )


if __name__ == "__main__":
    #    print(get_best_word_for_definition("clothing that you wear on your head"))   # uncomment to run a single query
    run_batch_of_queries("data/test.jsonl", "data/train.jsonl")
