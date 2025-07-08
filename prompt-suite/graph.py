from typing_extensions import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_google_genai import ChatGoogleGenerativeAI
import os


class GraphState(TypedDict):
    user_prompt: str
    messages: Annotated[list[HumanMessage | AIMessage], add_messages]
    initial_prompt: str
    # Multi-criteria scores
    clarity: int
    specificity: int
    completeness: int
    relevance: int
    feedback: str
    refined_prompt: str
    final_prompt: str

builder = StateGraph(GraphState, input_schema=GraphState, output_schema=GraphState)

from langchain_openai import ChatOpenAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key="AIzaSyBr01wyBax_1znBBa87t_N1QskRoWxuzRM")

def prompt_generator(state: GraphState) -> GraphState:
    instruction = "Your Objective is to assess the given prompt use your agentic structure and iterate and narrow down to 2 better, more specific and detailed prompts. You are a senior Prompt Engineer and it is your duty to concisely generate 2 modified prompts from the given prompt. Use various techniques such as in-context learning (where you give examples to teach the LLM without finetuning it) or anything and everything at your disposal, REMEMBER to give a clean output with no unnecessary sentences and cut out all the fluff"
    msg = llm.invoke([HumanMessage(content=f"{instruction}\n\nPrompt: {state['user_prompt']}")])
    return {"messages": [msg], "initial_prompt": msg.content}

def prompt_evaluator(state: GraphState) -> GraphState:
    evaluation_instruction = (
        "You are a senior prompt engineer. Evaluate the following prompt for: "
        "Clarity, Specificity, Completeness, and Relevance. "
        "Score each from 1 (poor) to 10 (excellent), then provide a brief suggestion for improvement. "
        "Respond in this format:\n"
        "Clarity: <number>\n"
        "Specificity: <number>\n"
        "Completeness: <number>\n"
        "Relevance: <number>\n"
        "Feedback: <your feedback>\n\n"
        "Prompt:\n"
    )
    prompt_to_evaluate = state.get("initial_prompt", "")
    msg = llm.invoke([HumanMessage(content=f"{evaluation_instruction}{prompt_to_evaluate}")])
    import re
    def extract_score(label):
        match = re.search(rf"{label}:\\s*(\\d+)", msg.content)
        return int(match.group(1)) if match else 5
    clarity = extract_score("Clarity")
    specificity = extract_score("Specificity")
    completeness = extract_score("Completeness")
    relevance = extract_score("Relevance")
    feedback_match = re.search(r"Feedback:\s*(.*)", msg.content)
    feedback = feedback_match.group(1).strip() if feedback_match else "No feedback provided."
    return {
        "clarity": clarity,
        "specificity": specificity,
        "completeness": completeness,
        "relevance": relevance,
        "feedback": feedback
    }

def prompt_optimizer(state: GraphState) -> GraphState:
    # Identify weakest criteria
    criteria_scores = {
        "Clarity": state["clarity"],
        "Specificity": state["specificity"],
        "Completeness": state["completeness"],
        "Relevance": state["relevance"]
    }
    # Find the lowest scoring criteria (could be more than one)
    min_score = min(criteria_scores.values())
    weakest = [k for k, v in criteria_scores.items() if v == min_score]
    weakest_str = ", ".join(weakest)
    # Build optimization instruction
    optimization_instruction = (
        f"You are a senior prompt engineer. The following prompt was evaluated and needs improvement. "
        f"The weakest aspects are: {weakest_str} (score: {min_score}/10). "
        f"Feedback: {state['feedback']}\n"
        f"Please revise the prompt to specifically improve these aspects while keeping the original intent. "
        f"Return only the improved prompt, with no extra commentary.\n\nPrompt to improve:\n{state['initial_prompt']}"
    )
    msg = llm.invoke([HumanMessage(content=optimization_instruction)])
    return {"messages": [msg], "refined_prompt": msg.content}

def example_strategist(state: GraphState) -> GraphState:
    examples = ("Example:\nInput: ... \nOutput: ...\n")
    combined = state["refined_prompt"] + "\n\n" + examples
    return {"final_prompt": combined}

def validator(state: GraphState) -> GraphState:
    # Final check, here we assume valid
    return {}

builder.add_node("Generator", prompt_generator)
builder.add_node("Evaluator", prompt_evaluator)
builder.add_node("Optimizer", prompt_optimizer)
builder.add_node("ExampleStrategist", example_strategist)
builder.add_node("Validator", validator)

builder.add_edge(START, "Generator")
builder.add_edge("Generator", "Evaluator")
builder.add_edge("Evaluator", "Optimizer")
builder.add_edge("Optimizer", "ExampleStrategist")
builder.add_edge("ExampleStrategist", "Validator")
builder.add_edge("Validator", END)

graph = builder.compile()

def refine_prompt(user_text: str) -> str:
    result = graph.invoke({
        "user_prompt": user_text,
        "messages": [],
        "initial_prompt": "",
        "clarity": 0,
        "specificity": 0,
        "completeness": 0,
        "relevance": 0,
        "feedback": "",
        "refined_prompt": "",
        "final_prompt": ""
    })
    output = result["final_prompt"].strip()
    # Remove code block markers
    if output.startswith("```") and output.endswith("```"):
        output = output[3:-3].strip()
    # Remove stray markdown, dashes, slashes
    output = output.replace("```", "").replace("-", "").replace("/", "")
    # Replace literal \n and \n with actual newlines
    output = output.replace("\\n", "\n").replace("\n", "\n")
    # Collapse multiple newlines into a single newline
    import re
    output = re.sub(r'\n+', '\n', output)
    # Optionally, strip leading/trailing whitespace again
    output = output.strip()
    return output