import streamlit as st
from scorer import ScoringEngine

# Set page config
st.set_page_config(page_title="Nirmaan AI Intern Case Study", layout="centered")

st.title("🗣️ AI Communication Coach")
st.write("Paste your self-introduction transcript below to get a detailed AI score.")

# Input area
transcript = st.text_area("Transcript", height=200, placeholder="Hello everyone, myself Muskan...")
duration = st.number_input("Audio Duration (seconds)", min_value=1, value=52)

# Button to trigger analysis
if st.button("Score My Speech"):
    if not transcript:
        st.error("Please enter a transcript first.")
    else:
        with st.spinner("Analyzing your speech... (This may take a moment first time)"):
            # Initialize engine and calculate
            engine = ScoringEngine()
            total_score, breakdown, feedback = engine.analyze(transcript, duration)
            
            # Display Overall Score
            st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>Overall Score: {total_score}/100</h1>", unsafe_allow_html=True)
            
            # Display Feedback
            if feedback:
                st.subheader("💡 Improvement Areas")
                for tip in feedback:
                    st.warning(tip)
            else:
                st.success("Great job! No major critical issues found.")

            # Display Detailed Breakdown
            st.subheader("📊 Detailed Rubric Breakdown")
            
            # Create a nice table-like display
            for criterion, score in breakdown.items():
                col1, col2 = st.columns([3, 1])
                col1.write(f"**{criterion}**")
                col2.write(f"{score} pts")
                st.progress(score / (30 if criterion == 'Keywords' else 15 if criterion in ['Filler Words', 'Engagement'] else 10 if criterion in ['Speech Rate', 'Grammar', 'Vocabulary'] else 5))
            
            st.info("Note: This tool uses AI for semantic matching and standard algorithms for grammar/pacing.")