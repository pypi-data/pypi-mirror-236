from dotenv import load_dotenv
import os

# Pipeline input and output types.
INPUT_NODE_TYPES = ["text", "file"]
OUTPUT_NODE_TYPES = ["text", "file"]

# Node-specific parameters.
# TODO: this might be redundant (e.g. llm-openai-node.js)
# Map of LLMs to token limits
SUPPORTED_OPENAI_LLMS = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-4": 8192,
    "gpt-4-32k": 32768
}
SUPPORTED_ANTHROPIC_LLMS = {"claude-v2": 100000}
# Map of image gen models to possible sizes (in both dimensions; if in the 
# future non-square images can be generated we'll update this), and # of
# possible images to generate
SUPPORTED_IMAGE_GEN_MODELS = {
    "DALL·E 2": ([256, 512, 1024], list(range(1, 5))),
    "Stable Diffusion XL": ([512], [1])
}
SUPPORTED_SPEECH_TO_TEXT_MODELS = ["OpenAI Whisper"]
CHAT_MEMORY_TYPES = ["Full - Formatted", "Full - Raw", "Message Buffer", "Token Buffer"]

# Relevant API endpoints the SDK code needs. Could also refactor to get rid of
# MODE entirely.
load_dotenv()
MODE = os.environ.get('ENVIRONMENT', 'PROD')

API_VECTORSTORE_FETCH_ENDPOINT = 'http://localhost:8000/api/vectorstores/fetch' if MODE != 'PROD' else 'https://api.vectorshift.ai/api/vectorstores/fetch'
API_PIPELINE_SAVE_ENDPOINT = 'http://localhost:8000/api/pipelines/add' if MODE != 'PROD' else 'https://api.vectorshift.ai/api/pipelines/add'
API_PIPELINE_FETCH_ENDPOINT = 'http://localhost:8000/api/pipelines/fetch' if MODE != 'PROD' else 'https://api.vectorshift.ai/api/pipelines/fetch'
API_PIPELINE_RUN_ENDPOINT = 'http://localhost:8000/api/pipelines/run' if MODE != 'PROD' else 'https://api.vectorshift.ai/api/pipelines/run'