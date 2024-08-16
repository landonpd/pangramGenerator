# # CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python
# #
# # pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal

# from llama_cpp import Llama
# from pprint import pprint
# # Path to your GGUF model file
# MODEL_PATH = "/Users/landondixon/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
# # lm = Llama(model_path=MODEL_PATH)

# # DEFUALT_PROMPT="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# # Cutting Knowledge Date: December 2023
# # Today Date: 26 Jul 2024

# # {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

# # {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

# # """ #using triple quote so that I can use endlines in prompt if I need to
# # PROMPT=input("Please enter your prompt: ")


# # SYSTEM_PROMPT="Your a editor for a New York editing house and know everything about books and stuff."
# # FULL_PROMPT=DEFUALT_PROMPT.format(prompt=PROMPT,system_prompt=SYSTEM_PROMPT)

# # output = lm.create_completion(FULL_PROMPT)
# # pprint(output)


# llm = Llama(
#       model_path=MODEL_PATH,
#       n_gpu_layers=-1, # Uncomment to use GPU acceleration
#       # seed=1337, # Uncomment to set a specific seed
#       # n_ctx=2048, # Uncomment to increase the context window
# )
# llm = Llama(
#       model_path=MODEL_PATH,
#       chat_format="llama-2",
#       n_gpu_layers=-1, # Uncomment to use GPU acceleration
# )
# output = llm.create_chat_completion(
#       messages = [
#           {"role": "system", "content": "You are an assistant who perfectly describes images."},
#           {
#               "role": "user",
#               "content": "Describe this image in detail please."
#           }
#       ]
# )


# print(output)


# # python3 -m llama_cpp.server --model /Users/landondixon/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
# import string
# PROMPT="Can you make a new pangram please, a pangram is a sentence with at least one instance of all 26 letters. Try to make a pangram that actually sounds like a full sentence instead of a list of words.{sentence_starter}{phrases}{num_words} Only respond with the generated pangram."
# SENTENCE_STARTER_PROMPT="Here is a sentence starter for your pangram: \"{st}\"."
# PHRASES_PROMPT="Here are phrases that should be included in the pangram: \"{phrases}\"."
# NUMBER_OF_WORDS_PROMPT="Try and make your pangram {num} words long or shorter."

# def num_char(text):
#     result_str=text.replace(' ','')
#     for char in string.punctuation:
#         result_str=result_str.replace(char,'')
#     print(result_str)

