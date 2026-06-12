import random
import string

print("===== Random Password Generator =====")

# Get password length
length = int(input("Enter password length: "))

# Character set options
characters = ""

if input("Include lowercase letters? (y/n): ").lower() == "y":
    characters += string.ascii_lowercase

if input("Include uppercase letters? (y/n): ").lower() == "y":
    characters += string.ascii_uppercase

if input("Include numbers? (y/n): ").lower() == "y":
    characters += string.digits

if input("Include symbols? (y/n): ").lower() == "y":
    characters += string.punctuation

# Check if at least one character type is selected
if not characters:
    print("Error: You must select at least one character type!")
else:
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))

    print("\nGenerated Password:")
    print(password)