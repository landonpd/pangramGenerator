import os
import sys
from llama_cpp import Llama
from contextlib import contextmanager
# Path to your GGUF model file goes here
MODEL_PATH = "/Users/landondixon/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

DEFUALT_PROMPT="""<|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 26 Jul 2024

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

""" #using triple quote so that I can use endlines in prompt if I need to
#Use lots of adectives to help include all of the letters of the alphabet
SYSTEM_PROMPT="You are a famous, successful English author. You write mostly sci-fi and fantasy fiction and all of your books can be described as whimsical and humorous." #other ideas for personalities, new york times editor (serious and relevant options)
PROMPT="""
Hello, can you make a new, novel, unique pangram please, a pangram is a sentence with at least one instance of all 26 letters.

Here is a list parameters I want you to follow:
- Do not use or derive from these well known pangrams:\n{pans}
- Remember all 26 letters of the alphabet need to be in the sentence, not just the most and least common ones.
- Try to make a pangram that actually sounds like a real sentence instead of a list of disparate ideas.{sentence_starter}{phrases}{num_words}{num_char}
- Only respond with the generated pangram, like:

"<pangram>"

For instance:

"The quick brown fox jumps over the lazy dog."

Think carefully and quietly before you respond. I will tip you $200 for every good pangram.
"""
SENTENCE_STARTER_PROMPT="\n- Here is a sentence starter for your pangram: \"{st}\"."
PHRASES_PROMPT="\n- Here are phrases that should be included in the pangram: \"{phrases}\". Try to include them in a natural way."
NUMBER_OF_WORDS_PROMPT="\n- Try and make your pangram {num} words or shorter."
NUMBER_OF_CHAR_PROMPT="\n- Try and make your pangram {num} characters or shorter, not including punctuation."
KNOWN_PANGRMAS= [
    "A quick brown fox jumps over the lazy dog.",
    "Blowzy night-frumps vex'd Jack Q.",
    "Glum Schwartzkopf vex'd by NJ IQ.",
    "Jived fox nymph grabs quick waltz.",
    "Glib jocks quiz nymph to vex dwarf.",
    "Waltz, bad nymph, for quick jigs vex.",
    "Sphinx of black quartz, judge my vow.",
    "Quick zephyrs blow, vexing daft Jim.",
    "How vexingly quick daft zebras jump!",
    "The five boxing wizards jump quickly.",
    "Jackdaws love my big sphinx of quartz.",
    "Pack my box with five dozen liquor jugs.",
    "Big Fuji waves pitch enzymed kex liquor.",
    "Fix problem quickly with galvanized jets.",
    "Heavy boxes perform quick waltzes and jigs.",
]

@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def create_model(model_path):
    with suppress_output():
        return Llama(model_path=model_path)

def create_prompt(sentence_starter="",phrases=[],num_wrd=0,num_char=0): #probably will add sytem prompt choice as well with default being whimsical fantasy
    st=p=nw=nc=""
    prompt=PROMPT
    if len(sentence_starter)>0:
        st=SENTENCE_STARTER_PROMPT.format(st=sentence_starter)
    if len(phrases)>0:
        p=PHRASES_PROMPT.format(phrases='", "'.join(phrases))
    if num_wrd>0:
        nw=NUMBER_OF_WORDS_PROMPT.format(num=num_wrd)
    if num_char>0:
        nc=NUMBER_OF_CHAR_PROMPT.format(num=num_char )
    prompt=prompt.format(sentence_starter=st,phrases=p,num_words=nw,num_char=nc,pans="\n  ".join(KNOWN_PANGRMAS))
    # print(f"prompt used: {prompt}")
    return DEFUALT_PROMPT.format(prompt=prompt,system_prompt=SYSTEM_PROMPT),prompt


# Generate text calls create_completion which takes the prompt and continues it as if it was a sentence starter
def generate_text(prompt,model,rp=1,temp=.7,p=.1,k=35,max_tokens=0,suffix="",stoppers=[],seed=-1):
    '''
    rp: repeat penalty, penalty for tokens repeating, 1 is average, 1.5 is too extreme
    k: limits the next token to the k most likely tokens 1 to vocab size, usually 10-100
    p: limits the next token to a subset of tokens with a cummulative probabilaty higher than p 0 to 1, commonly .9 o 1
    temp: controls the randomness in generatino, lower more deterministic, higher more random, 0 to 1, commonly .5 to 1
    '''
    if seed!=-1: #this means we want deterministic outputs for testing purposes, might remove this capability later, or make a seperate function?
        output=model.create_completion(prompt, repeat_penalty=rp,temperature=0,min_p=p,top_k=k,max_tokens=100,suffix=suffix,stop=stoppers,seed=seed) #create_completion equals model() but because theres no typing I don't think I can do that
    else:
        output=model.create_completion(prompt, repeat_penalty=rp,temperature=temp,typical_p=p,top_k=k,max_tokens=100,suffix=suffix,stop=stoppers)
    return output["choices"][0]["text"].strip("\"") #might add strip() which removes whitespace at teh beginning and end, or something else if I specify it

#just generate_text but with specific params, I'd just combine these two functions into one, consider
def create_pangram(model,full_prompt):
    with suppress_output():
        return generate_text(full_prompt,model,stoppers=[".\""],temp=.9)



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
