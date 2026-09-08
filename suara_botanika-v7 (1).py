import streamlit as st
import time
import os
import uuid

# Set up page configuration
st.set_page_config(
    page_title="SUARA BOTANIKA - Aplikasi Edu-Sains Inklusif",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high contrast, large text, and beautiful child-friendly design
st.markdown("""
<style>
    /* Enlarge fonts for readability */
    html, body, [class*="css"] {
        font-size: 1.15rem;
    }
    .big-font {
        font-size: 1.8rem !important;
        font-weight: bold;
        color: #1E5631;
    }
    .title-text {
        font-size: 2.8rem !important;
        font-weight: 800;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle-text {
        font-size: 1.3rem !important;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Style buttons to be large and touch-friendly for ABK */
    div.stButton > button:first-child {
        font-size: 1.3rem !important;
        height: 3.5em !important;
        width: 100% !important;
        border-radius: 15px !important;
        background-color: #E8F5E9 !important;
        color: #1B5E20 !important;
        border: 3px solid #81C784 !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:first-child:hover {
        background-color: #C8E6C9 !important;
        border-color: #4CAF50 !important;
        transform: scale(1.02);
    }
    
    /* Interactive Card Styling */
    .materi-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #4CAF50;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    .abk-card {
        background-color: #FFF9C4;
        padding: 20px;
        border-radius: 15px;
        border: 3px dashed #FBC02D;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* Highlight container */
    .highlight-box {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #C8E6C9;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to display local image safely without crashing Streamlit
def display_image(image_path, caption="", use_container_width=True):
    if os.path.exists(image_path):
        st.image(image_path, caption=caption, use_container_width=use_container_width)
    else:
        # Try alternate extensions or warn nicely
        base, ext = os.path.splitext(image_path)
        alts = [base + ext.lower(), base + ext.upper(), base + ".jpg", base + ".JPG"]
        for alt in alts:
            if os.path.exists(alt):
                st.image(alt, caption=caption, use_container_width=use_container_width)
                return
        st.warning(f"⚠️ Gambar '{image_path}' tidak ditemukan secara lokal. Silakan pastikan file gambar tersebut diletakkan di dalam folder yang sama dengan file aplikasi ini.")

# -----------------------------------------------------------------------------
# Speech Synthesis (TTS) Helper using browser Javascript
# -----------------------------------------------------------------------------
if 'text_to_speak' not in st.session_state:
    st.session_state.text_to_speak = ""
if 'last_spoken' not in st.session_state:
    st.session_state.last_spoken = ""

def speak(text):
    """Sets the text to be spoken by the browser TTS."""
    st.session_state.text_to_speak = text

# Renders the speech script if there is new text to speak
if st.session_state.text_to_speak and st.session_state.text_to_speak != st.session_state.last_spoken:
    # Use JavaScript SpeechSynthesis to read the text. Language is set to Indonesian ('id-ID')
    js_speech = f"""
    <div style="display:none;">
    <script>
        if ('speechSynthesis' in window) {{
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();
            
            var utterance = new SpeechSynthesisUtterance({repr(st.session_state.text_to_speak)});
            utterance.lang = 'id-ID';
            utterance.rate = 0.85; // Slightly slower speed for kids and ABK
            utterance.pitch = 1.1; // Friendly higher pitch
            
            // Speak
            window.speechSynthesis.speak(utterance);
        }}
    </script>
    </div>
    """
    st.components.v1.html(js_speech, height=0, key=str(uuid.uuid4()))
    st.session_state.last_spoken = st.session_state.text_to_speak

# Function to clear speech state to allow repeating
def repeat_speech():
    st.session_state.last_spoken = ""
    st.rerun()

# -----------------------------------------------------------------------------
# Main Header & Layout
# -----------------------------------------------------------------------------
st.markdown('<div class="title-text">🌱 SUARA BOTANIKA 🌿</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Aplikasi Edu-Sains Inklusif tentang Dunia Tumbuhan & Kearifan Lokal</div>', unsafe_allow_html=True)

# Sidebar with Global Settings
with st.sidebar:
    display_image("daun.JPG", caption="Menu Utama")
    st.markdown("### 🎛️ Panel Kontrol")
    
    # Enable Voice Assistant
    voice_assistant = st.toggle("📢 Aktifkan Asisten Suara (TTS)", value=True)
    if voice_assistant:
        st.info("Asisten Suara Aktif! Setiap Anda menekan tombol bertanda 🔊, laptop akan membacakan teks tersebut secara otomatis.")
    
    st.divider()
    
    # Navigation Buttons (Large and friendly)
    st.markdown("### 🗺️ Jelajah Materi")
    menu = st.radio(
        "Pilih Menu Belajar:",
        [
            "🏠 Beranda & Panduan",
            "🔍 Bagian & Fungsi Tumbuhan",
            "🍃 Jenis-Jenis Organ Tumbuhan",
            "🍳 Dapur Fotosintesis (Game!)",
            "🌸 Perkembangbiakan Tumbuhan",
            "🏺 Kearifan Lokal: Jawa & Gresik",
            "📸 Kamera AI Detektif Daun",
            "📝 Kuis Interaktif Inklusif"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("🧑‍🏫 *Media Pembelajaran Interaktif Kelas IV SD*")

# -----------------------------------------------------------------------------
# Menu 1: Beranda & Panduan
# -----------------------------------------------------------------------------
if menu == "🏠 Beranda & Panduan":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<p class="big-font">Selamat Datang di Suara Botanika! 👋</p>', unsafe_allow_html=True)
        st.write(
            "Halo anak-anak hebat dan bapak-ibu guru profesional! Aplikasi **SUARA BOTANIKA (SUBO-APP)** "
            "adalah aplikasi sains interaktif yang dirancang khusus agar **semua anak bisa belajar bersama**, "
            "termasuk teman-teman kita yang berkebutuhan khusus (ABK) yang belum bisa membaca atau menulis secara fungsional."
        )
        
        # Audio introduction trigger
        intro_text = (
            "Halo anak hebat! Selamat datang di aplikasi Suara Botanika. "
            "Mari belajar tentang bagian tumbuhan, fotosintesis, dan kearifan lokal yang sangat seru! "
            "Kamu bisa menekan tombol-tombol bergambar besar untuk mendengar suaraku dan melihat foto-foto yang nyata. Selamat belajar!"
        )
        
        if st.button("🔊 Putar Suara Sambutan"):
            speak(intro_text)
            
        st.markdown("""
        ### ✨ Keunggulan Utama Aplikasi:
        - **Gambar Nyata & Konkret:** Menggantikan seluruh animasi kartun dengan fotografi nyata berkualitas tinggi agar ramah terhadap pemahaman siswa ABK hambatan intelektual.
        - **Ramah ABK (Inklusif):** Didukung teknologi *Text-to-Speech* (Suara AI) dan navigasi ikonik berukuran besar tanpa ketergantungan membaca-menulis.
        - **Koding & AI:** Mengintegrasikan game logika dapur fotosintesis dan simulasi deteksi kamera AI.
        - **Kearifan Lokal Nusantara:** Memadukan sains biologi tumbuhan dengan kearifan lokal Jawa (**Kue Iwel-Iwel**) dan kearifan lokal Gresik (**Lampion Damar Kurung**).
        """)
        
    with col2:
        # Display an illustrative image box
        st.markdown("""
        <div class="abk-card" style="text-align:center;">
            <h3>🌟 Zona Ramah ABK</h3>
            <p style="font-size:3.5rem; margin:10px 0;">👂👁️✋</p>
            <p>Aplikasi ini mengoptimalkan indra <b>Pendengaran (Auditori)</b>, <b>Penglihatan (Visual Nyata)</b>, dan <b>Sentuhan (Taktil)</b> untuk membantu anak-anak belajar secara bermakna.</p>
        </div>
        """, unsafe_allow_html=True)
        display_image("daun.JPG", caption="Semua anak berhak belajar sains dengan gembira!")

# -----------------------------------------------------------------------------
# Menu 2: Bagian & Fungsi Tumbuhan
# -----------------------------------------------------------------------------
elif menu == "🔍 Bagian & Fungsi Tumbuhan":
    st.markdown('<p class="big-font">🔍 Jelajahi Bagian Tubuh Tumbuhan</p>', unsafe_allow_html=True)
    st.write("Ketuk tombol bagian tumbuhan di bawah ini untuk melihat foto nyata dan mendengarkan suaranya!")
    
    # Create Columns for Large buttons
    cols = st.columns(5)
    
    parts_data = {
        "Akar 🌱": {
            "title": "Akar (The Root)",
            "desc": "Akar berada di dalam tanah. Berfungsi menyerap air dan zat hara dari tanah agar tumbuhan tumbuh subur, serta mencengkeram tanah agar tumbuhan kokoh berdiri.",
            "voice": "Halo! Aku Akar. Aku berada di dalam tanah. Tugasku menyerap air dan mengokohkan tanaman agar tidak mudah roboh saat tertiup angin kencang.",
            "image": "akar.JPG"
        },
        "Batang 🪵": {
            "title": "Batang (The Stem)",
            "desc": "Batang tumbuh tegak di atas tanah. Berfungsi menyalurkan air dari akar menuju daun, dan menyalurkan makanan hasil fotosintesis dari daun ke seluruh tubuh tumbuhan.",
            "voice": "Halo! Aku Batang. Aku seperti jalan raya bagi tanaman. Aku mengalirkan air dari bawah ke atas, serta menahan daun dan ranting agar tetap berdiri tegak!",
            "image": "batang.JPG"
        },
        "Daun 🍃": {
            "title": "Daun (The Leaf)",
            "desc": "Daun biasanya berwarna hijau karena memiliki zat klorofil. Berfungsi sebagai tempat memasak makanan (fotosintesis) dan alat pernapasan bagi tumbuhan.",
            "voice": "Halo! Aku Daun. Aku adalah dapur bagi tanaman! Di sinilah aku memasak makanan menggunakan sinar matahari, air, dan karbondioksida.",
            "image": "daun.JPG"
        },
        "Bunga 🌸": {
            "title": "Bunga (The Flower)",
            "desc": "Bunga memiliki warna yang indah untuk menarik serangga. Berfungsi sebagai organ perkembangbiakan generatif agar tumbuhan bisa menghasilkan buah dan biji.",
            "voice": "Halo! Aku Bunga. Aku adalah perhiasan tumbuhan yang sangat cantik! Aku bertugas melakukan penyerbukan agar tanaman bisa melestarikan keturunannya.",
            "image": "penyerbukan dengan bantuan lebah.JPG"
        },
        "Buah 🍎": {
            "title": "Buah & Biji (The Fruit)",
            "desc": "Buah berfungsi sebagai pelindung biji dan cadangan makanan bagi calon tumbuhan baru. Biji yang ditanam kembali akan tumbuh menjadi pohon yang baru.",
            "voice": "Halo! Aku Buah. Di dalam tubuhku, ada biji yang terlindungi dengan aman. Daging buahku yang manis juga biasa dimakan manusia dan hewan!",
            "image": "tunas pisang.JPG"
        }
    }
    
    # Initialize active part
    if "active_part" not in st.session_state:
        st.session_state.active_part = "Akar 🌱"
        
    for i, part in enumerate(parts_data.keys()):
        with cols[i]:
            if st.button(part):
                st.session_state.active_part = part
                speak(parts_data[part]["voice"])
                st.rerun()

    # Display active part information
    active = st.session_state.active_part
    info = parts_data[active]
    
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        # Display real high-quality photo
        display_image(info["image"], caption=f"Foto Nyata: {info['title']}")
        
        # Audio repeat button
        if st.button("🔊 Putar Ulang Suara"):
            speak(info["voice"])
            
    with col2:
        st.markdown(f'<div class="materi-card"><h3>📖 Penjelasan Lengkap</h3><p style="font-size:1.3rem; line-height:1.6;">{info["desc"]}</p></div>', unsafe_allow_html=True)
        
        # Inklusif note
        st.markdown("""
        <div class="abk-card">
            <h4>💡 Catatan Belajar Inklusif (Taktil):</h4>
            <p>Untuk siswa ABK, ajak mereka meraba tumbuhan asli di pot kelas: rasakan serat kasar pada akar, kerasnya kayu batang, tipisnya helai daun, halus kelopak bunga, dan empuknya daging buah asli.</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Menu 3: Jenis-Jenis Organ Tumbuhan
# -----------------------------------------------------------------------------
elif menu == "🍃 Jenis-Jenis Organ Tumbuhan":
    st.markdown('<p class="big-font">🍃 Eksplorasi Variasi Jenis Organ Tumbuhan</p>', unsafe_allow_html=True)
    st.write("Tumbuhan memiliki bentuk organ yang berbeda-beda. Mari pelajari bentuk nyata daun, batang, dan akar!")

    tabs = st.tabs(["🍃 Jenis Daun (Tulang Daun)", "🪵 Jenis Batang", "🌱 Jenis Akar"])
    
    with tabs[0]:
        st.subheader("Bentuk Tulang Daun (Fotografi Nyata)")
        col_daun = st.columns(4)
        
        daun_types = {
            "Menyirip 🍃": {
                "desc": "Tulang daun mirip susunan sirip ikan. Contoh: Daun Pisang (pembungkus iwel-iwel), Daun Jati, Daun Mangga.",
                "voice": "Tulang daun menyirip. Contohnya daun pisang pembungkus kue iwel-iwel, daun jati, dan daun mangga.",
                "image": "daun menyirip.JPG"
            },
            "Menjari 🍁": {
                "desc": "Tulang daun bercabang keluar seperti jari tangan manusia. Contoh: Daun Pepaya, Daun Singkong, Daun Jarak.",
                "voice": "Tulang daun menjari. Contohnya daun pepaya dan daun singkong yang mirip seperti jari tangan kita!",
                "image": "daun menjari.JPG"
            },
            "Melengkung 🍃": {
                "desc": "Tulang daun berupa garis-garis melengkung yang ujungnya menyatu. Contoh: Daun Sirih, Daun Genjer, Daun Kuping Gajah.",
                "voice": "Tulang daun melengkung. Contohnya daun sirih dan daun kuping gajah.",
                "image": "daun melengkung.JPG"
            },
            "Sejajar 🌾": {
                "desc": "Tulang daun sejajar berupa garis-garis lurus dari pangkal ke ujung. Contoh: Daun Pandan, Daun Padi, Daun Tebu, Daun Kelapa (Janur).",
                "voice": "Tulang daun sejajar. Contohnya daun pandan wangi dan daun kelapa atau janur untuk membuat ketupat.",
                "image": "daun sejajar.JPG"
            }
        }
        
        for idx, (k, v) in enumerate(daun_types.items()):
            with col_daun[idx]:
                st.markdown(f"### {k}")
                display_image(v["image"], caption=f"Foto Daun: {k}")
                st.info(v["desc"])
                if st.button(f"🔊 Suara: {k.split(' ')[0]}", key=f"daun_sound_{idx}"):
                    speak(v["voice"])
                    
    with tabs[1]:
        st.subheader("Jenis Batang Tumbuhan (Fotografi Nyata)")
        col_batang = st.columns(3)
        
        batang_types = {
            "Batang Berkayu 🪵": {
                "desc": "Sangat keras karena mengandung kambium kayu. Tumbuh besar dan tinggi. Contoh: Pohon Mangga, Pohon Jati, Pohon Beringin.",
                "voice": "Batang berkayu. Sangat keras dan berumur panjang. Contohnya pohon jati dan pohon mangga.",
                "image": "batang berkayu.JPG"
            },
            "Batang Basah 🌿": {
                "desc": "Lunak, berair, dan mudah dipatahkan. Contoh: Tanaman Bayam, Sawi, Kangkung, Pisang.",
                "voice": "Batang basah. Lunak dan berair banyak. Contohnya bayam, kangkung, dan pohon pisang.",
                "image": "batang basah.JPG"
            },
            "Batang Rumput 🌾": {
                "desc": "Mempunyai ruas-ruas yang jelas dan berongga di dalamnya. Contoh: Padi, Jagung, Rumput Teki, Bambu.",
                "voice": "Batang rumput. Beruas-ruas dan biasanya berongga. Contohnya tanaman padi dan rumput.",
                "image": "batang rumput.JPG"
            }
        }
        
        for idx, (k, v) in enumerate(batang_types.items()):
            with col_batang[idx]:
                st.markdown(f"### {k}")
                display_image(v["image"], caption=f"Foto Batang: {k}")
                st.success(v["desc"])
                if st.button(f"🔊 Suara: {k.split(' ')[1]}", key=f"batang_sound_{idx}"):
                    speak(v["voice"])
                    
    with tabs[2]:
        st.subheader("Jenis Akar Tumbuhan (Fotografi Nyata)")
        col_akar = st.columns(2)
        
        akar_types = {
            "Akar Serabut 🌾": {
                "desc": "Berbentuk serabut halus, ukuran hampir sama besar, keluar dari pangkal batang. Biasanya pada tanaman berkeping satu (monokotil). Contoh: Kelapa, Padi, Jagung, Rumput.",
                "voice": "Akar serabut. Berbentuk seperti helai-helai rambut halus. Contohnya akar rumput, padi, dan pohon kelapa.",
                "image": "akar serabut.JPG"
            },
            "Akar Tunggang 🌳": {
                "desc": "Memiliki akar pokok yang besar bercabang-cabang menjadi akar kecil. Tumbuh menghujam ke dalam tanah. Biasanya pada tanaman berkeping dua (dikotil). Contoh: Mangga, Jambu, Beringin.",
                "voice": "Akar tunggang. Memiliki satu akar pusat yang sangat besar dan kuat menghujam ke bumi. Contohnya pohon mangga dan pohon jambu.",
                "image": "akar tunggang.JPG"
            }
        }
        
        for idx, (k, v) in enumerate(akar_types.items()):
            with col_akar[idx]:
                st.markdown(f"### {k}")
                display_image(v["image"], caption=f"Foto Akar: {k}")
                st.warning(v["desc"])
                if st.button(f"🔊 Suara: {k.split(' ')[1]}", key=f"akar_sound_{idx}"):
                    speak(v["voice"])

# -----------------------------------------------------------------------------
# Menu 4: Dapur Fotosintesis & Video 3D (Game & Video)
# -----------------------------------------------------------------------------
elif menu == "🍳 Dapur Fotosintesis (Game!)":
    st.markdown('<p class="big-font">🍳 Dapur Fotosintesis & Video 3D</p>', unsafe_allow_html=True)
    
    tabs_foto = st.tabs(["💡 Pelajaran & Video 3D", "🎮 Game Masak Fotosintesis"])
    
    with tabs_foto[0]:
        st.subheader("🎥 Video Pembelajaran Fotosintesis")
        
        # Prioritize local uploaded video sources
        video_sources = ["WhatsApp Video 2026-09-08 at 09.13.17.mp4", "Proses Fotosintesis.mp4"]
        video_played = False
        for v_path in video_sources:
            if os.path.exists(v_path):
                st.video(v_path)
                st.success(f"Berhasil memutar video '{v_path}' secara lokal!")
                video_played = True
                break
                
        if not video_played:
            st.warning("⚠️ Berkas video lokal tidak terdeteksi langsung di komputer Anda.")
            st.info("💡 Memutar video animasi pembelajaran fotosintesis interaktif:")
            st.video("https://www.youtube.com/watch?v=sQK3Yr4Sc_k")
            display_image("daun.JPG", caption="Fotosintesis: Sinar matahari menyinari dedaunan hijau")
        
        st.markdown("""
        <div class="materi-card">
            <h3>📖 Narasi Skenario Video Belajar:</h3>
            <p style="font-size:1.15rem; line-height:1.6;">
                <b>Pernahkah kalian bertanya-tanya bagaimana tumbuhan bisa tumbuh besar dan menghasilkan buah yang lezat meskipun mereka tidak punya mulut untuk makan?</b><br><br>
                Rahasianya ada pada proses hebat bernama <b>Fotosintesis</b>! Fotosintesis adalah cara tumbuhan memasak makanannya sendiri di daun menggunakan bantuan matahari. [32]<br><br>
                <b>Bahan resep rahasianya meliputi:</b><br>
                1. <b>Air (H2O)</b> diserap oleh akar dari dalam tanah. [32]<br>
                2. <b>Udara Kotor (Karbon Dioksida - CO2)</b> dihirup oleh daun melalui lubang stomata. [32]<br>
                3. <b>Sinar Matahari</b> ditangkap oleh klorofil atau zat hijau daun. [32]<br>
                4. <b>Klorofil</b> bertindak seperti kompor yang mengubah energi cahaya menjadi energi kimia. [32]<br><br>
                Hasil masakan daun adalah <b>Glukosa/Gula</b> (makanan manis tumbuhan) dan <b>Oksigen (O2)</b> (udara bersih yang dilepaskan ke udara agar kita bisa bernapas segar!). [32]
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔊 Putar Suara Narasi Pelajaran"):
            speak(
                "Pernahkah kalian bertanya-tanya bagaimana tumbuhan bisa tumbuh besar dan menghasilkan buah yang lezat meskipun mereka tidak memiliki mulut untuk makan? "
                "Rahasianya ada pada proses hebat bernama fotosintesis! Fotosintesis adalah cara tumbuhan memasak makanannya sendiri di daun menggunakan bantuan matahari. "
                "Bahan resep rahasianya meliputi: air yang diserap oleh akar dari dalam tanah; udara kotor karbon dioksida yang dihirup oleh daun melalui lubang stomata; "
                "sinar matahari yang ditangkap oleh klorofil atau zat hijau daun; serta klorofil yang bertindak seperti kompor yang mengubah energi cahaya menjadi energi kimia. "
                "Hasil masakan daun adalah glukosa atau gula manis, dan oksigen segar yang kita hirup!"
            )
            
    with tabs_foto[1]:
        st.write("Bantu tumbuhan memasak makanannya! Pilih **4 bahan penting** di bawah ini, lalu ketuk tombol **MASAK!**")
        
        # Session state to track ingredients
        if "bahan_terpilih" not in st.session_state:
            st.session_state.bahan_terpilih = []
            
        bahan_tersedia = {
            "Cahaya Matahari ☀️": {
                "desc": "Sumber energi utama untuk memicu klorofil.",
                "voice": "Cahaya matahari, sumber energi utama untuk memasak.",
                "image": "daun.JPG"
            },
            "Air (H2O) 💧": {
                "desc": "Diserap oleh akar dari dalam tanah.",
                "voice": "Air, diserap oleh akar untuk dikirim ke daun.",
                "image": "air.JPG"
            },
            "Karbondioksida (CO2) 💨": {
                "desc": "Gas kotor di udara yang dihirup oleh daun.",
                "voice": "Karbondioksida, udara kotor yang disaring oleh daun.",
                "image": "karbondioksida.JPG"
            },
            "Klorofil (Zat Hijau Daun) 🟢": {
                "desc": "Zat hijau yang bertindak sebagai kompor daun.",
                "voice": "Klorofil, zat hijau daun tempat terjadinya pengolahan makanan.",
                "image": "klorofil.JPG"
            },
            "Kue Iwel-Iwel 🍽️": {
                "desc": "Makanan manusia, bukan bahan fotosintesis!",
                "voice": "Aduh, kue iwel-iwel itu makanan kita yang lezat, bukan bahan fotosintesis tanaman ya!",
                "image": "kue uwel iwel.JPG"
            },
            "Sampah Plastik 🗑️": {
                "desc": "Dapat merusak lingkungan dan menghambat pertumbuhan.",
                "voice": "Aduh! Sampah plastik merusak lingkungan, jangan dimasukkan ke daun.",
                "image": "sampak plastik.JPG"
            }
        }
        
        # Display Selection Grid
        cols = st.columns(3)
        for idx, (nama, info) in enumerate(bahan_tersedia.items()):
            col_idx = idx % 3
            with cols[col_idx]:
                display_image(info["image"], caption=nama)
                st.markdown(f"""
                <div style='background-color:#F5F5F5; padding:15px; border-radius:10px; margin-bottom:10px; border: 1px solid #DDD;'>
                    <strong>{nama}</strong><br><small>{info['desc']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Button to Add/Remove
                if nama in st.session_state.bahan_terpilih:
                    if st.button(f"❌ Lepas {nama.split(' ')[0]}", key=f"btn_remove_{idx}"):
                        st.session_state.bahan_terpilih.remove(nama)
                        st.rerun()
                else:
                    if st.button(f"➕ Masukkan {nama.split(' ')[0]}", key=f"btn_add_{idx}"):
                        st.session_state.bahan_terpilih.append(nama)
                        speak(info["voice"])
                        st.rerun()
                        
        # Show status
        st.divider()
        st.markdown("### 🧺 Keranjang Dapur Daun:")
        if len(st.session_state.bahan_terpilih) == 0:
            st.warning("Keranjang masih kosong! Pilih bahan di atas.")
        else:
            st.success(", ".join(st.session_state.bahan_terpilih))
            
        # Reset Button
        if st.button("🔄 Kosongkan Keranjang"):
            st.session_state.bahan_terpilih = []
            speak("Keranjang dikosongkan. Silakan pilih bahan lagi!")
            st.rerun()
            
        # Cook Button
        if st.button("🔥 MASAK SEKARANG!"):
            # Check correct ingredients
            kunci_bahan = ["Cahaya Matahari ☀️", "Air (H2O) 💧", "Karbondioksida (CO2) 💨", "Klorofil (Zat Hijau Daun) 🟢"]
            terpilih = st.session_state.bahan_terpilih
            
            # Check logic
            if len(terpilih) == 4 and all(x in terpilih for x in kunci_bahan):
                st.balloons()
                st.markdown("""
                <div style="background-color:#E8F5E9; padding:25px; border-radius:15px; border: 4px solid #4CAF50; text-align:center;">
                    <h2 style="color:#2E7D32;">🎉 SELAMAT! FOTOSINTESIS BERHASIL! 🌳</h2>
                    <p style="font-size:1.3rem;">Tumbuhanmu berhasil mengolah bahan makanan dengan sempurna! Proses ini menghasilkan:</p>
                    <div style="display:flex; justify-content:space-around; margin-top:15px;">
                        <div class="highlight-box"><h3>💨 Oksigen (O2)</h3><p>Dilepaskan ke udara agar kita bisa bernapas segar!</p></div>
                        <div class="highlight-box"><h3>🍞 Glukosa (Karbohidrat)</h3><p>Makanan manis untuk pertumbuhan tanaman itu sendiri!</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                speak(
                    "Selamat! Proses fotosintesis berhasil dengan sempurna. "
                    "Daun telah memasak makanan menggunakan cahaya matahari, air, karbondioksida, dan klorofil. "
                    "Hore! Sekarang dihasilkan oksigen segar untuk kita bernapas dan makanan manis berupa glukosa untuk tumbuhan."
                )
            else:
                st.error("Waduh, hasil masakan gagal! Periksa kembali bahan masakanmu di keranjang.")
                
                # Provide clue depending on errors
                if any(x in terpilih for x in ["Kue Iwel-Iwel 🍽️", "Sampah Plastik 🗑️"]):
                    clue = "Ada bahan penyusup yang bukan bahan masakan daun! Keluarkan Kue Iwel-Iwel atau Sampah Plastik ya."
                elif len(terpilih) < 4:
                    clue = f"Bahanmu masih kurang! Baru ada {len(terpilih)} bahan. Harus pas ada 4 bahan utama."
                else:
                    clue = "Bahan yang kamu pilih salah. Pastikan kamu memilih Matahari, Air, Udara Karbondioksida, dan Klorofil daun."
                    
                st.info(clue)
                speak("Waduh, proses memasak gagal. " + clue)

# -----------------------------------------------------------------------------
# Menu 5: Perkembangbiakan Tumbuhan
# -----------------------------------------------------------------------------
elif menu == "🌸 Perkembangbiakan Tumbuhan":
    st.markdown('<p class="big-font">🌸 Perkembangbiakan Tumbuhan (Fotografi Nyata)</p>', unsafe_allow_html=True)
    st.write("Bagaimana cara tumbuhan berkembang biak menjadi banyak? Pilih jenisnya untuk dipelajari!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="materi-card" style="border-left-color: #E91E63;">
            <h3 style="color:#E91E63;">🧬 Perkembangbiakan Vegetatif (Tanpa Kawin)</h3>
            <p>Tumbuhan baru berasal dari bagian tubuh induknya sendiri (tanpa penyerbukan).</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sub-menu Vegetatif
        veg_choice = st.selectbox(
            "Pilih Metode Vegetatif:",
            [
                "Tunas (Contoh: Pisang)",
                "Geragih / Stolon (Contoh: Stroberi)",
                "Spora (Contoh: Tanaman Paku)",
                "Cangkok (Vegetatif Buatan Manusia)"
            ]
        )
        
        veg_data = {
            "Tunas (Contoh: Pisang)": {
                "desc": "Tunas baru tumbuh di dekat induknya di bawah tanah dan membesar menjadi pohon baru. Contoh: pohon pisang dan bambu.",
                "voice": "Perkembangbiakan vegetatif dengan tunas. Contohnya adalah pohon pisang dan bambu. Tunas baru muncul dari dalam tanah dekat induknya.",
                "image": "tunas pisang.JPG"
            },
            "Geragih / Stolon (Contoh: Stroberi)": {
                "desc": "Batang yang menjalar di atas permukaan tanah. Di ruas-ruas batang tersebut akan tumbuh akar dan tunas tanaman baru. Contoh: Stroberi, Pegagan.",
                "voice": "Perkembangbiakan vegetatif dengan geragih atau stolon. Batang menjalar di atas tanah dan tumbuh akar baru. Contohnya stroberi.",
                "image": "daun.JPG"
            },
            "Spora (Contoh: Tanaman Paku)": {
                "desc": "Kotak spora yang terletak di bawah daun akan mengepak, dan spora yang terbawa angin akan tumbuh di tempat baru yang lembap. Contoh: Tanaman paku, lumut.",
                "voice": "Perkembangbiakan vegetatif dengan spora. Butiran spora sangat kecil diterbangkan angin dan tumbuh di tempat lembap. Contohnya tanaman paku dan lumut.",
                "image": "daun melengkung.JPG"
            },
            "Cangkok (Vegetatif Buatan Manusia)": {
                "desc": "Manusia mengupas kulit dahan kayu, dibalut tanah, dan dibungkus sabut kelapa/plastik sampai tumbuh akar baru untuk ditanam. Contoh: Mangga, Jambu.",
                "voice": "Perkembangbiakan vegetatif buatan dengan mencangkok. Dibantu manusia dengan menumbuhkan akar di dahan pohon berkambium. Contohnya pohon mangga.",
                "image": "batang.JPG"
            }
        }
        
        display_image(veg_data[veg_choice]["image"], caption=f"Foto: {veg_choice}")
        st.write(veg_data[veg_choice]["desc"])
        if st.button("🔊 Putar Suara Vegetatif"):
            speak(veg_data[veg_choice]["voice"])
            
    with col2:
        st.markdown("""
        <div class="materi-card" style="border-left-color: #9C27B0;">
            <h3 style="color:#9C27B0;">🐝 Perkembangbiakan Generatif (Kawin)</h3>
            <p>Terjadi melalui penyerbukan (bertemunya serbuk sari jantan dan putik betina) dibantu serangga, angin, atau manusia.</p>
        </div>
        """, unsafe_allow_html=True)
        
        gen_choice = st.selectbox(
            "Pilih Proses Generatif:",
            [
                "Penyerbukan oleh Lebah",
                "Penyerbukan oleh Angin",
                "Bagian Alat Kelamin Bunga"
            ]
        )
        
        gen_data = {
            "Penyerbukan oleh Lebah": {
                "desc": "Lebah yang mencari nektar manis tidak sengaja menempelkan serbuk sari dari benang sari ke kepala putik bunga. Ini adalah simbiosis mutualisme!",
                "voice": "Penyerbukan dibantu hewan seperti lebah dan kupu-kupu. Kaki mereka membawa serbuk sari ke kepala putik saat menghisap madu.",
                "image": "penyerbukan dengan bantuan lebah.JPG"
            },
            "Penyerbukan oleh Angin": {
                "desc": "Serbuk sari yang ringan ditiup angin kencang dan mendarat di kepala putik bunga lain yang searah angin. Contoh: Jagung, Padi, Rumput.",
                "voice": "Penyerbukan dibantu angin. Serbuk sari yang ringan terbang ditiup angin lalu mendarat di kepala putik bunga lain. Contohnya tanaman jagung dan padi.",
                "image": "daun sejajar.JPG"
            },
            "Bagian Alat Kelamin Bunga": {
                "desc": "Benang Sari adalah alat kelamin jantan (menghasilkan serbuk sari), sedangkan Putik adalah alat kelamin betina bagi bunga.",
                "voice": "Alat kelamin jantan bunga disebut benang sari yang menghasilkan debu serbuk sari. Sedangkan alat kelamin betina bunga disebut putik.",
                "image": "penyerbukan dengan bantuan lebah.JPG"
            }
        }
        
        display_image(gen_data[gen_choice]["image"], caption=f"Foto: {gen_choice}")
        st.write(gen_data[gen_choice]["desc"])
        if st.button("🔊 Putar Suara Generatif"):
            speak(gen_data[gen_choice]["voice"])

# -----------------------------------------------------------------------------
# Menu 6: Kearifan Lokal (Kue Iwel-Iwel & Damar Kurung)
# -----------------------------------------------------------------------------
elif menu == "🏺 Kearifan Lokal: Jawa & Gresik":
    st.markdown('<p class="big-font">🏺 Kearifan Lokal & Hubungan Sains Tumbuhan</p>', unsafe_allow_html=True)
    st.write("Belajar sains menjadi sangat bermakna ketika dihubungkan dengan adat istiadat dan kearifan lokal di sekitar kita.")
    
    tabs_lokal = st.tabs(["🍽️ Tradisi Kue Iwel-Iwel Jawa", "🏮 Lampion Damar Kurung Gresik"])
    
    with tabs_lokal[0]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Kue Iwel-Iwel dan Daun Pisang 🍽️
            Dalam adat tradisional Jawa, khususnya tradisi **Slametan 7 Bulanan (Tingkeban / Mitoni)** bagi ibu hamil, disajikan makanan khas yang disebut kue **Iwel-Iwel**. [1]
            
            *   **Filosofi:** Nama "iwel-iwel" melambangkan doa kesalehan untuk anak yang dilahirkan (*Ihiwalidaiyya* - doa bakti ke orang tua) agar senantiasa selamat.
            *   **Bahan Kue:** Terbuat dari tepung ketan, parutan kelapa muda, dan gula merah manis di tengahnya.
            *   **Bahan Pembungkus:** Dibungkus rapi menggunakan **Daun Pisang asli** lalu disemat dengan lidi dan dikukus hingga matang sempurna.
            """)
            
            iwel_voice = (
                "Kue iwel-iwel adalah jajanan tradisional Jawa dari ketan dan kelapa yang dibungkus daun pisang. "
                "Kue ini disajikan pada tradisi slametan tujuh bulanan bayi dalam kandungan sebagai tanda syukur dan doa agar bayi lahir selamat."
            )
            
            if st.button("🔊 Putar Suara Filosofi Iwel-Iwel"):
                speak(iwel_voice)
                
            st.markdown("""
            ### 🧪 Mengapa Harus Daun Pisang? (Hubungan Sains)
            1. **Struktur Daun (Menyirip):** Memudahkan daun dilipat membentuk tumpeng kecil tanpa sobek karena kelenturan seratnya.
            2. **Sifat Fisik Lilin (Kutikula):** Permukaan daun pisang dilapisi lilin alami yang mencegah kue lengket pada pembungkusnya saat dikukus panas.
            3. **Aroma Khas:** Suhu kukusan memicu keluarnya minyak esensial alami dari daun yang memberi aroma harum yang lezat pada kue iwel-iwel.
            """)
            
        with col2:
            display_image("iwel-iwel.JPG", caption="Kue Tradisional dibungkus Daun Pisang Nyata")
            st.markdown("""
            <div class="abk-card">
                <h3 style="text-align:center;">👩‍🍳 Ayo Mencoba!</h3>
                <p style="font-size:1.1rem; line-height:1.5;">
                Rasakan aroma daun pisang segar yang dikukus di kelas bersama bapak-ibu guru. <br><br>
                Ajak anak-anak melatih motorik halus dengan melipat daun pisang replika kue iwel-iwel di meja masing-masing!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
    with tabs_lokal[1]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Lampion Damar Kurung khas Gresik 🏮
            **Damar Kurung** adalah lampion kayu berbentuk kubus dengan dinding kertas yang dilukis indah, menceritakan adat istiadat, festival, dan kehidupan rakyat Kabupaten Gresik, Jawa Timur. Lampion bersejarah ini dipopulerkan oleh seniman legendaris perempuan, **Mbah Masmundari**.
            
            *   **Filosofi:** Damar Kurung melambangkan penerangan kehidupan dan sarana penyebaran pesan kebajikan serta keceriaan rakyat Gresik saat menyambut malam Lailatul Qadar di bulan Ramadan.
            *   **Hubungan Erat dengan Anatomi Tumbuhan (Sains):**
                1.  **Kerangka Lampion (Batang Rumput Bambu):** Dibuat menggunakan rajutan bilah bambu tipis. Bambu adalah tumbuhan berkeping satu dengan struktur **batang rumput (beruas-ruas and berongga)** yang sangat kuat namun elastis untuk dirangkai menjadi kubus.
                2.  **Dinding Lampion (Serat Selulosa Tumbuhan):** Menggunakan kertas putih tipis yang diolah dari bubur serat kayu tumbuhan (selulosa). Kertas ini menyebarkan cahaya lilin/lampu secara merata.
                3.  **Energi Bahan Bakar (Buah Kelapa):** Secara tradisional, Damar Kurung menyala menggunakan lampu minyak yang memanfaatkan minyak kelapa (diperas dari daging buah kelapa).
            """)
            
            damar_voice = (
                "Damar Kurung adalah lampion kayu tradisional khas Kabupaten Gresik yang dihiasi lukisan kertas siluet kehidupan warga pesisir. "
                "Kerangka lentera ini dibuat dari bambu, tumbuhan berbatang rumput yang lentur dan kuat, serta dindingnya menggunakan kertas dari serat selulosa tumbuhan."
            )
            
            if st.button("🔊 Putar Suara Filosofi Damar Kurung"):
                speak(damar_voice)
                
        with col2:
            display_image("damarkurung.JPG", caption="Lampion Tradisional Damar Kurung yang bersinar indah")
            st.markdown("""
            <div class="abk-card">
                <h3 style="text-align:center;">🏮 Zona Kreativitas</h3>
                <p style="font-size:1.1rem; line-height:1.5;">
                Cobalah meraba bilah kayu/bambu kerangka lampion Damar Kurung di kelas. <br><br>
                Ajak siswa menggambar struktur daun pisang, daun pepaya, and buah kelapa pada kertas lampion buatan mereka sendiri sebagai aplikasi sains seni terpadu!
                </p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Menu 7: Kamera AI Detektif Daun
# -----------------------------------------------------------------------------
elif menu == "📸 Kamera AI Detektif Daun":
    st.markdown('<p class="big-font">📸 Simulasi AI Detektif Daun</p>', unsafe_allow_html=True)
    st.write("Ayo bantu detektif AI mendeteksi bentuk tulang daun tumbuhan di sekitarmu!")
    
    # Selection of Leaf to Scan
    st.markdown("### 🔍 Pilih Jenis Daun yang Ingin Kamu Pindai (Scan):")
    leaf_to_scan = st.selectbox(
        "Pilihlah daun asli yang sudah kamu ambil dari kebun sekolah:",
        ["Silakan Pilih...", "Daun Pisang (Iwel-iwel)", "Daun Pepaya", "Daun Sirih", "Daun Pandan"]
    )
    
    if leaf_to_scan != "Silakan Pilih...":
        st.write("Menghubungkan kamera ponsel/laptop...")
        
        # Simulate Scanning Progress Bar
        bar = st.progress(0)
        status_text = st.empty()
        
        for percent in range(0, 101, 20):
            status_text.text(f"Detektif AI sedang memindai bentuk tulang daun... {percent}%")
            bar.progress(percent)
            time.sleep(0.3)
            
        st.success("Pemindaian Selesai!")
        
        # Results customized for each leaf
        if leaf_to_scan == "Daun Pisang (Iwel-iwel)":
            st.markdown("""
            <div class="materi-card">
                <h3>🟢 Hasil Deteksi AI Teachable Machine:</h3>
                <p style="font-size:1.4rem; color:#2E7D32;"><strong>Jenis: Daun Pisang (Bentuk Tulang Daun MENYIRIP)</strong></p>
                <p><strong>Rekomendasi Budaya:</strong> Sangat cocok digunakan untuk membungkus kue <strong>Iwel-Iwel</strong> tradisional dalam slametan karena daun lebar, lentur, dan harum.</p>
            </div>
            """, unsafe_allow_html=True)
            speak(
                "Deteksi kecerdasan buatan sukses! Ini adalah daun pisang dengan tulang daun menyirip. "
                "Daun ini sangat cocok digunakan untuk membungkus kue iwel-iwel tradisional dalam acara slametan karena daunnya lebar, lentur, dan harum saat dikukus."
            )
            
        elif leaf_to_scan == "Daun Pepaya":
            st.markdown("""
            <div class="materi-card">
                <h3>🟢 Hasil Deteksi AI Teachable Machine:</h3>
                <p style="font-size:1.4rem; color:#2E7D32;"><strong>Jenis: Daun Pepaya (Bentuk Tulang Daun MENJARI)</strong></p>
                <p><strong>Fakta Unik:</strong> Tulang daunnya bercabang lima seperti jemari tangan kita. Sering diolah menjadi sayur sehat yang kaya vitamin.</p>
            </div>
            """, unsafe_allow_html=True)
            speak(
                "Deteksi kecerdasan buatan sukses! Ini adalah daun pepaya dengan tulang daun menjari. "
                "Tulang daunnya bercabang lima seperti jemari tangan kita. Daun ini kaya vitamin dan sangat sehat!"
            )
            
        elif leaf_to_scan == "Daun Sirih":
            st.markdown("""
            <div class="materi-card">
                <h3>🟢 Hasil Deteksi AI Teachable Machine:</h3>
                <p style="font-size:1.4rem; color:#2E7D32;"><strong>Jenis: Daun Sirih (Bentuk Tulang Daun MELENGKUNG)</strong></p>
                <p><strong>Fakta Unik:</strong> Garis-garis tulang daunnya melengkung indah menuju satu titik. Berfungsi sebagai obat alami pembersih kuman.</p>
            </div>
            """, unsafe_allow_html=True)
            speak(
                "Deteksi kecerdasan buatan sukses! Ini adalah daun sirih dengan tulang daun melengkung. "
                "Garis-garis tulang daunnya melengkung indah menuju satu titik di ujung daun. Daun ini biasa digunakan sebagai obat alami pembunuh kuman."
            )
            
        elif leaf_to_scan == "Daun Pandan":
            st.markdown("""
            <div class="materi-card">
                <h3>🟢 Hasil Deteksi AI Teachable Machine:</h3>
                <p style="font-size:1.4rem; color:#2E7D32;"><strong>Jenis: Daun Pandan (Bentuk Tulang Daun SEJAJAR)</strong></p>
                <p><strong>Fakta Unik:</strong> Tulang daunnya lurus memanjang sejajar satu sama lain. Aromanya sangat wangi, sering digunakan ibu untuk memberi keharuman pada masakan kolak atau nasi.</p>
            </div>
            """, unsafe_allow_html=True)
            speak(
                "Deteksi kecerdasan buatan sukses! Ini adalah daun pandan dengan tulang daun sejajar. "
                "Tulang daunnya lurus memanjang dari pangkal ke ujung. Aromanya sangat wangi dan sering digunakan ibu untuk mengharumkan kolak atau nasi hangat."
            )
            
        # Re-scan button
        if st.button("📸 Pindai Daun Lain"):
            st.rerun()
    else:
        st.info("Pilih salah satu jenis daun di atas untuk memulai simulasi pemindaian AI.")

# -----------------------------------------------------------------------------
# Menu 8: Kuis Interaktif Inklusif
# -----------------------------------------------------------------------------
elif menu == "📝 Kuis Interaktif Inklusif":
    st.markdown('<p class="big-font">📝 SUBO-QUIZ: Kuis Interaktif Inklusif</p>', unsafe_allow_html=True)
    st.write("Kuis ini ramah untuk semua siswa, termasuk siswa berkebutuhan khusus! Gunakan tombol 🔊 untuk mendengarkan pertanyaan.")

    # Initialize score and current question index in session state
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False
    if "quiz_feedback" not in st.session_state:
        st.session_state.quiz_feedback = ""
    if "user_choice" not in st.session_state:
        st.session_state.user_choice = None
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False

    # Define Quiz Questions with Real Uploaded Images
    questions = [
        {
            "no": 1,
            "type": "Materi - Fungsi Akar",
            "question": "Perhatikan gambar akar pohon besar ini. Selain menyerap air dari dalam tanah, apa fungsi utama akar agar tanaman tidak mudah roboh saat tertiup angin kencang?",
            "image": "akar3.JPG",
            "options": [
                "A. Sebagai alat pernapasan utama tumbuhan",
                "B. Menopang dan mencengkeram tanah agar tumbuhan berdiri kokoh",
                "C. Tempat utama pembuatan makanan atau fotosintesis"
            ],
            "correct": "B. Menopang dan mencengkeram tanah agar tumbuhan berdiri kokoh",
            "voice": "Pertanyaan nomor satu. Perhatikan gambar akar pohon besar ini. Selain menyerap air dari dalam tanah, apa fungsi utama akar agar tanaman tidak mudah roboh saat tertiup angin kencang? Pilihan A, sebagai alat pernapasan utama tumbuhan. Pilihan B, menopang dan mencengkeram tanah agar tumbuhan berdiri kokoh. Pilihan C, tempat utama pembuatan makanan atau fotosintesis.",
            "clue": "Akar bertindak sebagai fondasi cakar mencengkeram tanah agar pohon tetap tegak!"
        },
        {
            "no": 2,
            "type": "Penalaran & Budaya Lokal - Daun Pisang",
            "question": "Kue tradisional iwel-iwel dibungkus rapi menggunakan daun pisang sebelum dikukus. Mengapa daun pisang memiliki struktur menyirip dan lapisan lilin alami yang sangat cocok untuk pembungkus makanan?",
            "image": "iwel-iwel.JPG",
            "options": [
                "A. Daun pisang dilapisi lilin alami agar kue tidak lengket saat dikukus dan memberi aroma harum alami",
                "B. Daun pisang mengandung pewarna buatan yang membuat rasa manis iwel-iwel bertambah",
                "C. Daun pisang memiliki duri tajam yang melindungi kue dari serangga"
            ],
            "correct": "A. Daun pisang dilapisi lilin alami agar kue tidak lengket saat dikukus dan memberi aroma harum alami",
            "voice": "Pertanyaan nomor dua. Kue tradisional iwel-iwel dibungkus rapi menggunakan daun pisang sebelum dikukus. Mengapa daun pisang memiliki struktur menyirip dan lapisan lilin alami yang sangat cocok untuk pembungkus makanan? Pilihan A, daun pisang dilapisi lilin alami agar kue tidak lengket saat dikukus dan memberi aroma harum alami. Pilihan B, daun pisang mengandung pewarna buatan yang membuat rasa manis iwel-iwel bertambah. Pilihan C, daun pisang memiliki duri tajam yang melindungi kue dari serangga.",
            "clue": "Lapisan lilin tipis (kutikula) mencegah air rembes dan mencegah adonan ketan lengket."
        },
        {
            "no": 3,
            "type": "Penalaran Sains - Fotosintesis",
            "question": "Dika menyimpan tanaman hiasnya di dalam lemari baju yang gelap gulita selama 2 minggu tanpa ada cahaya sedikit pun. Apa yang akan terjadi pada daun dan tumbuhan tersebut?",
            "image": "klorofil.JPG",
            "options": [
                "A. Daun akan tumbuh berbuah sangat banyak dan subur",
                "B. Daun menguning dan layu karena tidak dapat berfotosintesis (memasak makanan) tanpa adanya energi cahaya matahari",
                "C. Daun tetap hijau segar dan tumbuh tinggi karena terlindungi dari luar"
            ],
            "correct": "B. Daun menguning dan layu karena tidak dapat berfotosintesis (memasak makanan) tanpa adanya energi cahaya matahari",
            "voice": "Pertanyaan nomor tiga. Dika menyimpan tanaman hiasnya di dalam lemari baju yang gelap gulita selama dua minggu tanpa ada cahaya sedikit pun. Apa yang akan terjadi pada daun dan tumbuhan tersebut? Pilihan A, daun akan tumbuh berbuah sangat banyak dan subur. Pilihan B, daun menguning dan layu karena tidak dapat berfotosintesis atau memasak makanan tanpa adanya energi cahaya matahari. Pilihan C, daun tetap hijau segar dan tumbuh tinggi karena terlindungi dari luar.",
            "clue": "Tumbuhan memerlukan sinar matahari sebagai sumber energi klorofil untuk memasak makanan (fotosintesis)."
        },
        {
            "no": 4,
            "type": "Materi - Penyerbukan Generatif",
            "question": "Perhatikan gambar lebah yang hinggap pada bunga indah ini. Bagaimana serangga seperti lebah membantu proses perkembangbiakan generatif (kawin) pada bunga tersebut?",
            "image": "penyerbukan dengan bantuan lebah.JPG",
            "options": [
                "A. Lebah memakan benang sari agar kelopak bunga jatuh ke tanah",
                "B. Kaki lebah tidak sengaja menempelkan serbuk sari (jantan) ke kepala putik (betina) saat mencari madu manis",
                "C. Lebah meniup bunga sehingga biji tanaman terbang terbawa angin"
            ],
            "correct": "B. Kaki lebah tidak sengaja menempelkan serbuk sari (jantan) ke kepala putik (betina) saat mencari madu manis",
            "voice": "Pertanyaan nomor empat. Perhatikan gambar lebah yang hinggap pada bunga indah ini. Bagaimana serangga seperti lebah membantu proses perkembangbiakan generatif atau kawin pada bunga tersebut? Pilihan A, lebah memakan benang sari agar kelopak bunga jatuh ke tanah. Pilihan B, kaki lebah tidak sengaja menempelkan serbuk sari jantan ke kepala putik betina saat mencari madu manis. Pilihan C, lebah meniup bunga sehingga biji tanaman terbang terbawa angin.",
            "clue": "Lebah membawa serbuk sari dari satu bunga ke kepala putik bunga lain secara tidak sengaja ketika mengisap nektar!"
        },
        {
            "no": 5,
            "type": "Penalaran Sains - Struktur Batang",
            "question": "Mengapa batang pohon jati sangat keras dan kokoh untuk dijadikan kayu bangunan, sedangkan tanaman sayur bayam memiliki batang yang lunak dan berair?",
            "image": "batang.JPG",
            "options": [
                "A. Pohon jati memiliki batang berkayu yang mengandung kambium keras, sedangkan bayam memiliki batang basah yang lunak",
                "B. Tanaman bayam tidak menyerap air sehingga batangnya menjadi tipis kering",
                "C. Batang pohon jati dibuat dari batuan padat alami"
            ],
            "correct": "A. Pohon jati memiliki batang berkayu yang mengandung kambium keras, sedangkan bayam memiliki batang basah yang lunak",
            "voice": "Pertanyaan nomor lima. Mengapa batang pohon jati sangat keras dan kokoh untuk dijadikan kayu bangunan, sedangkan tanaman sayur bayam memiliki batang yang lunak dan berair? Pilihan A, pohon jati memiliki batang berkayu yang mengandung kambium keras, sedangkan bayam memiliki batang basah yang lunak. Pilihan B, tanaman bayam tidak menyerap air sehingga batangnya menjadi tipis kering. Pilihan C, batang pohon jati dibuat dari batuan padat alami.",
            "clue": "Kandungan kambium berkayu tebal di pohon jati membuatnya kuat bertahun-tahun, berbeda dengan batang sayur basah."
        }
    ]

    if st.session_state.quiz_finished:
        st.balloons()
        score = st.session_state.quiz_score
        
        # Determine SOLO Taxonomy Category
        if score == 100:
            solo_cat = "🎖️ EXTENDED ABSTRACT (Sangat Baik / Istimewa)"
            solo_desc = "Selamat! Anda memahami konsep bagian tumbuhan secara utuh, dapat melakukan penalaran ilmiah mendalam, serta mampu menghubungkannya dengan kearifan lokal secara kritis."
            solo_voice = "Luar biasa! Skor kamu seratus. Kamu mencapai tingkat Extended Abstract! Kamu memahami seluruh materi tumbuhan dan kearifan lokal secara sempurna!"
        elif score >= 80:
            solo_cat = "🟢 RELATIONAL (Baik)"
            solo_desc = "Bagus sekali! Anda mampu menghubungkan berbagai bagian tumbuhan, fungsi fotosintesis, serta kegunaan praktisnya dalam kehidupan sehari-hari."
            solo_voice = f"Hebat! Skor kamu {score}. Kamu mencapai tingkat Relasional! Kamu dapat menghubungkan bagian tumbuhan dengan kebiasaan di sekitar kita dengan sangat baik!"
        elif score >= 40:
            solo_cat = "🟡 MULTISTRUCTURAL (Cukup)"
            solo_desc = "Cukup baik! Anda memahami bagian-bagian tumbuhan secara terpisah, namun perlu belajar lagi untuk menghubungkan antar-konsep sains secara lebih mendalam."
            solo_voice = f"Bagus! Skor kamu {score}. Ayo terus belajar agar bisa menghubungkan bagian sains secara lebih mendalam!"
        else:
            solo_cat = "🔴 UNISTRUCTURAL / PRE-STRUCTURAL (Perlu Pendampingan)"
            solo_desc = "Anda baru mengenal beberapa bagian tumbuhan secara mendasar. Mari ulangi belajar menggunakan asisten suara di menu sebelumnya!"
            solo_voice = f"Terima kasih sudah mencoba! Skor kamu {score}. Ayo dengarkan penjelasan asisten suara di menu belajar agar lebih hebat!"

        st.markdown(f"""
        <div style="background-color:#E8F5E9; border-radius:15px; padding:30px; border: 4px solid #2E7D32; text-align:center;">
            <h2 style="color:#2E7D32;">🏁 KUIS SELESAI! 🏁</h2>
            <h1 style="font-size:4.5rem; color:#1B5E20; margin:10px 0;">Skor Anda: {score} / 100</h1>
            <div style="background-color:#FFF9C4; padding:15px; border-radius:10px; border: 2px dashed #FBC02D; margin-top:15px;">
                <h3 style="color:#F57F17; margin:0;">Evaluasi Tingkat Pemahaman:</h3>
                <h4 style="color:#D84315; margin:5px 0;">{solo_cat}</h4>
                <p style="color:#3E2723; margin-top:5px; font-size:1.15rem;">{solo_desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔊 Putar Hasil Penilaian"):
            speak(solo_voice)

        if st.button("🔄 Ulangi Kuis"):
            st.session_state.quiz_score = 0
            st.session_state.current_q = 0
            st.session_state.quiz_answered = False
            st.session_state.quiz_finished = False
            st.session_state.user_choice = None
            st.session_state.quiz_feedback = ""
            st.rerun()
    else:
        # Get current question
        current_idx = st.session_state.current_q
        q = questions[current_idx]

        # Header of question
        st.markdown(f'<div class="materi-card"><h3>Pertanyaan {q["no"]} dari 5</h3><p style="font-size:1.1rem; color:#666;">Topik: <strong>{q["type"]}</strong></p></div>', unsafe_allow_html=True)
        
        col_img, col_content = st.columns([1, 1.2])
        
        with col_img:
            # Display real high-quality image from Unsplash
            display_image(q["image"], caption=f"Gambar Nyata: {q['type']}")
            
            # Button for Text-to-Speech
            if st.button("🔊 Putar Suara Pertanyaan & Pilihan"):
                speak(q["voice"])
                
        with col_content:
            st.markdown(f"<h4>❓ {q['question']}</h4>", unsafe_allow_html=True)
            
            # Form or radio button for choice
            choice = st.radio(
                "Pilih jawaban yang menurutmu paling tepat:",
                q["options"],
                key=f"q_radio_{current_idx}",
                index=None if st.session_state.user_choice is None else q["options"].index(st.session_state.user_choice)
            )
            
            if st.button("🔍 Kirim Jawaban", disabled=choice is None or st.session_state.quiz_answered):
                st.session_state.quiz_answered = True
                st.session_state.user_choice = choice
                
                if choice == q["correct"]:
                    st.session_state.quiz_score += 20
                    st.session_state.quiz_feedback = "correct"
                    speak("Hebat! Jawabanmu betul sekali!")
                else:
                    st.session_state.quiz_feedback = "wrong"
                    speak("Aduh, sayang sekali jawabanmu kurang tepat. Jangan menyerah ya!")
                st.rerun()

            # Show Feedback if answered
            if st.session_state.quiz_answered:
                if st.session_state.quiz_feedback == "correct":
                    st.success(f"🎉 **BETUL SEKALI!** Skor bertambah +20.")
                else:
                    st.error(f"❌ **KURANG TEPAT.** Jawaban yang benar adalah: **{q['correct']}**")
                
                st.info(f"💡 **Penjelasan:** {q['clue']}")
                
                # Next Question Button
                if current_idx < len(questions) - 1:
                    if st.button("Berikutnya ➡️"):
                        st.session_state.current_q += 1
                        st.session_state.quiz_answered = False
                        st.session_state.user_choice = None
                        st.session_state.quiz_feedback = ""
                        st.rerun()
                else:
                    if st.button("Lihat Hasil Kuis 🏁"):
                        st.session_state.quiz_finished = True
                        st.rerun()

# -----------------------------------------------------------------------------
# Footnote / Help Instruction
# -----------------------------------------------------------------------------
st.divider()
st.info(
    "💡 **Instruksi Menjalankan Aplikasi:** Simpan file ini dengan nama `suara_botanika.py`, "
    "kemudian jalankan perintah `streamlit run suara_botanika.py` di terminal komputer Anda "
    "untuk membuka aplikasi interaktif ini langsung di web browser secara offline."
)