# sentence_starter=""
# phrases=[]
# num_wrd=0
# st=p=nd=""
# prompt=PROMPT
# if len(sentence_starter)>0:
#     st=SENTENCE_STARTER_PROMPT.format(st=sentence_starter)
# if len(phrases)>0:
#    p=PHRASES_PROMPT.format(phrases='", "'.join(phrases))
# if num_wrd>0:
#     nd=NUMBER_OF_WORDS_PROMPT.format(num=num_wrd)
# prompt=prompt.format(sentence_starter=st,phrases=p,num_words=nd)
# print(f"prompt used: {prompt}")
# num_char(prompt)
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
    "Jinxed wizards pluck ivy from the big quilt.",
    "Watch Jeopardy!, Alex Trebek's fun TV quiz game.",
    "Adjusting quiver and bow, Zompye killed the fox.",
    "Amazingly few discotheques provide jukeboxes.",
    "Cozy lummox gives smart squid who asks for job pen.",
    "The vixen jumped quickly on her foe, barking with zeal.",
    "Fat wealthy diva became rocking jazz saxophone queen.",
    "Mad Brother Farvis was quickly axed for crazy praying.",
    "Back home after jiving so, he expired with quizzicality.",
    "Sixty zippers were quickly picked from the woven jute bag.",
    "Crazy Fredericka bought many very exquisite opal jewels.",
    "Grumpy wizards make toxic brew for the evil queen and jack.",
    "How razorback-jumping frogs can level six piqued gymnasts!",
    "The wizard quickly jinxed the gnomes before they vaporized.",
    "All questions asked by five watched experts amaze the judge.",
    "The July sun caused a fragment of black pine wax to ooze on the velvet quilt.",
    "Anxious Al waved back his pa from the zinc quarry just sighted.",
    "Intoxicated Queen Elizabeth vows Mick Jagger is perfection.",
    "The girl loved a joyful boy who quickly fixed her zany problems.",
    "A quart jar of oil mixed with zinc oxide makes a very bright paint.",
    "Whenever the black fox jumped, the squirrel gazed suspiciously.",
    "Alfredo just must bring very exciting news to the plaza quickly.",
    "Joe was pleased over our gift of quail, mink, zebra, and clever oryx.",
    "If I give you cloth with quartz beads -- onyx, jasper, amethyst -- keep it.",
    "The job requires extra pluck and zeal from every young wage earner.",
    "Picking just six quinces, the new farmhand proves strong but lazy.",
    "A mad boxer shot a quick, gloved jab to the jaw of his dizzy opponent.",
    "Jaded zombies acted quaintly but kept driving their oxen forward.",
    "While making deep excavations, we found some quaint bronze jewelry.",
    "Engelbert Humperinck's exquisitely frothy & vacuous waltz is a joy.",
    "Six big juicy steaks sizzled in a pan as five workmen left the quarry.",
    "The soprano took Mozart's joyful quavers with grace and exuberance.",
    "We quickly seized the black axle and just saved it from going past him.",
    "If Grieg or Dvorak, for example, wrote jazz, it would be quaint and cheesy.",
    "While Suez sailors wax parquet decks, Afghan Jews vomit jauntily abaft.",
    "We promptly judged antique ivory buckles for the next prize.",
    "Venerable Will played jazz sax 'til 3 o'clock in the morning before he quit.",
    "The querulous snoozing taxi driver jumped crossly, woken by the foghorn.",
    "The public was amazed to view the quickness and dexterity of the juggler.",
    "The explorer was frozen in his big kayak just after making queer discoveries.",
    "Six javelins thrown by the quick savages whizzed forty paces beyond the mark.",
    "As we explored the gulf in Zanzibar, we quickly moved closer to the jutting rocks.",
    "Traveling beneath the azure sky in our jolly ox-cart, we often hit bumps quite hard.",
    "For civilization, Marxist thought just must be quickly replaced by ways of freedom.",
    "Ebenezer unexpectedly bagged two tranquil aardvarks with his jiffy vacuum cleaner.",
    "William said that everything about his jacket was in quite good condition except for the zipper.",
    "A foxy, quick, clever cat in Switzerland was hit by a fancy sports job with bumpy seats and a grumpy driver.",
    "Jelly-like above the high wire, six quaking pachyderms kept the climax of the extravaganza in a dazzling state of flux.",
    "No kidding -- Lorenzo called off his trip to visit Mexico City just because they told him the conquistadores were extinct.",
    "Forsaking monastic tradition, twelve jovial friars gave up their vocation for a questionable existence on the flying trapeze."
]
# array="\n".join(KNOWN_PANGRMAS)
# print(f"heres a string {array}")
#
import time
# Color constants
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  # Resets the color to default
CLEAR_AND_RETURN='\033c\033[H' #clears and returns cursor to default position, ask claude if this is a real clear, it is

# Example usage
print(f"{RED}This is red text{RESET}")
time.sleep(5)
print(f"{CLEAR_AND_RETURN}Everything was just cleared and {GREEN}This {RESET}is green text")
print(f"{BLUE}This is blue text{RESET}")

# You can also combine colors with other text
name = "Alice"
print(f"Hello, {YELLOW}{name}{RESET}! How are you?")



# Need to pipx install colorama,
# guarenteed to work on all platforms,
# Only want this if I am going to highlight stuff from the sentence, maybe like most common letter or whatever.
# from colorama import Fore, Back, Style
# import colorama

# # Initialize colorama
# colorama.init()

# # Example usage
# print(Fore.RED + "This is red text")
# print(Back.GREEN + "This has a green background")
# print(Fore.BLUE + Back.YELLOW + "Blue text on yellow background" + Style.RESET_ALL)
# print("This is back to normal")
