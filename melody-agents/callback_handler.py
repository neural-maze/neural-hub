from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from langchain_core.callbacks.base import BaseCallbackHandler

if TYPE_CHECKING:
    from langchain_core.agents import AgentAction, AgentFinish

import streamlit as st


class CustomStreamlitCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to std out."""

    def __init__(self, color: Optional[str] = None) -> None:
        """Initialize callback handler."""
        self.color = color

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        # print(f"\n\n\033[1m> Entering new {class_name} chain...\033[0m")  # noqa: T201
        with st.expander("Starting a new Agent Chain:", expanded=True):
            st.markdown(f"Entering new {class_name} chain...")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        # print("\n\033[1m> Finished chain.\033[0m")  # noqa: T201
        with st.expander("Finished chain."):
            st.write("Finished chain.")

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        # print_text(action.log, color=color or self.color)
        with st.expander("AI Thought Bubble - Next Action:", expanded=True):
            for line in action.log.split("\n"):
                st.markdown(line)

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""
        with st.expander("Tool Started", expanded=True):
            st.write(serialized)
            st.write(input_str)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        with st.expander("Tool Ended:", expanded=True):
            with st.expander("Obvervation:", expanded=True):
                if observation_prefix is not None:
                    #     print_text(f"\n{observation_prefix}")
                    st.markdown(f"\n{observation_prefix}")
            st.markdown(f"\n{output}")
            # print_text(output, color=color or self.color)
            if llm_prefix is not None:
                with st.expander("LLM Prefix:", expanded=True):
                    # print_text(f"\n{llm_prefix}")
                    st.markdown(f"\n{llm_prefix}")

    def on_text(
        self,
        text: str,
        color: Optional[str] = None,
        end: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when agent ends."""
        # print_text(text, color=color or self.color, end=end)
        with st.expander("Agent ending."):
            st.write("Agent ending")

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        # print_text(finish.log, color=color or self.color, end="\n")
        with st.expander("Agent Ended."):
            st.write("Agent ended")
