#this will (hopefully) be an AI that can generate panagrams, and if I get that, then I will
#make it so that a user can enter either words or phrases that they want to be in the panagram
#Going to start with a function that can double check that the inputted sentence is a panagram

#ok, to finish this up, add user input, user chooses context for their sentence, so they could pick whimsical fantasy author, new york times editor etc.
#user enters phrases and stater sentence
#user enters a target number of words
#ok user enters target
import string
import ml_llama as llama

DEFUALT_PROMPT="""<|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 26 Jul 2024

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

""" #using triple quote so that I can use endlines in prompt if I need to

SYSTEM_PROMPT="You are a famous, successful English author. You write mostly sci-fi and fantasy fiction and all of your books can be described as whimsical and humorous."
PROMPT="Can you make a new pangram please, a pangram is a sentence with at least one instance of all 26 letters. Try to make a pangram that actually sounds like a full sentence instead of a list of words.{sentence_starter}{phrases}{num_words} Only respond with the generated pangram."
SENTENCE_STARTER_PROMPT=" Here is a sentence starter for your pangram: \"{st}\"."
PHRASES_PROMPT=" Here are phrases that should be included in the pangram: \"{phrases}\"."
NUMBER_OF_WORDS_PROMPT=" Try and make your pangram {num} words or shorter."
def is_pangram(text):
    found=False
    missingLet=[]
    text=text.lower()
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

def num_words(text):
    return len(text.split(' '))

def num_char(text):
    return len(text.replace(' ',''))

def create_pangram(model,sentence_starter="",phrases=[],num_wrd=0): #probably will add sytem prompt choice as well with default being whimsical fantasy
    st=p=nd=""
    prompt=PROMPT
    if len(sentence_starter)>0:
        st=SENTENCE_STARTER_PROMPT.format(st=sentence_starter)
    if len(phrases)>0:
        p=PHRASES_PROMPT.format(phrases='", "'.join(phrases))
    if num_wrd>0:
        nd=NUMBER_OF_WORDS_PROMPT.format(num=num_wrd)
    prompt=prompt.format(sentence_starter=st,phrases=p,num_words=nd)
    print(f"prompt used: {prompt}")
    full_prompt=DEFUALT_PROMPT.format(prompt=prompt,system_prompt=SYSTEM_PROMPT)
    return llama.generate_text(full_prompt,model,seed=21) #play around with it, probably make a function that tests different values for different parameters, ,stop=[".","?","!"]
#so 4 letters per token, average number of letters per word is 6.47 so lets say 7, if I want 20 words, thats 7*20/4 for number of tokens approximateyly, could use this to narrow down the max_token

def is_good_len(text,target,counter):
    len=counter(text)
    return len<=target,len

def test_pangram(pangram,target,count_words): #add arg for what we are counting
    is_pan,missing_let=is_pangram(pangram)
    if count_words:
        good_len,len=is_good_len(pangram,target,num_words)
        counter="words"
    else:
        good_len,len=is_good_len(pangram,target,num_char)
        counter="characters"
    results=f"here is the generated pangram: \"{pangram}\"\n"
    if is_pan:
        results=results+"It is a valid pangram, yayyyyyyy!!!"
    else:
        results=results+f"It is not a valid pangram, missing letters: {missing_let}"
    if good_len:
        results=results+f"\nThe length of the pangram was valid, it was {len} {counter} long which was less than or equal to the target of {target}"
    else:
        results=results+f"\nThe length of the pangram was invalid, it was {len} {counter} long which was greater than the target of {target}"
    print(results)

#either a test to see if it is at or below the required length, or runs is_pangram and

def main():
    target_len=30
    model=llama.create_model(llama.MODEL_PATH)
    # output=llama.generate_text(FULL_PROMPT,model,seed=21)
    # print(output)
    pangram=create_pangram(model,"The universe is a lie",["hello world"],target_len)#,"the universe is a lie",["I like potatoes","hello World"])
    num_tok=llama.count_tokens(pangram,model)
    test_pangram(pangram,target_len,True)
    num_char("two words")
    print(f"the number of tokens in the pangram is {num_tok}")
    # print(f"testing prompt thing \"{PROMPT}\"")
    # sentence="The universe is a lie because wizards forgot to jump the equinox in kayaks"
    # print(f"testing pangram for \"{sentence}\"\nthe results are: {is_pangram(sentence)}")
if __name__=="__main__":
    main()
