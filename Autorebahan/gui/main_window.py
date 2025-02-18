import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Autorebahan Pro v2.0")
        self.geometry("1280x800")
        self.configure(bg='#F0F2F5')
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom Style
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=10)
        self.style.configure('Primary.TButton', font=('Segoe UI', 10), background='#0066FF', foreground='white')
        self.style.map('Primary.TButton',
            background=[('active', '#0052CC'), ('disabled', '#E0E0E0')],
            foreground=[('active', 'white'), ('disabled', '#9E9E9E')]
        )
        
        # Context Menu
        self.context_menu = tk.Menu(self, tearoff=0, bg='white', fg='#333333',
                                  activebackground='#0066FF', activeforeground='white')
        self.context_menu.add_command(label="Salin", command=self.copy_text)
        self.context_menu.add_command(label="Tempel", command=self.paste_text)
        
        # Main Container
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Build Tabs
        self.build_scrape_tab()
        self.build_spin_tab()
        
        # Status Bar
        self.status = ttk.Label(self, text="Siap", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def build_scrape_tab(self):
        self.tab_scrape = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_scrape, text=" 📥 Web Scrape ")
        
        # Header
        header_frame = ttk.Frame(self.tab_scrape)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        lbl_url = ttk.Label(header_frame, text="URL Target:", font=('Segoe UI', 10, 'bold'))
        lbl_url.pack(side=tk.LEFT, padx=(0, 5))
        
        self.ent_url = ttk.Entry(header_frame, width=60, font=('Segoe UI', 10))
        self.ent_url.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.ent_url.bind("<Button-3>", self.show_context_menu)
        
        btn_scrape = ttk.Button(header_frame, text="Mulai Scraping", style='Primary.TButton', command=self.on_scrape)
        btn_scrape.pack(side=tk.LEFT, padx=5)
        
        # Result Area
        result_frame = ttk.Frame(self.tab_scrape)
        result_frame.pack(expand=True, fill='both', padx=10, pady=(0, 10))
        
        self.txt_result = tk.Text(result_frame, wrap=tk.WORD, font=('Segoe UI', 10),
                                bg='white', fg='#333333', insertbackground='#0066FF')
        self.txt_result.pack(side=tk.LEFT, expand=True, fill='both')
        
        scroll = ttk.Scrollbar(result_frame, command=self.txt_result.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_result['yscrollcommand'] = scroll.set

    def build_spin_tab(self):
        self.tab_spin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_spin, text=" ✨ Spin Artikel ")
        
        main_frame = ttk.Frame(self.tab_spin)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Input Area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=5)
        
        ttk.Label(input_frame, text="Input Artikel:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.txt_input = tk.Text(input_frame, wrap=tk.WORD, font=('Segoe UI', 10),
                               bg='white', fg='#333333', insertbackground='#0066FF')
        self.txt_input.pack(expand=True, fill='both', pady=5)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(control_frame, text="Pengaturan Spin:", font=('Segoe UI', 10, 'bold')).pack(pady=5)
        
        # Spin Level
        ttk.Label(control_frame, text="Tingkat Spin:").pack(pady=5)
        self.spin_level = ttk.Spinbox(control_frame, from_=0, to=1, increment=0.1, width=5)
        self.spin_level.set(0.7)
        self.spin_level.pack(pady=5)
        
        # Spin Button
        btn_spin = ttk.Button(control_frame, text="Proses Spin", style='Primary.TButton', command=self.on_spin)
        btn_spin.pack(pady=20, ipadx=15)
        
        # Output Area
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=5)
        
        ttk.Label(output_frame, text="Hasil Spin:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.txt_output = tk.Text(output_frame, wrap=tk.WORD, font=('Segoe UI', 10),
                                bg='white', fg='#333333', insertbackground='#0066FF')
        self.txt_output.pack(expand=True, fill='both', pady=5)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def copy_text(self):
        self.clipboard_clear()
        widget = self.focus_get()
        if widget == self.ent_url:
            self.clipboard_append(widget.get())
        elif widget in [self.txt_result, self.txt_input, self.txt_output]:
            text = widget.get("sel.first", "sel.last")
            self.clipboard_append(text)

    def paste_text(self):
        widget = self.focus_get()
        if widget in [self.ent_url, self.txt_result, self.txt_input, self.txt_output]:
            widget.insert(tk.INSERT, self.clipboard_get())

    def on_scrape(self):
        from core.scraper import ContentScraper
        
        url = self.ent_url.get().strip()
        if not url:
            messagebox.showwarning("Peringatan", "Masukkan URL terlebih dahulu!")
            return
            
        self.txt_result.delete(1.0, tk.END)
        self.status.config(text="Memproses scraping...")
        self.update_idletasks()
        
        try:
            scraper = ContentScraper()
            hasil = scraper.scrape_url(url)
            
            if hasil['status'] == 'success':
                self.txt_result.insert(tk.END, f"=== JUDUL ===\n{hasil['title']}\n\n")
                self.txt_result.insert(tk.END, f"=== KONTEN ===\n{hasil['content']}")
                
                # Auto-fill ke spin
                self.notebook.select(self.tab_spin)
                self.txt_input.delete(1.0, tk.END)
                self.txt_input.insert(tk.END, hasil['content'])
                self.txt_input.focus_set()
                
                self.status.config(text="Scraping berhasil! Hasil telah dimuat ke tab Spin")
            else:
                messagebox.showerror("Error", f"Gagal scraping: {hasil['message']}")
                self.status.config(text="Gagal scraping")
                
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            self.status.config(text="Error saat scraping")

    def on_spin(self):
        from core.spinner import ArticleSpinner
        
        input_text = self.txt_input.get(1.0, tk.END).strip()
        if not input_text:
            messagebox.showwarning("Peringatan", "Masukkan teks yang akan di-spin!")
            return
            
        try:
            spin_level = float(self.spin_level.get())
            self.status.config(text="Memproses spinning...")
            self.update_idletasks()
            
            spinner = ArticleSpinner()
            spun_text = spinner.spin_text(input_text, spin_level)
            
            # Tampilkan hasil
            self.txt_output.delete(1.0, tk.END)
            self.txt_output.insert(tk.END, spun_text)
            
            # Hitung kualitas
            quality = spinner.calculate_quality(input_text, spun_text)
            self.status.config(text=f"Spin berhasil! Keunikan: {quality['uniqueness']}% | Struktur: {quality['structure']}% | Kosakata: {quality['vocabulary']}%")
            
        except ValueError:
            messagebox.showerror("Error", "Tingkat spin harus angka antara 0-1!")
            self.status.config(text="Input tidak valid")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal spinning: {str(e)}")
            self.status.config(text="Error saat spinning")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()