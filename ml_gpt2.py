from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import string
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = ''
# def generate_text(prompt, max_length=100):
#     # Load pre-trained model and tokenizer
#     model = GPT2LMHeadModel.from_pretrained('gpt2')
#     tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

#     # Set the pad token
#     tokenizer.pad_token = tokenizer.eos_token

#     # Encode the input prompt
#     input_ids = tokenizer.encode(prompt, return_tensors='pt', add_special_tokens=True) #return_tensors says use pytorch

#     # Create attention mask
#     attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)

#     # Generate text
#     output = model.generate(
#         input_ids, #the prompt tokenized
#         attention_mask=attention_mask,
#         max_length=max_length, #the max length of the text, including the input prompt
#         num_return_sequences=1, #The num of different sequences to generate, maybe generates two responses to the same prompt if its two
#         no_repeat_ngram_size=2, #determines the size of n-grams (phrases of n words) to not repeat, so here this won't repeat bigrams
#         do_sample=True,
#         top_k=50, #limits the next token to the k most likely tokens 1 to vocab size, usually 10-100
#         top_p=0.95, #limits the next token to a subset of tokens with a cummulative probabilaty higher than p 0 to 1, commonly .9 o 1
#         temperature=0.7, # controls the randomness in generatino, lower more deterministic, higher more random, 0 to 1, commonly .5 to 1
#         pad_token_id=tokenizer.eos_token_id
#     )

#     # Decode and return the generated text
#     generated_text = tokenizer.decode(output[0], skip_special_tokens=True) #special tokens are things like endofText, so that is not put back in
#     return generated_text


def generate_text(prompt, max_length=100):
    """
    Generate text using a pre-trained GPT-2 model.

    Args:
    prompt (str): The initial text to start generation from.
    max_length (int): The maximum length of the generated text.

    Returns:
    str: The generated text.
    """
    # Load pre-trained model and tokenizer
    # 'gpt2' is the smallest GPT-2 model
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    # Set the pad token to the EOS token
    # This is necessary because GPT-2 doesn't have a default pad token
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

    # Encode the input prompt
    # add_special_tokens=True adds the necessary special tokens
    input_ids = tokenizer.encode(prompt, return_tensors='pt', add_special_tokens=True)

    # Create attention mask
    # This tells the model which tokens to pay attention to (all of them in this case)
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

    try:
        # Generate text
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,  # Enable sampling
            top_k=50,        # Consider the top 50 most likely next words
            top_p=0.95,      # Consider the smallest set of words whose cumulative probability exceeds 0.95
            temperature=0.7, # Control randomness (lower is more deterministic)
            pad_token_id=tokenizer.eos_token_id,
            # Ensure the model stops at the EOS token
            eos_token_id=tokenizer.eos_token_id,
            # Don't generate beyond max_length
            max_new_tokens=max_length - len(input_ids[0])
        )

        # Decode the generated text
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

    except RuntimeError as e:
        print(f"An error occurred during text generation: {e}")
        return None



def isPangram(text):
    found=False
    missingLet=[]
    for letter in string.ascii_lowercase:
        for char in text:
            if letter==char:
                found=True
                # print(f"found the letter {letter}")
                break
        if not found:
            missingLet.append(letter)
        found=False
    if len(missingLet)==0:
        return True,missingLet
    else:
        return False,missingLet

# Example usage
# device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
prompt = "The quick brown fox"
generated_text = generate_text(prompt,30)
unique_letters,missing_let = isPangram(generated_text)

print(f"Generated text:\n{generated_text}")
print(f"\nNumber of unique letters used: {unique_letters}")
