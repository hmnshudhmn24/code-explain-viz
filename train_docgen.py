# train_docgen.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_dataset
import argparse

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, default="data_examples/sample_dataset.jsonl", help="jsonl with {'code','doc'}")
    p.add_argument("--output_dir", type=str, default="./code-explain-viz-model")
    p.add_argument("--epochs", type=int, default=1)
    return p.parse_args()

def preprocess_batch(examples, tokenizer, max_src=512, max_tgt=256):
    inputs = ["explain: " + c for c in examples["code"]]
    model_inputs = tokenizer(inputs, truncation=True, padding="max_length", max_length=max_src)
    labels = tokenizer(text_target=examples["doc"], truncation=True, padding="max_length", max_length=max_tgt)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def main():
    args = parse_args()
    model_name = "Salesforce/codet5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    ds = load_dataset("json", data_files={"train": args.data})
    tokenized = ds["train"].map(lambda x: preprocess_batch(x, tokenizer), batched=True, remove_columns=ds["train"].column_names)

    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=2,
        save_strategy="epoch",
        logging_steps=50
    )
    trainer = Seq2SeqTrainer(model=model, args=training_args, train_dataset=tokenized)
    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Saved model to", args.output_dir)

if __name__ == "__main__":
    main()
