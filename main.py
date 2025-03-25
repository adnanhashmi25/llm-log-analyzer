import json
import csv
import re
from transformers import pipeline
from datetime import datetime 
import os

# Load Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def load_txt_logs(file_path):
    """Reads plain text log files and extracts log entries."""
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            logs.append(line.strip())
    return logs


def load_json_logs(file_path):
    """Reads JSON log files."""
    with open(file_path, 'r') as file:
        return json.load(file)


def load_csv_logs(file_path):
    """Reads CSV log files."""
    logs = []
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            logs.append(row)
    return logs


def preprocess_logs(logs):
    """Extracts timestamps, error levels, and messages from logs."""
    processed_logs = []
    log_pattern = re.compile(r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+([\w\(\)_-]+)\[(\d+)\]:\s+(.*)')
    
    for log in logs:
        match = log_pattern.match(log)
        if match:
            timestamp, hostname, process, pid, message = match.groups()
            processed_logs.append({
                'timestamp': timestamp,
                'hostname': hostname,
                'process': process,
                'pid': pid,
                'message': message
            })
    return processed_logs


def summarize_logs_with_llm(logs):
    """Sends logs in smaller batches to Hugging Face summarization model and writes output to CSV."""
    log_texts = [f"{log['timestamp']} - {log['process']} - {log['message']}" for log in logs]
    summaries = []
    batch_size = 5  # Adjust based on performance
    current_time = datetime.now()
    print(f'time: {current_time.strftime("%H:%M")}')
    for i in range(0, len(log_texts), batch_size):
        batch = "\n".join(log_texts[i:i+batch_size])
        try:
            summary = summarizer(batch, max_length=150, min_length=50, do_sample=False)
            if summary and isinstance(summary, list) and "summary_text" in summary[0]:  
                summaries.append(summary[0]["summary_text"])
            else:
                summaries.append("No summary generated")
        except Exception as e:
            print(f"Error summarizing batch {i}: {e}")
            summaries.append("Error processing batch")
        current_time = datetime.now()
        print(f'time: {current_time.strftime("%H:%M")}')
    
    return summaries


def write_summary_to_csv(logs, summaries, output_file="log_summary.csv"):
    """Writes processed logs and their summaries to a CSV file."""
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Process", "Message", "Summary"])
        for log, summary in zip(logs, summaries):
            writer.writerow([log['timestamp'], log['process'], log['message'], summary])


if __name__ == "__main__":
    # Example usage
    current_dir = os.getcwd()
    input_folder = os.path.join(current_dir,'input')
    file_list = os.listdir(input_folder)
    for file in file_list:
        log_file = os.path.join(input_folder, file)
    # log_file = "input/Linux_2k.log"  # Replace with actual file
        logs = load_txt_logs(log_file)
        processed_logs = preprocess_logs(logs)
        summaries = summarize_logs_with_llm(processed_logs)
        write_summary_to_csv(processed_logs, summaries)
    print("Summarization complete. Results saved in 'log_summary.csv'.")
