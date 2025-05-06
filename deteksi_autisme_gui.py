import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Define global variables
gejala = [
    ('g1', 'Anak tidak melihat ke arah sesuatu yang orang tua atau orang lain tunjuk'),
    ('g2', 'Orang tua pernah berpikir bahwa anaknya tuli'),
    ('g3', 'Anak tidak pernah bermain pura-pura (misalnya pura-pura berbicara menggunakan telepon atau menyuapi boneka)'),
    ('g4', 'Anak tidak pernah menaiki benda-benda (misalnya furniture, alat-alat bermain atau tangga)'),
    ('g5', 'Anak suka menggerakkan jari-jari tangannya dengan cara yang aneh di dekat matanya'),
    ('g6', 'Anak tidak pernah menunjuk dengan satu jari untuk meminta sesuatu atau meminta tolong'),
    ('g7', 'Anak tidak pernah menunjuk dengan satu jari untuk menunjukkan sesuatu yang menarik kepada orang tua'),
    ('g8', 'Anak tidak tertarik pada anak lainnya'),
    ('g9', 'Anak tidak pernah memperlihatkan suatu benda dengan membawanya atau mengangkatnya untuk orang tua'),
    ('g10', 'Anak tidak memberikan respon ketika namanya dipanggil'),
    ('g11', 'Anak tidak tersenyum balik ketika orang tua atau orang lain tersenyum kepadanya'),
    ('g12', 'Anak menjadi marah atau terganggu ketika mendengar suara bising'),
    ('g13', 'Anak tidak bisa berjalan'),
    ('g14', 'Anak tidak menatap mata saat orang tua atau orang lain berbicara kepadanya'),
    ('g15', 'Anak tidak mencoba meniru apa yang dilakukan orang tua atau orang lain'),
    ('g16', 'Anak tidak melihat sekeliling untuk melihat apa yang sedang dilihat ketika orang tua melihat sesuatu'),
    ('g17', 'Anak tidak mencoba untuk membuat orang tua melihat kepadanya'),
    ('g18', 'Anak tidak mengerti saat orang tua memintanya melakukan sesuatu'),
    ('g19', 'Anak tidak menatap wajah orang tua atau orang lain ketika sesuatau yang baru terjadi'),
    ('g20', 'Anak tidak menyukai aktivitas yang bergerak (misalnya diayun-ayun atau dihentak-hentakkan pada lutut)')
]

resiko = {
    'rendah': ('Resiko Rendah', 'Tidak ada tindak lanjutan yang diperlukan, selain pengamatan untuk mengidentifikasi autisme. Jika anak di bawah 24 bulan, maka pemeriksaan dapat diulang lagi pada usia yang lebih tua, untuk mendapatkan data yang stabil.'),
    'medium': ('Resiko Medium', 'Perlu dilakukan wawancara tindak lanjut dengan psikolog.'),
    'tinggi': ('Resiko Tinggi', 'Anak beresiko tinggi mengalami gangguan autisme atau hambatan perkembangan lainnya. Anak harus segera dirujuk ke klinik tumbuh kembang anak, psikolog anak atau dokter spesialis anak.')
}

check_vars = {}  
name_entry = None  
age_entry = None  

def validate_inputs():
    """Validate user inputs for name and age"""
    # Validate name
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Nama anak harus diisi!")
        return False
    
    # Validate age
    try:
        age = int(age_entry.get().strip())
        if age <= 0:
            messagebox.showerror("Error", "Usia anak harus lebih dari 0 bulan!")
            return False
    except ValueError:
        messagebox.showerror("Error", "Usia anak harus berupa angka!")
        return False
    
    return True

