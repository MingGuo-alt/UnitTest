import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from zhipuai import ZhipuAI


def get_ai_response_in_thread(prompt_text, text_widget):
    try:
        client = ZhipuAI(api_key="") #填写您的API Key

        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
            stream=True,
        )

        # 在GUI中显示响应
        for chunk in response:
            for choice in chunk.choices:
                text_widget.insert(tk.END, choice.delta.content)
                text_widget.see(tk.END)  # 滚动到最后
                text_widget.update_idletasks()  # 强制更新GUI

    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_submit():
    prompt_text = input_entry.get()
    if prompt_text.lower() == "退出":
        root.destroy()
    else:
        thread = Thread(target=get_ai_response_in_thread, args=(prompt_text, output_text))
        thread.start()


root = tk.Tk()
root.title("ZhipuAI Chatbot")

input_label = tk.Label(root, text="请输入您的问题或输入'退出'结束对话：")
input_label.pack(pady=10)

input_entry = tk.Entry(root, width=50)
input_entry.pack()

submit_button = tk.Button(root, text="提交", command=on_submit)
submit_button.pack(pady=10)

output_scroll = scrolledtext.ScrolledText(root, height=20, width=50)
output_text = output_scroll
output_scroll.pack(pady=10, expand=True, fill="both")

root.mainloop()
