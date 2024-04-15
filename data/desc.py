print("Bot was started!")
def start(message):
    return (f"""Привет, {message.from_user.first_name}!""")
