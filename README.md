![workflow](https://github.com/lukalafaye/horiana-rag/actions/workflows/python-app.yml/badge.svg)

# Horiana RAG

A Python project for Retrieval-Augmented Generation (RAG) for document processing and embedding.
Development in progress.

Project planning: [https://almanac.io/docs/planning-hBCvSPzpM3keThdXXrDv6SF7fsEs9N9p](https://almanac.io/docs/planning-hBCvSPzpM3keThdXXrDv6SF7fsEs9N9p)

## Llama 3 server setup

1. Request access to Llama 3 70b on hugging face → [https://huggingface.co/meta-llama/Meta-Llama-3-70B](https://huggingface.co/meta-llama/Meta-Llama-3-70B)
2. Create access token in hugging face settings
3. Request ec2 quotas for all no demand ec2 instances -> [https://aws.amazon.com/getting-started/hands-on/request-service-quota-increase/](https://aws.amazon.com/getting-started/hands-on/request-service-quota-increase/). Note: Contacted sales service by email because they would not allow 95 vCPUs on my personal account. On demand != spot instances...
4. Create g5.??xlarge on demand ec2 instance -> Used AMI: Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.3.0 (Ubuntu 20.04) 20240716, 128gb ebs default + efs additional storage (see mounting efs tutorial)
?? is 2 for llama8b q4, 24 for llama70b q4
5. Connect to server (click connect) and use ssh key
6. Properly attach additional storage in file system -> [https://docs.aws.amazon.com/ebs/latest/userguide/ebs-using-volumes.html](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-using-volumes.html). Note: Make sure to change fstab to automatically attach storage on every reboot.
7. Run `sudo chown -R $USER:$USER /data` to fix permission issues
8. Update and upgrade system `sudo apt update && sudo apt upgrade`
9. `sudo apt install python3-apt` 
10. Create python environment: `cd /data/ && python -m venv venv && source venv/bin/activate` 
11. Install needed pip packages: `pip install vllm ray huggingface_hub[cli]`
12. Login to huggingface using access token: `huggingface-cli login`

### Run Llama3 with vLLM (cost++ g5.24xlarge)

```
python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3-70B-Instruct --tensor-parallel-size 8 --download-dir /data/ --api_key SecretToken # 8 gpus
```

### Run quantized Llama 3 with llama cpp (cost-- g5.12xlarge)

Download Q4 from [https://huggingface.co/lmstudio-community/Meta-Llama-3-70B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3-70B-Instruct-GGUF) to local folder.

Here is a download python script:

```
from huggingface_hub import hf_hub_download

# Specify the repository and the file you want to download
repo_id = 'lmstudio-community/Meta-Llama-3-70B-Instruct-GGUF'
filename = 'Meta-Llama-3-70B-Instruct-Q4_K_M.gguf'

# Download the file
file_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir='.')
print(f"Downloaded file saved to {file_path}")
```

Install and build `llama cpp`.

```
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make llama-server LLAMA_CUDA=1
```

Run 70b model server with `./llama-server -m /path/to/70b.gguf --gpu-layers 196 --split-mode layer --tensor-split 1,1,1,1 --port 8001 --api-key secret`.
Run 8b with: `./llama-server -m /path/to/8b.gguf --port 8001 --api-key secret`

### Notes

Note: --api-key is used in .llama3_env
You should create this file with:

```
BASE_URL="http://ec2-XX-XXX-XXX-XX.us-east-2.compute.amazonaws.com:8080/v1/"
API_KEY="secret"
PORT=8001
```

Note: Upload files with `scp -r -i /home/linus/.ssh/aws/luka.pem FilesFolder/ ubuntu@ec2-XX-XXX-XXX-XX.us-east-2.compute.amazonaws.com:/data/`.

Note: Get a permanent IP at [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html).

## Chomadb server setup

Run chroma server with docker

Instructions from [https://cookbook.chromadb.dev/security/auth/#token-authentication](https://cookbook.chromadb.dev/security/auth/#token-authentication).

```
docker run -d --rm \
-e CHROMA_SERVER_AUTHN_CREDENTIALS="chr0ma-t0k3n" \
-e CHROMA_SERVER_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider" \
-e CHROMA_AUTH_TOKEN_TRANSPORT_HEADER="Authorization" \
-p 8000:8000 \
-v ./chroma:/chroma/chroma \
chromadb/chroma:latest
```

Note: `chr0ma-t0k3n` is used in .chroma_env!

## Run project container

```
# docker build -t horiana-rag . # OPTIONAL - used to rebuild the image
docker run -it --network="host" --rm -v $(pwd):/app horiana-rag bash # --network option only works on Linux, this is for dev mode
```

Main scripts:

- `preprocess.py` -> extracts document dictionnary and tables from both pdf and docx files, stores output to pickle files
- `fetch_abstracts.py` -> fetches some abstracts using keywords and saves the dataframe in a local csv file
- `embed.py` -> retrieves tables pickle file and adds all tables to chromadb 
- 

## Todo 

Rag workflow