#this will (hopefully) be an AI that can generate panagrams, and if I get that, then I will
#make it so that a user can enter either words or phrases that they want to be in the panagram
#Going to start with a function that can double check that the inputted sentence is a panagram

#ok, to finish this up, add user input, user chooses context for their sentence, so they could pick whimsical fantasy author, new york times editor etc.
#user enters phrases and stater sentence
#user enters a target number of words
#ok user enters target
import ml_llama as llama
import analyze
DEFUALT_PROMPT="""<|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 26 Jul 2024

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

""" #using triple quote so that I can use endlines in prompt if I need to
#Use lots of adectives to help include all of the letters of the alphabet
SYSTEM_PROMPT="You are a famous, successful English author. You write mostly sci-fi and fantasy fiction and all of your books can be described as whimsical and humorous."
PROMPT="""Hello, can you make a new pangram please, a pangram is a sentence with at least one instance of all 26 letters. \
Remember all 26 letters of the alphabet need to be in the sentence, not just the most and least common ones. \
Try to make a pangram that actually sounds like a real sentence instead of a list of disparate ideas. \
{sentence_starter}{phrases}{num_words}{num_char} Only respond with the generated pangram."""
SENTENCE_STARTER_PROMPT=" Here is a sentence starter for your pangram: \"{st}\"."
PHRASES_PROMPT=" Here are phrases that should be included in the pangram: \"{phrases}\". Try to include them in a natural way"
NUMBER_OF_WORDS_PROMPT=" Try and make your pangram {num} words or shorter."
NUMBER_OF_CHAR_PROMPT=" Try and make your pangram {num} characters or shorter, not including punctuation."

def create_pangram(model,sentence_starter="",phrases=[],num_wrd=0,num_char=0): #probably will add sytem prompt choice as well with default being whimsical fantasy
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
    prompt=prompt.format(sentence_starter=st,phrases=p,num_words=nw,num_char=nc)
    print(f"prompt used: {prompt}")
    full_prompt=DEFUALT_PROMPT.format(prompt=prompt,system_prompt=SYSTEM_PROMPT)
    return llama.generate_text(full_prompt,model,seed=21) #play around with it, probably make a function that tests different values for different parameters, ,stop=[".","?","!"]
#so 4 letters per token, average number of letters per word is 6.47 so lets say 7, if I want 20 words, thats 7*20/4 for number of tokens approximateyly, could use this to narrow down the max_token
#make the above not seeded so that it isn't deterministic

#either a test to see if it is at or below the required length, or runs is_pangram and

def main():
    target_wrd=-1
    target_char=100
    model=llama.create_model(llama.MODEL_PATH)
    # output=llama.generate_text(FULL_PROMPT,model,seed=21)
    # print(output)
    pangram=create_pangram(model,"The universe is a lie",["hello world"],target_wrd,target_char)#,"the universe is a lie",["I like potatoes","hello World"])
    num_tok=llama.count_tokens(pangram,model)
    analyze.pangram_stats(pangram,target_wrd,target_char)
    print(f"the number of tokens in the pangram is {num_tok}")
    # print(f"testing prompt thing \"{PROMPT}\"")
    # sentence="The universe is a lie because wizards forgot to jump the equinox in kayaks"
    # print(f"testing pangram for \"{sentence}\"\nthe results are: {is_pangram(sentence)}")
if __name__=="__main__":
    main()
