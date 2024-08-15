#this will (hopefully) be an AI that can generate panagrams, and if I get that, then I will
#make it so that a user can enter either words or phrases that they want to be in the panagram
#Going to start with a function that can double check that the inputted sentence is a panagram

#ok, to finish this up, add user input, user chooses context for their sentence, so they could pick whimsical fantasy author, new york times editor etc.
#user enters phrases and stater sentence
#user enters a target number of words
#ok user enters target
import ml_llama as llama
import analyze
import string
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
def create_pangram(model,full_prompt): #probably will add sytem prompt choice as well with default being whimsical fantasy
    return llama.generate_text(full_prompt,model,stoppers=[".\""],temp=.9)[1:] #play around with it, probably make a function that tests different values for different parameters, ,stop=[".","?","!"]
def create_prompt(sentence_starter="",phrases=[],num_wrd=0,num_char=0):
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

#so 4 letters per token, average number of letters per word is 6.47 so lets say 7, if I want 20 words, thats 7*20/4 for number of tokens approximateyly, could use this to narrow down the max_token
#make the above not seeded so that it isn't deterministic

#either a test to see if it is at or below the required length, or runs is_pangram and
#ok, test generating lots and lots of responses first, see if when it isn't

def main():
    st=""#"The universe is a lie"
    phrases=[]#["I like potatoes","hello World"]
    target_wrd=-1
    target_char=-1
    num_pans=1000
    model=llama.create_model(llama.MODEL_PATH)

    full_prompt,_=create_prompt(st,phrases,target_wrd,target_char)
    # pangram=create_pangram(model)#,"the universe is a lie",["I like potatoes","hello World"],target_wrd,target_char)
    # num_tok=llama.count_tokens(pangram,model)
    # print(analyze.pangram_stats_print(pangram,target_wrd,target_char))
    # print(f"the number of tokens in the pangram is {num_tok}")


    pangrams=[]
    num_toks=[]
    for i in range(num_pans):
        temp_pan=create_pangram(model,full_prompt)
        pangrams.append(temp_pan)
        num_toks.append(llama.count_tokens(temp_pan,model))
        if i%10==0:
            print(f"\n\n{i} pangrams generated\n\n")
    missing_let,wrong_count=analyze.test_missing_let_freq(pangrams)
    for i in range(len(missing_let)):
        print(f"{string.ascii_lowercase[i]}:{missing_let[i]}")

    is_pans,len_wrds,len_chars,distances=analyze.stats_aggregation(pangrams)
    print(f"\n\nHere are the {num_pans} generated pangrams.\n")
    for i in range(len(pangrams)):
        print(f"{pangrams[i]}\n\nThis is a {is_pans[i]} pangram with {len_wrds[i]} words, {len_chars[i]} characters, and an average distance to other generated pangrams of {distances[i]}.\n------\n")
    print(f"number of false pangrams: {wrong_count} out of {num_pans}. {round(((num_pans-wrong_count)/num_pans)*100)}% correct")
    print(f"average num of tokens: {analyze.ave(num_toks)}\naverage num of words: {analyze.ave(len_wrds)}\naverage num of characters: {analyze.ave(len_chars)}\naverage edit distance: {analyze.ave(distances)}")
if __name__=="__main__":
    main()
