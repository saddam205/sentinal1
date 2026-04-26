import os
import torch
import json
from datasets import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)

from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# ==============================
# CONFIG
# ==============================
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"
OUTPUT_DIR = "./models/deepseek_lora"
DATA_PATH = "./training/final_cyber_dataset.jsonl"   # ✅ FIXED PATH

MAX_LENGTH = 128
BATCH_SIZE = 1
GRAD_ACCUM = 16
EPOCHS = 2
LR = 2e-4

os.makedirs(OUTPUT_DIR, exist_ok=True)

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

print("🚀 DeepSeek LoRA Training (FINAL)")
print(f"📌 Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")

# ==============================
# TOKENIZER
# ==============================
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# ==============================
# QUANTIZATION
# ==============================
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# ==============================
# MODEL
# ==============================
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
    dtype=torch.float16   # ✅ FIXED (no warning)
)

model = prepare_model_for_kbit_training(model)
model.config.use_cache = False

# ==============================
# LoRA
# ==============================
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ==============================
# LOAD DATA
# ==============================
print("\n📚 Loading dataset...")

data = []

if os.path.exists(DATA_PATH):
    print(f"✅ Using dataset: {DATA_PATH}")

    with open(DATA_PATH) as f:
        for line in f:
            try:
                sample = json.loads(line)

                # ✅ FIX: Support BOTH formats
                if "text" in sample:
                    data.append({"text": sample["text"]})
                elif "question" in sample and "answer" in sample:
                    text = f"<|user|>\n{sample['question']}\n<|assistant|>\n{sample['answer']}"
                    data.append({"text": text})

            except Exception as e:
                continue
else:
    print("⚠️ Dataset not found → fallback mode")

    base_data = [
        ("What is SQL injection?", "SQL injection is a vulnerability where attackers inject malicious SQL queries."),
        ("Explain XSS attack", "XSS allows attackers to inject scripts."),
    ]

    data = [{"text": f"<|user|>\n{q}\n<|assistant|>\n{a}"} for q, a in base_data] * 200

print(f"📊 Total samples: {len(data)}")

dataset = Dataset.from_list(data)

# ==============================
# TOKENIZE
# ==============================
def tokenize(example):
    tokens = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

dataset = dataset.map(tokenize, remove_columns=["text"])

# ==============================
# SPLIT (SAFE)
# ==============================
dataset = dataset.train_test_split(test_size=0.1, seed=42)

train_dataset = dataset["train"]
val_dataset = dataset["test"]

# ==============================
# TRAINING CONFIG (COMPATIBLE)
# ==============================
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM,
    num_train_epochs=EPOCHS,
    logging_steps=50,
    save_steps=500,
    save_total_limit=2,
    fp16=True,
    learning_rate=LR,
    warmup_ratio=0.05,
    lr_scheduler_type="cosine",
    optim="paged_adamw_8bit",
    report_to="none",
    remove_unused_columns=False,
    gradient_checkpointing=True,
    max_grad_norm=0.3
    # ❌ REMOVED evaluation_strategy (not supported in your version)
)

# ==============================
# TRAINER
# ==============================
trainer = Trainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    args=training_args,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

# ==============================
# TRAIN
# ==============================
print("\n🔥 Training started...")
trainer.train()

# ==============================
# SAVE
# ==============================
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"\n✅ Model saved → {OUTPUT_DIR}")

# ==============================
# TEST
# ==============================
print("\n🧪 Testing model...")

model.eval()

prompt = "<|user|>\nAnalyze this network traffic\n<|assistant|>\n"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        temperature=0.7,
        do_sample=True,
        repetition_penalty=1.1
    )

print("\n🤖 Response:")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))