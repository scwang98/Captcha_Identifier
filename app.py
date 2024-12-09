from fastapi import FastAPI
from pydantic import BaseModel
from captcha_locator import CaptchaLocator
import time

# 创建 FastAPI 实例
app = FastAPI()

locator = CaptchaLocator()

def locate(image_base64, words):
    start_time = time.time()
    results = locator.run(image_base64, words)
    time_consuming = time.time() - start_time

    return (results, time_consuming)

# 定义输入数据的模型
class AddRequest(BaseModel):
    image_base64: str
    words: list

# 定义 RESTful 路由
@app.post("/locate")
def add(request: AddRequest):
    (results, time_consuming) = locate(request.image_base64, request.words)
    return {
        "result": results,
        "time": time_consuming
    }
