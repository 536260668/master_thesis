# -*- coding: utf-8 -*-
"""
图片裁剪工具 - Web界面
支持无损裁剪、多次裁剪、预设比例
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from PIL import Image
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB最大上传

# 目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
UPLOAD_DIR = os.path.join(BASE_DIR, 'temp_uploads')

# 确保目录存在
for dir_path in [STATIC_DIR, OUTPUT_DIR, UPLOAD_DIR]:
    os.makedirs(dir_path, exist_ok=True)


@app.route('/')
def index():
    """主页面"""
    return send_from_directory(STATIC_DIR, 'crop.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    """上传图片并返回图片信息"""
    if 'image' not in request.files:
        return jsonify({'error': '未选择文件'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    # 检查文件类型
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        return jsonify({'error': f'不支持的文件类型: {file_ext}'}), 400

    # 保存临时文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_filename = f"temp_{timestamp}{file_ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    file.save(temp_path)

    # 获取图片信息
    with Image.open(temp_path) as img:
        width, height = img.size
        mode = img.mode

    # 返回图片信息和临时文件名
    return jsonify({
        'success': True,
        'filename': temp_filename,
        'original_name': file.filename,
        'width': width,
        'height': height,
        'mode': mode
    })


@app.route('/get_image/<filename>')
def get_image(filename):
    """获取上传的图片（用于预览）"""
    return send_from_directory(UPLOAD_DIR, filename)


@app.route('/crop', methods=['POST'])
def crop_image():
    """执行裁剪操作"""
    data = request.json
    filename = data.get('filename')
    x = int(data.get('x', 0))
    y = int(data.get('y', 0))
    width = int(data.get('width', 100))
    height = int(data.get('height', 100))

    if not filename:
        return jsonify({'error': '未指定图片文件'}), 400

    temp_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(temp_path):
        return jsonify({'error': '图片文件不存在'}), 400

    try:
        # 打开图片并裁剪
        with Image.open(temp_path) as img:
            # 确保裁剪区域在图片范围内
            img_width, img_height = img.size
            x = max(0, min(x, img_width - width))
            y = max(0, min(y, img_height - height))
            width = min(width, img_width - x)
            height = min(height, img_height - y)

            # 裁剪
            cropped = img.crop((x, y, x + width, y + height))

            # 生成输出文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            original_name = os.path.splitext(filename)[0].replace('temp_', '')
            output_filename = f"{original_name}_crop_{timestamp}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            # 无损保存为PNG
            cropped.save(output_path, 'PNG', optimize=False)

            # 获取裁剪后图片大小
            output_size = os.path.getsize(output_path)

            return jsonify({
                'success': True,
                'output_filename': output_filename,
                'output_path': output_path,
                'crop_x': x,
                'crop_y': y,
                'crop_width': width,
                'crop_height': height,
                'file_size': output_size
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_image(filename):
    """下载裁剪后的图片"""
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


@app.route('/list_outputs', methods=['GET'])
def list_outputs():
    """列出所有裁剪输出的文件"""
    try:
        files = []
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                filepath = os.path.join(OUTPUT_DIR, filename)
                stat = os.stat(filepath)
                files.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                })
        # 按创建时间倒序排列
        files.sort(key=lambda x: x['created'], reverse=True)
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clear_outputs', methods=['POST'])
def clear_outputs():
    """清空输出目录"""
    try:
        for filename in os.listdir(OUTPUT_DIR):
            filepath = os.path.join(OUTPUT_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
        return jsonify({'success': True, 'message': f'已清空 {len(os.listdir(OUTPUT_DIR))} 个文件'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("图片裁剪工具")
    print("=" * 50)
    print(f"请访问: http://localhost:5000")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 50)
    app.run(host='127.0.0.1', port=5000, debug=True)
