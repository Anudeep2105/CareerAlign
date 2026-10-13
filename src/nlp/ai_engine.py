import json
import openai
from typing import Dict, Any

class AIParser:
    def __init__(self, api_key: str):
        # Using Groq for free, fast inference (OpenAI compatible)
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def parse_resume_text(self, text: str, model: str = "llama-3.1-8b-instant") -> Dict[str, Any]:
        prompt = f"""
        Extract the following information from the resume text and return it as a structured JSON object.
        Fields to extract:
        - contact_details: {{name, email, phone, location}}
        - work_history: [{{job_title, company, start_date, end_date, responsibilities: []}}]
        - education: [{{degree, school, graduation_year}}]
        - skills: []
        
        Resume Text:
        {text}
        """
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are a professional HR resume parser. Output ONLY valid JSON."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

    def optimize_resume(self, current_resume_text: str, job_description: str, model: str = "llama-3.1-8b-instant") -> str:
        prompt = f"""
        You are an expert ATS (Applicant Tracking System) optimizer.
        Task: Rewrite the provided resume to be highly compatible with the given Job Description.
        
        Guidelines:
        1. Identify key skills and keywords from the JD.
        2. Integrate those keywords naturally into the professional experience and skills sections.
        3. Quantify achievements (use metrics like %, $, numbers).
        4. Maintain a professional, clean, and standard ATS-friendly format.
        5. Do NOT lie; only highlight and rephrase existing experience to match the JD requirements.
        
        Job Description:
        {job_description}
        
        Current Resume:
        {current_resume_text}
        
        Output the final optimized resume as a professionally formatted text document.
        """
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are a professional ATS resume writer."},
                      {"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content


