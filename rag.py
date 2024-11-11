import operator
from typing import List, Annotated, TypedDict
from langchain_community.llms import Ollama
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END
import json
from IPython.display import Image, display

# Initialize Ollama LLM
LLM_MODEL = "llama3.2:3b"
llm = Ollama(model=LLM_MODEL)
llm_json_mode = Ollama(model=LLM_MODEL, format="json")


# Define nodes and their prompts in a dictionary
# NODES = {
#     "node1": {
#         "name": "Order Tracking",
#         "prompt": "You need to help track orders of the various users only. Please address the following customer inquiry: {question}",
#     },
#     "node2": {
#         "name": "Product Information",
#         "prompt": "You need to provide information about various products related to this question: {question}",
#     },
#     "node3": {
#         "name": "Review Product",
#         "prompt": "Respond with proper reviews fetched from the database for the given asked queries. Please respond to the following query: {question}",
#     },
# }


class GraphState(TypedDict):
    chat_message: str
    generation: str
    max_retries: int
    answers: int
    loop_step: Annotated[int, operator.add]


def route_question(state: GraphState) -> dict:
    print("---ROUTE QUESTION---")
    route_prompt = f"""Based on the following user question, decide which node to route to:
{', '.join([f"{key}: {value['name']}" for key, value in NODES.items()])}

User question: {state["chat_message"]}

Return JSON with a single key 'node' that is one of: {', '.join(NODES.keys())}.
"""
    route_response = llm_json_mode.invoke([HumanMessage(content=route_prompt)])
    node = json.loads(route_response)["node"]
    global ROUTED_NODE
    ROUTED_NODE = node
    print(f"---ROUTE QUESTION TO {node.upper()}---")
    return {"route": node, "loop_step": state["loop_step"] + 1}


def generate_node_function(node_info):
    def node_function(state: GraphState) -> dict:
        prompt = node_info["prompt"] + state["chat_message"]
        generation = llm.invoke([HumanMessage(content=prompt)])
        global GENERATED_OUTPUT
        GENERATED_OUTPUT = generation
        return {"generation": generation, "loop_step": state["loop_step"] + 1}

    return node_function


def validator(state: GraphState) -> dict:
    print("---VALIDATOR---")
    chat_message = state["chat_message"]
    generation = state["generation"]
    prompt = f"""Given the following user question and generated answer, determine if the answer is relevant and not a hallucination.

User question: {chat_message}

Generated answer: {generation}

Is the answer relevant and not a hallucination? Return JSON with a single key 'is_valid' that is either 'yes' or 'no'.
"""
    response = llm_json_mode.invoke([HumanMessage(content=prompt)])
    is_valid = json.loads(response)["is_valid"]

    if is_valid == "yes":
        return {"validator": "end", "loop_step": state["loop_step"] + 1}
    elif state["loop_step"] <= state["max_retries"]:
        return {"validator": "retry", "loop_step": state["loop_step"] + 1}
    else:
        return {"validator": "max_retries", "loop_step": state["loop_step"] + 1}


def create_workflow():
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("route", route_question)
    for node_key, node_info in NODES.items():
        workflow.add_node(node_key, generate_node_function(node_info))
    workflow.add_node("validator", validator)

    # Set entry point
    workflow.set_entry_point("route")

    # Add edges
    workflow.add_conditional_edges(
        "route",
        lambda x: x["route"],
        {node_key: node_key for node_key in NODES.keys()},
    )
    for node_key in NODES.keys():
        workflow.add_edge(node_key, "validator")

    # Set conditional edges for validator
    workflow.add_conditional_edges(
        "validator",
        lambda x: x["validator"],
        {"end": END, "retry": "route", "max_retries": END},
    )

    return workflow.compile()


def run_workflow(input_message: str, nodes: dict, max_retries: int = 2):
    global EVENT_LOGS
    EVENT_LOGS = []

    global NODES
    NODES = nodes

    for k, v in NODES.items():
        NODES[k]["prompt"] = NODES[k]["prompt"].format(question=input_message)

    g = create_workflow()
    print(NODES)

    inputs = {
        "chat_message": input_message,
        "max_retries": max_retries,
        "loop_step": 0,
    }
    for event in g.stream(inputs, stream_mode="values"):
        EVENT_LOGS.append(event)

    return {
        "events": EVENT_LOGS,
        "routed_node": ROUTED_NODE,
        "generated_output": GENERATED_OUTPUT,
    }

    # Display the graph
    # display(Image(g.get_graph().draw_mermaid_png()))
