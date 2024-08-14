from llama_cpp import Llama

# Path to your GGUF model file
MODEL_PATH = "/Users/landondixon/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

def create_model(model_path):
    return Llama(model_path=model_path)

# Generate text calls create_completion which takes the prompt and continues it as if it was a sentence starter
def generate_text(prompt,model,temp=.7,p=.1,k=50,max_tokens=100,suffix="",stop=[],seed=-1):
    #k: limits the next token to the k most likely tokens 1 to vocab size, usually 10-100
    #p: limits the next token to a subset of tokens with a cummulative probabilaty higher than p 0 to 1, commonly .9 o 1
    #temp: controls the randomness in generatino, lower more deterministic, higher more random, 0 to 1, commonly .5 to 1
    if seed!=-1:
        output=model.create_completion(prompt, temperature=0,min_p=p,top_k=k,max_tokens=100,suffix=suffix,stop=stop,seed=seed) #create_completion equals model() but because theres no typing I don't think I can do that
    else:
        output=model.create_completion(prompt, temperature=0,typical_p=p,top_k=k,max_tokens=100,suffix=suffix,stop=stop)
    return output["choices"][0]["text"] #might add strip() which removes whitespace at teh beginning and end, or something else if I specify it

def count_tokens(text,model): #one token is about 4 letters
    tokens=model.tokenize(text.encode())
    return len(tokens)

# Print the generated text
# print("\nthe above is just the output from running llama, below is the response to the prompt\n")
# prompt="Write a limerick about Bob who likes kabobs"
# model=create_model(MODEL_PATH)
# text_output=generate_text(prompt,model)
# num_tok=count_tokens(text_output,model)
# print(f"the number of tokens in \"{text_output}\" is {num_tok}")
# #
