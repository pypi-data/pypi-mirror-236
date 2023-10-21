import json
import boto3
import pdfplumber
import textract

s3_client = boto3.client("s3")

def extract_text_from_docx(file_path):
    print("in doc")
    if file_path.lower().endswith(('.docx')):
        text = textract.process(file_path).decode('utf-8')
        new_text = (text.encode('ascii', 'ignore')).decode("utf-8").replace('\n', ' ').replace('\t', ' ')
        return new_text
    else:
        return "non supported file type"

def extract_text_from_pdf(file_path):
    print("in pdf")
    if file_path.lower().endswith(('.pdf')):
        extracted_text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                extracted_text += page_text
        return (extracted_text.encode('ascii', 'ignore')).decode("utf-8").replace('\n', ' ').replace('\t', ' ')
    else:
        return None

def lambda_handler(event):
    file_key = event['file_key']
    s3_bucket = event['s3_bucket']
    temp_docx_file_path = "/tmp/temp_file.docx"
    temp_pdf_file_path = "/tmp/temp_file.pdf"
    if file_key.lower().endswith(('.docx')):
        s3_client.download_file(s3_bucket, file_key, temp_docx_file_path)
        extracted_text = extract_text_from_docx(temp_docx_file_path)
    elif file_key.lower().endswith(('.pdf')):
        s3_client.download_file(s3_bucket, file_key, temp_pdf_file_path)
        extracted_text = extract_text_from_pdf(temp_pdf_file_path)
    else:
        extracted_text = "Non-supported file type"
    
    print("Extracted Text:", extracted_text)
    return {
        'statusCode': 200,
        'body': json.dumps({"text": extracted_text})
    }