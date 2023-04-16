import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD


class DropTarget:
    def __init__(self, widget):
        self.widget = widget
        self.widget.drop_target_register(DND_FILES)
        self.widget.dnd_bind("<<Drop>>", self.drop_event)

    def register_callback(self, callback):
        self.callback = callback

    def drop_event(self, event):
        files = event.widget.dnd_request_filedrop(DND_FILES)
        if len(files) == 1:
            path = files[0]
            if os.path.isdir(path):
                if messagebox.askyesno("移动文件夹", f"是否移动文件夹 '{os.path.basename(path)}' 到项目 '{event.widget['text']}'？"):
                    dest_dir = os.path.join("F:/项目整理", event.widget["text"])
                    if not os.path.exists(dest_dir):
                        os.mkdir(dest_dir)
                    os.rename(path, os.path.join(dest_dir, os.path.basename(path)))
            else:
                res = messagebox.askyesno("创建新项目标签", "是否用文件夹相同名字创建项目标签？")
                if res:
                    new_label = os.path.basename(path)
                    self.callback(new_label)
                    dest_dir = os.path.join("F:/项目整理", new_label)
                    if not os.path.exists(dest_dir):
                        os.mkdir(dest_dir)
                    os.rename(path, os.path.join(dest_dir, os.path.basename(path)))
                else:
                    selected_label = self.select_label()
                    if selected_label:
                        dest_dir = os.path.join("F:/项目整理", selected_label)
                        os.rename(path, os.path.join(dest_dir, os.path.basename(path)))

    def select_label(self):
        label = None
        if len(labels) > 0:
            dialog = tk.Toplevel()
            dialog.title("选择项目标签")
            dialog.geometry("300x150")
            dialog.grab_set()
            label_var = tk.StringVar(value=labels[0])
            label_listbox = tk.Listbox(dialog, listvariable=label_var)
            label_listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
            def on_select(event):
                nonlocal label
                selected = event.widget.get(event.widget.curselection())
                label = selected
                dialog.destroy()
            label_listbox.bind("<<ListboxSelect>>", on_select)
        else:
            messagebox.showerror("错误", "未找到可用项目标签，请先创建标签")
        return label


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x300")
        self.root.title("项目整理")
        self.labels_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.labels_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        self.add_label_btn = tk.Button(self.labels_frame, text="+", command=self.add_label)
        self.add_label_btn.pack(pady=10)
        self.load_labels()
        self.drop_target = DropTarget(self.root)
        self.drop_target.register_callback(self.on_new_label)
        self.root.mainloop()

    def on_new_label(self, new_label):
        if new_label not in labels:
            labels.append(new_label)
