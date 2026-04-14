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
    
    if q1 == "Amazon Textract":
        st.success("""**Correct!** **The Simple Explanation:** Think of Textract as a super-smart, automated data entry worker. If you hand it a picture of a form, it doesn't just see a picture; it actually reads the words, recognizes where the checkboxes are, and understands how a table is laid out.
        **Real-World Example:** A hospital receives thousands of paper patient intake forms. Instead of paying someone to type all that information into a database by hand, they scan the paper forms, run the images through Amazon Textract, and it automatically pulls the names, dates, and medical history into their computer system in seconds.""")
    elif q1 == "Amazon Comprehend":
        st.error("""**Incorrect.** **The Simple Explanation:** Comprehend is like a mood-reader or a summarizer. It doesn't look at pictures or scans; it reads raw text and tries to figure out what the text *means* (Is it positive? Negative? What are the key phrases?).
        **Real-World Example:** You would use Comprehend to read thousands of Twitter comments to figure out if people are generally happy or angry about a new product you just launched.""")
    elif q1 == "Amazon Lex":
        st.error("""**Incorrect.** **The Simple Explanation:** Lex is the brain you use to build chatbots or automated phone menus. It listens to voice or reads chat text to figure out what a person wants to do.
        **Real-World Example:** When you call an airline and a robot says, "Tell me what you need," and you say, "I want to book a flight," Amazon Lex is the service figuring out your intent.""")
    elif q1 == "Amazon Kendra":
        st.error("""**Incorrect.** **The Simple Explanation:** Kendra is like a private Google search engine for a company's internal files. It searches for answers, but it doesn't extract data from scanned images.
        **Real-World Example:** An employee types, "What is the holiday policy?" into their company portal, and Kendra searches through thousands of internal HR PDFs to find the exact paragraph with the answer.""")

    st.divider()
    
    st.markdown("### Question 2")
    q2 = st.radio(
        "What is the primary use case for Amazon Macie in an ML pipeline?",
        ["Training foundation models", "Orchestrating container deployments", "Discovering and protecting PII in S3", "Translating text"],
        index=None
    )
    
    if q2 == "Discovering and protecting PII in S3":
        st.success("""**Correct!** **The Simple Explanation:** Macie is like an automated security guard that constantly digs through your digital filing cabinets (Amazon S3 buckets) looking for sensitive secrets you accidentally left lying around, like credit card numbers or Social Security numbers.
        **Real-World Example:** Before you feed 10 years of customer support emails into a machine learning model to train it, Macie scans the emails to ensure no customers accidentally included their bank account numbers, preventing your AI from accidentally learning and repeating that secret data.""")
    elif q2 == "Training foundation models":
        st.error("""**Incorrect.** **The Simple Explanation:** Building and training the actual AI models is done in the "factories" of AWS, which are Amazon SageMaker or Amazon Bedrock. Macie is strictly the security guard protecting the data, not the builder.
        **Real-World Example:** You use SageMaker to build an AI that predicts house prices. You use Macie to make sure the data you feed it doesn't have people's private financial records.""")
    elif q2 == "Orchestrating container deployments":
        st.error("""**Incorrect.** **The Simple Explanation:** Container orchestration (like Amazon ECS or EKS) is like the shipping department. It makes sure the software packages are delivered and running smoothly on different servers. Macie does not manage how software runs; it just reads data.
        **Real-World Example:** Running a massive website that needs to scale up instantly when a million people log on during a Super Bowl ad.""")
    elif q2 == "Translating text":
        st.error("""**Incorrect.** **The Simple Explanation:** Changing text from one language to another is handled by Amazon Translate. Macie only looks for security risks in the language it already is in.
        **Real-World Example:** Automatically changing an English instruction manual into Spanish for a global launch.""")

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
