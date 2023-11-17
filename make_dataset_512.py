from datasets import load_dataset
from transformers import AutoTokenizer
import json

base_model_id = "mistralai/Mistral-7B-v0.1"

tokenizer = AutoTokenizer.from_pretrained(
    base_model_id,
    padding_side="left",
    add_eos_token=True,
    add_bos_token=True,
)
tokenizer.pad_token = tokenizer.eos_token


def formatting_func(example):
    text = f"""Given a context of a post score a comment from 1 to 10.

    ### context: {example['title']} {example['post_text']}
    ### comment: {example['selftext']}

    ### score: {example['grade']}"""
    return text


def generate_and_tokenize_prompt(prompt):
    return tokenizer(formatting_func(prompt))


dataset = load_dataset('json', data_files='datasets/reddit_posts_dataset.json')
tokenized_train_dataset = dataset['train'].map(generate_and_tokenize_prompt)

dataset_file256 = open(f'datasets/reddit_posts_256max_dataset.json', 'w+')
dataset_file512 = open(f'datasets/reddit_posts_512max_dataset.json', 'w+')

count256 = 0
count512 = 0

for x in tokenized_train_dataset:
    if len(x['input_ids']) < 257:
        replie_dict = {}
        replie_dict['title'] = x['title']
        replie_dict['post_text'] = x['post_text']
        replie_dict['grade'] = x['grade']
        replie_dict['selftext'] = x['selftext']
        dataset_file256.write(str(json.dumps(replie_dict))+'\n')
        count256 += 1
    if len(x['input_ids']) < 513:
        replie_dict = {}
        replie_dict['title'] = x['title']
        replie_dict['post_text'] = x['post_text']
        replie_dict['grade'] = x['grade']
        replie_dict['selftext'] = x['selftext']
        dataset_file512.write(str(json.dumps(replie_dict))+'\n')
        count512 += 1

print(count256, count512)
