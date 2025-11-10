import json
import os
import tomllib
from pathlib import Path

import torch
from slanggen import datatools, models
from slanggen.custom_logger import logger
# from loguru import logger
from torch import nn, optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    # get config
    configfile = Path("slanggen.toml").resolve()
    with configfile.open(mode="rb") as f:
        config = tomllib.load(f)

    # load data
    datafile = Path(config["data"]["assets_dir"]) / config["data"]["filename"]
    url = config["data"].get("url")

    # preprocess to DataLoader
    processed_words = datatools.load_data(datafile, url)
    tokenizer = models.buildBPE(
        corpus=processed_words, vocab_size=config["model"]["vocab_size"]
    )
    padded_sequences = datatools.preprocess(processed_words, tokenizer)
    dataset = datatools.ShiftedDataset(padded_sequences)
    loader = DataLoader(
        dataset,  # type: ignore
        batch_size=config["training"]["batch_size"],
        shuffle=True,
    )

    # train model
    model, history = train(loader, tokenizer.get_vocab_size(), config)

    # save artefacts
    artefacts_dir = Path(config["data"]["artefacts_dir"])
    tfile = artefacts_dir / "tokenizer.json"
    tokenizer.save(str(tfile))

    torch.save(model.state_dict(), artefacts_dir / "model.pth")
    # save config to artefacts folder
    with open(artefacts_dir / "config.json", "w") as f:
        f.write(json.dumps(config, indent=4))
    logger.info(f"Model and tokenizer saved to {artefacts_dir}")

    history_file = artefacts_dir / "history.txt"
    with open(history_file, "w") as f:
        f.write("\n".join(map(str, history)))
    logger.info(f"Training history saved to {history_file}")


def train(loader, vocab_size: int, config: dict):
    modelconfig = {
        "vocab_size": vocab_size,
        "embedding_dim": config["model"]["embedding_dim"],
        "hidden_dim": config["model"]["hidden_dim"],
        "num_layers": config["model"]["num_layers"],
    }
    model = models.SlangRNN(modelconfig)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config["training"]["learning_rate"])
    scheduler = ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=config["training"]["factor"],
        patience=config["training"]["patience"],
        min_lr=config["training"]["min_lr"],
    )
    epochs = config["training"]["epochs"]
    history = []
    last_lr = 0.0

    for epoch in range(epochs):
        loss = 0.0

        for x, y in loader:
            optimizer.zero_grad()
            hidden = model.init_hidden(x)

            output, hidden = model(x, hidden)

            loss += loss_fn(output.view(-1, vocab_size), y.view(-1))

        loss.backward()  # type: ignore
        optimizer.step()
        scheduler.step(loss)
        history.append(loss.item())  # type: ignore
        curr_lr = scheduler.get_last_lr()[0]

        if (epoch + 1) % 10 == 0:
            logger.info(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")  # type: ignore
            if last_lr != curr_lr:
                last_lr = curr_lr
                logger.info(f"Current learning rate: {curr_lr}")
    return model, history


if __name__ == "__main__":
    main()
