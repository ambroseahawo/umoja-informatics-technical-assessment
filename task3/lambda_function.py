def greet_user(event, context):
    # Extract the name from the dictionary
    name = event.get("name", "Guest")  # Default to "Guest" if "name" is not provided

    # Create the response message
    response = {"message": f"Hello, {name}!"}

    return response
