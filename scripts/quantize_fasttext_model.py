import fasttext

model_path = 'models/fasttext-sentiment-model.ftz'
# model_path = 'models/fasttext-sentiment-model-quantized.ftz'

print(f"Loading model from {model_path}")
model = fasttext.load_model(model_path)

print("Quantizing model")
model.quantize(input=model_path, qnorm=True, retrain=True)

print("Saving quantized model to models/fasttext-sentiment-model-quantized.ftz")
model.save_model("models/fasttext-sentiment-model-quantized.ftz")
