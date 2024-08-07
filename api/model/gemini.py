import os

import dotenv
import google.generativeai as genai

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GLC_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 100,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="always response as Russian language",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("hello how's going")

print(response.text)