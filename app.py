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

# --- SESSION STATE INITIALIZATION ---
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
        "1. ML & GenAI Fundamentals", 
        "2. Bedrock API Playground", 
        "3. Security & Governance"
    ])

# --- HELPER FUNCTIONS ---
def get_bedrock_client():
    if env_mode == "LocalStack (Local)":
        return boto3.client('bedrock-runtime', region_name='us-east-1', 
                            endpoint_url=endpoint_url, aws_access_key_id="test", aws_secret_access_key="test")
    else:
        return boto3.client('bedrock-runtime', region_name='us-east-1')

# --- QUIZ DATA ---
quiz_data = [
    {
        "question": "Which service is best suited for extracting text, handwriting, and data from scanned documents?",
        "options": ["Amazon Comprehend", "Amazon Textract", "Amazon Lex", "Amazon Kendra"],
        "answer": "Amazon Textract",
        "explanations": {
            "Amazon Textract": """✅ **Correct! The answer is Amazon Textract.**
            
🤖 **System AI Analysis:**
Great job choosing the correct answer! Let me break this down so you fully understand the mechanics behind it.

Imagine you have a stack of paper tax forms and you need to type all that data into a spreadsheet. You could hire a data entry clerk to look at the papers, find the boxes, and type the numbers. Amazon Textract is that highly trained clerk, but digitized. It doesn't just take a "picture" of the document; it actually understands the structure.

Here is how it works in a real-world pipeline:
1. You upload a scanned PDF or image to an Amazon S3 bucket.
2. Your system triggers Amazon Textract to analyze the document.
3. Textract uses Optical Character Recognition (OCR) and Machine Learning to read the text.
4. It identifies relationships—for example, it knows that "First Name" is linked to "John" right next to it, and it keeps table rows and columns intact.
5. It outputs structured JSON data that you can instantly save to a database like DynamoDB.

By using Textract, you eliminate manual data entry and capture structured data instantly. Perfect choice!""",

            "Amazon Comprehend": """❌ **Incorrect. The answer is not Amazon Comprehend.**

🤖 **System AI Analysis:**
Let's clarify what Comprehend does so you don't miss this on the exam. 

Comprehend is a Natural Language Processing (NLP) service. It is like a mood-reader or a summarizer. It cannot look at pictures, scans, or PDFs to extract words. It requires you to hand it plain text, and then it figures out what that text *means* (e.g., Is this text positive or negative? Does it mention a city or a person's name?). 

If you want to extract text from a scanned document, you must use **Amazon Textract** first, and then you could pass that extracted text to Comprehend for analysis.""",

            "Amazon Lex": """❌ **Incorrect. The answer is not Amazon Lex.**

🤖 **System AI Analysis:**
Let's look at why Lex isn't the right fit here.

Lex is the artificial intelligence brain behind conversational interfaces. Think of it as the engine you use to build chatbots or automated customer service phone menus. It listens to voice audio or reads chat text to figure out a user's intent. It has absolutely no ability to read scanned documents, handwriting, or forms. For document extraction, **Amazon Textract** is the required service.""",

            "Amazon Kendra": """❌ **Incorrect. The answer is not Amazon Kendra.**

🤖 **System AI Analysis:**
This is a very common distractor on the exam! Let's clear it up.

Amazon Kendra is a highly intelligent, enterprise search engine. It is like a private Google for your company's internal files. While Kendra *can* search through documents to find answers to questions, it is not the service you use to extract raw text, tables, or handwriting into structured data for an ML pipeline. To do the actual raw extraction from an image or PDF, you need **Amazon Textract**."""
        }
    },
    {
        "question": "What is the primary use case for Amazon Macie in an ML pipeline?",
        "options": ["Training foundation models", "Orchestrating container deployments", "Discovering and protecting PII in S3", "Translating text"],
        "answer": "Discovering and protecting PII in S3",
        "explanations": {
            "Discovering and protecting PII in S3": """✅ **Correct! The answer is Discovering and protecting PII in S3.**

🤖 **System AI Analysis:**
Spot on! Macie is a crucial governance and security tool. Let's look at why it is tested so heavily on the exam.

Imagine you are running a massive digital library where millions of files are dropped off daily. You need to make sure no one accidentally left their diary or credit card in those files before you let an AI model read them. Amazon Macie is your automated security guard that constantly opens the books, scans for secrets, and alerts you if it finds anything sensitive.

Here is how it works in an ML workflow:
1. Your company dumps raw customer data (emails, logs, support tickets) into an Amazon S3 data lake.
2. Before SageMaker can use this data to train a foundation model, Amazon Macie is enabled on the bucket.
3. Macie uses machine learning and pattern matching to scan the files.
4. It specifically looks for Personally Identifiable Information (PII) like Social Security numbers, credit cards, or medical data.
5. If it finds PII, it triggers an alert so you can redact or delete the data *before* the AI trains on it and potentially leaks it.

Using Macie ensures you maintain compliance and Responsible AI practices!""",

            "Training foundation models": """❌ **Incorrect. The answer is not Training foundation models.**

🤖 **System AI Analysis:**
Let's separate the security tools from the building tools. 

Building and training the actual AI foundation models is done in the "factories" of AWS, which are **Amazon SageMaker** or **Amazon Bedrock**. Amazon Macie does not train or host models. It is strictly a data security and privacy service used to protect the data *before* it gets sent to those factories.""",

            "Orchestrating container deployments": """❌ **Incorrect. The answer is not Orchestrating container deployments.**

🤖 **System AI Analysis:**
Let's clarify this piece of the architecture.

Container orchestration is like the shipping department of a company—it makes sure software packages are delivered, scaled, and running smoothly on different servers. In AWS, this is handled by services like **Amazon ECS** or **Amazon EKS**. Amazon Macie does not manage infrastructure or containers; it is a security service that scans S3 buckets for sensitive data.""",

            "Translating text": """❌ **Incorrect. The answer is not Translating text.**

🤖 **System AI Analysis:**
This is an easy one to separate! 

Translating text from one language to another (like English to Spanish) is handled by the dedicated ML service called **Amazon Translate**. Amazon Macie has nothing to do with translation; it simply reads data in its native language to look for security risks and PII."""
        }
    }
]

# --- PAGE 1: QUIZ ENGINE (DOMAIN 1) ---
if page == "1. ML & GenAI Fundamentals":
    st.header("🧠 Foundation Models & AWS Services")
    
    if st.session_state.current_q < len(quiz_data):
        q = quiz_data[st.session_state.current_q]
        st.markdown(f"### Question {st.session_state.current_q + 1} of {len(quiz_data)}")
        st.write(q["question"])
        
        # User makes a selection
        choice = st.radio("Select an answer:", q["options"], index=None, key=f"q_{st.session_state.current_q}")
        
        if choice:
            st.session_state.selected_answer = choice
            
            # Show customized feedback
            st.markdown(q["explanations"][choice])
            
            # Show Next Button
            st.button("Next Question ➡️", on_click=next_question, type="primary")
            
    else:
        st.success("🎉 You've completed this domain's practice questions!")
        st.button("Restart Quiz", on_click=reset_quiz)

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
