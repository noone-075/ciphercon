import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from .core import create_connection, finish_connection, get_connection, get_public_key, setup


class CipherconGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Ciphercon GUI")
        self.geometry("820x620")
        self.resizable(False, False)
        self.connection = None

        self._build_ui()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook.add(self._build_setup_tab(), text="Setup")
        notebook.add(self._build_create_tab(), text="Create")
        notebook.add(self._build_finish_tab(), text="Finish")
        notebook.add(self._build_connect_tab(), text="Connect")

    def _build_setup_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self)

        if get_public_key():
            ttk.Label(frame, text="RSA keys already exist.").pack(pady=12)
        else:
            button = ttk.Button(frame, text="Generate RSA Keys", command=self._on_setup)
            button.pack(pady=12)

        label = ttk.Label(frame, text="Your public key:")
        label.pack(anchor=tk.W, padx=4)

        self.public_key_text = scrolledtext.ScrolledText(frame, width=96, height=22)
        self.public_key_text.pack(padx=4, pady=4)
        self.public_key_text.configure(state="normal")
        self.public_key_text.insert(tk.END, get_public_key().decode() if get_public_key() else "")
        
        return frame

    def _build_create_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self)

        name_frame = ttk.Frame(frame)
        name_frame.pack(fill=tk.X, padx=4, pady=4)

        ttk.Label(name_frame, text="Connection name:").pack(side=tk.LEFT)
        self.create_name = ttk.Entry(name_frame, width=30)
        self.create_name.pack(side=tk.LEFT, padx=8)

        ttk.Label(frame, text="Other person's public key:").pack(anchor=tk.W, padx=4)
        self.other_public_key_text = scrolledtext.ScrolledText(frame, width=96, height=12)
        self.other_public_key_text.pack(padx=4, pady=4)

        password_frame = ttk.Frame(frame)
        password_frame.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(password_frame, text="Password (optional):").pack(side=tk.LEFT)
        self.create_password = ttk.Entry(password_frame, width=30, show="*")
        self.create_password.pack(side=tk.LEFT, padx=8)

        ttk.Button(frame, text="Create Connection", command=self._on_create_connection).pack(pady=8)

        ttk.Label(frame, text="Encrypted symmetric key to send:").pack(anchor=tk.W, padx=4)
        self.encrypted_key_text = scrolledtext.ScrolledText(frame, width=96, height=10)
        self.encrypted_key_text.pack(padx=4, pady=4)
        self.encrypted_key_text.configure(state="normal")

        return frame

    def _build_finish_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self)

        name_frame = ttk.Frame(frame)
        name_frame.pack(fill=tk.X, padx=4, pady=4)

        ttk.Label(name_frame, text="Connection name:").pack(side=tk.LEFT)
        self.finish_name = ttk.Entry(name_frame, width=30)
        self.finish_name.pack(side=tk.LEFT, padx=8)

        ttk.Label(frame, text="Encrypted symmetric key from peer:").pack(anchor=tk.W, padx=4)
        self.finish_key_text = scrolledtext.ScrolledText(frame, width=96, height=12)
        self.finish_key_text.pack(padx=4, pady=4)

        password_frame = ttk.Frame(frame)
        password_frame.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(password_frame, text="Password (optional):").pack(side=tk.LEFT)
        self.finish_password = ttk.Entry(password_frame, width=30, show="*")
        self.finish_password.pack(side=tk.LEFT, padx=8)

        ttk.Button(frame, text="Finish Connection", command=self._on_finish_connection).pack(pady=8)
        ttk.Label(frame, text="Status:").pack(anchor=tk.W, padx=4)
        self.finish_status = ttk.Label(frame, text="Ready")
        self.finish_status.pack(anchor=tk.W, padx=4)

        return frame

    def _build_connect_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self)

        top_frame = ttk.Frame(frame)
        top_frame.pack(fill=tk.X, padx=4, pady=4)

        ttk.Label(top_frame, text="Connection name:").pack(side=tk.LEFT)
        self.connect_name = ttk.Entry(top_frame, width=24)
        self.connect_name.pack(side=tk.LEFT, padx=8)

        ttk.Label(top_frame, text="Password (optional):").pack(side=tk.LEFT)
        self.connect_password = ttk.Entry(top_frame, width=24, show="*")
        self.connect_password.pack(side=tk.LEFT, padx=8)

        ttk.Button(top_frame, text="Load Connection", command=self._on_load_connection).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame, text="Encrypted / decrypted value:").pack(anchor=tk.W, padx=4)
        self.connect_text = scrolledtext.ScrolledText(frame, width=96, height=12)
        self.connect_text.pack(padx=4, pady=4)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=4, pady=4)

        ttk.Button(button_frame, text="Encrypt Text", command=self._on_encrypt_text).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="Decrypt Text", command=self._on_decrypt_text).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="Encrypt File...", command=self._on_encrypt_file).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="Decrypt File...", command=self._on_decrypt_file).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame, text="Result:").pack(anchor=tk.W, padx=4)
        self.connect_result_text = scrolledtext.ScrolledText(frame, width=96, height=12)
        self.connect_result_text.pack(padx=4, pady=4)
        self.connect_result_text.configure(state="normal")

        return frame

    def _on_setup(self) -> None:
        try:
            setup()
            public_key = get_public_key().decode()
            self.public_key_text.delete("1.0", tk.END)
            self.public_key_text.insert(tk.END, public_key)
            messagebox.showinfo("Ciphercon", "RSA keys generated successfully.")
            self._build_setup_tab() # refresh
        except Exception as exc:
            messagebox.showerror("Ciphercon", f"Unable to generate keys:\n{exc}")

    def _on_create_connection(self) -> None:
        name = self.create_name.get().strip()
        public_key_text = self.other_public_key_text.get("1.0", tk.END).strip()
        password = self.create_password.get().strip() or None

        if not name or not public_key_text:
            messagebox.showwarning("Ciphercon", "Name and public key are required.")
            return

        try:
            conn, encrypted_key = create_connection(name, public_key_text.encode(), password)
            self.encrypted_key_text.delete("1.0", tk.END)
            self.encrypted_key_text.insert(tk.END, encrypted_key.decode())
            messagebox.showinfo("Ciphercon", "Connection created. Share the encrypted key with your peer.")
        except Exception as exc:
            messagebox.showerror("Ciphercon", f"Unable to create connection:\n{exc}")

    def _on_finish_connection(self) -> None:
        name = self.finish_name.get().strip()
        encrypted_key_text = self.finish_key_text.get("1.0", tk.END).strip()
        password = self.finish_password.get().strip() or None

        if not name or not encrypted_key_text:
            messagebox.showwarning("Ciphercon", "Name and encrypted key are required.")
            return

        try:
            finish_connection(name, encrypted_key_text.encode(), password)
            self.finish_status.config(text="Connection finished successfully.")
            messagebox.showinfo("Ciphercon", "Connection finished successfully.")
        except Exception as exc:
            self.finish_status.config(text="Connection failed.")
            messagebox.showerror("Ciphercon", f"Unable to finish connection:\n{exc}")

    def _on_load_connection(self) -> None:
        name = self.connect_name.get().strip()
        password = self.connect_password.get().strip() or None

        if not name:
            messagebox.showwarning("Ciphercon", "Connection name is required.")
            return

        try:
            self.connection = get_connection(name, password)
            self.connect_result_text.delete("1.0", tk.END)
            self.connect_result_text.insert(tk.END, f"Loaded connection '{name}'. You can encrypt or decrypt now.")
        except Exception as exc:
            self.connection = None
            messagebox.showerror("Ciphercon", f"Unable to load connection:\n{exc}")

    def _on_encrypt_text(self) -> None:
        if not self.connection:
            messagebox.showwarning("Ciphercon", "Load a connection first.")
            return

        plaintext = self.connect_text.get("1.0", tk.END).strip().encode()
        if not plaintext:
            messagebox.showwarning("Ciphercon", "Enter text to encrypt.")
            return

        try:
            encrypted = self.connection.encrypt(plaintext)
            self.connect_result_text.delete("1.0", tk.END)
            self.connect_result_text.insert(tk.END, encrypted.decode())
        except Exception as exc:
            messagebox.showerror("Ciphercon", f"Encrypt failed:\n{exc}")

    def _on_decrypt_text(self) -> None:
        if not self.connection:
            messagebox.showwarning("Ciphercon", "Load a connection first.")
            return

        ciphertext = self.connect_text.get("1.0", tk.END).strip().encode()
        if not ciphertext:
            messagebox.showwarning("Ciphercon", "Enter text to decrypt.")
            return

        try:
            decrypted = self.connection.decrypt(ciphertext)
            self.connect_result_text.delete("1.0", tk.END)
            self.connect_result_text.insert(tk.END, decrypted.decode(errors="replace"))
        except Exception as exc:
            messagebox.showerror("Ciphercon", f"Decrypt failed:\n{exc}")

    def _on_encrypt_file(self) -> None:
        if not self.connection:
            messagebox.showwarning("Ciphercon", "Load a connection first.")
            return

        file_path = filedialog.askopenfilename(title="Select file to encrypt")
        if not file_path:
            return

        try:
            data = open(file_path, "rb").read()
            encrypted = self.connection.encrypt(data)
            save_path = filedialog.asksaveasfilename(
                title="Save encrypted file",
                defaultextension=".enc",
                filetypes=[("Encrypted files", "*.enc"), ("All files", "*")],
            )
            if not save_path:
                return

            open(save_path, "wb").write(encrypted)
            messagebox.showinfo("Ciphercon", f"Encrypted file saved to:\n{save_path}")
        except Exception as exc:
            messagebox.showerror("Ciphercon", f"File encryption failed:\n{exc}")

    def _on_decrypt_file(self) -> None:
        if not self.connection:
            messagebox.showwarning("Ciphercon", "Load a connection first.")
            return

        file_path = filedialog.askopenfilename(title="Select file to decrypt")
        if not file_path:
            return

        try:
            data = open(file_path, "rb").read()
            decrypted = self.connection.decrypt(data)
            save_path = filedialog.asksaveasfilename(
                title="Save decrypted file",
                defaultextension=".bin",
                filetypes=[("All files", "*.*")],
            )
            if not save_path:
                return

            open(save_path, "wb").write(decrypted)
            messagebox.showinfo("Ciphercon", f"Decrypted file saved to:\n{save_path}")
        except Exception as exc:
            messagebox.showerror("Ciphercon", f"File decryption failed:\n{exc}")


def main() -> None:
    app = CipherconGUI()
    app.mainloop()
