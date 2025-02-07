import fasttext


# Train a FastText model
model = fasttext.train_supervised("data/fasttext/train.ft.txt")

# Save model
model.save_model('models/fasttext-sentiment-model.ftz')
