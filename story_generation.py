from dotenv import load_dotenv
load_dotenv()
import os
import logging
from google import genai
from gtts import gTTS
from io import BytesIO

# Set up logging (optional but helpful)
logging.basicConfig(level=logging.INFO)

# Load API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Initialize client
client = genai.Client(api_key=api_key)

def create_advanced_prompt(style):
    base_prompt = f"""
Your Persona: You are a friendly and engaging storyteller. Your goal is to tell a story that is fun and easy to read.
Your Main Goal: Write a story in simple, clear, and modern English.
Your Task: Create one single story that connects all the provided images in order.
Style Requirement: The story must fit the '{style}' genre.
Core Instructions:
1. Tell One Single Story: Connect all images into a narrative with a beginning, middle, and end.
2. Use Every Image: Include a key detail from each image.
3. Creative Interpretation: Infer the relationships between the images.
4. Nationality: Use only Indian names, characters, places, and personas.

Output Format:
- Title: Start with a simple and clear title.
- Length: The story must be between 4 and 5 paragraphs.
"""

    style_instruction = ""
    if style == "Morale":
        style_instruction = "\nSpecial Section: After the story, you MUST add a section starting with the exact tag [MORAL]: followed by the single-sentence moral of the story."
    elif style == "Mystery":
        style_instruction = "\nSpecial Section: After the story, you MUST add a section starting with the exact tag [SOLUTION]: that reveals the culprit and the key clue."
    elif style == "Thriller":
        style_instruction = "\nSpecial Section: After the story, you MUST add a section starting with the exact tag [TWIST]: that reveals a final, shocking twist."

    return base_prompt + style_instruction


def generate_story_from_images(images, style):
    try:
        prompt = create_advanced_prompt(style)
        
        # Gemini expects a list of parts: [text, image1, image2, ...]
        # So we build contents as: [prompt, img1, img2, ...]
        contents = [prompt] + images

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",  # ⚠️ Verify this model name!
            contents=contents
        )

        # Check if response was blocked
        if not response.text:
            # Sometimes .text is empty due to safety filters
            return "Error: The AI response was blocked for safety reasons. Please try different images."

        return response.text.strip()

    except Exception as e:
        error_msg = f"Error: Failed to generate story. Details: {str(e)}"
        logging.error(error_msg)
        return error_msg


def narrate_story(story_text):
    try:
        tts = gTTS(text=story_text, lang="en", slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        error_msg = f"Error: Audio narration failed. {str(e)}"
        logging.error(error_msg)
        return None  # Return None so caller can handle it