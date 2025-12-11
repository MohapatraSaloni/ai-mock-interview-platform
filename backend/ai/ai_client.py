import os
import json
from typing import List, Dict, Any

from dotenv import load_dotenv
import google.generativeai as genai

from .prompts import (
    build_question_prompt,
    build_evaluation_prompt,
    build_summary_prompt,
)

# 1. Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

# 2. Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# 3. Choose a model (flash is cheaper/faster, good for hackathon)
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


def _call_gemini(system_prompt: str, user_prompt: str) -> str:
    """
    Low-level helper: sends combined system + user prompt to Gemini
    and returns the response text.
    """
    full_prompt = system_prompt.strip() + "\n\n" + user_prompt.strip()

    response = model.generate_content(full_prompt)

    # response.text is the combined generated text
    return (response.text or "").strip()


# 4. High-level function: generate a new interview question
def generate_question(role: str, history: List[Dict[str, str]]) -> str:
    """
    role: 'ML Engineer', 'Data Analyst', etc.
    history: list of {'question': str, 'answer': str} from previous Q&A.

    Returns: a single new interview question as string.
    """
    system_prompt, user_prompt = build_question_prompt(role, history)
    question = _call_gemini(system_prompt, user_prompt)
    return question.strip()


# 5. High-level function: evaluate a candidate's answer
def evaluate_answer(role: str, question: str, answer: str) -> Dict[str, Any]:
    """
    role: job role (e.g. 'ML Engineer')
    question: the question asked
    answer: candidate's answer (transcript text)

    Returns: dict with scores + feedback, e.g.
    {
      "communication_score": 8,
      "technical_score": 7,
      "confidence_score": 6,
      "feedback": {
        "communication": "...",
        "technical": "...",
        "confidence": "..."
      }
    }
    """
    system_prompt, user_prompt = build_evaluation_prompt(role, question, answer)
    response_text = _call_gemini(system_prompt, user_prompt)

    # We expect Gemini to respond with pure JSON text (because of our prompt).
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback if model returns something unexpected
        data = {
            "communication_score": None,
            "technical_score": None,
            "confidence_score": None,
            "feedback": {
                "communication": "Could not parse evaluation response.",
                "technical": "Could not parse evaluation response.",
                "confidence": "Could not parse evaluation response.",
            },
            "raw_response": response_text,
        }

    return data


# 6. High-level function: generate final summary & improvement plan
def generate_final_summary(
    role: str, qa_list: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    qa_list: list of objects like:
    {
      "question": str,
      "answer": str,
      "scores": {
        "communication": number,
        "technical": number,
        "confidence": number
      }
    }

    Returns:
    {
      "overall_scores": {
        "communication": number,
        "technical": number,
        "confidence": number
      },
      "strengths": [str, ...],
      "weaknesses": [str, ...],
      "improvement_plan": [str, ...]
    }
    """
    system_prompt, user_prompt = build_summary_prompt(role, qa_list)
    response_text = _call_gemini(system_prompt, user_prompt)

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        data = {
            "overall_scores": None,
            "strengths": [],
            "weaknesses": [],
            "improvement_plan": [],
            "raw_response": response_text,
        }

    return data
