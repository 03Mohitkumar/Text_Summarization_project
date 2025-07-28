import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from summarizer import TextSummarizer

class SummarizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarization Tool")
        self.root.geometry("800x600")

        self.summarizer = TextSummarizer()


        self.input_method_var = tk.StringVar(value="file")


        tk.Label(root, text="Choose input method:").pack(anchor="w", padx=10, pady=5)
        tk.Radiobutton(root, text="Load text from a file", variable=self.input_method_var, value="file",
                       command=self.toggle_input_method).pack(anchor="w", padx=20)
        tk.Radiobutton(root, text="Paste text manually", variable=self.input_method_var, value="manual",
                       command=self.toggle_input_method).pack(anchor="w", padx=20)


        self.file_frame = tk.Frame(root)
        self.file_frame.pack(fill="x", padx=10, pady=5)
        self.file_path_var = tk.StringVar()
        tk.Entry(self.file_frame, textvariable=self.file_path_var).pack(side="left", fill="x", expand=True)
        tk.Button(self.file_frame, text="Browse", command=self.browse_file).pack(side="left", padx=5)


        self.manual_frame = tk.Frame(root)

        self.manual_text = scrolledtext.ScrolledText(self.manual_frame, height=10)
        self.manual_text.pack(fill="both", expand=True)
        self.manual_frame.pack_forget()


        tk.Button(root, text="Summarize", command=self.summarize_text).pack(pady=10)


        tk.Label(root, text="Original Text (truncated to 1000 chars):").pack(anchor="w", padx=10)
        self.original_text_box = scrolledtext.ScrolledText(root, height=10, state="disabled")
        self.original_text_box.pack(fill="both", expand=True, padx=10, pady=5)


        tk.Label(root, text="Summary:").pack(anchor="w", padx=10)
        self.summary_text_box = scrolledtext.ScrolledText(root, height=7, state="disabled")
        self.summary_text_box.pack(fill="both", expand=True, padx=10, pady=5)

    def toggle_input_method(self):
        method = self.input_method_var.get()
        if method == "file":
            self.manual_frame.pack_forget()
            self.file_frame.pack(fill="x", padx=10, pady=5)
        else:
            self.file_frame.pack_forget()
            self.manual_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.file_path_var.set(file_path)

    def summarize_text(self):

        method = self.input_method_var.get()
        if method == "file":
            path = self.file_path_var.get().strip().strip('"').strip("'")
            if not path:
                messagebox.showerror("Error", "Please select a file path.")
                return
            if not os.path.isfile(path):
                messagebox.showerror("Error", f"File not found:\n{path}")
                return
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = self.manual_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Error", "Please enter some text to summarize.")
                return

        if len(text) == 0:
            messagebox.showinfo("Info", "No text provided.")
            return


        self.original_text_box.configure(state="normal")
        self.original_text_box.delete("1.0", tk.END)
        display_text = text[:1000] + ("..." if len(text) > 1000 else "")
        self.original_text_box.insert(tk.END, display_text)
        self.original_text_box.configure(state="disabled")


        try:
            summary = self.summarizer.summarize(text)
        except Exception as e:
            messagebox.showerror("Summarization Error", str(e))
            return

        self.summary_text_box.configure(state="normal")
        self.summary_text_box.delete("1.0", tk.END)
        self.summary_text_box.insert(tk.END, summary)
        self.summary_text_box.configure(state="disabled")

def main():
    root = tk.Tk()
    app = SummarizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
