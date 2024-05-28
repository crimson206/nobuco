import re
import torch
import logging
import os
from db import Item, Session, ItemHolder

logger = logging.getLogger("unittest_automation")
logging.basicConfig(filename=f"{logger.name}.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def find_target_directory(root_dir, target_hint):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if target_hint in dirpath:
            return dirpath
    return None


def load_content(path):
    with open(path, 'r') as file:
            content = file.read()
    return content

def extract_between(text, start, end, multiple=False):
    target = r'(.*?)'
    pattern = re.escape(start) + target + re.escape(end)
    matches = re.findall(pattern, text)

    if multiple:
        results = []
        for match in matches:
            results.append([item.strip() for item in match.strip().split(',')])
        return results
    else:
        if matches:
            return [item.strip() for item in matches[0].strip().split(',')]
        else:
            return None

def get_targets_from_path(path):
    with open(path, 'r') as file:
            content = file.read()
    start = '@converter('
    end = ', channel_ordering_strategy'
    extract_between(content, start, end, multiple=True)

def extract_doc(target):
    split = str(target).split(".")
    if "Tensor" in split:
        docs = getattr(torch.Tensor, split[-1]).__doc__
    elif "F" in split:
        try:
            docs = getattr(torch.nn.functional, split[-1]).__doc__
        except:
            try:
                docs = getattr(torch.functional, split[-1]).__doc__
            except:
                docs = None
    elif "nn" in split:
        docs = getattr(torch.nn, split[-1]).__doc__
    else:
        docs = getattr(torch, split[-1]).__doc__

    return docs

def filter_docs(parsed_docs):
    filtered = []
    for session in parsed_docs:
        if session["header"] in ["Args", "Shape", "Examples", "Example"]:
            filtered.append(session)
    return filtered

def convert_parsed_to_str(parsed_docs):
    formatted_string = ""

    for item in parsed_docs:
        formatted_string += item['header'] + '\n'
        formatted_string += '    ' + item['content'].replace('\n', '\n    ') + '\n\n'
    return formatted_string

def parse_sections(text, header_indent, unit_indent):
    lines = text.split('\n')
    parsed_data = []
    current_header = None
    current_content = []

    for line in lines:
        # Remove leading indentation
        line = line[header_indent:]

        # Check if the line is a header
        if line and line[0].isalpha() and line.strip().endswith(':'):
            # If there's a current header, save its content before starting a new one
            if current_header is not None:
                parsed_data.append({'header': current_header, 'content': '\n'.join(current_content)})
                current_content = []
            # Set new header
            current_header = line.rstrip(':')
        else:
            if current_header is not None:
                # Add line to current content
                current_content.append(line[unit_indent:])

    # Don't forget to save the last header-content pair
    if current_header is not None:
        parsed_data.append({'header': current_header, 'content': '\n'.join(current_content)})

    return parsed_data

def generate_prompt(template, target, doc, example):
    processed_docs = convert_parsed_to_str(filter_docs(doc))
    if len(processed_docs)==0:
        processed_docs = "Not Given"
    
    prompt = template.format(
        target=target,
        doc=processed_docs,
        phase1_example=example
    )
    
    return prompt


def get_preprocessed_itemholder(file_name, target_hint="nobuco/node_converters"):
    # Get the current working directory
    cwd = os.getcwd()
    
    # Find the target directory that contains the hint
    target_directory = find_target_directory(cwd, target_hint)
    
    if target_directory:
        # Construct the full path
        full_path = os.path.join(target_directory, file_name)
    else:
        raise FileNotFoundError(f"Directory containing hint '{target_hint}' not found from {cwd}")
    
    content = load_content(full_path)
    
    start = '@converter('
    end = ', channel_ordering_strategy'
    targets = extract_between(content, start, end, multiple=True)

    itemholder = ItemHolder(
        file_name=file_name
    )

    for target in targets:
        try:
            docs = extract_doc(target[0])
            item = Item(
                name=str(target[0]),
                docs=docs,
            )
            itemholder.items.append(item)
        except Exception as error:
            itemholder.failed_items.append(str(target[0]))
            logger.error(error)

    for item in itemholder.items:
        func_type = parse_sections(item.docs, 0, 4)
        cls_type = parse_sections(item.docs, 4, 4)
        func_type_headers = [session["header"] for session in func_type]
        if any(keyword in func_type_headers for keyword in ["Example", "Examples", "Args"]):
            item.parsed_docs = func_type
        else:
            item.parsed_docs = cls_type

    return itemholder
