import json
from collections import defaultdict

from dotenv import load_dotenv
from langgraph.prebuilt import ToolInvocation

load_dotenv()

from typing import List
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage
from schemas import AnswerQuestion, Reflection
from chains import parser, tool_executor


def execute_tools(state: List[BaseMessage]) -> List[ToolMessage]:
    tool_invocation = state[-1]
    parsed_tool_calls = parser.invoke(tool_invocation)
    ids = []
    tool_invocations = []
    for parsed_call in parsed_tool_calls:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocations.append(
                ToolInvocation(
                    tool="tavily_search_results_json",
                    tool_input=query,
                )
            )
            ids.append(parsed_call["id"])

    outputs = tool_executor.batch(tool_invocations)

    # Map each output to its corresponding ID and tool input
    outputs_map = defaultdict(dict)
    for id_, output, invocation in zip(ids, outputs, tool_invocations):
        outputs_map[id_][invocation.tool_input] = output

    # Convert the mapped outputs to ToolMessage objects
    tool_messages = []
    for id_, mapped_output in outputs_map.items():
        tool_messages.append(
            ToolMessage(content=json.dumps(mapped_output), tool_call_id=id_)
        )

    return tool_messages


if __name__ == "__main__":

    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous soc problem domain,"
        " list startups that do that and raised capital."
    )

    answer = AnswerQuestion(
        answer="",
        reflection=Reflection(missing="", superfluous=""),
        search_queries=[
            "AI-powered SOC startups funding",
            "AI SOC problem domain specifics",
            "Technologies used by AI-powered SOC startups",
        ],
        id="call_KpYHichFFEmLitHFvFhKy1Ra"
    )

    raw_res = execute_tools(
        state=[
            human_message,
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": AnswerQuestion.__name__,
                        "args": answer.model_dump(),
                        "id": "call_KpYHichFFEmLitHFvFhKy1Ra"
                    }
                ]
            )
        ]
    )

    print(raw_res)

