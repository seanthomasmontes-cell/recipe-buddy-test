import os
import streamlit as st
import openai
from fpdf import FPDF

import os
import openai
import streamlit as st
from fpdf import FPDF

# Option 1: Hardcode your key (simplest, only for testing — not safe to share)
openai.api_key = "YOUR_OPENAI_API_KEY"


# Option 2: Safe way using environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")


st.title("Recipe Buddy 🍳")
st.write("Generate recipes from your pantry items!")

# User inputs
pantry = st.text_input("Pantry items (comma separated)", placeholder="e.g. pasta, tomato, garlic")
diet = st.selectbox("Diet", ["None","Vegetarian","Vegan","Gluten-free","Dairy-free","Nut-free"])
max_time = st.number_input("Max cook time (minutes)", min_value=5, max_value=240, value=30)
servings = st.number_input("Servings", min_value=1, value=2)

# Prompt template
prompt = f"""
You are a professional recipe writer. Create a clear recipe using ONLY these pantry items: {pantry}.
Constraints: Diet = {diet}, Max time = {max_time} minutes, Servings = {servings}.
Return: Title, Prep time, Cook time, Servings, Ingredient list with quantities, Numbered steps, One quick tip, 2 substitutions.
Keep it simple and beginner-friendly.
"""

if st.button("Generate Recipe"):
    if not pantry.strip():
        st.error("Please enter some pantry items first.")
    else:
        with st.spinner("Generating recipe..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=250
            )
            recipe_text = response["choices"][0]["message"]["content"]
        st.markdown("### Your Recipe")
        st.write(recipe_text)

        # Simple PDF download
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in recipe_text.split("\n"):
            pdf.multi_cell(0, 7, line)
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        st.download_button("Download PDF", data=pdf_bytes, file_name="recipe.pdf", mime="application/pdf")
venv/
__pycache__/
*.pyc
.env
