import gradio as gr
import time
from zhipuai import ZhipuAI
from typing import *

# 最大历史对话长度
MAX_HISTORY_LEN = 50

client = ZhipuAI(api_key="")  # 填写您自己的APIKey

with gr.Blocks(title="智小优") as demo:
    gr.HTML("""<h1 align="center">智小优</h1>""")
    gr.Markdown("<h1><center>你的私人AI助手</center></h1>")
    # 对话框
    chatbot = gr.Chatbot(render=True)
    # 提问框
    msg = gr.Textbox(placeholder="请输入你的问题")

    with gr.Row():
        submit = gr.Button('提交')
        clear = gr.Button("清空")

    def user(user_message: str, history: List[List]) -> Tuple:
        """
        Args:
            user_message: 用户输入
            history: 历史问答
        Returns:
        """
        return "", history + [[user_message, None]]

    def bot(history: List[List]) -> None:
        history_record = ""
        for i in history:
            print(i)
            for k in i:
                if k != None:
                    history_record += k

        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                # {"role": "user", "content": history[-1][0]}
                {"role": "user", "content": history_record}
            ],
            stream=True
        )
        # print(type(history[-1][0]))
        # print(len(history[-1]))
        # print(history[-1])
        # print(len(history[-1][0]))
        # print(history[-1][0])

        history[-1][1] = ""

        for chunk in response:
            for choice in chunk.choices:
                # content = choice.delta.content
                if content := choice.delta.content:
                    history[-1][1] += content
                    time.sleep(0.05)
                    # 如果超过最大历史长度，弹出最老的历史对话
                    if len(history) > MAX_HISTORY_LEN:
                        history.pop(0)
                    print(history)
                    yield history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    # 触发事件监听
    submit.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == '__main__':
    demo.queue().launch()

