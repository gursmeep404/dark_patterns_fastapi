# import openai
# import os
# import json
# import re
# from dotenv import load_dotenv
# load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY")

# def analyze_frame_with_gpt(base64_image):
#     prompt = (
#         "You are analyzing a user interface screenshot to detect the presence of dark patterns.\n\n"
#         "Carefully examine the image and identify any dark patterns present. Restrict your classification to ONLY the following 13 categories:\n"
#         "1. False Urgency\n"
#         "2. Basket Sneaking\n"
#         "3. Confirmshaming\n"
#         "4. Forced Action\n"
#         "5. Subscription Trap\n"
#         "6. Interface Interference\n"
#         "7. Bait & Switch\n"
#         "8. Drip Pricing\n"
#         "9. Disguised Advertisement\n"
#         "10. Nagging\n"
#         "11. Trick Question\n"
#         "12. SaaS Billing\n"
#         "13. Rogue Malware\n\n"
#         "Return your response strictly in valid JSON with the following fields:\n"
#         "- text: a snippet of the visible UI text that contains the dark pattern (or is evidence of it)\n"
#         "- pattern: one of the 13 categories listed above (do not invent new ones)\n"
#         "- fix: how this can be improved to respect user rights\n"
#         "- violations: list of legal rules or regulations that may be violated (e.g., GDPR, DPDP, FTC guidelines)\n\n"
#         "Only output valid JSON and no other text. Do not explain your reasoning. Assume the image is from a real-world product."
#     )


#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/jpeg;base64,{base64_image}"
#                             }
#                         },
#                         {
#                             "type": "text",
#                             "text": prompt
#                         }
#                     ]
#                 }
#             ],
#             temperature=0.3
#         )

#         content = response["choices"][0]["message"]["content"]
#         print("GPT raw response:", repr(content))

#         # Strip code block formatting
#         content_cleaned = re.sub(r"^```json|```$", "", content.strip(), flags=re.MULTILINE).strip()

#         return json.loads(content_cleaned)

#     except Exception as e:
#         print(f"Error analyzing frame: {e}")
#         return {
#             "text": "",
#             "pattern": "",
#             "fix": "",
#             "violations": []
#         }

# def analyze_frame_with_gpt(base64_image):
#     # Instead of calling OpenAI, just return dummy data
#     return {
#         "text": "Are you sure you want to cancel? You will lose your benefits.",
#         "pattern": "confirmshaming",
#         "fix": "Use neutral language like 'Are you sure you want to cancel?'",
#         "violations": ["GDPR Article 7", "DPDP Clause 6"]
#     }
import google.generativeai as genai
import os
import json
import re
import base64 # Import base64 for decoding
from dotenv import load_dotenv
load_dotenv()

# Configure the Gemini API key from environment variables
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in your .env file.")
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_frame_with_gemini(base64_image):
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
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Decode the base64 image string to bytes
        image_data_bytes = base64.b64decode(base64_image)

        # Create an inline image part
        image_part = {
            "mime_type": "image/jpeg", # Or image/png, image/webp depending on your actual image type
            "data": image_data_bytes
        }
        
        # The contents list now includes the image part and the text prompt
        contents = [image_part, {"text": prompt}]
        
        response = model.generate_content(
            contents,
            generation_config=genai.GenerationConfig(
                temperature=0.3
            )
        )

        content = response.text
        print("Gemini raw response:", repr(content))

        content_cleaned = re.sub(r"^```json|```$", "", content.strip(), flags=re.MULTILINE).strip()

        return json.loads(content_cleaned)

    except Exception as e:
        print(f"Error analyzing frame with Gemini: {e}")
        return {
            "text": "",
            "pattern": "",
            "fix": "",
            "violations": []
        }
