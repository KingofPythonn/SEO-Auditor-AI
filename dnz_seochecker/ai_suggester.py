# dnz_seochecker/ai_suggester.py

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

class AISuggester:
    def __init__(self):
        load_dotenv()  # Load from .env file

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise EnvironmentError("Missing OPENROUTER_API_KEY in environment or .env file.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = "deepseek/deepseek-r1-0528:free"

    def build_prompt(self, report):
        # Same as before
        return (
            "You are an advanced SEO consultant.\n"
            "Analyze this website SEO report (JSON) and provide actionable, detailed, human-readable recommendations.\n"
            "Be specific about missing elements, too-long or too-short fields, broken links, meta-tags, and general SEO best practices.\n"
            "Respond in clear bullet points in English or Persian if appropriate.\n\n"
            f"SEO Report JSON:\n{json.dumps(report, indent=2, ensure_ascii=False)}"
        )
        

    def get_ai_suggestions(self, report):
        prompt = self.build_prompt(report)
        print("[INFO] Sending report to OpenRouter model for AI suggestions...")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an advanced SEO consultant."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_response = response.choices[0].message.content
        print("[INFO] Received AI suggestions.")
        return ai_response
