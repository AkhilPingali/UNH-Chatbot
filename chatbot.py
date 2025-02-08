import argparse
import openai
import os

def upload_file(api_key, file_path, purpose="fine-tune"):
    openai.api_key = api_key
    try:
        with open(file_path, "rb") as file:
            response = openai.File.create(
                file=file,
                purpose=purpose
            )
        print("File uploaded successfully:", response)
        #print(response.id)
    except Exception as e:
        print("Error during file upload:", e)
    return response.id

def check_file_status(api_key, file_id):
    openai.api_key = api_key
    try:
        response = openai.File.retrieve(file_id)
        print("File status:", response)
    except Exception as e:
        print("Error checking file status:", e)

def check_job_status(api_key, job_id=None):
    openai.api_key = api_key
    if not job_id:
        # Read job_id from file if not provided as an argument
        try:
            with open("job_id.txt", "r") as f:
                job_id = f.read().strip()
        except FileNotFoundError:
            print("No job_id provided and job_id.txt file not found.")
            return

    try:
        response = openai.FineTuningJob.retrieve(job_id)
        print("Job status:", response)
    except Exception as e:
        print("Error checking job status:", e)

def fine_tune_model(api_key, training_file_id):
    openai.api_key = api_key
    try:
        response = openai.FineTuningJob.create(
            training_file=training_file_id,
            model="gpt-3.5-turbo"
        )
        job_id = response["id"]         
        print("Fine-tuning started with job_id:", job_id)
        
        # Save job_id to file for later use
        with open(training_file_id, "w") as f:
            f.write(job_id)
            
        print("Job ID saved to job_id.txt")
        return job_id
    except Exception as e:
        print("Error during fine-tuning:", e)
        return None

def save_model_id(api_key, job_id):
    openai.api_key = api_key
    try:
        response = openai.FineTuningJob.retrieve(job_id)
        status = response.get("status")
        
        if status == "succeeded":
            model_id = response["fine_tuned_model"]
            print(f"Fine-tuned model ID: {model_id}")
            
            # Save model ID to a file
            with open("model_id.txt", "w") as f:
                f.write(model_id)
            print("Model ID saved to model_id.txt")
        else:
            print(f"Job status is '{status}', model ID not available yet.")
    except Exception as e:
        print("Error retrieving job details:", e)


def use_fine_tuned_model(api_key, model_id, prompt):
    openai.api_key = api_key
    try:
        # Use ChatCompletion for chat-based models like gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        print("Model response:", response['choices'][0]['message']['content'])
    except Exception as e:
        print("Error using fine-tuned model:", e)

def main():
    parser = argparse.ArgumentParser(description="Unified command-line tool for various OpenAI tasks.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_upload = subparsers.add_parser("upload", help="Upload a file for fine-tuning")
    parser_upload.add_argument("-k", "--api_key", required=True, help="Your OpenAI API key")
    parser_upload.add_argument("-f", "--file", required=True, help="The path to the file to upload")
    parser_upload.add_argument("-p", "--purpose", default="fine-tune", help="Purpose of the file (default: fine-tune)")

    parser_check_file = subparsers.add_parser("check_file_status", help="Check the status of an uploaded file")
    parser_check_file.add_argument("-k", "--api_key", required=True, help="Your OpenAI API key")
    parser_check_file.add_argument("-id", "--file_id", required=True, help="The ID of the file to check")

    parser_check_job = subparsers.add_parser("check_job_status", help="Check the status of a fine-tuning job")
    parser_check_job.add_argument("-k", "--api_key", required=True, help="Your OpenAI API key")
    parser_check_job.add_argument("-id", "--job_id", help="The ID of the fine-tuning job to check (optional, reads from job_id.txt if not provided)")

    parser_fine_tune = subparsers.add_parser("fine_tune", help="Start fine-tuning a model")
    parser_fine_tune.add_argument("-k", "--api_key", required=True, help="Your OpenAI API key")
    parser_fine_tune.add_argument("-f", "--file_id", required=False, help="The ID of the training file for fine-tuning")

    parser_use_model = subparsers.add_parser("use_model", help="Use a fine-tuned model for text completion")
    parser_use_model.add_argument("-k", "--api_key", required=True, help="Your OpenAI API key")
    parser_use_model.add_argument("-m", "--model_id", required=True, help="The ID of the fine-tuned model to use")
    parser_use_model.add_argument("-p", "--prompt", required=True, help="The prompt to send to the model")

    parser_save_model = subparsers.add_parser("save_model_id", help="Save the fine-tuned model ID")
    parser_save_model.add_argument("-k", "--api_key", required=True, help="Your OpenAI API key")
    parser_save_model.add_argument("-id", "--job_id", required=True, help="The ID of the fine-tuning job to retrieve the model ID")

# In the main function



    args = parser.parse_args()

    if args.command == "upload":
        upload_fileid=upload_file(api_key=args.api_key, file_path=args.file, purpose=args.purpose)
        print(upload_fileid)
    elif args.command == "check_file_status":
        check_file_status(api_key=args.api_key, file_id=args.file_id)
    elif args.command == "check_job_status":
        Job_id=-check_job_status(api_key=args.api_key, job_id=args.job_id)
        print(Job_id)
    elif args.command == "fine_tune":
        finetune_id=fine_tune_model(api_key=args.api_key, training_file_id=args.file_id)
        print(finetune_id)
    elif args.command == "save_model_id":
        save_model_id(api_key=args.api_key, job_id=args.job_id)
        print(save_model_id)    
    elif args.command == "use_model":
       output= use_fine_tuned_model(api_key=args.api_key, model_id=args.model_id, prompt=args.prompt)
       print(output)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
