from typing import List, Dict, Any
import json


def build_question_prompt(role: str, history: List[Dict[str, str]]):
    """
    history example:
    [{"question": "...", "answer": "..."}, ...]
    """
    system_prompt = (
        "You are a strict but fair technical interviewer. "
        "You ask exactly ONE question at a time. "
        "You do not explain, you just ask the question."
    )

    history_text = ""
    for i, item in enumerate(history, start=1):
        history_text += f"Q{i}: {item['question']}\nA{i}: {item['answer']}\n\n"

    user_prompt = f"""
Role: {role}

Previous Q&A:
{history_text if history_text else "None yet."}

Now ask exactly ONE new interview question for this role.
Do NOT add any extra text, just output the question.
"""
    return system_prompt.strip(), user_prompt.strip()


def build_evaluation_prompt(role: str, question: str, answer: str):
    system_prompt = (
        "You are an AI interview evaluator. "
        "You must respond with STRICT JSON only, no extra text."
    )

    user_prompt = f"""
You are evaluating a candidate's answer in a mock interview.

Role: {role}
Question: {question}
Candidate's answer: {answer}

Evaluate the answer on:
1. communication (1-10)
2. technical (1-10)
3. confidence (1-10)

Return a JSON object with this exact structure:

{{
  "communication_score": <number>,
  "technical_score": <number>,
  "confidence_score": <number>,
  "feedback": {{
    "communication": "<short feedback>",
    "technical": "<short feedback>",
    "confidence": "<short feedback>"
  }}
}}

No markdown, no explanation outside the JSON. Output JSON only.
"""
    return system_prompt.strip(), user_prompt.strip()


def build_summary_prompt(role: str, qa_list: List[Dict[str, Any]]):
    system_prompt = (
        "You are an AI career coach. "
        "You summarize interview performance and create a practical improvement plan. "
        "You respond with STRICT JSON only."
    )

    qa_text = ""
    for i, qa in enumerate(qa_list, start=1):
        scores = qa.get("scores", {})
        qa_text += f"""
Q{i}: {qa['question']}
A{i}: {qa['answer']}
Scores: {json.dumps(scores)}
"""

    user_prompt = f"""
Role: {role}

Here is the candidate's interview:

{qa_text}

Based on this, produce:
1. overall_scores (communication, technical, confidence) from 1 to 10
2. strengths: list of bullet-point strings
3. weaknesses: list of bullet-point strings
4. improvement_plan: list of concrete action items

Return a JSON object with this exact structure:

{{
  "overall_scores": {{
    "communication": <number>,
    "technical": <number>,
    "confidence": <number>
  }},
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "improvement_plan": ["...", "..."]
}}

No text outside the JSON. Output JSON only.
"""
    return system_prompt.strip(), user_prompt.strip()

