import csv
import json
from pathlib import Path

BASE_DIR = Path("data")
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

COMMENTS_FILE = RAW_DIR / "comments.json"
TRAIN_FILE = RAW_DIR / "train-balanced.csv"
TEST_FILE = RAW_DIR / "test-balanced.csv"

OUTPUT_TRAIN_JSON = PROCESSED_DIR / "train_data.json"
OUTPUT_TEST_JSON = PROCESSED_DIR / "test_data.json"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_comments(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def parse_balanced_csv(csv_path, comments_dict):
    samples = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            if len(row) != 3:
                continue
            _, response_ids_part, labels_part = row
            response_ids = response_ids_part.strip().split()
            labels = labels_part.strip().split()

            for rid, label in zip(response_ids, labels):
                if rid in comments_dict:
                    text = comments_dict[rid]['text']
                    samples.append({"text": text, "label": int(label)})
    return samples

def save_to_json(samples, out_path):
    with open(out_path, 'w') as f:
        json.dump(samples, f, indent=2)

def main():
    print("Loading comments.json...")
    comments = load_comments(COMMENTS_FILE)

    print("Processing train-balanced.csv...")
    train_data = parse_balanced_csv(TRAIN_FILE, comments)
    print(f"Saving {len(train_data)} samples to {OUTPUT_TRAIN_JSON}...")
    save_to_json(train_data, OUTPUT_TRAIN_JSON)

    print("Processing test-balanced.csv...")
    test_data = parse_balanced_csv(TEST_FILE, comments)
    print(f"Saving {len(test_data)} samples to {OUTPUT_TEST_JSON}...")
    save_to_json(test_data, OUTPUT_TEST_JSON)

    print("Data Processed")

if __name__ == "__main__":
    main()
