# CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python
#
# pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal

from llama_cpp import Llama
from pprint import pprint
# Path to your GGUF model file
MODEL_PATH = "/Users/landondixon/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
# lm = Llama(model_path=MODEL_PATH)

# DEFUALT_PROMPT="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# Cutting Knowledge Date: December 2023
# Today Date: 26 Jul 2024

# {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

# {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

# """ #using triple quote so that I can use endlines in prompt if I need to
# PROMPT=input("Please enter your prompt: ")


# SYSTEM_PROMPT="Your a editor for a New York editing house and know everything about books and stuff."
# FULL_PROMPT=DEFUALT_PROMPT.format(prompt=PROMPT,system_prompt=SYSTEM_PROMPT)

# output = lm.create_completion(FULL_PROMPT)
# pprint(output)


llm = Llama(
      model_path=MODEL_PATH,
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      # seed=1337, # Uncomment to set a specific seed
      # n_ctx=2048, # Uncomment to increase the context window
)
llm = Llama(
      model_path=MODEL_PATH,
      chat_format="llama-2",
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
)
output = llm.create_chat_completion(
      messages = [
          {"role": "system", "content": "You are an assistant who perfectly describes images."},
          {
              "role": "user",
              "content": "Describe this image in detail please."
          }
      ]
)


print(output)


# python3 -m llama_cpp.server --model /Users/landondixon/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
