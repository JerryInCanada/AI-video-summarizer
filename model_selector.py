"""
Model Selector - 
Used for quickly switching models. Future integration into the UI is possible.
"""
import config

def list_models():
    """List all available models"""
    print("=" * 60)
    print("Available AI models".center(60))
    print("=" * 60)
    
    for key, model in config.AVAILABLE_MODELS.items():
        current = " [current]" if key == config.SELECTED_MODEL else ""
        print(f"\n{key.upper()}{current}")
        print(f"  name: {model['name']}")
        print(f"  Model ID: {model['model_id']}")
        print(f"  Description: {model['description']}")
    
    print("\n" + "=" * 60)

def select_model(model_type):
    """
    Select Model
    
    Args:
        model_type: claude / gpt / gemini
    """
    if model_type not in config.AVAILABLE_MODELS:
        print(f"Error: Unsupported model type '{model_type}'")
        print(f"Options: {', '.join(config.AVAILABLE_MODELS.keys())}")
        return False
    
    # Update the config.py file
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace SELECTED_MODEL
    import re
    content = re.sub(
        r'SELECTED_MODEL = "[^"]*"',
        f'SELECTED_MODEL = "{model_type}"',
        content
    )
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✓ Switched to model: {config.AVAILABLE_MODELS[model_type]['name']}")
    print(f"  This model will be used on the next run.")
    return True

def get_current_model():
    """Get the currently selected model"""
    return config.SELECTED_MODEL, config.AVAILABLE_MODELS[config.SELECTED_MODEL]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_models()
        elif command == "select" and len(sys.argv) > 2:
            model_type = sys.argv[2]
            select_model(model_type)
        else:
            print("usage:")
            print("  python model_selector.py list              # List all models")
            print("  python model_selector.py select claude     # Select Claude model")
            print("  python model_selector.py select gpt        # Select GPT model")
            print("  python model_selector.py select gemini     # Select Gemini model")
    else:
        list_models()

