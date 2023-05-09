import random

# list of delegates
delegates = ['delegate1', 'delegate2', 'delegate3', 'delegate4', 'delegate5']

# Fisher-Yates shuffle algorithm
for i in range(len(delegates) - 1, 0, -1):
    j = random.randint(0, i)
    delegates[i], delegates[j] = delegates[j], delegates[i]

# select the first delegate for transaction validation
selected_delegate = delegates[0]
delegates.pop(0) # To avoid repetition of same delegate

# print the selected delegate
print(f"Selected delegate for transaction validation: {selected_delegate}")
