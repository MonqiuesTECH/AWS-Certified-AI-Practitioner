import streamlit as st
import boto3
import json
from botocore.exceptions import ClientError
from questions import quiz_data  # This dynamically pulls all 90 questions!

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AIF-C01 Study Hub",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
# This is what allows the app to remember your place out of the 90 questions
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None

def next_question():
    st.session_state.current_q += 1
    st.session_state.selected_answer = None

def reset_quiz():
    st.session_state.current_q = 0
    st.session_state.selected_answer = None

# --- SIDEBAR & ENVIRONMENT SETUP ---
with st.sidebar:
    st.title("AWS AIF-C01 Hub")
    st.markdown("Accelerated Exam Prep")
    
    st.subheader("Environment")
    env_mode = st.radio("AWS Target", ["LocalStack (Local)", "AWS Cloud (Live)"])
    
    if env_mode == "LocalStack (Local)":
        endpoint_url = "http://localhost:4566"
        st.info("Operating in LocalStack mode.")
    else:
        endpoint_url = None
        st.warning("Operating in Live AWS mode. Watch billing!")

    st.divider()
    page = st.radio("Exam Domains", [
        "1. Adaptive Simulator (Exam Prep)", 
        "2. Bedrock API Playground", 
        "3. Security & Governance"
    ])

# --- HELPER FUNCTIONS ---
def get_bedrock_client():
    """Initializes boto3 client based on selected environment."""
    if env_mode == "LocalStack (Local)":
        return boto3.client('bedrock-runtime', region_name='us-east-1', 
                            endpoint_url=endpoint_url, aws_access_key_id="test", aws_secret_access_key="test")
    else:
        return boto3.client('bedrock-runtime', region_name='us-east-1')

# --- PAGE 1: ADAPTIVE SIMULATOR (DOMAIN 1) ---
if page == "1. Adaptive Simulator (Exam Prep)":
    st.header("🤖 Cyber Punk Training Module: Adaptive Simulator")
    st.write("*(Operating at NORMAL Difficulty Level)*")
    
    # This automatically adjusts whether you have 5 or 90 questions in your file
    total_questions = len(quiz_data)
    
    if st.session_state.current_q < total_questions:
        q = quiz_data[st.session_state.current_q]
        st.markdown(f"### Question: {st.session_state.current_q + 1} / {total_questions}")
        st.write(q["question"])
        
        # User makes a selection
        choice = st.radio("Select an answer:", q["options"], index=None, key=f"q_{st.session_state.current_q}")
        
        if choice:
            st.session_state.selected_answer = choice
            
            # Show customized feedback from the questions.py file
            st.markdown(q["explanations"][choice])
            
            # Show Next Button
            st.button("Next Question ➡️", on_click=next_question, type="primary")
            
    else:
        st.success(f"🎉 You've completed all {total_questions} questions in the Adaptive Simulator!")
        st.button("Restart Simulator", on_click=reset_quiz)

# --- PAGE 2: BEDROCK PLAYGROUND (DOMAINS 2 & 3) ---
elif page == "2. Bedrock API Playground":
    st.header("⚡ Amazon Bedrock API Tester")
    
    with st.expander("📖 Guided Lab Instructions (Click to open)", expanded=True):
        st.markdown("""
        **Exam Focus: Model Invocations & Token Parameters**
        To master this section for the exam, complete the following scenarios:
        1. **Test Latency vs. Output:** Select `anthropic.claude-v2`, set max tokens to 500, and ask it to "Write a 3 paragraph essay on cloud computing." Watch how long it takes.
        2. **Test Hallucination Mitigation (Temperature):** Set the Temperature to `0.0`. Ask it a factual question ("What is the capital of France?"). A temperature of 0 ensures deterministic, highly focused answers. 
        3. **Test Creative Variance:** Change the Temperature to `1.0` and ask it to "Write a poem about a server crashing." A temperature of 1 introduces randomness and creativity.
        """)

    col1, col2 = st.columns([1, 2])
    with col1:
        model_id = st.selectbox("Select Foundation Model", [
            "anthropic.claude-v2",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "meta.llama3-8b-instruct-v1:0"
        ])
        max_tokens = st.slider("Max Tokens", 50, 1000, 200)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        
    with col2:
        prompt_text = st.text_area("Enter your prompt:", "Explain the difference between RAG and Fine-Tuning in 3 sentences.")
        if st.button("Invoke Model", type="primary"):
            client = get_bedrock_client()
            
            # Formatting payload based on specific model requirements
            if "claude" in model_id:
                body = json.dumps({
                    "prompt": f"\n\nHuman:{prompt_text}\n\nAssistant:",
                    "max_tokens_to_sample": max_tokens,
                    "temperature": temperature
                })
            else:
                body = json.dumps({"inputText": prompt_text})

            try:
                with st.spinner("Invoking model..."):
                    response = client.invoke_model(modelId=model_id, contentType="application/json", accept="application/json", body=body)
                    response_body = json.loads(response.get('body').read())
                    st.write(response_body.get('completion', response_body))
            except Exception as e:
                st.error("API Call Failed. Ensure your AWS credentials are set or LocalStack is running.")
                st.code(str(e))

# --- PAGE 3: SECURITY SIMULATOR (DOMAINS 4 & 5) ---
elif page == "3. Security & Governance":
    st.header("🛡️ Responsible AI & IAM Simulator")
    
    with st.expander("📖 Guided Lab Instructions (Click to open)", expanded=True):
        st.markdown("""
        **Exam Focus: Principle of Least Privilege**
        AWS heavily tests your ability to spot bad security policies. 
        1. **Trigger the Alert:** Click "Analyze Policy" on the default JSON below. Notice how it flags the wildcard `s3:*`. This is an exam anti-pattern.
        2. **Fix the Policy:** Edit the JSON text box. Change `"s3:*"` to `"s3:GetObject"`. Change the Resource from `"*"` to `"arn:aws:s3:::my-training-data-bucket/*"`. 
        3. **Re-Test:** Click "Analyze Policy" again. It should now pass your security check. 
        """)
    
    sample_policy = """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateTrainingJob",
                "s3:*"
            ],
            "Resource": "*"
        }
    ]
}"""
    policy_input = st.text_area("Paste SageMaker Execution Role Policy (JSON):", value=sample_policy, height=250)
    
    if st.button("Analyze Policy"):
        if "s3:*" in policy_input:
            st.error("🚨 CRITICAL FINDING: Wildcard S3 permissions detected (`s3:*`). This violates the principle of least privilege. Scope this down to specific buckets containing your training data.")
        elif "Resource\": \"*\"" in policy_input:
            st.warning("⚠️ WARNING: Wildcard resource detected. Restrict actions to specific ARNs where possible.")
        else:
            st.success("✅ Policy looks securely scoped for production ML workloads.")
