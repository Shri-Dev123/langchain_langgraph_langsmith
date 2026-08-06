

create_agent(
  model = "gpt-5.6",
  tools=[tool_1, tool_2],
  system_prompt="""You are a helpful assistant that can use the provided tools to answer questions.""",
  response_format= ToolStrategy(structuredSchema),
  context_schema = ContextSchemaDefinition,
  state_schema = CustomState(agentState),
  checkpointer = InMemorySaver,
  middleware = []
)