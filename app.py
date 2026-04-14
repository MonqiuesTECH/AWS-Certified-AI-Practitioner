import streamlit as st
import boto3
import json
from botocore.exceptions import ClientError

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AIF-C01 Study Hub",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR & ENVIRONMENT SETUP ---
with st.sidebar:
    st.title("AWS AIF-C01 Hub")
    st.markdown("Accelerated 8-Week Exam Prep")
    
    st.subheader("Environment")
    env_mode = st.radio("AWS Target", ["LocalStack (Local)", "AWS Cloud (Live)"])
    
    if env_mode == "LocalStack (Local)":
        endpoint_url = "http://localhost:4566"
        st.info("Operating in LocalStack mode. Ensure Docker is running.")
    else:
        endpoint_url = None
        st.warning("Operating in Live AWS mode. Watch your billing!")

    st.divider()
    page = st.radio("Exam Domains", [
        "1. ML & GenAI Fundamentals", 
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

# --- PAGE 1: QUIZ ENGINE (DOMAIN 1) ---
if page == "1. ML & GenAI Fundamentals":
    st.header("🧠 Foundation Models & AWS Services")
    st.write("Test your knowledge on when to use which AWS AI service.")
    
    st.markdown("### Question 1")
    q1 = st.radio(
        "Which service is best suited for extracting text, handwriting, and data from scanned documents?",
        ["Amazon Comprehend", "Amazon Textract", "Amazon Lex", "Amazon Kendra"],
        index=None
    )
    
    # Detailed explanations for Q1
    if q1 == "Amazon Textract":
        st.success("**Correct!** Amazon Textract uses OCR and machine learning to extract text, handwriting, and structured data (like tables and forms) from scanned documents.")
    elif q1 == "Amazon Comprehend":
        st.error("**Incorrect.** Comprehend is an NLP service used to find insights and relationships in text (like sentiment analysis or entity extraction), but it cannot extract text from an image/scan.")
    elif q1 == "Amazon Lex":
        st.error("**Incorrect.** Lex is used for building conversational interfaces (chatbots) using voice and text. It does not parse document files.")
    elif q1 == "Amazon Kendra":
        st.error("**Incorrect.** Kendra is an intelligent enterprise search service. While it can search through documents, Textract is the specific service used for the raw extraction of the text itself.")

    st.divider()
    
    st.markdown("### Question 2")
    q2 = st.radio(
        "What is the primary use case for Amazon Macie in an ML pipeline?",
        ["Training foundation models", "Orchestrating container deployments", "Discovering and protecting PII in S3", "Translating text"],
        index=None
    )
    
    # Detailed explanations for Q2
    if q2 == "Discovering and protecting PII in S3":
        st.success("**Correct!** Amazon Macie uses ML and pattern matching to discover and protect sensitive data (like Personally Identifiable Information) stored in Amazon S3 buckets before it accidentally gets used in a training job.")
    elif q2 == "Training foundation models":
        st.error("**Incorrect.** Amazon SageMaker or Bedrock (Custom Models) are used for training and fine-tuning models. Macie is strictly a data security and privacy service.")
    elif q2 == "Orchestrating container deployments":
        st.error("**Incorrect.** Amazon ECS or EKS are used for container orchestration. Macie does not manage infrastructure.")
    elif q2 == "Translating text":
        st.error("**Incorrect.** Amazon Translate handles text translation. Macie is designed to scan data lakes for security risks.")

# --- PAGE 2: BEDROCK PLAYGROUND (DOMAINS 2 & 3) ---
elif page == "2. Bedrock API Playground":
    st.header("⚡ Amazon Bedrock API Tester")
    st.write("Test model invocations and token generation. (Note: LocalStack GenAI support is limited; use Live AWS for full model access).")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        model_id = st.selectbox("Select Foundation Model", [
            "anthropic.claude-v2",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "meta.llama3-8b-instruct-v1:0",
            "amazon.titan-text-express-v1"
        ])
        max_tokens = st.slider("Max Tokens", 50, 1000, 200)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        
    with col2:
        prompt_text = st.text_area("Enter your prompt:", "Explain the difference between RAG and Fine-Tuning in 3 sentences.")
        
        if st.button("Invoke Model", type="primary"):
            client = get_bedrock_client()
            
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
                    response = client.invoke_model(
                        modelId=model_id,
                        contentType="application/json",
                        accept="application/json",
                        body=body
                    )
                    response_body = json.loads(response.get('body').read())
                    st.write(response_body.get('completion', response_body))
            except Exception as e:
                st.error("API Call Failed. Ensure your AWS credentials are set or LocalStack is running.")
                with st.expander("View Error Details"):
                    st.code(str(e))

# --- PAGE 3: SECURITY SIMULATOR (DOMAINS 4 & 5) ---
elif page == "3. Security & Governance":
    st.header("🛡️ Responsible AI & IAM Simulator")
    st.write("Analyze IAM policies for Least Privilege violations.")
    
    st.subheader("IAM Policy Analyzer")
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
            st.success("✅ Policy looks reasonably scoped.")

    st.divider()
    st.subheader("Bedrock Guardrails Checklist")
    st.checkbox("Denied Topics configured (e.g., Hate speech, self-harm)")
    st.checkbox("PII Redaction enabled (e.g., SSN, Credit Cards)")
    st.checkbox("Word Filters applied (Profanity blocking)")
