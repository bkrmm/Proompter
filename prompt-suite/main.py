from fastapi import FastAPI
import uvicorn
from graph import refine_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
import os

app = FastAPI()

@app.post("/refine_prompt")
async def api_refine(data: dict):
    final = refine_prompt(data["prompt"])
    return {"final_prompt": final}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=2137)

#TODO: Add system prompt to make the string input into a generative, iterative prompt with techniques such as in-context learning, etc.

"""
http://127.0.0.1:2137/docs
{
  "prompt": "what is antibiotics"
}
"""