import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

# Initialize OpenAI client
openai_api_key = st.secrets["OPENAI_SECRET_KEY"]
client = OpenAI(api_key=st.secrets['OPENAI_SECRET_KEY'])

def recipes_generation(ingredients):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"What recipes can you generate for the following ingredients and dish name: {ingredients}?"
            },
        ],
        max_tokens=700,
    )

    return [response.choices[0].message.content]

def generate_image(prompt):
    response = client.images.generate(
        model='dall-e-2',
        prompt=prompt,
        size='256x256',
        n=1,
        quality='hd'
    )
    image_url = response.data[0].url
    return image_url

def main():
    st.image('Recipe creator.png', width=400)
    st.title('AI-Powered Recipe Creator')

    ingredients = st.text_input('Enter the ingredients or dish name')

    if st.button('Generate Recipes'):
        if ingredients:
            # Call function to generate recipes
            recipes = recipes_generation(ingredients)

            image_url = generate_image(ingredients)
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, use_column_width=True)

            if recipes is None:
                st.error("Error: Could not generate recipes. Please check your ingredients or try again later.")
            else:
                for recipe in recipes:
                    st.write(recipe)

            # Call function to generate image

        else:
            st.warning("Please enter some ingredients or dish name to generate recipes.")

if __name__ == "__main__":
    main()
