import streamlit as st
import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

load_dotenv()
llm = Gemini(model="models/gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

# Page Config
st.set_page_config(
    page_title="Ad Copy Generator",
    page_icon="🚀",
    layout="centered",
)

# App Header
st.title("🚀 Ad Copy Generator")
st.subheader("Fill out the campaign details below to generate ad copies")

# Form
with st.form("ad_copy_form"):
    st.markdown("### 📦 Product Details")
    product_name = st.text_input("Product Name")
    product_description = st.text_area("Product Description")
    problem_solved = st.text_area("The Problem It Solves")
    usp = st.text_input("Unique Selling Proposition (USP) [Optional]")

    st.markdown("### 🎯 Target Audience")
    age_group = st.selectbox(
        "Target Age Group",
        ["18-24", "25-34", "35-44", "45-54", "55+"]
    )
    gender = st.selectbox(
        "Target Gender",
        ["All Genders", "Male", "Female", "Non-binary"]
    )

    st.markdown("### 🏆 Campaign Settings")
    campaign_goal = st.selectbox(
        "Campaign Goal",
        ["Lead Generation", "Sales", "Brand Awareness", "Website Visits"]
    )
    tone = st.selectbox(
        "Desired Tone",
        ["Friendly", "Professional", "Fun"]
    )

    submitted = st.form_submit_button("Generate Ad Copy")

if submitted:
    # Combine inputs into a prompt context string
    context = f"""
    Product Name: {product_name}
    Product Description: {product_description}
    The Problem It Solves: {problem_solved}
    Unique Selling Proposition (USP): {usp}
    Target Audience:
        Age Group: {age_group}
        Gender: {gender}
    Campaign Goal: {campaign_goal}
    Desired Tone: {tone}
    """

    # --- Define the ad generation function (must accept arguments) ---
    def generate_ad(platform: str) -> str:
        prompt = (
            f"Generate a high-converting ad copy for {platform}.\n"
            f"Product Details:\n{context}\n\n"
            f"Requirements:\n"
            f"- Tailor the ad copy for {platform} audience.\n"
            f"- Match the campaign goal: {campaign_goal}.\n"
            f"- Keep the tone: {tone}.\n"
            f"- Use an engaging Call-to-Action.\n"
        )
        response = llm.complete(prompt)
        return response.text.strip()

    # --- Wrap the function as a FunctionTool with correct signature ---
    ad_tool = FunctionTool.from_defaults(
        fn=generate_ad,
        name="generate_ad",
        description="Generate ad copy for a specific platform. Accepts platform name as argument.",
    )

    # --- Create a single agent with the tool ---
    ad_agent = FunctionCallingAgentWorker.from_tools(
        [ad_tool],
        llm=llm,
        system_prompt="You are an expert ad copywriter. You generate high-converting ads for specific platforms using structured inputs.",
    )

    ad_runner = AgentRunner(ad_agent)

    # --- Generate ad copies for all platforms ---
    platforms = ["Facebook", "Instagram", "LinkedIn", "Google Ads"]
    ad_copies = {}

    for platform in platforms:
        response = ad_runner.chat(f"Generate ad copy for {platform}")
        ad_copies[platform] = response.response

    # --- Display ad copies ---
    st.success("✅ Ad Copies Generated Successfully!")
    st.markdown("### ✨ Preview of Ad Copies:")
    for platform, copy in ad_copies.items():
        with st.expander(f"{platform} Ad Copy"):
            st.write(copy)

    # --- Allow download ---
    all_ads_text = "\n\n".join(
        f"--- {platform} Ad Copy ---\n{copy}" for platform, copy in ad_copies.items()
    )
    st.download_button(
        label="📥 Download All Ad Copies (TXT)",
        data=all_ads_text,
        file_name="ad_copies.txt",
        mime="text/plain",
    )
