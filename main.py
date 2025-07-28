import os
from summarizer import TextSummarizer

def load_text_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    summarizer = TextSummarizer()

    print("Choose input method:")
    print("1. Load text from a file")
    print("2. Enter/paste text manually")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        file_path = input("Enter the relative path to the text file (e.g., data/sample_text.txt): ").strip()
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        text = load_text_from_file(file_path)
    elif choice == '2':
        print("Enter/paste your text (finish by entering a blank line):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)
    else:
        print("Invalid choice. Exiting.")
        return

    if not text.strip():
        print("No text provided to summarize!")
        return

    summary = summarizer.summarize(text)

    print("\n--- Original Text (truncated to 500 chars) ---")
    print(text[:500] + ("..." if len(text) > 500 else ""))
    print("\n--- Summary ---")
    print(summary)

if __name__ == "__main__":
    main()

