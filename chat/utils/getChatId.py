def generate_chat_id(user1, user2):
    # Ensure consistent ordering to make it independent of who is the user1 or user2
    Patients = sorted([str(user1.username), str(user2.username)])
    combined = "".join(Patients)

    # TODO : Ensure at most 95 characters
    # Create a hash of the combined string
    chat_id = hashlib.sha256(combined.encode()).hexdigest()
    return chat_id
