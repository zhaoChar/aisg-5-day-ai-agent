from model import Agent

agent = Agent()

# Example usage
while True:
    query = input('Enter your query: ')
    
    if (query == 'exit()'):
        break

    max_calls = 1

    for i in range(max_calls):
        # print(f"iterations: {i + 1}")
        agent.call_model(query)
