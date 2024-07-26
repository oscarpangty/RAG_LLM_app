from transformers import AutoModel, AutoTokenizer

# Specify the model name
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Verify the model and tokenizer are loaded successfully
print("Model and tokenizer loaded successfully")
