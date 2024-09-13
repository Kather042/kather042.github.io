# app.py
from flask import Flask, request, jsonify
from gradio_client import Client
import base64

app = Flask(__name__)


@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    client = Client("https://s5k.cn/api/v1/studio/ByteDance/Hyper-FLUX-8Steps-LoRA/gradio/")
    result = client.predict(
        height=data.get('height', 1024),
        width=data.get('width', 1024),
        steps=data.get('steps', 8),
        scales=data.get('scales', 3.5),
        prompt=data.get('prompt', ''),
        seed=data.get('seed', 3413),
        api_name="/process_image"
    )

    # 假设result是一个包含图像数据的列表或字典
    # 这里的处理方式可能需要根据实际返回的数据结构进行调整
    if isinstance(result, list) and len(result) > 0:
        image_data = result[0]
        # 如果图像数据是文件路径，读取文件并转为base64
        with open(image_data, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return jsonify({'image': encoded_string})
    else:
        return jsonify({'error': 'No image data received'}), 400


if __name__ == '__main__':
    app.run(debug=True)