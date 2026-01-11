from server import sdk
print("SDK Agents:", sdk.agents)
for agent in sdk.agents:
    print(f"Agent Name: {agent.name}")
