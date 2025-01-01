import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="34b3a1631973091f47522767f7601644.e0QU7sGy3DNf2NzG") # 填写您自己的APIKey

# 创建FastAPI应用
app = FastAPI()

# 定义请求体模型
class Query(BaseModel):
    text: str


# 定义路由
@app.post("/chat")
async def chat(query: Query):
    # 声明全局变量以便在函数内部使用模型和分词器
    response = client.chat.completions.create(
        model="glm-4-flash",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": query.text
            }
        ]
    )
    return {
        "result": response.choices[0].message,  # 返回生成的响应
    }


# 主函数入口
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080, workers=1)