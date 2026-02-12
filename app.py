from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sazkiya123"

# ========== DATABASE ==========
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sazkiya_rental_db",
    autocommit=True
)

# ========== FOLDER UPLOAD ==========
UPLOAD_FOLDER = 'static/img/mobil'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========== LOGIN ==========
@app.route("/")
def home():
    if "role" in session:
        if session["role"] == "admin":
            return redirect("/admin")
        return redirect("/user")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email_sazkiya"]
        password = request.form["password_sazkiya"]
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_sazkiya WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["nama"] = user["nama"]
            
            if user["role"] == "admin":
                return redirect("/admin")
            return redirect("/user")
        
        flash("Email atau password salah", "error")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form["nama_sazkiya"]
        email = request.form["email_sazkiya"]
        hp = request.form["hp_sazkiya"]
        password = request.form["password_sazkiya"]
        
        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users_sazkiya (nama, email, hp, password, role, created_at) VALUES (%s, %s, %s, %s, 'user', NOW())",
                (nama, email, hp, password)
            )
            cursor.close()
            flash("Registrasi berhasil!", "success")
            return redirect("/login")
        except:
            flash("Email sudah terdaftar!", "error")
    return render_template("register.html")

# ========== ADMIN DASHBOARD ==========
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM mobil_sazkiya")
    total_mobil = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM users_sazkiya WHERE role='user'")
    total_user = cursor.fetchone()['total']
    cursor.close()
    
    return render_template("admin_dashboard.html", total_mobil=total_mobil, total_user=total_user)

# ========== DATA MOBIL ==========
@app.route('/admin/mobil')
def mobil_list():
    if session.get("role") != "admin":
        return redirect("/login")
    
    search = request.args.get('search', '').strip()
    cursor = db.cursor(dictionary=True)
    
    if search:
        cursor.execute("SELECT * FROM mobil_sazkiya WHERE nama_mobil LIKE %s ORDER BY created_at DESC", (f'%{search}%',))
    else:
        cursor.execute("SELECT * FROM mobil_sazkiya ORDER BY created_at DESC")
    
    mobil = cursor.fetchall()
    cursor.close()
    
    return render_template('admin_mobil.html', mobil=mobil, search_query=search)

# ========== TAMBAH MOBIL ==========
@app.route('/admin/mobil/tambah', methods=["GET", "POST"])
def mobil_tambah():
    if session.get("role") != "admin":
        return redirect("/login")
    
    if request.method == "POST":
        nama = request.form["nama_mobil"]
        harga = request.form["harga"]
        status = request.form["status"]
        gambar = "default.jpg"
        
        file = request.files["gambar"]
        if file and file.filename and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            gambar = f"mobil_{timestamp}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, gambar))
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO mobil_sazkiya (nama_mobil, harga, status, gambar, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (nama, harga, status, gambar)
        )
        cursor.close()
        
        flash("Mobil berhasil ditambahkan!", "success")
        return redirect("/admin/mobil")
    
    return render_template("tambah_mobil.html")

# ========== EDIT MOBIL ==========
@app.route('/admin/mobil/edit/<int:id>', methods=["GET", "POST"])
def mobil_edit(id):
    if session.get("role") != "admin":
        return redirect("/login")
    
    cursor = db.cursor(dictionary=True)
    
    if request.method == "POST":
        nama = request.form["nama_mobil"]
        harga = request.form["harga"]
        status = request.form["status"]
        file = request.files["gambar"]
        
        if file and file.filename and allowed_file(file.filename):
            cursor.execute("SELECT gambar FROM mobil_sazkiya WHERE id=%s", (id,))
            old = cursor.fetchone()
            
            if old and old['gambar'] != "default.jpg":
                old_path = os.path.join(UPLOAD_FOLDER, old['gambar'])
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            ext = file.filename.rsplit('.', 1)[1].lower()
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            gambar = f"mobil_{id}_{timestamp}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, gambar))
            
            cursor.execute(
                "UPDATE mobil_sazkiya SET nama_mobil=%s, harga=%s, status=%s, gambar=%s WHERE id=%s",
                (nama, harga, status, gambar, id)
            )
        else:
            cursor.execute(
                "UPDATE mobil_sazkiya SET nama_mobil=%s, harga=%s, status=%s WHERE id=%s",
                (nama, harga, status, id)
            )
        
        cursor.close()
        flash("Mobil berhasil diupdate!", "success")
        return redirect("/admin/mobil")
    
    cursor.execute("SELECT * FROM mobil_sazkiya WHERE id=%s", (id,))
    mobil = cursor.fetchone()
    cursor.close()
    
    if not mobil:
        flash("Data tidak ditemukan!", "error")
        return redirect("/admin/mobil")
    
    return render_template("edit_mobil.html", mobil=mobil)

# ========== HAPUS MOBIL ==========
@app.route('/admin/mobil/hapus/<int:id>')
def mobil_hapus(id):
    if session.get("role") != "admin":
        return redirect("/login")
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT gambar FROM mobil_sazkiya WHERE id=%s", (id,))
    mobil = cursor.fetchone()
    
    if mobil and mobil['gambar'] != "default.jpg":
        file_path = os.path.join(UPLOAD_FOLDER, mobil['gambar'])
        if os.path.exists(file_path):
            os.remove(file_path)
    
    cursor.execute("DELETE FROM mobil_sazkiya WHERE id=%s", (id,))
    cursor.close()
    
    flash("Mobil berhasil dihapus!", "success")
    return redirect("/admin/mobil")

# ========== USER DASHBOARD ==========
@app.route("/user")
def user():
    if session.get("role") != "user":
        return redirect("/login")
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mobil_sazkiya WHERE status='Tersedia'")
    mobil = cursor.fetchall()
    cursor.close()
    
    return render_template("user_dashboard.html", mobil=mobil, nama=session.get("nama"))

# ========== LOGOUT ==========
@app.route("/logout")
def logout():
    session.clear()
    flash("Berhasil logout!", "success")
    return redirect("/login")

# ========== PROFIL ==========
@app.route('/profil')
def profil():
    data = {
        "nama_perusahaan": "Sazrent",
        "deskripsi": "Sazrent adalah layanan rental kendaraan profesional.",
        "alamat": "Jl. Raya Perusahaan No. 123, Jakarta",
        "telepon": "(021) 1234-5678",
        "whatsapp": "6283194842327",
        "email": "info@sazrent.co.id",
        "tahun_berdiri": "2010",
        "jumlah_armada": "150+"
    }
    return render_template('profil.html', profil=data)

# ========== TESTIMONI ==========
@app.route("/testi")
def testi():
    foto = []
    folder = 'static/testi'
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                foto.append(f)
    return render_template("testi.html", foto=foto)

if __name__ == "__main__":
    app.run(debug=True, port=5000)