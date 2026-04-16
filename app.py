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

# --- QUIZ DATA (Embedded directly to prevent ModuleNotFoundError) ---
quiz_data = [
    {
        "question": "Which service is best suited for extracting text, handwriting, and data from scanned documents?",
        "options": ["Amazon Comprehend", "Amazon Textract", "Amazon Lex", "Amazon Kendra"],
        "answer": "Amazon Textract",
        "explanations": {
            "Amazon Textract": "✅ **Correct! The answer is Amazon Textract.**\n\n🤖 **System AI Analysis:**\nGreat job choosing the correct answer! Let me break this down so you fully understand the mechanics behind it.\n\nImagine you have a stack of paper tax forms and you need to type all that data into a spreadsheet. Amazon Textract is that highly trained clerk, but digitized. It doesn't just take a 'picture' of the document; it actually understands the structure, keeping table rows and columns intact.",
            "Amazon Comprehend": "❌ **Incorrect. The answer is not Amazon Comprehend.**\n\n🤖 **System AI Analysis:**\nComprehend is a Natural Language Processing (NLP) service. It is like a mood-reader or a summarizer. It cannot look at pictures, scans, or PDFs to extract words.",
            "Amazon Lex": "❌ **Incorrect. The answer is not Amazon Lex.**\n\n🤖 **System AI Analysis:**\nLex is the artificial intelligence brain behind conversational interfaces (chatbots). It has absolutely no ability to read scanned documents.",
            "Amazon Kendra": "❌ **Incorrect. The answer is not Amazon Kendra.**\n\n🤖 **System AI Analysis:**\nAmazon Kendra is a highly intelligent, enterprise search engine, like a private Google for your company's internal files. It searches for answers, but does not extract raw text from images."
        }
    },
    {
        "question": "What is the primary use case for Amazon Macie in an ML pipeline?",
        "options": ["Training foundation models", "Orchestrating container deployments", "Discovering and protecting PII in S3", "Translating text"],
        "answer": "Discovering and protecting PII in S3",
        "explanations": {
            "Discovering and protecting PII in S3": "✅ **Correct! The answer is Discovering and protecting PII in S3.**\n\n🤖 **System AI Analysis:**\nMacie is an automated security guard that constantly opens the books, scans for secrets, and alerts you if it finds anything sensitive (like SSNs or credit cards) in your S3 buckets before your AI accidentally trains on it.",
            "Training foundation models": "❌ **Incorrect. The answer is not Training foundation models.**\n\n🤖 **System AI Analysis:**\nBuilding and training the actual AI foundation models is done in Amazon SageMaker or Amazon Bedrock. Macie is strictly a data security service.",
            "Orchestrating container deployments": "❌ **Incorrect. The answer is not Orchestrating container deployments.**\n\n🤖 **System AI Analysis:**\nContainer orchestration is handled by services like Amazon ECS or Amazon EKS. Macie does not manage infrastructure.",
            "Translating text": "❌ **Incorrect. The answer is not Translating text.**\n\n🤖 **System AI Analysis:**\nTranslating text from one language to another is handled by Amazon Translate."
        }
    },
    {
        "question": "A retail company wants to group its customers into distinct purchasing segments based on their historical buying behavior, but they do not have predefined labels for these segments. Which machine learning approach is MOST appropriate?",
        "options": ["Supervised learning", "Unsupervised learning", "Reinforcement learning", "Generative AI"],
        "answer": "Unsupervised learning",
        "explanations": {
            "Unsupervised learning": "✅ **Correct! The answer is Unsupervised learning.**\n\n🤖 **System AI Analysis:**\nImagine you are given a giant bucket of mixed Legos and told to 'organize them.' You don't have a manual telling you what categories exist; you just start grouping them naturally. In machine learning, when you have raw data without predefined labels, you use Unsupervised Learning.",
            "Supervised learning": "❌ **Incorrect. The answer is not Supervised learning.**\n\n🤖 **System AI Analysis:**\nSupervised learning requires 'labeled' data. It is like having flashcards where the question is on the front and the exact answer is on the back.",
            "Reinforcement learning": "❌ **Incorrect. The answer is not Reinforcement learning.**\n\n🤖 **System AI Analysis:**\nReinforcement learning is like training a dog with treats. You put an AI 'agent' in an environment, and it learns by trial and error.",
            "Generative AI": "❌ **Incorrect. The answer is not Generative AI.**\n\n🤖 **System AI Analysis:**\nGenerative AI creates new content based on patterns it learned from training data. It does not sort or segment existing databases."
        }
    },
    {
        "question": "Which of the following describes the process of passing a small set of example input-output pairs to a foundation model within the prompt to improve its accuracy on a specific task?",
        "options": ["Fine-tuning", "Retrieval-Augmented Generation (RAG)", "Few-shot prompting", "Pre-training"],
        "answer": "Few-shot prompting",
        "explanations": {
            "Few-shot prompting": "✅ **Correct! The answer is Few-shot prompting.**\n\n🤖 **System AI Analysis:**\nImagine you are hiring a new assistant to write thank-you notes. Instead of sending them to a 6-month writing class, you just hand them a clipboard with three examples and say, 'Write the next one like these.'",
            "Fine-tuning": "❌ **Incorrect. The answer is not Fine-tuning.**\n\n🤖 **System AI Analysis:**\nFine-tuning is a permanent alteration of the model using thousands of examples.",
            "Retrieval-Augmented Generation (RAG)": "❌ **Incorrect. The answer is not RAG.**\n\n🤖 **System AI Analysis:**\nRAG is like giving the AI an open-book test to find facts, not giving it formatting examples.",
            "Pre-training": "❌ **Incorrect. The answer is not Pre-training.**\n\n🤖 **System AI Analysis:**\nPre-training is the initial phase where a foundation model reads the entire internet."
        }
    },
    {
        "question": "An enterprise wants to build an AI chatbot using Amazon Bedrock. The chatbot must be able to search the company's internal HR documents stored in Amazon S3 to answer employee questions about the holiday policy. Which architectural pattern should be used?",
        "options": ["Model Fine-tuning", "Retrieval-Augmented Generation (RAG)", "Prompt Injection", "Transfer Learning"],
        "answer": "Retrieval-Augmented Generation (RAG)",
        "explanations": {
            "Retrieval-Augmented Generation (RAG)": "✅ **Correct! The answer is Retrieval-Augmented Generation (RAG).**\n\n🤖 **System AI Analysis:**\nRAG searches your S3 bucket for the HR manual, Retrieves the paragraph about holidays, Augments the employee's question with that paragraph, and Generates the correct answer. This is the most highly tested concept on the AIF-C01 exam!",
            "Model Fine-tuning": "❌ **Incorrect. The answer is not Model Fine-tuning.**\n\n🤖 **System AI Analysis:**\nFine-tuning bakes information permanently into the model. If the HR policy changes, the AI is stuck with old info unless you pay to retrain it.",
            "Prompt Injection": "❌ **Incorrect. The answer is not Prompt Injection.**\n\n🤖 **System AI Analysis:**\nPrompt Injection is a cybersecurity attack, not an architectural pattern.",
            "Transfer Learning": "❌ **Incorrect. The answer is not Transfer Learning.**\n\n🤖 **System AI Analysis:**\nTransfer learning is reusing a model trained for one task as the starting point for a second task."
        }
    },
    {
        "question": "A healthcare company builds an AI application using Amazon Bedrock to summarize patient notes. They must ensure the AI never generates responses containing medical advice or diagnoses. Which Amazon Bedrock feature natively provides this protection?",
        "options": ["Amazon Bedrock Agents", "Amazon Bedrock Guardrails", "Amazon Bedrock Knowledge Bases", "AWS IAM Policies"],
        "answer": "Amazon Bedrock Guardrails",
        "explanations": {
            "Amazon Bedrock Guardrails": "✅ **Correct! The answer is Amazon Bedrock Guardrails.**\n\n🤖 **System AI Analysis:**\nGuardrails are the 'bouncers' of your AI application. They allow you to set strict boundaries (like a 'Denied Topic' for Medical Advice) and block the request before the model even answers.",
            "Amazon Bedrock Agents": "❌ **Incorrect. The answer is not Amazon Bedrock Agents.**\n\n🤖 **System AI Analysis:**\nAgents are the 'doers' that take actions, like calling APIs. They do not enforce safety boundaries.",
            "Amazon Bedrock Knowledge Bases": "❌ **Incorrect. The answer is not Amazon Bedrock Knowledge Bases.**\n\n🤖 **System AI Analysis:**\nKnowledge Bases connect your AI to your data sources for RAG. They do not stop a model from generating off-limits topics.",
            "AWS IAM Policies": "❌ **Incorrect. The answer is not AWS IAM Policies.**\n\n🤖 **System AI Analysis:**\nIAM policies control who can access the API, but they cannot read human language to block medical advice."
        }
    },
    {
        "question": "An organization requires that all API calls made to Amazon Bedrock are recorded for compliance auditing, including who made the call and when. Which AWS service provides this capability?",
        "options": ["Amazon CloudWatch", "AWS CloudTrail", "AWS Config", "Amazon Macie"],
        "answer": "AWS CloudTrail",
        "explanations": {
            "AWS CloudTrail": "✅ **Correct! The answer is AWS CloudTrail.**\n\n🤖 **System AI Analysis:**\nThink of CloudTrail as the security camera footage for your AWS account. It records the Who, When, and What for every API call made.",
            "Amazon CloudWatch": "❌ **Incorrect. The answer is not Amazon CloudWatch.**\n\n🤖 **System AI Analysis:**\nCloudWatch tracks system performance metrics (like CPU spikes), not user API auditing.",
            "AWS Config": "❌ **Incorrect. The answer is not AWS Config.**\n\n🤖 **System AI Analysis:**\nConfig tracks the configuration state of your resources, not the historical log of API invocations.",
            "Amazon Macie": "❌ **Incorrect. The answer is not Amazon Macie.**\n\n🤖 **System AI Analysis:**\nMacie scans S3 buckets for sensitive data. It does not audit API calls."
        }
    },
    {
        "question": "A company wants to provide its software engineers with an AI-powered assistant that can generate code snippets, debug errors, and explain unfamiliar code directly within their Integrated Development Environment (IDE). Which AWS service is explicitly designed for this?",
        "options": ["Amazon Q Developer", "Amazon Q Business", "Amazon SageMaker Studio", "Amazon Bedrock"],
        "answer": "Amazon Q Developer",
        "explanations": {
            "Amazon Q Developer": "✅ **Correct! The answer is Amazon Q Developer.**\n\n🤖 **System AI Analysis:**\nThink of Amazon Q Developer as an expert senior programmer sitting right next to you. It integrates directly into your IDE (like VS Code). If a question mentions 'engineers', 'IDEs', or 'coding', the answer is Q Developer.",
            "Amazon Q Business": "❌ **Incorrect. The answer is not Amazon Q Business.**\n\n🤖 **System AI Analysis:**\nQ Business is the corporate desk-worker's assistant used to search enterprise wikis and documents.",
            "Amazon SageMaker Studio": "❌ **Incorrect. The answer is not Amazon SageMaker Studio.**\n\n🤖 **System AI Analysis:**\nSageMaker Studio is a workbench for data scientists to train models, not an AI coding assistant.",
            "Amazon Bedrock": "❌ **Incorrect. The answer is not Amazon Bedrock.**\n\n🤖 **System AI Analysis:**\nBedrock is the underlying API service. Q Developer is the pre-built application you actually put in the IDE."
        }
    },
    {
        "question": "An e-commerce platform wants to predict the exact dollar amount a customer is likely to spend over the next 12 months based on their past purchase history. Which type of machine learning task is this?",
        "options": ["Regression", "Classification", "Clustering", "Generative AI"],
        "answer": "Regression",
        "explanations": {
            "Regression": "✅ **Correct! The answer is Regression.**\n\n🤖 **System AI Analysis:**\nIf the answer you are looking for is a continuous number (like a dollar amount or temperature), you are using Regression.",
            "Classification": "❌ **Incorrect. The answer is not Classification.**\n\n🤖 **System AI Analysis:**\nClassification is used when the answer is a specific category or label (e.g., 'Spam' or 'Not Spam').",
            "Clustering": "❌ **Incorrect. The answer is not Clustering.**\n\n🤖 **System AI Analysis:**\nClustering groups similar data together without predefined labels. It doesn't forecast specific future numerical values.",
            "Generative AI": "❌ **Incorrect. The answer is not Generative AI.**\n\n🤖 **System AI Analysis:**\nGenerative AI creates new content; it is not used for numerical financial forecasting."
        }
    },
    {
        "question": "You are using an Amazon Titan image generation model in Amazon Bedrock to create marketing assets. You need to ensure that all images generated by the model can be identified as AI-generated to prevent misinformation. How is this achieved natively in AWS?",
        "options": ["Amazon Titan automatically applies an invisible watermark to generated images.", "You must write an AWS Lambda function to add a metadata tag.", "Amazon Macie scans the images and tags them as AI-generated.", "You must use Amazon Rekognition to classify the images before saving."],
        "answer": "Amazon Titan automatically applies an invisible watermark to generated images.",
        "explanations": {
            "Amazon Titan automatically applies an invisible watermark to generated images.": "✅ **Correct! The answer is Amazon Titan automatically applies an invisible watermark.**\n\n🤖 **System AI Analysis:**\nAWS built safety directly into the Amazon Titan models. Every image generated automatically contains an invisible, tamper-resistant watermark. No extra coding required.",
            "You must write an AWS Lambda function to add a metadata tag.": "❌ **Incorrect. The answer is not writing a Lambda function.**\n\n🤖 **System AI Analysis:**\nThe Titan model handles watermarking internally at the pixel level; custom code is not the native solution.",
            "Amazon Macie scans the images and tags them as AI-generated.": "❌ **Incorrect. The answer is not Amazon Macie.**\n\n🤖 **System AI Analysis:**\nMacie scans S3 buckets for sensitive text like passwords. It does not classify AI images.",
            "You must use Amazon Rekognition to classify the images before saving.": "❌ **Incorrect. The answer is not Amazon Rekognition.**\n\n🤖 **System AI Analysis:**\nRekognition identifies objects in an image (e.g., 'Is there a car?'). It is not used to apply AI watermarks."
        }
    },
    {
        "question": "A data scientist needs to train a machine learning model using Amazon SageMaker. The training data is stored in an Amazon S3 bucket that is encrypted with an AWS KMS key. What permissions must the SageMaker execution role have to successfully run the training job?",
        "options": ["s3:GetObject and kms:Decrypt", "s3:PutObject and kms:Encrypt", "s3:ListBucket only", "sagemaker:CreatePresignedDomainUrl"],
        "answer": "s3:GetObject and kms:Decrypt",
        "explanations": {
            "s3:GetObject and kms:Decrypt": "✅ **Correct! The answer is s3:GetObject and kms:Decrypt.**\n\n🤖 **System AI Analysis:**\nSageMaker needs to physically pull the data files out of S3 (`s3:GetObject`), and because the data is locked, it also needs the key to unlock and read the text inside (`kms:Decrypt`).",
            "s3:PutObject and kms:Encrypt": "❌ **Incorrect. The answer is not s3:PutObject and kms:Encrypt.**\n\n🤖 **System AI Analysis:**\nThese permissions are for writing and locking new data, not reading historical training data.",
            "s3:ListBucket only": "❌ **Incorrect. The answer is not s3:ListBucket only.**\n\n🤖 **System AI Analysis:**\nListing a bucket only lets you see file names, not actually read the contents.",
            "sagemaker:CreatePresignedDomainUrl": "❌ **Incorrect. The answer is not sagemaker:CreatePresignedDomainUrl.**\n\n🤖 **System AI Analysis:**\nThis permission lets a human log into the SageMaker interface. It doesn't help the background model read S3 data."
        }
    },
    {
        "question": "A company is migrating a customer support application to use Amazon Bedrock. They notice their billing costs are higher than expected. Which factor primarily determines the cost of invoking foundation models in Amazon Bedrock?",
        "options": ["The number of input and output tokens", "The amount of time the model takes to respond", "The amount of RAM provisioned for the model", "The geographical location of the end user"],
        "answer": "The number of input and output tokens",
        "explanations": {
            "The number of input and output tokens": "✅ **Correct! The answer is The number of input and output tokens.**\n\n🤖 **System AI Analysis:**\nIn the world of Generative AI, you pay by the word. Bedrock charges you a tiny fraction of a cent for every token you send (Input) and every token the model generates (Output).",
            "The amount of time the model takes to respond": "❌ **Incorrect. The answer is not The amount of time the model takes to respond.**\n\n🤖 **System AI Analysis:**\nUnlike Lambda or EC2, Bedrock On-Demand pricing is not billed by execution time or seconds.",
            "The amount of RAM provisioned for the model": "❌ **Incorrect. The answer is not The amount of RAM provisioned for the model.**\n\n🤖 **System AI Analysis:**\nBedrock is serverless. You don't manage or pay for the underlying RAM or CPUs.",
            "The geographical location of the end user": "❌ **Incorrect. The answer is not The geographical location of the end user.**\n\n🤖 **System AI Analysis:**\nThe end user's location has no direct impact on the Amazon Bedrock API token cost."
        }
    }
]

# --- SESSION STATE INITIALIZATION ---
# This allows the app to remember your place out of the total questions
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
    
    # This automatically adjusts whether you have 10 or 90 questions
    total_questions = len(quiz_data)
    
    if st.session_state.current_q < total_questions:
        q = quiz_data[st.session_state.current_q]
        st.markdown(f"### Question: {st.session_state.current_q + 1} / {total_questions}")
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
