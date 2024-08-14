#this will (hopefully) be an AI that can generate panagrams, and if I get that, then I will
#make it so that a user can enter either words or phrases that they want to be in the panagram
#Going to start with a function that can double check that the inputted sentence is a panagram
import string
import ml_llama as llama

DEFUALT_PROMPT="""<|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 26 Jul 2024

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

""" #using triple quote so that I can use endlines in prompt if I need to
PROMPT="Can you make a new pangram please, a pangram is a sentence with at least one instance of all 26 letters. Try to make a pangram that actually sounds like a full sentence instead of a list of words. Only respond with the generated pangram."
SYSTEM_PROMPT="You are a famous, successful English author. You write mostly sci-fi and fantasy fiction and all of your books can be described as whimsical and humorous."
#ok, to finish this up, add user input, user chooses context for their sentence, so they could pick whimsical fantasy author, new york times editor etc.
#user enters phrases and stater sentence
#user enters a target number of words
SENTENCE_STARTER_PROMPT=" Here is a sentence starter for your pangram: "
PHRASES_PROMPT=" Here are phrases that should be included in the pangram: "
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

def create_pangram(model,sentence_starter="",phrases=[]): #one token is about 4 letters
    prompt=PROMPT
    if len(sentence_starter)>0:
        prompt=prompt+SENTENCE_STARTER_PROMPT+"\""+sentence_starter+"\"."
    if len(phrases)>0:
        prompt=prompt+PHRASES_PROMPT
        for phrase in phrases:
            prompt=prompt+phrase+", "
    print(f"prompt used: {prompt}")
    full_prompt=DEFUALT_PROMPT.format(prompt=prompt,system_prompt=SYSTEM_PROMPT)
    return llama.generate_text(full_prompt,model,seed=21) #play around with it, probably make a function that tests different values for different parameters, ,stop=[".","?","!"]


def test_pangram(pangram):
    is_pan,missing_let=is_pangram(pangram)
    results=f"here is the generated pangram: \"{pangram}\"\n"
    if is_pan:
        results=results+"It is a valid pangram, yayyyyyyy!!!"
    else:
        results=results+f"It is not a valid pangram, missing letters: {missing_let}"
    print(results)

def main():
    model=llama.create_model(llama.MODEL_PATH)
    # output=llama.generate_text(FULL_PROMPT,model,seed=21)
    # print(output)
    pangram=create_pangram(model,"The universe is a lie",["hello world"])#,"the universe is a lie",["I like potatoes","hello World"])
    num_tok=llama.count_tokens(pangram,model)
    test_pangram(pangram)
    print(f"the number of tokens in the pangram is {num_tok}")
    # print(f"testing prompt thing \"{PROMPT}\"")
    # sentence="The universe is a lie because wizards forgot to jump the equinox in kayaks"
    # print(f"testing pangram for \"{sentence}\"\nthe results are: {is_pangram(sentence)}")
if __name__=="__main__":
    main()
