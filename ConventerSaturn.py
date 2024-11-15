import os
from tkinter import filedialog, Tk, Label, Button, StringVar, Entry, OptionMenu, Frame, messagebox
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD
from moviepy.editor import VideoFileClip  # Импортируем VideoFileClip


# Полный список поддерживаемых форматов
SUPPORTED_IMAGE_FORMATS = ['jpeg', 'png', 'jpg', 'bmp', 'gif', 'tiff', 'webp']
SUPPORTED_VIDEO_FORMATS = ['webm', 'mp4', 'avi', 'mov', 'mkv']


def convert_image(input_file, output_file):
    try:
        with Image.open(input_file) as img:
            img.save(output_file)
        messagebox.showinfo("Успех", f"Изображение сохранено в: {output_file}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def convert_video(input_file, output_file):
    try:
        clip = VideoFileClip(input_file)  # Загружаем видеофайл
        clip.write_videofile(output_file, codec='libx264', audio_codec='aac')  # Сохраняем в нужном формате
        messagebox.showinfo("Успех", f"Видео сохранено в: {output_file}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def on_select_input():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        input_var.set(file_path)


def on_drop(event):
    input_var.set(event.data)


def convert_image_format():
    input_file = input_var.get()
    output_format = image_output_var.get()

    download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "ConverterSaturn")
    os.makedirs(download_folder, exist_ok=True)

    base_name = os.path.splitext(input_file)[0]
    output_file = os.path.join(download_folder, f"{os.path.basename(base_name)}.{output_format}")

    if any(input_file.lower().endswith(ext) for ext in SUPPORTED_IMAGE_FORMATS):
        convert_image(input_file, output_file)
    else:
        messagebox.showerror("Ошибка", "Неподдерживаемый формат файла.")


def convert_video_format():
    input_file = input_var.get()
    output_format = video_output_var.get()

    download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "ConverterSaturn")
    os.makedirs(download_folder, exist_ok=True)

    base_name = os.path.splitext(input_file)[0]
    output_file = os.path.join(download_folder, f"{os.path.basename(base_name)}.{output_format}")

    if any(input_file.lower().endswith(ext) for ext in SUPPORTED_VIDEO_FORMATS):
        convert_video(input_file, output_file)
    else:
        messagebox.showerror("Ошибка", "Неподдерживаемый формат файла.")


def create_interface():
    root = TkinterDnD.Tk()
    root.title("ConverterSaturn")
    root.geometry("600x300")
    root.configure(bg="#F8F9FA")

    global input_var, image_output_var, video_output_var
    input_var = StringVar()
    image_output_var = StringVar(value='jpg')
    video_output_var = StringVar(value='mp4')
    frame = Frame(root, padx=20, pady=20, bg="#F8F9FA")
    frame.pack(fill='both', expand=True)

    title = Label(frame, text="ConverterSaturn", font=("Helvetica", 24, "bold"), bg="#F8F9FA", fg="#007BFF")
    title.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    Label(frame, text="Выберите файл:", font=("Helvetica", 12), bg="#F8F9FA").grid(row=1, column=0, sticky='e')
    Entry(frame, textvariable=input_var, width=40, font=("Helvetica", 12), bd=2, relief='groove').grid(row=1, column=1, padx=(0, 10), sticky='ew')
    Button(frame, text="Обзор", command=on_select_input, font=("Helvetica", 12), bg="#007BFF", fg="white").grid(row=1, column=2)

    Label(frame, text="Конвертировать изображения в:", font=("Helvetica", 12), bg="#F8F9FA").grid(row=2, column=0, pady=(10, 0), sticky='e')
    OptionMenu(frame, image_output_var, *SUPPORTED_IMAGE_FORMATS).grid(row=2, column=1, padx=(0, 10))
    Button(frame, text="Конвертировать Фото", command=convert_image_format, font=("Helvetica", 12), bg="#28A745", fg="white").grid(row=2, column=2)

    Label(frame, text="Конвертировать видео в:", font=("Helvetica", 12), bg="#F8F9FA").grid(row=3, column=0, pady=(10, 0), sticky='e')
    OptionMenu(frame, video_output_var, *SUPPORTED_VIDEO_FORMATS).grid(row=3, column=1, padx=(0, 10))
    Button(frame, text="Конвертировать Видео", command=convert_video_format, font=("Helvetica", 12), bg="#17A2B8", fg="white").grid(row=3, column=2)

    # Настройка перетаскивания файла
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    frame.columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    create_interface()
