# -*- coding: utf-8 -*-
"""app_creation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sguK4GohScbDFj7Toyodw7faqhPrfc1a
"""

import json
import torch
import gradio as gr
import onnxruntime as rt
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

with open("encoded_keywords.json", "r") as fp:
  encode_keywords = json.load(fp)

keywords = list(encode_keywords.keys())

inf_session = rt.InferenceSession('bert_quantized.onnx')
input_name = inf_session.get_inputs()[0].name
output_name = inf_session.get_outputs()[0].name

def classify_keywords(abstract):
  input_ids = tokenizer(abstract)['input_ids'][:512]

  logits = inf_session.run([output_name], {
      input_name: [input_ids]
  })[0]

  logits = torch.FloatTensor(logits)

  probs = torch.sigmoid(logits)[0]

  return dict(zip(keywords, map(float, probs)))

label = gr.Label(num_top_classes = 5)

interface = gr.Interface(
    fn = classify_keywords,
    inputs = "text",
    outputs = label
  )

interface.launch()







