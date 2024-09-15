import os
import zipfile
import concurrent.futures
import torch
import numpy as np
import platform

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Extract >> Using {device} for extraction")
print(f"Extract >> GPU: {'Will not be used' if device == 'cuda' else 'Will be used'}")
print(f"Extract >> System: {platform.system()} {platform.release()}")
print(f"Extract >> CUDA Available: {torch.cuda.is_available()}")
print(f"Extract >> CUDA Version: {torch.version.cuda}")
print(f"Extract >> Current Device: {torch.cuda.current_device()}")
print(f"Extract >> Device Name: {torch.cuda.get_device_name(0)}")

def extract_file_gpu(zip_file, member, output_dir):
    with open(zip_file, 'rb') as f:
        zip_content = f.read()

    with torch.no_grad():
        decompressed_data = torch.from_numpy(np.frombuffer(zip_content, dtype=np.uint8)).to(device)
        decompressed_data = torch.dequantize(decompressed_data)

    with open(os.path.join(output_dir, member), 'wb') as f:
        f.write(decompressed_data.cpu().numpy())

def update_display(progress_list):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Extract >> Extracting files... (Press Ctrl+C to quit)")
    print("Extract >> File Name")

    for file_name in progress_list:
        print(f"Extract >> {file_name:<30} Done!")

def extract_zip(file_path):
    if not os.path.isfile(file_path) or not file_path.endswith('.zip'):
        print("The specified file does not exist or is not a ZIP file.")
        return

    zip_dir = os.path.dirname(file_path)
    zip_name = os.path.splitext(os.path.basename(file_path))[0]
    default_output_dir = os.path.join(zip_dir, zip_name)

    output_dir = input(f"Enter output directory (leave blank for '{default_output_dir}'): ").strip()
    
    if not output_dir:
        output_dir = default_output_dir

    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        members = zip_ref.namelist()
        progress_list = members.copy()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(extract_file_gpu, zip_ref, member, output_dir): member for member in members}
            while futures:
                update_display(progress_list)
                for future in concurrent.futures.as_completed(futures):
                    futures.pop(future)

    print(f"Extraction completed to: {output_dir}")

if __name__ == "__main__":
    try:
        file_path = input("\nExtract >> Enter the path to the ZIP file: ").strip().strip('"')
        extract_zip(file_path)
    except KeyboardInterrupt:
        print("\nExtract >> Goodbye!")
