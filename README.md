# Marketing

A multi-agent workflow that generates marketing material for different social media platforms e.g. LinkedIn, Facebook, Instagram etc.

---

## Running Locally

1. Create an environment variable and install the required packages from `requirements.txt`.
2. Create a `.env` file with your **GEMINI_API_KEY**.

---

## Deploying on AWS (EC2)

### **Step 1: Launch EC2 Instance**
- Create an EC2 instance on AWS with:
  - **OS**: Amazon Linux
  - **Network Settings**: Enable **HTTP** and **Custom TCP (port 8501)** for Streamlit.
  - **Key Pair**: Generate and download the `.pem` file.

---

### **Step 2: Build Docker Image Locally**

If you're on Mac (default architecture ARM64), avoid conflicts by using buildx:

(bash)
docker buildx build --platform linux/amd64 -t ad-generator:latest --load .

### **Step 3: Save Docker Image**

Save the Docker image as `marketing.tar` file in your working directory with the `latest` tag:

(bash)
docker save -o marketing.tar ad-generator:latest

### **Step 4: Set Permissions on PEM File**

By default, the `.pem` file has overly permissive access rights. Restrict the access using `chmod` to meet SSH security requirements:

(bash)
chmod 400 marketing.pem

### **Step 5: Transfer Docker Image to EC2 Instance**

Use **SCP (Secure Copy Protocol)** to transfer the `.tar` Docker image file to your EC2 virtual machine.  
**Note:** Replace `13.233.79.194` with your own EC2 instance’s public IPv4 address:

(bash)
scp -i marketing.pem marketing.tar ec2-user@13.233.79.194:~/

### **Step 6: Connect to EC2 Instance via SSH**

Establish a Secure Shell (SSH) connection with your EC2 virtual machine.  
Replace `13.233.79.194` with your EC2 instance’s public IPv4 address:

(bash)
ssh -i marketing.pem ec2-user@13.233.79.194

### **Step 7: Load Docker Image on EC2 Instance**

Once connected to your EC2 instance, load the Docker image from the `.tar` file:

(bash)
docker load -i marketing.tar

### **Step 8: Create `.env` File on EC2 Instance**

Since the `.env` file is not included in the Docker image, you need to create it manually on the EC2 instance and add your Gemini API key:

(bash)
nano .env

### **Step 9: Run Docker Container Using `.env` File**

Start the Docker container on your EC2 instance using the `.env` file for environment variables:

(bash)
docker run -d --name marketing-app -p 8501:8501 \
--env-file .env ad-generator:latest

### **Step 10: Alternative — Pass API Key Directly When Running Container**

Alternatively, you can skip creating the `.env` file and pass the API key directly in the Docker run command.  
Replace `"your_actual_api_key_here"` with your Gemini API key:

(bash)
docker run -d --name marketing-app -p 8501:8501 \
-e GEMINI_API_KEY="your_actual_api_key_here" \
ad-generator:latest



