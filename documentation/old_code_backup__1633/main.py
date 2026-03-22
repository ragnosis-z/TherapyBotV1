from fastapi import FastAPI
from schemas import ChatRequest, ChatResponse
from prompts import get_system_prompt
from safety import safety_check

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    safety_response = safety_check(request.message)
    if safety_response:
        return ChatResponse(
            response=safety_response,
            mode=request.mode
        )

    system_prompt = get_system_prompt(request.mode)

    # TEMP response (no AI yet)
    response = f"[{request.mode.upper()} MODE] I hear you."

    return ChatResponse(
        response=response,
        mode=request.mode
    )

