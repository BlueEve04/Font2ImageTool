from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox


def generate_single_char_images(chars, font_path, output_dir, font_color, image_size=(100, 100)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    font_size = 50  # 字体大小
    font = ImageFont.truetype(font_path, font_size)

    for char in chars:
        img = Image.new('RGBA', image_size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        text_bbox = draw.textbbox((0, 0), char, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

        draw.text(position, char, fill=font_color, font=font)

        # 不改会死
        char_map = {':': 'mh', '-': 'fh', '°': 'wd'}
        char = char_map.get(char, char) + '_bl'

        output_path = os.path.join(output_dir, f"{char}.png")
        img.save(output_path)
        print(f"图片已保存：{output_path}")


def start_generation():
    chars = entry_chars.get()
    font_path = filedialog.askopenfilename(title="选择字体文件", filetypes=[("字体文件", "*.ttf")])
    if not font_path:
        messagebox.showwarning("警告", "未选择字体文件！")
        return

    output_dir = filedialog.askdirectory(title="选择输出目录")
    if not output_dir:
        messagebox.showwarning("警告", "未选择输出目录！")
        return

    font_color = colorchooser.askcolor(title="选择字体颜色")[1]
    if not font_color:
        messagebox.showwarning("警告", "未选择字体颜色！")
        return

    try:
        generate_single_char_images(chars, font_path, output_dir, font_color)
        messagebox.showinfo("成功", "图片生成完成！")
    except Exception as e:
        messagebox.showerror("错误", f"图片生成失败：{e}")


# GUI
root = tk.Tk()
root.title("字符图片生成器 - Powererd by BlueEve")
root.geometry("400x300")

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="请输入字符：").grid(row=0, column=0, padx=5, pady=5)
entry_chars = tk.Entry(frame, width=30)
entry_chars.insert(0, "1234567890:°C-")
entry_chars.grid(row=0, column=1, padx=5, pady=5)

btn_generate = tk.Button(root, text="生成图片", command=start_generation, bg="#4CAF50", fg="white")
btn_generate.pack(pady=20)

root.mainloop()