def symptoms():
    global symptoms_window, check_vars
    
    if not validate_inputs():
        return
    
    # symptoms window
    symptoms_window = tk.Toplevel(root)
    symptoms_window.title("Pilih Gejala")
    symptoms_window.geometry("800x600")
    symptoms_window.configure(bg="#f0f0f0")
    
    # Header
    header_frame = tk.Frame(symptoms_window, bg="#4682B4", padx=10, pady=10)
    header_frame.pack(fill=tk.X)
    
    header_label = tk.Label(
        header_frame, 
        text=f"Pilih Gejala untuk {name_entry.get().strip()}",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#4682B4"
    )
    header_label.pack()
    
    # Instructions
    instruction_label = tk.Label(
        symptoms_window,
        text="Jawablah pertanyaan berikut dengan mengklik kotak jika gejala tersebut dialami anak:",
        bg="#f0f0f0",
        font=("Arial", 10, "bold"),
        anchor="w",
        padx=10,
        pady=10
    )
    instruction_label.pack(fill=tk.X)
    
    # Create canvas with scrollbar for gejala
    container = tk.Frame(symptoms_window, bg="#f0f0f0")
    container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(container, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    gejala_frame = tk.Frame(canvas, bg="#f0f0f0")
    gejala_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=gejala_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Add Symptom Checkboxes
    for i, (id, desc) in enumerate(gejala):
        if id not in check_vars:
            check_vars[id] = tk.BooleanVar()
        cb = tk.Checkbutton(
            gejala_frame,
            text=desc,
            variable=check_vars[id],
            bg="#f0f0f0",
            anchor="w",
            padx=5,
            pady=3,
            wraplength=650
        )
        cb.grid(row=i, column=0, sticky="w")
    
    # Button Frame
    button_frame = tk.Frame(symptoms_window, bg="#f0f0f0", pady=10)
    button_frame.pack(fill=tk.X)
    
    # Buttons
    diagnose_button = tk.Button(
        button_frame,
        text="Lakukan Diagnosis",
        command=evaluate_results,
        bg="#4682B4",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=5
    )
    diagnose_button.pack(side=tk.LEFT, padx=10)
    
    cancel_button = tk.Button(
        button_frame,
        text="Kembali",
        command=symptoms_window.destroy,
        bg="#808080",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=5
    )
    cancel_button.pack(side=tk.LEFT, padx=10)
    
    reset_symptoms_button = tk.Button(
        button_frame,
        text="Reset Gejala",
        command=lambda: reset_symptoms(),
        bg="#FF6347",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=5
    )
    reset_symptoms_button.pack(side=tk.LEFT, padx=10)
    
    # Center the window
    symptoms_window.update_idletasks()
    width = symptoms_window.winfo_width()
    height = symptoms_window.winfo_height()
    x = (symptoms_window.winfo_screenwidth() // 2) - (width // 2)
    y = (symptoms_window.winfo_screenheight() // 2) - (height // 2)
    symptoms_window.geometry(f'{width}x{height}+{x}+{y}')

def reset_symptoms():
    """Reset all symptom checkboxes"""
    for var in check_vars.values():
        var.set(False)

def evaluate_results():
    """Calculate results and show diagnosis"""
    if not validate_inputs():
        return
    
    # Get data
    nama_anak = name_entry.get().strip()
    umur_anak = int(age_entry.get().strip())
    
    # Calculate score
    total_skor = sum(var.get() for var in check_vars.values())
    
    # Determine risk level
    if total_skor <= 2:
        level_resiko = 'rendah'
    elif total_skor <= 7:
        level_resiko = 'medium'
    else:
        level_resiko = 'tinggi'
    
    # Get detected gejala
    deteksi_gejala = []
    for id, var in check_vars.items():
        if var.get():
            symptom = next((desc for s_id, desc in gejala if s_id == id), None)
            deteksi_gejala.append(symptom)
    
    # Show results
    show_results(level_resiko, deteksi_gejala, nama_anak, umur_anak, total_skor)

def show_results(level_resiko, deteksi_gejala, nama_anak, umur_anak, total_skor):
    """Display results in a new window"""
    # Create a new window for results
    result_window = tk.Toplevel(root)
    result_window.title("Hasil Diagnosis")
    result_window.geometry("600x450")
    result_window.configure(bg="#f0f0f0")
    
    # Header
    tk.Label(
        result_window,
        text=f"Hasil Diagnosis untuk {nama_anak} ({umur_anak} bulan)",
        font=("Arial", 14, "bold"),
        bg="#4682B4",
        fg="white",
        padx=10,
        pady=10
    ).pack(fill=tk.X)
    
    # Age comment
    age_comment = ""
    if umur_anak < 24:
        age_comment = "Anak berusia di bawah 24 bulan, diagnosis mungkin perlu diulang pada usia yang lebih tua."
    elif umur_anak <= 36:
        age_comment = "Anak berusia antara 24-36 bulan, ideal untuk deteksi dini autisme."
    else:
        age_comment = "Anak berusia di atas 36 bulan."
    
    tk.Label(
        result_window,
        text=age_comment,
        font=("Arial", 10, "italic"),
        bg="#f0f0f0",
        padx=10,
        pady=5
    ).pack(fill=tk.X)
    
    # Risk level
    risk_name, risk_solution = resiko[level_resiko]
    
    risk_frame = tk.Frame(result_window, bg="#f0f0f0", padx=10, pady=5)
    risk_frame.pack(fill=tk.X)
    
    tk.Label(
        risk_frame,
        text="Diagnosis:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        anchor="w"
    ).pack(fill=tk.X)
    
    risk_bg_color = "#90EE90" if level_resiko == 'rendah' else "#FFD700" if level_resiko == 'medium' else "#FF6347"
    
    risk_label = tk.Label(
        risk_frame,
        text=risk_name,
        font=("Arial", 12),
        bg=risk_bg_color,
        padx=10,
        pady=5
    )
    risk_label.pack(fill=tk.X, pady=5)
    
    # Solution
    solution_frame = tk.Frame(result_window, bg="#f0f0f0", padx=10, pady=5)
    solution_frame.pack(fill=tk.X)
    
    tk.Label(
        solution_frame,
        text="Solusi:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        anchor="w"
    ).pack(fill=tk.X)
    
    solution_text = scrolledtext.ScrolledText(
        solution_frame,
        wrap=tk.WORD,
        width=40,
        height=5,
        font=("Arial", 11)
    )
    solution_text.insert(tk.INSERT, risk_solution)
    solution_text.configure(state="disabled")
    solution_text.pack(fill=tk.X, pady=5)
    
    # Detected gejala
    if deteksi_gejala:
        gejala_frame = tk.Frame(result_window, bg="#f0f0f0", padx=10, pady=5)
        gejala_frame.pack(fill=tk.BOTH, expand=True)
    
    # Footer note
    tk.Label(
        result_window,
        text="Catatan: diagnosis ini hanya sebagai rujukan awal.\nSilakan konsultasikan dengan dokter spesialis anak atau psikolog untuk diagnosis yang lebih akurat.",
        font=("Arial", 10, "italic"),
        bg="#f0f0f0",
        justify=tk.LEFT,
        padx=10,
        pady=10
    ).pack(fill=tk.X, side=tk.BOTTOM)
    
    # Close button
    tk.Button(
        result_window,
        text="Tutup",
        command=result_window.destroy,
        bg="#4682B4",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=5
    ).pack(pady=10)

def reset_form():
    """Reset all form fields"""
    # Clear inputs
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    
    # Reset checkboxes
    for var in check_vars.values():
        var.set(False)

def create_widgets(root):
    global name_entry, age_entry

    # Header
    header_frame = tk.Frame(root, bg="#4682B4", padx=10, pady=10)
    header_frame.pack(fill=tk.X)
    
    header_label = tk.Label(
        header_frame, 
        text="Sistem Pakar Deteksi Dini Autisme pada Anak",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#4682B4"
    )
    header_label.pack()
    
    # Input Frame
    input_frame = tk.LabelFrame(root, text="Data Anak", padx=20, pady=20, bg="#f0f0f0", font=("Arial", 12))
    input_frame.pack(fill=tk.X, padx=50, pady=30)
    
    # Name
    tk.Label(input_frame, text="Nama Anak:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
    name_entry = tk.Entry(input_frame, width=20, font=("Arial", 12))
    name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10)
    
    # Age
    tk.Label(input_frame, text="Usia Anak (bulan):", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
    age_entry = tk.Entry(input_frame, width=10, font=("Arial", 12))
    age_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=10)
    
    # Buttons Frame
    buttons_frame = tk.Frame(root, bg="#f0f0f0", pady=20)
    buttons_frame.pack(fill=tk.X)
    
    # Continue Button (to symptoms)
    start_button = tk.Button(
        buttons_frame,
        text="Mulai",
        command=symptoms,
        bg="#4682B4",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=15,
        pady=8
    )
    start_button.pack(side=tk.LEFT, padx=10)
    
    # Reset Button
    reset_button = tk.Button(
        buttons_frame,
        text="Reset",
        command=reset_form,
        bg="#FF6347",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=15,
        pady=8
    )
    reset_button.pack(side=tk.LEFT, padx=10)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistem Pakar Deteksi Dini Autisme pada Anak")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")
    
    create_widgets(root)
    root.mainloop()