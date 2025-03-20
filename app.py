from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import shutil

app = Flask(__name__)
CORS(app)

def clear_data_directory():
    # 如果data目录存在，删除它及其所有内容
    if os.path.exists('data'):
        shutil.rmtree('data')
    # 重新创建空的data目录
    os.makedirs('data')
    os.makedirs('data/images')

# 在应用启动时清空数据
clear_data_directory()

@app.route('/api/saveCaseData', methods=['POST'])
def save_case_data():
    case_data = request.get_json()
    if not case_data:
        return jsonify({'error': '没有收到数据'}), 400

    try:
        with open('data/caseData.json', 'w', encoding='utf-8') as f:
            json.dump(case_data, f, ensure_ascii=False, indent=2)
        return jsonify({'message': '案件数据已成功保存'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/uploadImages', methods=['POST'])
def upload_images():
    # 每次上传图片前清空images目录
    if os.path.exists('data/images'):
        shutil.rmtree('data/images')
    os.makedirs('data/images')

    if 'description' in request.form:
        description = request.form['description']
    else:
        description = ''

    if 'images' not in request.files:
        return jsonify({'error': '没有收到图片文件'}), 400

    images = request.files.getlist('images')
    image_info = []

    try:
        for image in images:
            filename = image.filename
            filepath = os.path.join('data/images', filename)
            image.save(filepath)
            image_info.append({'filename': filename, 'filepath': filepath})

        image_data = {
            'description': description,
            'images': image_info
        }
        with open('data/imageData.json', 'w', encoding='utf-8') as f:
            json.dump(image_data, f, ensure_ascii=False, indent=2)

        return jsonify({'message': '图片数据已成功保存'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)