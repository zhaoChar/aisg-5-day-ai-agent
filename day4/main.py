from model import Agent

# Example usage
query = "What is (8 * 5.43 + 7) ^ 6.5"
agent = Agent(query)

max_calls = 1

for i in range(max_calls):
    print(f"iterations: {i + 1}")
    agent.call_model()

# # check finish reason     
# if finish_reason == "STOP":
#     return repsonse 
# elif "mock_function":
#     agent.call_model()
#     #append the results 

    #continue 