import torch, os
import pandas as pd
from transformers import RobertaTokenizerFast, RobertaModel
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
from sklearn.utils.class_weight import compute_class_weight

class DeepLearningMetaphorDetector:
    def __init__(self, language: str = 'en'):
        self.language = language
        self.tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base')
        self.roberta_model = RobertaModel.from_pretrained('roberta-base')
        self.model = torch.nn.Sequential(
            torch.nn.Linear(768, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Linear(256, 2),
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        self.model.to(self.device)
        self.roberta_model.to(self.device)

        if torch.cuda.device_count() > 1:
            print(f"Using {torch.cuda.device_count()} GPUs")
            # Wrap models in DataParallel for multi-GPU support
            self.model = torch.nn.DataParallel(self.model)
            self.roberta_model = torch.nn.DataParallel(self.roberta_model)

    def preprocess_data(self, data_path: str):
        train_data = self._load_data(os.path.join(data_path, 'VUA18', 'train.tsv'))
        test_data = self._load_data(os.path.join(data_path, 'VUA18', 'test.tsv'))
        return train_data, test_data

    def _load_data(self, file_path: str):
        df = pd.read_csv(file_path, sep='\t', header=0)
        df = df[['sentence', 'label', 'POS', 'w_index']]
        df['label'] = df['label'].astype(int)
        data = df.to_dict('records')
        return data

    def train(self, train_data):
        dataset = EmbeddingDataset(train_data, self.tokenizer, self.roberta_model, self.device)

        # class weights to handle imbalanced data
        labels = [item['label'] for item in train_data]
        class_weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)
        class_weights = torch.tensor(class_weights, dtype=torch.float).to(self.device)

        self.loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-4)

        dataloader = DataLoader(dataset, batch_size=10240*4, shuffle=True)
        print(f"Training Deep Learning Model on {self.device}...")

        for epoch in range(3):
            self.model.train()
            total_loss = 0
            for batch in dataloader:
                embeddings = batch['embeddings'].to(self.device)
                labels = batch['labels'].to(self.device)
                outputs = self.model(embeddings)
                loss = self.loss_fn(outputs, labels)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            avg_loss = total_loss / len(dataloader)
            print(f"Epoch {epoch + 1}, Loss: {avg_loss:.4f}")
        print("Deep Learning Model Training Complete.")

    def test(self, test_data):
        dataset = EmbeddingDataset(test_data, self.tokenizer, self.roberta_model, self.device)
        dataloader = DataLoader(dataset, batch_size=10240, shuffle=False)
        self.model.eval()
        y_true = []
        y_pred = []
        with torch.no_grad():
            for batch in dataloader:
                embeddings = batch['embeddings'].to(self.device)
                labels = batch['labels']
                outputs = self.model(embeddings)
                predictions = torch.argmax(outputs, dim=1)
                y_true.extend(labels.cpu().tolist())
                y_pred.extend(predictions.cpu().tolist())
        accuracy = accuracy_score(y_true, y_pred)
        print(f"Deep Learning Model Accuracy: {accuracy * 100:.2f}%")
        print(classification_report(y_true, y_pred, target_names=['Literal', 'Metaphorical']))

    def predict(self, text: str, word_index: int) -> int:
        self.model.eval()
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.roberta_model(**inputs)
            word_embeddings = outputs.last_hidden_state[0]  # Get embeddings for all words
            target_embedding = word_embeddings[word_index].unsqueeze(0)  # Get embedding for target word
            outputs = self.model(target_embedding)
            prediction = torch.argmax(outputs, dim=1).item()
            return prediction


class EmbeddingDataset(Dataset):
    def __init__(self, data, tokenizer, model, device, max_length=128):
        self.samples = data
        self.tokenizer = tokenizer
        self.model = model
        self.device = device
        self.max_length = max_length

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        sentence = sample['sentence']
        label = sample['label']
        word_index = sample['w_index']

        inputs = self.tokenizer(sentence,
                                return_tensors='pt',
                                truncation=True,
                                padding='max_length',
                                max_length=self.max_length)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            word_embeddings = outputs.last_hidden_state[0]  # Get embeddings for all words
            target_embedding = word_embeddings[word_index]  # Get embedding for target word

        item = {
            'embeddings': target_embedding,
            'labels': torch.tensor(label, dtype=torch.long, device=self.device),
            'pos': sample['POS']
        }
        return item
