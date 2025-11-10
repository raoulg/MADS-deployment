import random
import string

import tokenizers as tk
import torch
from torch import nn


def buildBPE(corpus: list[str], vocab_size: int) -> tk.Tokenizer:
    tokenizer = tk.Tokenizer(tk.models.BPE(unk_token="<unk>"))  # type: ignore
    trainer = tk.trainers.BpeTrainer(  # type: ignore
        vocab_size=vocab_size,
        min_frequency=1,
        special_tokens=["<pad>", "<s>", "</s>", "<unk>", "<mask>"],
    )

    # handle spaces better by removing the prefix space
    tokenizer.pre_tokenizer = tk.pre_tokenizers.ByteLevel(add_prefix_space=False)  # type: ignore
    tokenizer.decoder = tk.decoders.ByteLevel()  # type: ignore

    # train the BPE model
    tokenizer.train_from_iterator(corpus, trainer)
    tokenizer.enable_padding(pad_id=0, pad_token="<pad>")
    return tokenizer


class SlangRNN(nn.Module):
    def __init__(self, config: dict):
        super(SlangRNN, self).__init__()
        self.config = config
        self.num_layers = config["num_layers"]

        self.embedding = nn.Embedding(config["vocab_size"], config["embedding_dim"])
        self.project = nn.Linear(config["embedding_dim"], config["hidden_dim"])
        self.rnn = nn.RNN(
            config["embedding_dim"],
            config["hidden_dim"],
            batch_first=True,
            dropout=0.2,
            num_layers=self.num_layers,
        )
        self.norm = nn.LayerNorm(config["hidden_dim"])
        self.activation = nn.GELU()
        self.fc = nn.Linear(config["hidden_dim"], config["vocab_size"])

    def forward(self, x, hidden):
        embedded = self.embedding(x)
        identity = self.project(embedded.clone())
        x, hidden = self.rnn(embedded, hidden)
        x = self.norm(x + identity)
        x = self.activation(x)
        x = self.fc(x)
        return x, hidden

    def init_hidden(self, x):
        return torch.zeros(self.num_layers, x.shape[0], self.config["hidden_dim"])


def generate_word(start_letter, model, tokenizer, max_length, temperature=1.0):
    start_token_idx = tokenizer.encode("<s>").ids[0]
    start_letter_idx = tokenizer.encode(start_letter).ids[0]
    input_seq = torch.tensor([[start_token_idx, start_letter_idx]], dtype=torch.long)

    generated_word = [start_letter_idx]
    hidden = model.init_hidden(input_seq)
    for _ in range(max_length - 1):
        with torch.no_grad():
            output, hidden = model(input_seq, hidden)
        output = output.squeeze(0)
        output = output[-1, :].view(-1).div(temperature).exp()
        next_token = torch.multinomial(output, 1).item()
        if next_token == tokenizer.token_to_id("<pad>"):
            break
        generated_word.append(next_token)
        input_seq = torch.tensor([generated_word], dtype=torch.long)
    return tokenizer.decode(generated_word)


def sample_n(
    corpus: list[str], n: int, model, tokenizer, max_length=20, temperature=1.0
) -> list[str]:
    words = [w[3:-4] for w in corpus]  # remove start/stop tokens
    output_words = []
    for _ in range(n):
        random_start_letter = random.choice(string.ascii_lowercase)
        new_word = generate_word(
            random_start_letter,
            model,
            tokenizer,
            max_length=max_length,
            temperature=temperature,
        )
        if new_word not in words:
            output_words.append(new_word)
    return output_words
