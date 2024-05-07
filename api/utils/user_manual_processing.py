from pdf2image import convert_from_path
import base64
import tempfile
import json
from openai import OpenAI
from decouple import config  # Import config
import pdb

# Constants
API_KEY = config('API_KEY')
MODEL_NAME = "gpt-4-turbo"
TEMP_IMAGE_SUFFIX = '.png'
IMAGE_FORMAT = 'PNG'

client = OpenAI(api_key=API_KEY)

def convert_pdf_to_base64_images(pdf_path):
    images = convert_from_path(pdf_path)
    base64_images = []
    for image in images:
        with tempfile.NamedTemporaryFile(suffix=TEMP_IMAGE_SUFFIX) as temp_image:
            image.save(temp_image.name, IMAGE_FORMAT)
            with open(temp_image.name, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                base64_images.append(encoded_string.decode('utf-8'))
    return base64_images

def create_openai_prompt(base64_images):
    prompt = "Extract troubleshooting information from the attached images of a user manual. For each troubleshooting issue, follow the naming and formatting conventions used in the manual. Include the page number for each problem identified. Return the results in a clean JSON format only, without any additional explanations or text."
    content = [{"type": "text", "text": prompt}]
    for base64_image in base64_images:
        content.append({"type": "image_url", "image_url": { "url": f"data:image/png;base64,{base64_image}"}})
    return content

def get_troubleshooting_info(content):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": content}],
    )
    json_str = response.choices[0].message.content
    json_str = json_str.strip('`').replace('json\n', '').strip()
    return json.loads(json_str)

def main(pdf_path):
    base64_images = convert_pdf_to_base64_images(pdf_path)

    content = create_openai_prompt(base64_images)

    troubleshooting_info = get_troubleshooting_info(content)

    print(troubleshooting_info)

    return troubleshooting_info

if __name__ == "__main__":
    main()
