import re
from pathlib import Path

import requests
import torch
from bs4 import BeautifulSoup
from slanggen.custom_logger import logger
from torch.nn.utils.rnn import pad_sequence


def get_data(filename: Path, url: str) -> list[str]:
    logger.info(f"Getting data from {url}")
    # Send a GET request to the website
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the rows
    rows = soup.find_all("tr", style=True)

    # Extract the street language words from the second <td> element in each row
    street_language_words = [row.find_all("td")[1].get_text(strip=True) for row in rows]

    # Process each word: remove text inside parentheses, remove "/g", split on commas and pipes
    logger.info(f"Processing {len(street_language_words)} street language words")
    processed_words = []
    for word in street_language_words:
        # Remove text inside parentheses
        word = re.sub(r"\(.*?\)", "", word)
        # Remove "/g"
        word = word.replace("/g", "")
        # Split on commas and pipes
        split_words = re.split(r",|\||/", word)
        # Strip and add each split word to the processed list
        processed_words.extend([w.strip().lower() for w in split_words])

    # add start and end tokens to each word / sentence
    processed_words = ["<s>" + word + "</s>" for word in processed_words if word]

    # Save the processed words to a file
    logger.info(f"Saving processed words to {filename}")
    with open(filename, "w", encoding="utf-8") as file:
        for word in processed_words:
            file.write(word + "\n")
    return processed_words


def load_data(filename: Path, url: str) -> list[str]:
    if not filename.exists():
        logger.info(f"File {filename} not found. donwloading from {url}")
        processed_words = get_data(filename, url)
    else:
        logger.info(f"Loading processed words from {filename}")
        with open(filename, "r", encoding="utf-8") as file:
            processed_words = [line.strip() for line in file]
    logger.info(f"Loaded {len(processed_words)} words")
    return processed_words


def preprocess(corpus: list[str], tokenizer) -> torch.Tensor:
    encoded_sequences = [tokenizer.encode(word).ids for word in corpus]
    padded_sequences = pad_sequence(
        [torch.tensor(seq) for seq in encoded_sequences], batch_first=True
    )
    return padded_sequences


class ShiftedDataset:
    def __init__(self, sequences: torch.Tensor):
        self.X = sequences[:, :-1]
        self.y = sequences[:, 1:]

    def to(self, device):
        self.X = self.X.to(device)
        self.y = self.y.to(device)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

    def __repr__(self):
        return f"ShiftedDataset {self.X.shape}"
