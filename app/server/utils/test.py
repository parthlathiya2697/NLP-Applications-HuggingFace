# from transformers import PegasusForConditionalGeneration, PegasusTokenizer
# import torch

# src_text = [
#     """ PG&E stated it scheduled the blackouts in response to forecasts for high winds amid dry conditions. The aim is to reduce the risk of wildfires. Nearly 800 thousand customers were scheduled to be affected by the shutoffs which were expected to last through at least midday tomorrow."""
# ]

# model_name = "google/pegasus-xsum"
# device = "cuda" if torch.cuda.is_available() else "cpu"
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
# batch = tokenizer(src_text, truncation=True, padding="longest", return_tensors="pt").to(device)
# translated = model.generate(**batch)
# tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
# assert (
#     tgt_text[0]
#     == "California's largest electricity provider has turned off power to hundreds of thousands of customers."
# )


# from transformers import T5Tokenizer, T5ForConditionalGeneration

# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

# input_ids = tokenizer("translate English to Spanish: The house is wonderful.", return_tensors="pt").input_ids
# outputs = model.generate(input_ids)
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))



# import torch
# from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
# model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

# inputs = tokenizer("Very bad morning", return_tensors="pt")

# with torch.no_grad():
#     logits = model(**inputs).logits

# predicted_class_id = logits.argmax().item()
# print('\n\n')
# print(model.config.id2label[predicted_class_id])


# from transformers import RobertaTokenizer, RobertaForQuestionAnswering
# import torch

# tokenizer = RobertaTokenizer.from_pretrained("deepset/roberta-base-squad2")
# model = RobertaForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

# question, text = "Who was Jim Henson?", "Jim Henson was a nice puppet"

# inputs = tokenizer(question, text, return_tensors="pt")
# with torch.no_grad():
#     outputs = model(**inputs)

# answer_start_index = outputs.start_logits.argmax()
# answer_end_index = outputs.end_logits.argmax()

# predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
# print(tokenizer.decode(predict_answer_tokens))



# from transformers import GPT2Tokenizer, GPT2LMHeadModel

# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# model = GPT2LMHeadModel.from_pretrained("gpt2")

# inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
# outputs = model.generate(inputs.input_ids, labels=inputs["input_ids"], temperature = 1.0, k=400, 
# p=0.9, repetition_penalty = 1.0, num_return_sequences = 1, length = 1000)
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))


from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# training
input_ids = tokenizer("The <extra_id_0> walks in <extra_id_1> park", return_tensors="pt").input_ids
labels = tokenizer("<extra_id_0> cute dog <extra_id_1> the <extra_id_2>", return_tensors="pt").input_ids
outputs = model(input_ids=input_ids, labels=labels)
loss = outputs.loss
logits = outputs.logits

# inference
input_ids = tokenizer(
    "summarize: studies have shown that owning a dog is good for you", return_tensors="pt"
).input_ids  # Batch size 1
outputs = model.generate(input_ids, length = 1000)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# studies have shown that owning a dog is good for you.