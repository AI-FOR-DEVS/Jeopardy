import autogen

local_config = [
    {
        "model": 'gpt-3.5',
        "base_url": "http://localhost:1234/v1"
    }
]

assistant = autogen.AssistantAgent(
    "assistant",
    system_message="You are a helpful assistant.",
    llm_config={"config_list": local_config}
)

user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    default_auto_reply="ok",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "_output", "use_docker": False},
    is_termination_msg=lambda x: x.get("content", "") and x.get(
        "content", "").rstrip().endswith("TERMINATE")
)

user_proxy.initiate_chat(
    assistant,
    message=f"""
      Write a short poem and conclude with the word 'TERMINATE'
    """
)
