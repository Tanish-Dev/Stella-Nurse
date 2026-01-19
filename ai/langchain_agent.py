import os
import logging
from typing import AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables import RunnableConfig

# Import tools
try:
    from ai.tools import check_vitals, get_medicine_schedule, recall_patient_memory, trigger_emergency_alert
except ImportError:
    # Handle case where run from subfolder
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ai.tools import check_vitals, get_medicine_schedule, recall_patient_memory, trigger_emergency_alert

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Stella, a compassionate and professional medical nurse assistant for an embedded robot.
Your goal is to care for the patient, monitor their vitals, and provide helpful reminders.

CORE RULES:
1. **Safety First**: rapid escalation of emergencies. If a user reports severe symptoms (chest pain, difficulty breathing, falls), use the `trigger_emergency_alert` tool immediately.
2. **No Diagnosis**: Never diagnose conditions or prescribe medications. Suggest consulting a doctor for medical advice.
3. **Tone**: Be calm, concise, warm, and professional. Keep responses short (1-2 sentences) as they will be spoken aloud.
4. **Tools**: Use the provided tools to check vitals, memories, or schedules when relevant. check_vitals is useful when the user complains of feeling unwell.
"""

class NurseAgent:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        self.agent_executor = None
        logger.info(f"Nurse AI agent initialized with model {model_name}")

    async def initialize(self):
        """Initialize LangChain agent with tools and LLM"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY not found. Agent capabilities will be limited.")
        
        # specific for Gemini which handles tool calling well
        llm = ChatGoogleGenerativeAI(
            model=self.model_name, 
            temperature=0, 
            convert_system_message_to_human=True
        )
        
        tools = [check_vitals, get_medicine_schedule, recall_patient_memory, trigger_emergency_alert]
        
        # Bind tools to LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(llm, tools, prompt)
        
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True,
            return_intermediate_steps=False
        )
        logger.info("LangChain agent executor created.")

    async def process_stream(self, user_input: str, chat_history: list[BaseMessage] = []) -> AsyncGenerator[str, None]:
        """
        Process user input and yield chunks of text for TTS.
        This allows for lower latency responses.
        """
        if not self.agent_executor:
            await self.initialize()
            
        logger.info(f"Processing input: {user_input}")
        
        # Streaming response from the agent
        # Note: AgentExecutor streaming is a bit complex, strictly getting token-by-token from the final answer 
        # requires parsing the stream events. For simplicity in this demo, we might await the final response 
        # or implement a custom stream handler. 
        # Here we use .astream_events or .astream if supported, but standard AgentExecutor 
        # is often better handled by awaiting result for tools, then streaming final answer.
        # Alternatively, we can just yield the final string for now if tool use is involved.
        
        try:
             # Using invoke for reliability with tools, then we can simulate streaming or just return
             # True streaming with tools requires iterating over the iterator
             async for event in self.agent_executor.astream(
                {"input": user_input, "chat_history": chat_history}
            ):
                # We are looking for the 'output' key in the final chunk or intermediate tokens
                if "output" in event:
                    # yield event["output"] # This is usually the final result in default executor
                    pass
            
             # Fallback to standard invoke to ensure tools run correctly, then yield result
             # Ideally we hook into the LLM stream.
             result = await self.agent_executor.ainvoke({"input": user_input, "chat_history": chat_history})
             yield result["output"]

        except Exception as e:
            logger.error(f"Error in agent processing: {e}")
            yield "I apologize, I am having trouble processing that right now."

