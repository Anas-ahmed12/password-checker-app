import streamlit as st
import re
import random
import string

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*()_+=]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    return min(score, 5), feedback

def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+="
    return ''.join(random.choice(characters) for _ in range(14))

def evaluate_entropy(password):
    entropy = len(set(password)) * len(password)
    if entropy > 100:
        return "High", "green"
    elif entropy > 50:
        return "Medium", "orange"
    else:
        return "Low", "red"

def suggest_improvements(password):
    suggestions = []
    if len(password) < 12:
        suggestions.append("Increase password length to at least 12 characters.")
    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters for better security.")
    if not re.search(r"[a-z]", password):
        suggestions.append("Include lowercase letters.")
    if not re.search(r"\d", password):
        suggestions.append("Use numbers to strengthen your password.")
    if not re.search(r"[!@#$%^&*()_+=]", password):
        suggestions.append("Special characters make passwords harder to crack.")
    return suggestions

# Streamlit UI
st.set_page_config(page_title="AI Password Strength Meter", page_icon="🔐", layout="centered")
st.title("🔐 AI-Powered Password Strength Checker")
st.subheader("Ensure your password is strong and secure!")

st.markdown("""
<style>
    body { background-color: #f8f9fa; }
    .stProgress > div > div > div > div { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

password = st.text_input("Enter Your Password", type="password")

if password:
    score, feedback = check_password_strength(password)
    entropy_level, entropy_color = evaluate_entropy(password)
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    colors = ["red", "orange", "yellow", "lightgreen", "green"]
    
    st.markdown(f"**Strength:** <span style='color:{colors[score-1]}; font-weight:bold'>{strength_levels[score-1]}</span>", unsafe_allow_html=True)
    st.progress(score / 5)
    
    st.markdown(f"**Entropy Level:** <span style='color:{entropy_color}; font-weight:bold'>{entropy_level}</span>", unsafe_allow_html=True)
    
    if feedback:
        st.warning("\n".join(feedback))
    else:
        st.success("✅ Your password is very strong!")
    
    improvements = suggest_improvements(password)
    if improvements:
        st.info("🔹 Suggested Improvements:")
        for suggestion in improvements:
            st.write(f"- {suggestion}")

if st.button("🔑 Generate Secure Password"):
    strong_password = generate_strong_password()
    st.text_input("Generated Password", value=strong_password, disabled=True)
    st.info("🔹 Tip: Use a mix of uppercase, lowercase, numbers, and special characters!")
