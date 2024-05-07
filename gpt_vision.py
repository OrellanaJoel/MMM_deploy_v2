"""This module will use GPT Vision capabilities to analyze graphs from MMM model results."""

import requests
from encode_image import encode_figure_to_base64
import streamlit as st

OPENAI_API_KEY = st.secrets.OPENAI_API_KEY["OPENAI_API_KEY"]

def generate_insights_with_vision(figure, api_key=OPENAI_API_KEY, media_names=None):
    """Generate business insights with the given figure and prompt."""
    # Getting the base64 string
    print('Encoding figure...')
    base64_image = encode_figure_to_base64(figure)
    print("Encoded figure.")
    prompt = f"""The following image is a graph of the results of a Media Mix Model.
        Act as a Media Mix Model expert and return useful insights, provide a condensed summarization that could be used to take bussiness decisions.
      Analyze the image and provide insights on the results.
      You can extract the media channel names from this list: {media_names} or extract from the graph.
      If you could not extract the media name correclty, change your strategy to return insights without media names.
      These insights could be used for marketers, data scientist and company owners. So they should be short, helpful and concise.
      Return only short bullet points, no more than 3 or 4, no additional text. Impersonal, Professional and Neutral text. Don't add any other text.
      Return as markdown format. Add emphasis, bold and italic to show key aspects when necessary.
      Dont add prefix or suffix for markdown. Don't add this: ```markdown or ```
  """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 500
    }
    print('Creating a detailed analysis...')
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30)
    print(response.status_code)
    print(response.text)
    return response.json()['choices'][0]['message']['content']