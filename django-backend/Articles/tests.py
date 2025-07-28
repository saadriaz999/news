from django.test import TestCase

# from transformers import T5Tokenizer, T5ForConditionalGeneration
#
# # Create your tests here.
# import os
# from Summarizer.settings import BASE_DIR
#
# path = os.path.join(BASE_DIR, "media", "ml_models", "flan-t5-small-cnn_dailymail")
# model = T5ForConditionalGeneration.from_pretrained(path)
# tokenizer = T5Tokenizer.from_pretrained(path)
#
# text = """
# "If you click 'Accept all', we and our partners, including 239 who are part of the IAB Transparency &amp; Consent Framework, will also store and/or access information on a device (in other words, use … [+702 chars]"
# """
# input_text = "summarize: " + text
# inputs = tokenizer(input_text, return_tensors="pt", max_length=1000, truncation=True)
# summary_ids = model.generate(inputs.input_ids, max_length=150, min_length=30, length_penalty=2.0, num_beams=1)
# summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
# print(summary)


