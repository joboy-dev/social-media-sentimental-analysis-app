def generate_message(message: str, type: str='success'):
    emoji = ""
    
    if type == "error":
        emoji = "❌"  # Red cross for errors
    elif type == "warning":
        emoji = "⚠️"  # Warning sign
    elif type == "info":
        emoji = "ℹ️"  # Information symbol
    elif type == "success":
        emoji = "✅"
    
    return f"{emoji} {message}"