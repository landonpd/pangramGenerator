#this will (hopefully) be an AI that can generate panagrams, and if I get that, then I will
#make it so that a user can enter either words or phrases that they want to be in the panagram
#Going to start with a function that can double check that the inputted sentence is a panagram

#ok, to finish this up, add user input, user chooses context for their sentence, so they could pick whimsical fantasy author, new york times editor etc.
#user enters phrases and stater sentence
#user enters a target number of words
#ok user enters target
import string
import ml_llama as llama
import analyze
import pangram as ps
#so 4 letters per token, average number of letters per word is 6.47 so lets say 7, if I want 20 words, thats 7*20/4 for number of tokens approximateyly, could use this to narrow down the max_token

#generates pangrams using the prompt until the result is a valid pangram
def generate_pangram(model,prompt):
    pan=ps.Pangram(llama.create_pangram(model,prompt))
    while not pan.is_valid:
        pan=ps.Pangram(llama.create_pangram(model,prompt))
    return ps.PangramStats(pan,model)

#generates variable amount of valid pangrams
def generate_pangrams(model,prompt,num):
    pans=[]
    for i in range(num):
        pans.append(generate_pangram(model,prompt))
    return pans
def main():
    st=""#"The universe is a lie"
    phrases=[]#["I like potatoes","hello World"]
    target_wrd=-1
    target_char=-1
    num_pans=1
    #get user inputs for the above things
    st=input("Enter a sentence starter, click enter to forego a starter: ")
    # print(st)
    phrase=input("Enter phrases to include in your pangram, hit enter to stop entering phrases: ")

    while phrase!="":
        phrases.append(phrase)
        phrase=input("Enter phrases to include in your pangram, hit enter to stop entering phrases: ")

    # print(phrases)
    target_wrd=int(input("Enter a target number of words, enter -1 to forgoe a target: "))
    # print(target_wrd)
    target_wrd=int(input("Enter a target number of characters, enter -1 to forgoe a target: "))
    num_pans=int(input("enter how many pangrams you want generated: "))
    #create the model, generate the prompt,
    model=llama.create_model(llama.MODEL_PATH)
    full_prompt,_=llama.create_prompt(st,phrases,target_wrd,target_char)
    pangrams=generate_pangrams(model,full_prompt,num_pans)
    for pan in pangrams:
        print(f"{pan}\n------\n") #pangram.stats_print(target_wrd,target_char)
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


    #below is code to run and collect data from lots of pangrams, useful for finding patterns in the data
    # pangrams=[]
    # num_toks=[]
    # for i in range(num_pans):
    #     temp_pan=llama.create_pangram(model,full_prompt)
    #     pangrams.append(temp_pan)
    #     num_toks.append(llama.count_tokens(temp_pan,model))
    #     if i%10==0:
    #         print(f"\n\n{i} pangrams generated\n\n")
    # missing_let,wrong_count=analyze.test_missing_let_freq(pangrams)
    # for i in range(len(missing_let)):
    #     print(f"{string.ascii_lowercase[i]}:{missing_let[i]}")

    # is_pans,len_wrds,len_chars,distances=analyze.stats_aggregation(pangrams)
    # print(f"\n\nHere are the {num_pans} generated pangrams.\n")
    # for i in range(len(pangrams)):
    #     print(f"{pangrams[i]}\n\nThis is a {is_pans[i]} pangram with {len_wrds[i]} words, {len_chars[i]} characters, and an average distance to other generated pangrams of {distances[i]}.\n------\n")
    # print(f"number of false pangrams: {wrong_count} out of {num_pans}. {round(((num_pans-wrong_count)/num_pans)*100)}% correct")
    # print(f"average num of tokens: {analyze.ave(num_toks)}\naverage num of words: {analyze.ave(len_wrds)}\naverage num of characters: {analyze.ave(len_chars)}\naverage edit distance: {analyze.ave(distances)}")
if __name__=="__main__":
    main()
