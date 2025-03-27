import streamlit as st
import datetime
from prompts_specs import choose_prompt
import requests as rq
from pydantic import BaseModel

class McpInput(BaseModel):
    user_input: str

allowed_actions = ['Create Issue', 'Create Pull Request', 'Create Comment under Issue', 'Create Comment under Pull Request']
today = datetime.datetime.now()
one_year_from_today = datetime.date(today.year+1, today.month, today.day)

st.set_page_config(
    page_title="ZapGit",
    page_icon=":cat:",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/AstraBert/zapgit/discussions/categories/general',
        'Report a bug': "https://github.com/AstraBert/zapgit/issues/",
        'About': "Automate Your GitHub Flows with Zapier MCP!"
    }
)

st.title(":orange[ZapGit] - GitHub automation with MCP :cat:")
st.markdown("## Powered by [:orange[Zapier]](https://zapier.com) and [:orange[LlamaIndex]](https://www.llamaindex.ai)")
st.markdown("Create and comment issues and PRs, get summaries on Discord and plan fix/merge reminders on Google Calendar!")
st.markdown("### How to use ZapGit")
st.markdown("> _You need to have a Discord account and a server with a channel where you can connect ZapGit to, as well as a Google account to connect ZapGit to Calendar_")
st.markdown("1. You should, first of all, create an account on [Zapier](https://zapier.com) and get your MCP URL on [the dedicated page](https://actions.zapier.com/settings/mcp/)\n2. Once you are done, go to the ['Actions' page](https://actions.zapier.com/mcp/actions/) and create the actions: 'Discord: Send Channel Message', 'GitHub: Create Issue', 'Google Calendar: Quick Add Event', 'GitHub: Create Comment', 'GitHub: Create Pull Request'\n3. Report the MCP URL in the dedicated space down here, as well as the GitHub repo. Choose an action and then fill all the provided input fields.")

mcp_url = st.text_input("Zapier MCP URL (keep this secret!)", type="password")
github_repo = st.text_input("GitHub repository", value="https://github.com/")
action = st.selectbox(label="Select your action", options=allowed_actions)
if action == 'Create Issue':
    target = st.text_input(label = "Title for the Issue")
    request = st.text_input(label="Content of the Issue")
    server = st.text_input(label="Discord Server where to send the summary message")
    channel = st.text_input(label="Discord Server Channel ID where to send the summary message", placeholder="e.g. 104499429202")
    date = st.date_input(label="Choose a time and a date when to schedule a reminder for your action", value=today, min_value=today, max_value=one_year_from_today)
    submit_btn = st.button(label="Run Action!", type="primary")
    if submit_btn: 
        prompt = choose_prompt(action=action, arguments={"repository": github_repo, "server": server, "channel": channel, "target": target, "request": request, "date": str(date)})
        response = rq.post("http://zapbackend:443/mcp", json=McpInput(user_input=prompt).model_dump(), headers={"Content-Type": "application/json", "x-api-key": mcp_url})
        process = response.json()["process"]
        report = response.json()["response"]
        st.markdown(report)
        with st.expander(label="See agent process"):
            st.markdown(process)
elif action == 'Create Pull Request':
    target = st.text_input(label = "Title for the Pull Request")
    pr_base = st.text_input(label="Base branch for the Pull Request (only for 'Create Pull Request')", value="")
    pr_head = st.text_input(label="Head branch for the Pull Request (only for 'Create Pull Request')", value="")
    request = st.text_input(label="Content of the Pull Request")
    server = st.text_input(label="Discord Server where to send the summary message")
    channel = st.text_input(label="Discord Server Channel ID where to send the summary message", placeholder="e.g. 104499429202")
    date = st.date_input(label="Choose a time and a date when to schedule a reminder for your action", value=today, min_value=today, max_value=one_year_from_today)
    submit_btn = st.button(label="Run Action!", type="primary")
    if submit_btn: 
        prompt = choose_prompt(action=action, arguments={"repository": github_repo, "server": server, "channel": channel, "target": target, "request": request, "date": str(date), "base": pr_base, "head": pr_head})
        response = rq.post("http://zapbackend:443/mcp", json=McpInput(user_input=prompt).model_dump(), headers={"Content-Type": "application/json", "x-api-key": mcp_url})
        process = response.json()["process"]
        report = response.json()["response"]
        st.markdown(report)
        with st.expander(label="See agent process"):
            st.markdown(process)
elif action == 'Create Comment under Issue':
    target = st.text_input(label = "Identifier of the issue", placeholder="e.g. 10")
    request = st.text_input(label="Content of the comment")
    server = st.text_input(label="Discord Server where to send the summary message")
    channel = st.text_input(label="Discord Server Channel ID where to send the summary message", placeholder="e.g. 104499429202")
    date = st.date_input(label="Choose a time and a date when to schedule a reminder for your action", value=today, min_value=today, max_value=one_year_from_today)
    submit_btn = st.button(label="Run Action!", type="primary")
    if submit_btn: 
        prompt = choose_prompt(action=action, arguments={"repository": github_repo, "server": server, "channel": channel, "target": target, "request": request, "date": str(date)})
        response = rq.post("http://zapbackend:443/mcp", json=McpInput(user_input=prompt).model_dump(), headers={"Content-Type": "application/json", "x-api-key": mcp_url})
        process = response.json()["process"]
        report = response.json()["response"]
        st.markdown(report)
        with st.expander(label="See agent process"):
            st.markdown(process)
else:
    target = st.text_input(label = "Identifier of the pull request", placeholder="e.g. 10")
    request = st.text_input(label="Content of the comment")
    server = st.text_input(label="Discord Server where to send the summary message")
    channel = st.text_input(label="Discord Server Channel ID where to send the summary message", placeholder="e.g. 104499429202")
    date = st.date_input(label="Choose a time and a date when to schedule a reminder for your action", value=today, min_value=today, max_value=one_year_from_today)
    submit_btn = st.button(label="Run Action!", type="primary")
    if submit_btn: 
        prompt = choose_prompt(action=action, arguments={"repository": github_repo, "server": server, "channel": channel, "target": target, "request": request, "date": str(date)})
        response = rq.post("http://zapbackend:443/mcp", json=McpInput(user_input=prompt).model_dump(), headers={"Content-Type": "application/json", "x-api-key": mcp_url})
        process = response.json()["process"]
        report = response.json()["response"]
        st.markdown(report)
        with st.expander(label="See agent process"):
            st.markdown(process)

    