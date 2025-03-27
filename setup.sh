docker compose up -f compose.local.yaml redis -d

conda env create -f environment.local.yml

conda activate zapgit

cd scripts/

uvicorn api:app --host 0.0.0.0 --port 8000

conda deactivate