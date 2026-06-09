from dotenv import load_dotenv
from langchain.chat_models import init_chat_model 
from langchain.tools import tool 
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict, Annotated  
from langgraph.types import interrupt, Command



@tool 
def get_stock_price(symbol: str) -> float:
    """Return the current stock price of a given stock symbol"""
    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6
    }.get(symbol, 0.0)


@tool
def buy_stocks(symbol:str, quantity:int, total_price:float) -> str:
    """Buy stocks given the stock symbol and quantity"""
    decision = interrupt(f"Approve buying {quantity} {symbol} stocks for ${total_price:.2f}?")
    if decision == "yes":
        return f"You bought {quantity} {symbol} stocks for ${total_price:.2f}"
    else:
        return f"You cancelled buying {quantity} {symbol} stocks for ${total_price:.2f}"


def get_llm(model_name, tools):
        
    llm = init_chat_model(model = model_name)
    llm_with_tools = llm.bind_tools(tools)
    return llm_with_tools


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]} 

def build_graph():
    builder = StateGraph(State)

    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot",tools_condition)
    builder.add_edge("tools", "chatbot")
    builder.add_edge("chatbot", END)

    graph = builder.compile(checkpointer = memory)
    return graph

def invoke_graph(query, config):   
    message = [{"role": "user", "content": query}]
    state = graph.invoke({"messages": message}, config = config)
    return state


if __name__ == "__main__":

    model_name = "groq:qwen/qwen3-32b"
    tools = [get_stock_price, buy_stocks]
    config = {"configurable": {"thread_id": "buy_thread"}}

    load_dotenv()

    # adding memory 
    memory = MemorySaver()

    llm_with_tools = get_llm(model_name, tools)

    graph = build_graph()

    queries = [
        "What is the current price of 10 MSFT stocks?",
        "Buy 10 MSFT stocks at current price"
    ]

    for query in queries:
        state = invoke_graph(query, config)
        if "__interrupt__" in state:
            print(state["__interrupt__"][0].value)

            decision = input("Approve (yes/no): ")

            state = graph.invoke(Command(resume = decision), config = config)
        print(state["messages"][-1].content)





