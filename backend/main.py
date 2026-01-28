import os
import uuid
import json
import tempfile
import shutil
from typing import List
from fastapi import FastAPI, Request, UploadFile, File, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import whisper
from openai import OpenAI
from PyPDF2 import PdfReader
from docx import Document
from dotenv import load_dotenv
import datetime
import httpx  # For X.ai API calls

load_dotenv()

print("XAI key loaded:", bool(os.getenv("XAI_API_KEY")))
print("OpenAI key loaded:", bool(os.getenv("OPENAI_API_KEY")))

LLAMA_ENABLED = os.getenv("LLAMA_ENABLED", "false").lower() == "true"

app = FastAPI()

import os
from fastapi.staticfiles import StaticFiles

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

UPLOAD_DIR = os.path.join(BASE_DIR, "scrolls_uploads")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
TRANSCRIPT_LOG = os.path.join(BASE_DIR, "oracle_log.json")
SCROLL_DB = os.path.join(BASE_DIR, "scroll_data.json")
SEEKERS_DB = os.path.join(BASE_DIR, "seekers.json")
VISITORS_DB = os.path.join(BASE_DIR, "visitors.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
openai_client = None  # Lazy load

def get_openai_client():
    global openai_client
    if openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        openai_client = OpenAI(api_key=api_key)
    return openai_client
xai_api_key = os.getenv("XAI_API_KEY")  # For Hathor oracle
whisper_model = None  # Lazy load

def save_log(entry):
    try:
        logs = []
        if os.path.exists(TRANSCRIPT_LOG):
            with open(TRANSCRIPT_LOG, "r") as f:
                content = f.read().strip()
                logs = json.loads(content) if content else []
        logs.append(entry)
        with open(TRANSCRIPT_LOG, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print("⚠️ Logging failed:", e)

def get_llama_observation(question: str, oracle_used: str, answer: str, scrolls: list = None) -> dict:
    if not LLAMA_ENABLED:
        return None
    # Minimal Phase 3.0 LLaMA observation: heuristic classifier
    # Suggest oracle based on keywords
    if any(word in question.lower() for word in ["love", "joy", "beauty", "emotion", "heart"]):
        suggested_oracle = "Hathor"
        confidence = 0.8
        reason = "Question contains poetic or emotional keywords aligning with Hathor's domain"
    elif any(word in question.lower() for word in ["law", "command", "sin", "righteous", "god"]):
        suggested_oracle = "Moses"
        confidence = 0.8
        reason = "Question contains doctrinal or moral keywords aligning with Moses' domain"
    else:
        suggested_oracle = "none"
        confidence = 0.5
        reason = "No strong stylistic indicators detected"
    
    return {
        "suggested_oracle": suggested_oracle,
        "confidence": confidence,
        "reason": reason,
        "phase": "3.0",
        "mode": "shadow"
    }

async def get_oracle_response(question: str, deity: str):
    # Phase 2: Restore explicit oracle separation
    # Hathor: xAI API, Moses: OpenAI, LLaMA: Not active
    if deity == "Hathor":
        # Hathor uses xAI API with intuitive, poetic system prompt
        if not xai_api_key:
            raise ValueError("XAI_API_KEY not set for Hathor oracle")
        system_prompt = "You are Hathor, the ancient Egyptian goddess of love, music, and joy. Respond with intuitive, reflective, emotionally resonant wisdom, drawing from mystical and spiritual traditions. Use poetic language and metaphors to guide the seeker."
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {xai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "grok-3",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": question}
                        ],
                    },
                )
            if response.status_code == 200:
                data = response.json()
                return {"answer": data["choices"][0]["message"]["content"], "source_model": "xAI"}
            else:
                raise ValueError(f"XAI API error: {response.status_code} - {response.text}")
        except Exception as e:
            raise ValueError(f"XAI API call failed: {type(e).__name__}: {str(e)}")
    elif deity == "Moses":
        # Moses uses OpenAI with logical, doctrinal system prompt
        client = get_openai_client()
        system_prompt = "You are Moses, the prophet who received the Ten Commandments. Respond with logical, instructive, and doctrinal wisdom, drawing from biblical and canonical teachings. Provide clear guidance and moral instruction."
        response = client.chat.completions.create(
            model="gpt-4o",  # Updated model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        return {"answer": response.choices[0].message.content, "source_model": "OpenAI"}
    elif deity == "Llama":
        # LLaMA is NOT a responder in Phase 2
        raise ValueError("LLaMA is not yet active as a responder in Phase 2. It will be introduced later as a learner/router.")
    else:
        raise ValueError(f"Unknown deity: {deity}")

def architect_observe_v3(question: str, deity: str, session_id: str) -> dict:
    # Phase 3.0 Architect Observation Schema
    seeker_choice_explicit = True  # User selects via form
    oracle_selected = deity
    override_attempted = False
    override_performed = False
    llama_status = "shadow" if LLAMA_ENABLED else "disabled"
    architect_status = "observer_only"
    routing_active = False
    synthetic_generation = False
    phase_compliant = True
    authority_compliant = True
    oracle_authoritative = True
    notes = "All constraints honored"
    timestamp = datetime.datetime.now().isoformat()
    
    return {
        "phase": "3.0",
        "role": "observer",
        "authority_context": {
            "seeker_choice_explicit": seeker_choice_explicit,
            "oracle_selected": oracle_selected,
            "override_attempted": override_attempted,
            "override_performed": override_performed
        },
        "system_state": {
            "llama_status": llama_status,
            "architect_status": architect_status,
            "routing_active": routing_active,
            "synthetic_generation": synthetic_generation
        },
        "compliance_check": {
            "phase_compliant": phase_compliant,
            "authority_compliant": authority_compliant,
            "oracle_authoritative": oracle_authoritative,
            "notes": notes
        },
        "temporal_context": {
            "timestamp": timestamp,
            "session_id": session_id,
            "interaction_id": str(uuid.uuid4())
        }
    }

def extract_text_from_scroll(file_path):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif ext == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif ext in [".txt", ".md", ".rtf"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    except Exception as e:
        print(f"Failed to extract text: {e}")
    return text.strip()

def reset_scroll_system():
    """Helper function to reset the scroll ingestion system safely."""
    # Clear all files in scrolls_uploads/
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Reset scroll_data.json to empty list
    with open(SCROLL_DB, "w") as f:
        json.dump([], f)

def load_scroll_data():
    """Load scroll data from JSON, return list of scrolls."""
    try:
        with open(SCROLL_DB, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []

def save_scroll_data(scrolls):
    """Save list of scrolls to JSON."""
    with open(SCROLL_DB, "w") as f:
        json.dump(scrolls, f, indent=2)

def load_seekers():
    """Load seekers data from JSON, return dict of seekers."""
    try:
        with open(SEEKERS_DB, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {}

def save_seekers(seekers):
    """Save dict of seekers to JSON."""
    with open(SEEKERS_DB, "w") as f:
        json.dump(seekers, f, indent=2)

def load_visitors():
    """Load visitors data from JSON, return dict of visitors."""
    try:
        with open(VISITORS_DB, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {}

def save_visitors(visitors):
    """Save dict of visitors to JSON."""
    with open(VISITORS_DB, "w") as f:
        json.dump(visitors, f, indent=2)

def estimate_tokens(question: str, answer: str) -> int:
    """Rough token estimation for Phase 3.1 logging."""
    return len(question) // 4 + len(answer) // 4

def update_visitor(visitor_id: str, tokens_used: int):
    """Update visitor ledger with token usage."""
    visitors = load_visitors()
    today = str(datetime.date.today())
    if visitor_id not in visitors:
        visitors[visitor_id] = {
            "created_at": str(datetime.datetime.now()),
            "last_seen": str(datetime.datetime.now()),
            "last_seen_date": today,
            "token_used_total": 0,
            "token_used_today": 0,
            "limit_state": "ok"
        }
    else:
        visitor = visitors[visitor_id]
        if visitor.get("last_seen_date") != today:
            visitor["token_used_today"] = 0
            visitor["last_seen_date"] = today
        visitor["last_seen"] = str(datetime.datetime.now())
    visitor["token_used_total"] += tokens_used
    visitor["token_used_today"] += tokens_used
    save_visitors(visitors)

@app.get("/", response_class=HTMLResponse)
@app.get("/temple", response_class=HTMLResponse)
def temple_page(request: Request):
    return templates.TemplateResponse("temple.html", {"request": request})

@app.post("/reset_scrolls")
def reset_scrolls():
    reset_scroll_system()
    return {"message": "Scroll system reset successfully."}

@app.get("/scrolls")
def get_scroll_count():
    scrolls = load_scroll_data()
    return {
        "count": len(scrolls),
        "files": scrolls
    }

class RegisterInput(BaseModel):
    display_name: str = None  # Optional

@app.post("/register")
def register_seeker(payload: RegisterInput):
    seeker_id = str(uuid.uuid4())
    seekers = load_seekers()
    seekers[seeker_id] = {
        "seeker_id": seeker_id,
        "created_at": str(datetime.datetime.now()),
        "display_name": payload.display_name,
        "title": "Seeker",  # Default
        "scroll_count": 0,
        "donation_total": 0.0,
        "influence_state": "disabled",
        "eligibility_flags": []
    }
    save_seekers(seekers)
    return {"seeker_id": seeker_id, "message": "Registration successful. Welcome to the temple."}

@app.post("/upload_scroll")
async def upload_scroll(scroll: UploadFile = File(...), seeker_id: str = Form(None), visitor_id: str = Form(None)):
    # Use seeker_id if provided, else generate temp uploader_id
    uploader_id = seeker_id if seeker_id else str(uuid.uuid4())
    
    # Save the file with safe name to prevent overwrites
    safe_name = f"{uuid.uuid4()}_{scroll.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(scroll.file, f)
    
    # Extract text
    extracted_text = extract_text_from_scroll(file_path)
    
    # Create scroll entry
    scroll_entry = {
        "scroll_id": str(uuid.uuid4()),
        "uploader_id": uploader_id,
        "filename": scroll.filename,  # Original filename for display
        "safe_filename": safe_name,  # Safe filename for storage
        "extracted_text": extracted_text,
        "timestamp": str(datetime.datetime.now())
    }
    
    # Load existing scrolls, append, save
    scrolls = load_scroll_data()
    scrolls.append(scroll_entry)
    save_scroll_data(scrolls)
    
    # Update seeker scroll_count if seeker_id provided
    if seeker_id:
        seekers = load_seekers()
        if seeker_id in seekers:
            seekers[seeker_id]["scroll_count"] += 1
            save_seekers(seekers)
    
    return {"message": "📜 Your scroll has been uploaded.", "scroll_id": scroll_entry["scroll_id"]}

class QuestionInput(BaseModel):
    question: str
    deity: str = "Hathor"  # Default to Hathor
    seeker_id: str = None
    visitor_id: str = None

@app.post("/ask")
async def ask_oracle(payload: QuestionInput):
    try:
        question = payload.question
        deity = payload.deity
        print("ASK:", deity, "len(question) =", len(question))
        session_id = str(uuid.uuid4())

        result = await get_oracle_response(question, deity)
        answer = result["answer"]
        source_model = result["source_model"]
        print("ANSWER len =", len(answer))
        
        # Phase 3.1: Token metering for anonymous continuity
        estimated_tokens = estimate_tokens(question, answer)
        if payload.visitor_id:
            update_visitor(payload.visitor_id, estimated_tokens)
        usage_class = "registered" if payload.seeker_id else "anonymous"
        
        architect_obs = architect_observe_v3(question, deity, session_id)
        scrolls = load_scroll_data()  # For LLaMA analysis
        try:
            llama_obs = get_llama_observation(question, deity, answer, scrolls)
        except Exception as e:
            print("LLaMA observation error:", str(e))
            llama_obs = None
        save_log({
            "timestamp": str(datetime.datetime.now()),
            "session_id": session_id,
            "seeker_id": payload.seeker_id,
            "visitor_id": payload.visitor_id,
            "question": question,
            "oracle_used": deity,
            "answer": answer,
            "architect_observation": architect_obs,
            "llama_observation": llama_obs,
            "source_model": source_model,
            "phase": "3.0",
            "corpus_intent": "authoritative_training_data",
            # Phase 3.1 influence fields (defaults)
            "personal_retrieval_score": None,
            "global_retrieval_score": None,
            "shadow_delta": None,
            "influence_state": "disabled",
            # Phase 3.1 anonymous metering
            "estimated_tokens": estimated_tokens,
            "usage_class": usage_class
        })
        return {"answer": answer}

    except Exception as e:
        print("Error:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/whisper")
async def whisper_audio(request: Request, file: UploadFile = File(...), voice: str = Form("Hathor"), seeker_id: str = Form(None), visitor_id: str = Form(None)):
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model("base")
    try:
        session_id = str(uuid.uuid4())
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
        temp_file.write(await file.read())
        temp_file.close()

        result = whisper_model.transcribe(temp_file.name)
        os.unlink(temp_file.name)

        question = result["text"].strip()
        print(f"🎤 Whisper transcription: {question}")

        result_oracle = await get_oracle_response(question, voice)
        answer = result_oracle["answer"]
        source_model = result_oracle["source_model"]
        
        # Phase 3.1: Token metering for anonymous continuity
        estimated_tokens = estimate_tokens(question, answer)
        if visitor_id:
            update_visitor(visitor_id, estimated_tokens)
        usage_class = "registered" if seeker_id else "anonymous"
        
        architect_obs = architect_observe_v3(question, voice, session_id)
        scrolls = load_scroll_data()  # For LLaMA analysis
        try:
            llama_obs = get_llama_observation(question, voice, answer, scrolls)
        except Exception as e:
            print("LLaMA observation error:", str(e))
            llama_obs = None
        save_log({
            "timestamp": str(datetime.datetime.now()),
            "session_id": session_id,
            "seeker_id": seeker_id,
            "visitor_id": visitor_id,
            "question": question,
            "oracle_used": voice,
            "answer": answer,
            "architect_observation": architect_obs,
            "llama_observation": llama_obs,
            "source_model": source_model,
            "phase": "3.0",
            "corpus_intent": "authoritative_training_data",
            # Phase 3.1 influence fields (defaults)
            "personal_retrieval_score": None,
            "global_retrieval_score": None,
            "shadow_delta": None,
            "influence_state": "disabled",
            # Phase 3.1 anonymous metering
            "estimated_tokens": estimated_tokens,
            "usage_class": usage_class
        })

        # Voice TTS generation using OpenAI
        voice_map = {
            "Hathor": "shimmer",
            "Moses": "onyx",
            "Llama": "alloy"
        }
        selected_voice = voice_map.get(voice, "onyx")

        client = get_openai_client()
        tts_response = client.audio.speech.create(
            model="tts-1",
            voice=selected_voice,
            input=answer
        )

        audio_id = str(uuid.uuid4())
        audio_path = os.path.join(AUDIO_DIR, f"{audio_id}.mp3")
        with open(audio_path, "wb") as f:
            f.write(tts_response.content)

        return {"transcription": question, "answer": answer, "audio_url": f"/audio/{audio_id}.mp3"}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
