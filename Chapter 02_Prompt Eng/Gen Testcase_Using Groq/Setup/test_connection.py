# This script checks whether Python can securely connect to Groq.
import os
from dotenv import load_dotenv
from groq import Groq
# Checks Groq connection
# Load variables from .env
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found.")

# Connect to Groq
client = Groq(api_key=api_key)

print("API key loaded successfully.")
print("Groq client created successfully.")