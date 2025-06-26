import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
def analyze_frame_with_gpt(base64_image):
    prompt = (
        "This is a screenshot from a user interface.\n"
        "Identify any dark patterns and return a JSON with the following fields:\n"
        "- text: visible line with dark pattern\n"
        "- pattern: type/category (e.g., 'sneak into basket')\n"
        "- fix: how to fix the UI\n"
        "- violations: list of possible legal rules broken (e.g., GDPR, DPDP)\n"
        "Only output valid JSON."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            temperature=0.3
        )

        content = response["choices"][0]["message"]["content"]
        print("GPT raw response:", repr(content))  

        return json.loads(content)

    except Exception as e:
        print(f"Error analyzing frame: {e}")
        return {
            "text": "",
            "pattern": "",
            "fix": "",
            "violations": []
        }


# def analyze_frame_with_gpt(base64_image):
#     # Instead of calling OpenAI, just return dummy data
#     return {
#         "text": "Are you sure you want to cancel? You will lose your benefits.",
#         "pattern": "confirmshaming",
#         "fix": "Use neutral language like 'Are you sure you want to cancel?'",
#         "violations": ["GDPR Article 7", "DPDP Clause 6"]
#     }
