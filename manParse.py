import json

# Define TypeScript file
TS_FILENAME = "data.ts"

def placeholder(value, default="[PH]"):
    return value.strip() if value and value.strip() else default

def get_user_input(prompt):
    return input(prompt).strip()

def create_new_entry():
    return {
        "word": {
            "definition": placeholder(get_user_input("Enter English meaning: ")),
            "type": placeholder(get_user_input("Enter word type: ")),
            "dictionary": {
                "hiragana": placeholder(get_user_input("Enter dictionary hiragana: ")),
                "kanji": placeholder(get_user_input("Enter dictionary kanji: ")),
            },
        },
        "presentAffirmative": {
            "hiragana": placeholder(get_user_input("Enter present affirmative hiragana: ")),
            "kanji": placeholder(get_user_input("Enter present affirmative kanji: ")),
        },
        "presentNegative": {
            "hiragana": placeholder(get_user_input("Enter present negative hiragana: ")),
            "kanji": placeholder(get_user_input("Enter present negative kanji: ")),
        },
        "pastAffirmative": {
            "hiragana": placeholder(get_user_input("Enter past affirmative hiragana: ")),
            "kanji": placeholder(get_user_input("Enter past affirmative kanji: ")),
        },
        "pastNegative": {
            "hiragana": placeholder(get_user_input("Enter past negative hiragana: ")),
            "kanji": placeholder(get_user_input("Enter past negative kanji: ")),
        },
    }

def append_to_ts_file(filename, new_entry):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            json_data = content.split("=", 1)[1].strip().rstrip(";")
            data = json.loads(json_data) if json_data else []
        
        data.append(new_entry)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("export const conjugationData: ConjugationItem[] = ")
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write(";")
            
        print("New entry added successfully!")
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON. Initializing a new array.")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("export const conjugationData: ConjugationItem[] = ")
            json.dump([new_entry], f, ensure_ascii=False, indent=2)
            f.write(";")
        print("Created a new TypeScript file with the entry.")
    except Exception as e:
        print(f"Error updating TypeScript file: {e}")

# Execution
new_entry = create_new_entry()
append_to_ts_file(TS_FILENAME, new_entry)
