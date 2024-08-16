# ok, to finish this up,
# TODO: modify prompt and post proccessing to generate more than one at a time, will really help make this faster, issue, generating multiple things, they are way less accurate
# Consider adding pretty ui, if it is easier than bubble tea than definitly, if not then leave it gross for now
# Consider making it so that when generating a function the results have to match params, so it has to start with the sentence starter, it has to have all the phrases, it has to be under the char and word limit. Could break because could cause infinite loop, would have to put a limiter on it.
#TODO: consider removing all options except context and phrases, really good at phrases, bad at all other options, before I remove them I will see how long it takes to make a real pangram if I just ask it for a sentence and have a sentence starter and what not, When not focused on making a pangram it can make better, more unique sentences, but it will probably take a looot longer, maybe if I don't mention pangrams by name?
#
# In analyze.py
# look at each individual optional parameter and make sure it works, (e.g num characters makes it longer right now)
# add a function that generates random strings, when testing edit distance make two strings of the average length and find thier edit distance from each other (or maybe do this like 50 times) to compare to the edit distance for the sentences, actual sentences have spaces and punctuation, so they are actually longer, don't know what to do with that
# Use time function to compare to when I specify m and when I don't
import string
import ml_llama as llama
import pangram as ps
#so 4 letters per token, average number of letters per word is 6.47 so lets say 7, if I want 20 words, thats 7*20/4 for number of tokens approximateyly, could use this to narrow down the max_token

CLEAR_AND_RETURN='\033c\033[H'

def main():
    choices="1. A humorous and whimsical sci-fi and fantasy author\n2. A head editor for the New York Times who also likes word puzzles.\n3. An early 20th century news broadcaster with the classic mid-atlantic accent.\n4. A gossip columnist all up to date on all the latest celebrity gossip.\n5. A genius scientist who always uses big words and confusing jargon.\n6. A zooligist who travels the world and writes about all the interesting animals they've seen."
    st=""#"The universe is a lie"
    phrases=[]#["I like potatoes","hello World"]
    target_wrd=-1
    target_char=-1
    context_choice=0
    # num_pans=1
    #get user inputs for the above things
    st=input("Enter a sentence starter, click enter to forego a starter: ")
    # print(st)
    phrase=input(f"{CLEAR_AND_RETURN}Enter phrases to include in your pangram, hit enter to stop entering phrases: ")

    while phrase!="":
        phrases.append(phrase)
        phrase=input(f"{CLEAR_AND_RETURN}Enter phrases to include in your pangram, hit enter to stop entering phrases: ")

    # print(phrases)
    target_wrd=int(input(f"{CLEAR_AND_RETURN}Enter a target number of words, enter -1 to forgoe a target: "))
    # print(target_wrd)
    target_wrd=int(input(f"{CLEAR_AND_RETURN}Enter a target number of characters, enter -1 to forgoe a target: "))

    context_choice=int(input(f"{CLEAR_AND_RETURN}Here is a list of contexts to choose from for your pangrams:\n{choices}\nPick which context to use: "))-1
    #num_pans=int(input(f"{CLEAR_AND_RETURN}enter how many pangrams you want generated: "))
    print(f"{CLEAR_AND_RETURN}Creating your pangram.")
    #create the model, generate the prompt,
    model=llama.create_model(llama.MODEL_PATH)
    full_prompt,readable=llama.create_prompt(context_choice,st,phrases,target_wrd,target_char)
    pan=llama.generate_true_pangram(full_prompt,model)
    print(f"{CLEAR_AND_RETURN}Here is your pangram.\n")
    # for pan in pangrams:
    print(f"{pan}") #pangram.stats_print(target_wrd,target_char)
    # if target_wrd!=-1:
    #     if pangram.char_target(target_wrd):
    #         print(f"The pangram has a valid number of characters,it has less than or {target_wrd} words.")
    #     else:
    #         print(f"The pangram has an invalid number of characters,it has more than {target_wrd} words.")
    # if target_char!=-1:
    #     if pangram.char_target(target_char):
    #         print(f"The pangram has a valid number of characters,it has less than or {target_char} characters.")
    #     else:
    #         print(f"The pangram has an invalid number of characters,it has more than {target_char} characters.")

if __name__=="__main__":
    main()
