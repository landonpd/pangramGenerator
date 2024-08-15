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
#so 4 letters per token, average number of letters per word is 6.47 so lets say 7, if I want 20 words, thats 7*20/4 for number of tokens approximateyly, could use this to narrow down the max_token
#make the above not seeded so that it isn't deterministic

#either a test to see if it is at or below the required length, or runs is_pangram and
#ok, test generating lots and lots of responses first, see if when it isn't

def main():
    st=""#"The universe is a lie"
    phrases=[]#["I like potatoes","hello World"]
    target_wrd=-1
    target_char=-1
    num_pans=5
    model=llama.create_model(llama.MODEL_PATH)

    full_prompt,_=llama.create_prompt(st,phrases,target_wrd,target_char)
    pangram=llama.create_pangram(model,full_prompt)#,"the universe is a lie",["I like potatoes","hello World"],target_wrd,target_char)
    num_tok=llama.count_tokens(pangram,model)
    print(analyze.pangram_stats_print(pangram,target_wrd,target_char))
    print(f"the number of tokens in the pangram is {num_tok}")

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
