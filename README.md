<h1 align="center">ZapGit🐈</h1>

<h2 align="center">Automate Your GitHub Flows with MCP!</h2>

<div align="center">
    <h3>If you find ZapGit userful, please consider to donate and support the project:</h3>
    <a href="https://github.com/sponsors/AstraBert"><img src="https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA" alt="GitHub Sponsors Badge"></a>
</div>
<br>
<div align="center">
    <img src="logo.png" alt="ZapGit Logo" width=300 height=300>
</div>
<br>

[**ZapGit**](https://zapgit.cloud) is aimed at creating an all-in-one place for you to manage and plan tasks like creating and commenting issues and pull requests on GitHub, using [Zapier](https://zapier.com) MCP servers and [LlamaIndex](https://www.llamaindex.ai).

## Install and launch🚀

The first step, common to both the Docker and the source code setup approaches, is to clone the repository and access it:

```bash
git clone https://github.com/AstraBert/zapgit.git
cd zapgit
```

Once there, you can choose one of the two following approaches:

### Docker (recommended)🐋

> _Required: [Docker](https://docs.docker.com/desktop/) and [docker compose](https://docs.docker.com/compose/)_

- Add the `groq_api_key` variable in the [`.env.example`](./.env.example) file and modify the name of the file to `.env`. Get these keys:
    + [On Groq Console](https://console.groq.com/keys)

```bash
mv .env.example .env
```

- Launch the Docker application:

```bash
# If you are on Linux/macOS
bash start_services.sh
# If you are on Windows
.\start_services.ps1
```

- Or do it manually:

```bash
docker compose up -f compose.local.yaml redis -d
docker compose up -f compose.local.yaml zapbackend -d
docker compose up -f compose.local.yaml zapfrontend -d
```

You will see the application running on http://localhost:8501 and you will be able to use it. Depending on your connection and on your hardware, the set up might take some time (up to 15 mins to set up) - but this is only for the first time your run it!

### Source code🗎

> _Required: [Docker](https://docs.docker.com/desktop/), [docker compose](https://docs.docker.com/compose/) and [conda](https://anaconda.org/anaconda/conda)_

- Add the `groq_api_key` variable in the [`.env.example`](./.env.example) file and modify the name of the file to `.env`. Get these keys:
    + [On Groq Console](https://console.groq.com/keys)

```bash
mv .env.example scripts/.env
```

- Set up the app using the dedicated script:

```bash
# For MacOs/Linux users
bash setup.sh
# For Windows users
.\setup.ps1
```

- Or you can do it manually, if you prefer:

```bash
docker compose up -f compose.local.yaml redis -d

conda env create -f environment.local.yml

conda activate zapgit

cd scripts/

uvicorn api:app --host 0.0.0.0 --port 8000

conda deactivate
```

- Now you can open another terminal and run:

```bash
conda activate zapgit
cd scripts/
streamlit run frontend.py
conda deactivate
```

You will see the application running on http://localhost:8501 and you will be able to use it.

## How it works

### Database services

- **Redis** is used for API rate limiting control

### Workflow

The workflow is very simple:

- When you submit a request, the request gets routed to a template prompt, which is completed based on the request details (thanks to [banks](https://github.com/masci/banks))
- The chosen prompt is passed on to an Agent, which connects to Zapier MCP servers and starts executing all the commands contained in your requests
- Once the agent is done, it returns to you a final response and its agentic process. You should now see the action (create comment/issue/PR) on GitHub, a message on Discord detailing the action and a reminder event planned on Calendar.

## Contributing

Contributions are always welcome! Follow the contributions guidelines reported [here](CONTRIBUTING.md).

## License and rights of usage

The software is provided under MIT [license](./LICENSE).
