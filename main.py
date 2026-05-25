from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import groq
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key from environment variable
client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are CodeNova AI, expert coding assistant."},
            {"role": "user", "content": request.message}
        ],
        temperature=0.7,
        max_tokens=2048
    )
    return {"reply": response.choices[0].message.content}

@app.get("/")
def root():
    return {"status": "CodeNova AI Running!"}
