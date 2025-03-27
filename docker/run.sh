eval "$(conda shell.bash hook)"

conda activate zapgit
cd /backend/
uvicorn api:app --host 0.0.0.0 --port 443
conda deactivate
