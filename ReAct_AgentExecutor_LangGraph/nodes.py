from dotenv import load_dotenv
from langgraph.prebuilt.tool_executor import ToolExecutor

from react import react_agent_runnable, tools
from state import AgentState

load_dotenv()


def run_agent_reasoning_engine(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}


tool_executor = ToolExecutor(tools)


def execute_tools(state: AgentState):
    agent_action = state["agent_outcome"]
    # agent_action contiene tutta la informazione su quale funzione eseguire
    # e con quali argomenti avviarla
    output = tool_executor.invoke(agent_action)
    # langGraph prenderà questo risultato e va a verificare lo stato attuale
    # nell'attributo intermediate_steps e va ad aggiungere alla lista la nuova tupla
    # che creiamo ora
    return {"intermediate_steps": [(agent_action, str(output))]}

