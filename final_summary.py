# import and initialize the tokenizer and model from the checkpoint
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import nltk
def generate_summary(file_text):
  summary_text = []

  # dividing the text into chuncks
  FileContent = file_text.strip()

  # checkpoint = "sshleifer/distilbart-cnn-12-6"
  checkpoint = "philschmid/bart-large-cnn-samsum"

  tokenizer = AutoTokenizer.from_pretrained(checkpoint)
  model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

  # extract the sentences from the document

  nltk.download('punkt')
  sentences = nltk.tokenize.sent_tokenize(FileContent)

  # Create the chunks

  # initialize
  length = 0
  chunk = ""
  chunks = []
  count = -1
  for sentence in sentences:
    count += 1
    combined_length = len(tokenizer.tokenize(sentence)) + length # add the no. of sentence tokens to the length counter

    if combined_length  <= tokenizer.max_len_single_sentence: # if it doesn't exceed
      chunk += sentence + " " # add the sentence to the chunk
      length = combined_length # update the length counter

      # if it is the last sentence
      if count == len(sentences) - 1:
        chunks.append(chunk.strip()) # save the chunk
      
    else: 
      chunks.append(chunk.strip()) # save the chunk
      
      # reset 
      length = 0 
      chunk = ""

      # take care of the overflow sentence
      chunk += sentence + " "
      length = len(tokenizer.tokenize(sentence))
  len(chunks)

  # Some checks

  [len(tokenizer.tokenize(c)) for c in chunks]

  [len(tokenizer(c).input_ids) for c in chunks]

  # inputs to the model
  inputs = [tokenizer(chunk, return_tensors="pt") for chunk in chunks]

  for input in inputs:
    output = model.generate(**input)
    summary_text1 = (tokenizer.decode(*output, skip_special_tokens=True))
    summary_text.append(summary_text1)

  print(summary_text)
  return summary_text

