import logging
import sys

import streamlit as st

from xpipe_wiki.manager_factory import XPipeRobotManagerFactory, XPipeRobotRevision

logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Sidebar contents
with st.sidebar:
    st.title("🤗💬 LLM Chat App")
    st.markdown(
        """
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [X-Pipe](https://github.com/ctripcorp/x-pipe)
    """
    )
    # add_vertical_space(5)
    st.write("Made by Nick")


def main() -> None:
    st.header("X-Pipe Wiki 机器人 💬")
    robot_manager = XPipeRobotManagerFactory.get_or_create(
        XPipeRobotRevision.SIMPLE_OPENAI_VERSION_0
    )
    robot = robot_manager.get_robot()
    query = st.text_input("X-Pipe Wiki 问题:")
    if query:
        response = robot.ask(question=query)
        st.write(response)


if __name__ == "__main__":
    main()
