import openai
import os
import json
import re
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_frame_with_gpt(base64_image):
    prompt = (
        "You are analyzing a user interface screenshot to detect the presence of dark patterns.\n\n"
        "Carefully examine the image and identify any dark patterns present. Restrict your classification to ONLY the following 13 categories:\n"
        "1. False Urgency\n"
        "2. Basket Sneaking\n"
        "3. Confirmshaming\n"
        "4. Forced Action\n"
        "5. Subscription Trap\n"
        "6. Interface Interference\n"
        "7. Bait & Switch\n"
        "8. Drip Pricing\n"
        "9. Disguised Advertisement\n"
        "10. Nagging\n"
        "11. Trick Question\n"
        "12. SaaS Billing\n"
        "13. Rogue Malware\n\n"
        "Return your response strictly in valid JSON with the following fields:\n"
        "- text: a snippet of the visible UI text that contains the dark pattern (or is evidence of it)\n"
        "- pattern: one of the 13 categories listed above (do not invent new ones)\n"
        "- fix: how this can be improved to respect user rights\n"
        "- violations: list of legal rules or regulations that may be violated (e.g., GDPR, DPDP, FTC guidelines)\n\n"
        "Only output valid JSON and no other text. Do not explain your reasoning. Assume the image is from a real-world product."
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

        # Strip code block formatting
        content_cleaned = re.sub(r"^```json|```$", "", content.strip(), flags=re.MULTILINE).strip()

        return json.loads(content_cleaned)

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
