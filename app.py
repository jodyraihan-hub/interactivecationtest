import streamlit as st

from streamlit_agraph import agraph, Node, Edge, Config

import random

# ============================================
# IMPORT SOAL DARI STORAGE
# ============================================

from quiz_storage import get_random_questions

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Analisis Kation Golongan I, III, IV",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DATA KATION
# ============================================

cation_data = {
    "Golongan I": {
        "label": "Ag⁺, Pb²⁺, Hg₂²⁺",
        "color": "#FF6B6B",
        "reagen": "HCl encer",
        "precipitate": "AgCl (putih), PbCl₂ (putih), Hg₂Cl₂ (putih)",
        "steps": [
            {
                "action": "Tambahkan HCl encer ke sampel",
                "result": "Terbentuk endapan putih: AgCl, PbCl₂, Hg₂Cl₂",
                "filtrate": "Filtrat → Golongan III (setelah skip Golongan II)",
                "residue": "AgCl, PbCl₂, Hg₂Cl₂"
            },
            {
                "action": "Tambahkan H₂O panas pada endapan",
                "result": "PbCl₂ larut, AgCl dan Hg₂Cl₂ tidak larut",
                "filtrate": "Pb²⁺ (larut)",
                "residue": "AgCl, Hg₂Cl₂"
            },
            {
                "action": "Pada filtrat Pb²⁺: Tambahkan K₂CrO₄",
                "result": "Endapan kuning PbCrO₄",
                "confirm": "Pb²⁺ terkonfirmasi ✅"
            },
            {
                "action": "Pada residu AgCl, Hg₂Cl₂: Tambahkan NH₄OH",
                "result": "AgCl larut → [Ag(NH₃)₂]⁺; Hg₂Cl₂ → Hg (hitam) + Hg(NH₂)Cl (putih)",
                "filtrate": "[Ag(NH₃)₂]⁺",
                "residue": "Hg + Hg(NH₂)Cl"
            },
            {
                "action": "Pada filtrat [Ag(NH₃)₂]⁺: Tambahkan HNO₃",
                "result": "Endapan putih AgCl terbentuk kembali",
                "confirm": "Ag⁺ terkonfirmasi ✅"
            }
        ]
    },
    "Golongan III": {
        "label": "Fe³⁺, Al³⁺, Cr³⁺",
        "color": "#4ECDC4",
        "reagen": "NH₄OH berlebih + NH₄Cl",
        "precipitate": "Fe(OH)₃ (coklat), Al(OH)₃ (putih/gel), Cr(OH)₃ (abu-abu/hijau)",
        "steps": [
            {
                "action": "Tambahkan NH₄OH + NH₄Cl pada filtrat",
                "result": "Fe(OH)₃ (coklat), Al(OH)₃ (putih/gel), Cr(OH)₃ (abu-abu) terendap",
                "filtrate": "Filtrat → Golongan IV",
                "residue": "Fe(OH)₃, Al(OH)₃, Cr(OH)₃"
            },
            {
                "action": "Tambahkan NaOH berlebih + H₂O₂ pada endapan",
                "result": "Al(OH)₃ → [Al(OH)₄]⁻, Cr(OH)₃ → CrO₄²⁻ (keduanya larut), Fe(OH)₃ tidak larut",
                "filtrate": "[Al(OH)₄]⁻, CrO₄²⁻",
                "residue": "Fe(OH)₃"
            },
            {
                "action": "Pada residu Fe(OH)₃: Tambahkan HCl + KSCN",
                "result": "Larutan merah darah [Fe(SCN)]²⁺",
                "confirm": "Fe³⁺ terkonfirmasi ✅"
            },
            {
                "action": "Pada filtrat [Al(OH)₄]⁻: Tambahkan HCl perlahan",
                "result": "Endapan putih/gel Al(OH)₃ kembali terbentuk",
                "confirm": "Al³⁺ terkonfirmasi ✅"
            },
            {
                "action": "Pada filtrat CrO₄²⁻: Tambahkan Pb(NO₃)₂",
                "result": "Endapan kuning PbCrO₄",
                "confirm": "Cr³⁺ terkonfirmasi ✅"
            }
        ]
    },
    "Golongan IV": {
        "label": "Ba²⁺, Sr²⁺, Ca²⁺",
        "color": "#FFD93D",
        "reagen": "(NH₄)₂CO₃ + NH₄OH + NH₄Cl",
        "precipitate": "BaCO₃ (putih), SrCO₃ (putih), CaCO₃ (putih)",
        "steps": [
            {
                "action": "Tambahkan (NH₄)₂CO₃ + NH₄OH + NH₄Cl pada filtrat",
                "result": "BaCO₃, SrCO₃, CaCO₃ terendap putih",
                "filtrate": "Filtrat → Golongan V (Mg²⁺, K⁺, Na⁺, NH₄⁺)",
                "residue": "BaCO₃, SrCO₃, CaCO₃"
            },
            {
                "action": "Tambahkan CH₃COOH (asam asetat) pada endapan",
                "result": "Semua karbonat larut menjadi asetat",
                "filtrate": "Ba²⁺, Sr²⁺, Ca²⁺ (sebagai asetat)",
                "residue": "-"
            },
            {
                "action": "Pada larutan asetat: Tambahkan K₂CrO₄",
                "result": "Endapan kuning BaCrO₄, Sr²⁺ dan Ca²⁺ tetap larut",
                "filtrate": "Sr²⁺, Ca²⁺",
                "residue": "BaCrO₄ (kuning)"
            },
            {
                "action": "Pada filtrat Sr²⁺, Ca²⁺: Tambahkan (NH₄)₂SO₄",
                "result": "Endapan putih SrSO₄, Ca²⁺ tetap larut",
                "filtrate": "Ca²⁺",
                "residue": "SrSO₄ (putih)"
            },
            {
                "action": "Pada filtrat Ca²⁺: Tambahkan (NH₄)₂C₂O₄",
                "result": "Endapan putih CaC₂O₄",
                "confirm": "Ca²⁺ terkonfirmasi ✅"
            }
        ]
    }
}

# ============================================
# QUIZ QUESTIONS
# ============================================

quiz_questions = {
    "Golongan I": [
        {
            "question": "Reagen apa yang digunakan untuk mengendapkan kation Golongan I?",
            "options": ["H₂SO₄ encer", "HCl encer", "NH₄OH", "NaOH"],
            "correct": 1,
            "explanation": "HCl encer digunakan karena Ag⁺, Pb²⁺, dan Hg₂²⁺ membentuk garam klorida yang tidak larut."
        },
        {
            "question": "Warna endapan PbCl₂ adalah...",
            "options": ["Kuning", "Hitam", "Putih", "Merah"],
            "correct": 2,
            "explanation": "PbCl₂ membentuk endapan berwarna putih saat bereaksi dengan HCl encer."
        },
        {
            "question": "Bagaimana cara memisahkan Pb²⁺ dari AgCl dan Hg₂Cl₂?",
            "options": ["Tambahkan NH₄OH", "Panaskan dengan air panas", "Tambahkan HNO₃", "Tambahkan NaOH"],
            "correct": 1,
            "explanation": "PbCl₂ larut dalam air panas karena kelarutannya meningkat signifikan dengan suhu, sedangkan AgCl dan Hg₂Cl₂ tetap sebagai endapan."
        },
        {
            "question": "Reagen apa yang digunakan untuk mengkonfirmasi keberadaan Pb²⁺?",
            "options": ["KSCN", "K₂CrO₄", "NH₄OH", "HNO₃"],
            "correct": 1,
            "explanation": "K₂CrO₄ menghasilkan endapan kuning PbCrO₄ yang mengkonfirmasi keberadaan Pb²⁺."
        },
        {
            "question": "Apa yang terjadi pada Hg₂Cl₂ saat ditambahkan NH₄OH?",
            "options": [
                "Larut sempurna",
                "Berubah menjadi endapan kuning",
                "Terbentuk Hg (hitam) + Hg(NH₂)Cl (putih)",
                "Tidak bereaksi"
            ],
            "correct": 2,
            "explanation": "Hg₂Cl₂ mengalami disproporsionasi dengan NH₄OH: Hg₂²⁺ → Hg⁰ (hitam) + Hg²⁺ yang membentuk Hg(NH₂)Cl (putih)."
        },
        {
            "question": "Kompleks apa yang terbentuk saat AgCl dilarutkan dalam NH₄OH?",
            "options": ["Ag(OH)₂⁻", "[Ag(NH₃)₂]⁺", "AgNO₃", "AgCl₂⁻"],
            "correct": 1,
            "explanation": "[Ag(NH₃)₂]⁺ adalah kompleks diamminperak(I) yang larut dalam larutan amonia berlebih."
        },
        {
            "question": "Untuk mengkonfirmasi Ag⁺ setelah pembentukan [Ag(NH₃)₂]⁺, reagen apa yang ditambahkan?",
            "options": ["HCl", "HNO₃", "H₂SO₄", "H₃PO₄"],
            "correct": 1,
            "explanation": "Penambahan HNO₃ mengasidifikasi larutan sehingga AgCl mengendap kembali, mengkonfirmasi keberadaan Ag⁺."
        },
        {
            "question": "Warna endapan PbCrO₄ adalah...",
            "options": ["Putih", "Merah", "Kuning", "Hitam"],
            "correct": 2,
            "explanation": "PbCrO₄ adalah endapan berwarna kuning cerah yang merupakan konfirmasi Pb²⁺."
        },
        {
            "question": "Mengapa PbCl₂ dapat dipisahkan dari AgCl menggunakan air panas?",
            "options": [
                "PbCl₂ lebih berat",
                "PbCl₂ memiliki kelarutan yang meningkat dengan suhu",
                "PbCl₂ bersifat asam",
                "AgCl tidak stabil"
            ],
            "correct": 1,
            "explanation": "Kelarutan PbCl₂ meningkat signifikan dengan suhu (kelarutan endotermik), sehingga larut dalam air panas sedangkan AgCl tetap tidak larut."
        },
        {
            "question": "Kation mana yang TIDAK termasuk dalam Golongan I analisis kation?",
            "options": ["Ag⁺", "Pb²⁺", "Ba²⁺", "Hg₂²⁺"],
            "correct": 2,
            "explanation": "Ba²⁺ termasuk Golongan IV, bukan Golongan I. Golongan I terdiri dari Ag⁺, Pb²⁺, dan Hg₂²⁺."
        }
    ],
    "Golongan III": [
        {
            "question": "Reagen pengendap Golongan III adalah...",
            "options": ["HCl encer", "(NH₄)₂CO₃", "NH₄OH + NH₄Cl", "NaOH + H₂O₂"],
            "correct": 2,
            "explanation": "NH₄OH + NH₄Cl digunakan. NH₄Cl berfungsi sebagai penyangga untuk menekan [OH⁻] agar Mg²⁺ tidak ikut terendap."
        },
        {
            "question": "Warna endapan Fe(OH)₃ adalah...",
            "options": ["Putih", "Kuning", "Coklat/Merah", "Hitam"],
            "correct": 2,
            "explanation": "Fe(OH)₃ membentuk endapan berwarna coklat kemerahan yang khas."
        },
        {
            "question": "Reagen apa yang digunakan untuk mengkonfirmasi Fe³⁺?",
            "options": ["K₂CrO₄", "KSCN", "NH₄OH", "Pb(NO₃)₂"],
            "correct": 1,
            "explanation": "KSCN (kalium tiosianat) menghasilkan warna merah darah [Fe(SCN)]²⁺ yang sangat sensitif untuk Fe³⁺."
        },
        {
            "question": "Fungsi NH₄Cl dalam pengendapan Golongan III adalah...",
            "options": [
                "Meningkatkan pH larutan",
                "Menekan [OH⁻] agar Mg²⁺ tidak terendap",
                "Mengoksidasi Fe²⁺ menjadi Fe³⁺",
                "Melarutkan endapan"
            ],
            "correct": 1,
            "explanation": "NH₄Cl berfungsi sebagai buffer/penyangga yang menekan konsentrasi OH⁻ sehingga Mg(OH)₂ tidak terbentuk pada pH tersebut."
        },
        {
            "question": "Bagaimana Al(OH)₃ dapat dibedakan dari Fe(OH)₃?",
            "options": [
                "Al(OH)₃ berwarna merah",
                "Al(OH)₃ larut dalam NaOH berlebih",
                "Al(OH)₃ mengendap dalam HCl",
                "Al(OH)₃ bereaksi dengan KSCN"
            ],
            "correct": 1,
            "explanation": "Al(OH)₃ bersifat amfoter sehingga larut dalam NaOH berlebih membentuk [Al(OH)₄]⁻, sedangkan Fe(OH)₃ tidak larut dalam basa berlebih."
        },
        {
            "question": "Cr³⁺ dioksidasi menjadi CrO₄²⁻ menggunakan...",
            "options": ["HCl", "H₂O₂ + NaOH berlebih", "NH₄OH", "H₂SO₄"],
            "correct": 1,
            "explanation": "H₂O₂ dalam suasana basa (NaOH berlebih) mengoksidasi Cr³⁺ dari Cr(OH)₃ menjadi CrO₄²⁻ (kromat) yang larut."
        },
        {
            "question": "Warna larutan [Fe(SCN)]²⁺ adalah...",
            "options": ["Kuning", "Biru", "Merah Darah", "Hijau"],
            "correct": 2,
            "explanation": "[Fe(SCN)]²⁺ menghasilkan warna merah darah yang intens, sangat sensitif bahkan pada konsentrasi rendah."
        },
        {
            "question": "Untuk mengkonfirmasi Cr³⁺, filtrat CrO₄²⁻ ditambahkan...",
            "options": ["KSCN", "K₂CrO₄", "Pb(NO₃)₂", "NH₄OH"],
            "correct": 2,
            "explanation": "Pb(NO₃)₂ bereaksi dengan CrO₄²⁻ membentuk endapan kuning PbCrO₄ yang mengkonfirmasi Cr³⁺."
        },
        {
            "question": "Al(OH)₃ dikonfirmasi dengan cara...",
            "options": [
                "Menambahkan KSCN",
                "Menambahkan HCl perlahan pada filtrat [Al(OH)₄]⁻",
                "Memanaskan dengan NaOH",
                "Menambahkan K₂CrO₄"
            ],
            "correct": 1,
            "explanation": "Penambahan HCl perlahan pada [Al(OH)₄]⁻ akan mengendapkan kembali Al(OH)₃ (putih/gel) ketika pH turun ke titik isoelektrik."
        },
        {
            "question": "Kation mana yang TIDAK termasuk Golongan III?",
            "options": ["Fe³⁺", "Al³⁺", "Cr³⁺", "Ca²⁺"],
            "correct": 3,
            "explanation": "Ca²⁺ termasuk Golongan IV, bukan Golongan III. Golongan III terdiri dari Fe³⁺, Al³⁺, dan Cr³⁺."
        }
    ],
    "Golongan IV": [
        {
            "question": "Reagen pengendap Golongan IV adalah...",
            "options": ["HCl encer", "NH₄OH + NH₄Cl", "(NH₄)₂CO₃ + NH₄OH + NH₄Cl", "NaOH"],
            "correct": 2,
            "explanation": "(NH₄)₂CO₃ mengendapkan Ba²⁺, Sr²⁺, Ca²⁺ sebagai karbonat. NH₄OH + NH₄Cl mencegah MgCO₃ ikut terendap."
        },
        {
            "question": "Semua karbonat Golongan IV (BaCO₃, SrCO₃, CaCO₃) dilarutkan dengan...",
            "options": ["HCl pekat", "NaOH", "CH₃COOH (asam asetat)", "H₂SO₄"],
            "correct": 2,
            "explanation": "Asam asetat (CH₃COOH) digunakan untuk melarutkan karbonat menjadi asetat yang larut, tanpa memasukkan anion pengganggu."
        },
        {
            "question": "Bagaimana Ba²⁺ dipisahkan dari Sr²⁺ dan Ca²⁺?",
            "options": [
                "Dengan menambahkan NH₄OH",
                "Dengan menambahkan K₂CrO₄ pada larutan asetat",
                "Dengan pemanasan",
                "Dengan menambahkan NaOH"
            ],
            "correct": 1,
            "explanation": "K₂CrO₄ mengendapkan Ba²⁺ sebagai BaCrO₄ (kuning) di pH netral, sedangkan SrCrO₄ dan CaCrO₄ lebih larut pada kondisi ini."
        },
        {
            "question": "Warna endapan BaCrO₄ adalah...",
            "options": ["Putih", "Kuning", "Merah", "Hitam"],
            "correct": 1,
            "explanation": "BaCrO₄ adalah endapan berwarna kuning yang mengkonfirmasi keberadaan Ba²⁺."
        },
        {
            "question": "Reagen apa yang digunakan untuk memisahkan Sr²⁺ dari Ca²⁺?",
            "options": ["K₂CrO₄", "(NH₄)₂CO₃", "(NH₄)₂SO₄", "(NH₄)₂C₂O₄"],
            "correct": 2,
            "explanation": "(NH₄)₂SO₄ mengendapkan SrSO₄ (putih) sedangkan CaSO₄ lebih larut, sehingga Ca²⁺ tetap dalam larutan."
        },
        {
            "question": "Cara mengkonfirmasi Ca²⁺ adalah dengan menambahkan...",
            "options": ["K₂CrO₄", "(NH₄)₂SO₄", "(NH₄)₂C₂O₄", "KSCN"],
            "correct": 2,
            "explanation": "(NH₄)₂C₂O₄ (ammonium oksalat) mengendapkan Ca²⁺ sebagai CaC₂O₄ (putih) yang mengkonfirmasi keberadaan Ca²⁺."
        },
        {
            "question": "Mengapa NH₄Cl ditambahkan dalam pengendapan Golongan IV?",
            "options": [
                "Mengoksidasi kation",
                "Mencegah pengendapan MgCO₃",
                "Melarutkan endapan",
                "Menaikkan pH"
            ],
            "correct": 1,
            "explanation": "NH₄Cl menekan konsentrasi CO₃²⁻ melalui efek ion bersama pada NH₃/NH₄⁺, sehingga MgCO₃ tidak terendap."
        },
        {
            "question": "Warna endapan SrSO₄ adalah...",
            "options": ["Kuning", "Merah", "Putih", "Abu-abu"],
            "correct": 2,
            "explanation": "SrSO₄ membentuk endapan berwarna putih saat Sr²⁺ bereaksi dengan SO₄²⁻."
        },
        {
            "question": "Kation mana yang TIDAK termasuk Golongan IV?",
            "options": ["Ba²⁺", "Sr²⁺", "Ca²⁺", "Fe³⁺"],
            "correct": 3,
            "explanation": "Fe³⁺ termasuk Golongan III, bukan Golongan IV. Golongan IV terdiri dari Ba²⁺, Sr²⁺, dan Ca²⁺."
        },
        {
            "question": "Warna endapan CaC₂O₄ adalah...",
            "options": ["Kuning", "Putih", "Merah", "Biru"],
            "correct": 1,
            "explanation": "CaC₂O₄ (kalsium oksalat) membentuk endapan putih yang mengkonfirmasi Ca²⁺."
        }
    ]
}

def get_random_questions(group, n=10):
    questions = quiz_questions.get(group, [])
    if len(questions) <= n:
        return random.sample(questions, len(questions))
    return random.sample(questions, n)

# ============================================
# DIGITALISASI KIMIA - DATA
# ============================================

CATION_PROFILES = {
    "Ag⁺": {
        "group": "I",
        "reactions": [
            "Ag⁺ + Cl⁻ → AgCl↓ (Putih)",
            "AgCl + 2NH₃ → [Ag(NH₃)₂]⁺ + Cl⁻",
            "[Ag(NH₃)₂]⁺ + 2H⁺ + Cl⁻ → AgCl↓ (Putih) + 2NH₄⁺"
        ],
        "confirmasi": "Endapan putih AgCl → larut dalam NH₄OH → endapan putih kembali dengan HNO₃",
        "warna_endapan": "Putih",
        "icon": "🥈"
    },
    "Pb²⁺": {
        "group": "I",
        "reactions": [
            "Pb²⁺ + 2Cl⁻ → PbCl₂↓ (Putih)",
            "PbCl₂ → Pb²⁺ + 2Cl⁻  (larut dalam H₂O panas)",
            "Pb²⁺ + CrO₄²⁻ → PbCrO₄↓ (Kuning)"
        ],
        "confirmasi": "Endapan kuning PbCrO₄ setelah penambahan K₂CrO₄",
        "warna_endapan": "Kuning",
        "icon": "🟡"
    },
    "Hg₂²⁺": {
        "group": "I",
        "reactions": [
            "Hg₂²⁺ + 2Cl⁻ → Hg₂Cl₂↓ (Putih)",
            "Hg₂Cl₂ + 2NH₃ → Hg↓ (Hitam) + Hg(NH₂)Cl↓ (Putih) + NH₄⁺ + Cl⁻"
        ],
        "confirmasi": "Endapan hitam Hg dan putih Hg(NH₂)Cl saat ditambahkan NH₄OH",
        "warna_endapan": "Hitam + Putih",
        "icon": "⚫"
    },
    "Fe³⁺": {
        "group": "III",
        "reactions": [
            "Fe³⁺ + 3OH⁻ → Fe(OH)₃↓ (Coklat)",
            "Fe(OH)₃ + 3HCl → FeCl₃ + 3H₂O",
            "Fe³⁺ + SCN⁻ → [Fe(SCN)]²⁺ (Merah Darah)"
        ],
        "confirmasi": "Warna merah darah [Fe(SCN)]²⁺ dengan KSCN",
        "warna_endapan": "Coklat/Merah",
        "icon": "🟤"
    },
    "Al³⁺": {
        "group": "III",
        "reactions": [
            "Al³⁺ + 3OH⁻ → Al(OH)₃↓ (Putih/Gel)",
            "Al(OH)₃ + OH⁻ → [Al(OH)₄]⁻  (larut dalam NaOH berlebih)",
            "[Al(OH)₄]⁻ + H⁺ → Al(OH)₃↓ (Putih)"
        ],
        "confirmasi": "Endapan putih/gel Al(OH)₃ yang larut dalam NaOH berlebih dan mengendap kembali dengan asam",
        "warna_endapan": "Putih/Gel",
        "icon": "⚪"
    },
    "Cr³⁺": {
        "group": "III",
        "reactions": [
            "Cr³⁺ + 3OH⁻ → Cr(OH)₃↓ (Abu-abu/Hijau)",
            "2Cr(OH)₃ + 3H₂O₂ + 4OH⁻ → 2CrO₄²⁻ + 8H₂O",
            "Pb²⁺ + CrO₄²⁻ → PbCrO₄↓ (Kuning)"
        ],
        "confirmasi": "Endapan kuning PbCrO₄ setelah oksidasi Cr(OH)₃ dengan H₂O₂/NaOH",
        "warna_endapan": "Abu-abu/Hijau → Kuning (PbCrO₄)",
        "icon": "🟢"
    },
    "Ba²⁺": {
        "group": "IV",
        "reactions": [
            "Ba²⁺ + CO₃²⁻ → BaCO₃↓ (Putih)",
            "BaCO₃ + 2CH₃COOH → Ba²⁺ + 2CH₃COO⁻ + H₂O + CO₂",
            "Ba²⁺ + CrO₄²⁻ → BaCrO₄↓ (Kuning)"
        ],
        "confirmasi": "Endapan kuning BaCrO₄ dengan K₂CrO₄ pada suasana netral/asetat",
        "warna_endapan": "Kuning",
        "icon": "🟨"
    },
    "Sr²⁺": {
        "group": "IV",
        "reactions": [
            "Sr²⁺ + CO₃²⁻ → SrCO₃↓ (Putih)",
            "SrCO₃ + 2CH₃COOH → Sr²⁺ + 2CH₃COO⁻ + H₂O + CO₂",
            "Sr²⁺ + SO₄²⁻ → SrSO₄↓ (Putih)"
        ],
        "confirmasi": "Endapan putih SrSO₄ dengan (NH₄)₂SO₄",
        "warna_endapan": "Putih",
        "icon": "🔲"
    },
    "Ca²⁺": {
        "group": "IV",
        "reactions": [
            "Ca²⁺ + CO₃²⁻ → CaCO₃↓ (Putih)",
            "CaCO₃ + 2CH₃COOH → Ca²⁺ + 2CH₃COO⁻ + H₂O + CO₂",
            "Ca²⁺ + C₂O₄²⁻ → CaC₂O₄↓ (Putih)"
        ],
        "confirmasi": "Endapan putih CaC₂O₄ dengan (NH₄)₂C₂O₄",
        "warna_endapan": "Putih",
        "icon": "⬜"
    }
}

DIG_QUESTIONS = [
    {
        "id": "q1",
        "text": "Apakah terbentuk endapan putih saat sampel ditambahkan HCl encer?",
        "yes": "q2",
        "no": "q_g3_start",
        "hint": "Kation Golongan I (Ag⁺, Pb²⁺, Hg₂²⁺) membentuk garam klorida tidak larut."
    },
    {
        "id": "q2",
        "text": "Apakah sebagian endapan larut saat dipanaskan dengan air panas?",
        "yes": "q3",
        "no": "q4",
        "hint": "PbCl₂ larut dalam air panas karena kelarutannya meningkat dengan suhu."
    },
    {
        "id": "q3",
        "text": "Apakah filtrat (air panas) membentuk endapan kuning saat ditambahkan K₂CrO₄?",
        "yes": "confirm_Pb",
        "no": "q4",
        "hint": "PbCrO₄ berwarna kuning — tanda khas Pb²⁺."
    },
    {
        "id": "q4",
        "text": "Apakah endapan yang tidak larut dalam air panas berubah menjadi hitam saat ditambahkan NH₄OH?",
        "yes": "confirm_Hg",
        "no": "q5",
        "hint": "Hg₂Cl₂ mengalami disproporsionasi dengan NH₄OH: Hg⁰ (hitam) + Hg(NH₂)Cl (putih)."
    },
    {
        "id": "q5",
        "text": "Apakah endapan larut dalam NH₄OH dan terbentuk endapan putih kembali saat ditambahkan HNO₃?",
        "yes": "confirm_Ag",
        "no": "q_g3_start",
        "hint": "AgCl larut dalam NH₄OH membentuk [Ag(NH₃)₂]⁺, lalu mengendap kembali dengan asam."
    },
    {
        "id": "q_g3_start",
        "text": "Apakah terbentuk endapan (coklat/putih/abu-abu) saat sampel ditambahkan NH₄OH + NH₄Cl?",
        "yes": "q_g3_1",
        "no": "q_g4_start",
        "hint": "Fe(OH)₃ (coklat), Al(OH)₃ (putih), Cr(OH)₃ (abu-abu/hijau) menandakan Golongan III."
    },
    {
        "id": "q_g3_1",
        "text": "Apakah terbentuk warna merah darah saat endapan dilarutkan HCl lalu ditambahkan KSCN?",
        "yes": "confirm_Fe",
        "no": "q_g3_2",
        "hint": "[Fe(SCN)]²⁺ berwarna merah darah — sangat sensitif untuk Fe³⁺."
    },
    {
        "id": "q_g3_2",
        "text": "Apakah endapan larut dalam NaOH berlebih + H₂O₂ dan terbentuk endapan putih/gel saat filtrat diasamkan?",
        "yes": "confirm_Al",
        "no": "q_g3_3",
        "hint": "Al(OH)₃ bersifat amfoter — larut dalam basa berlebih → [Al(OH)₄]⁻, mengendap kembali saat diasamkan."
    },
    {
        "id": "q_g3_3",
        "text": "Apakah filtrat berwarna kuning/jingga (CrO₄²⁻) dan membentuk endapan kuning dengan Pb(NO₃)₂?",
        "yes": "confirm_Cr",
        "no": "q_g4_start",
        "hint": "CrO₄²⁻ berwarna kuning dan membentuk PbCrO₄ (kuning) dengan Pb(NO₃)₂."
    },
    {
        "id": "q_g4_start",
        "text": "Apakah terbentuk endapan putih saat sampel ditambahkan (NH₄)₂CO₃ + NH₄OH + NH₄Cl?",
        "yes": "q_g4_1",
        "no": "no_match",
        "hint": "BaCO₃, SrCO₃, CaCO₃ semuanya berwarna putih — khas Golongan IV."
    },
    {
        "id": "q_g4_1",
        "text": "Setelah dilarutkan dengan CH₃COOH, apakah terbentuk endapan kuning dengan K₂CrO₄?",
        "yes": "confirm_Ba",
        "no": "q_g4_2",
        "hint": "BaCrO₄ berwarna kuning — mengkonfirmasi Ba²⁺."
    },
    {
        "id": "q_g4_2",
        "text": "Apakah terbentuk endapan putih dengan (NH₄)₂SO₄?",
        "yes": "confirm_Sr",
        "no": "q_g4_3",
        "hint": "SrSO₄ berwarna putih — mengkonfirmasi Sr²⁺."
    },
    {
        "id": "q_g4_3",
        "text": "Apakah terbentuk endapan putih dengan (NH₄)₂C₂O₄?",
        "yes": "confirm_Ca",
        "no": "no_match",
        "hint": "CaC₂O₄ (putih) mengkonfirmasi Ca²⁺."
    }
]

DIG_Q_MAP = {q["id"]: q for q in DIG_QUESTIONS}

# ============================================
# DIGITALISASI KIMIA - RENDER
# ============================================

def render_digitalisasi():
    st.title("🔍 Digitalisasi Analisis Kation")
    st.caption("Jawab serangkaian pertanyaan berdasarkan observasi lab untuk mengidentifikasi kation dalam sampel Anda.")
    st.divider()

    if "dig_current" not in st.session_state:
        st.session_state.dig_current = "q1"
        st.session_state.dig_history = []
        st.session_state.dig_result  = None

    col_r, col_s = st.columns([8, 2])
    with col_s:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.dig_current = "q1"
            st.session_state.dig_history = []
            st.session_state.dig_result  = None
            st.rerun()

    if st.session_state.dig_history:
        with st.expander("📋 Jejak Analisis", expanded=False):
            for i, (qid, ans) in enumerate(st.session_state.dig_history, 1):
                icon = "✅" if ans else "❌"
                st.write(f"{i}. {icon} {DIG_Q_MAP[qid]['text']}")

    # Show result
    if st.session_state.dig_result:
        result_key = st.session_state.dig_result

        if result_key == "no_match":
            st.error("⚠️ **Kation Tidak Teridentifikasi**\n\nBerdasarkan jawaban Anda, kation tidak dapat diidentifikasi dalam Golongan I, III, atau IV. Kemungkinan sampel mengandung kation Golongan II atau V, atau terdapat kesalahan prosedur.")
            return

        ion_key = result_key.replace("confirm_", "")
        ion_map = {
            "Pb": "Pb²⁺", "Ag": "Ag⁺", "Hg": "Hg₂²⁺",
            "Fe": "Fe³⁺", "Al": "Al³⁺", "Cr": "Cr³⁺",
            "Ba": "Ba²⁺", "Sr": "Sr²⁺", "Ca": "Ca²⁺"
        }
        ion = ion_map.get(ion_key, ion_key)
        profile = CATION_PROFILES.get(ion, {})
        grp = profile.get("group", "?")
        grp_label = {"I": "Golongan I", "III": "Golongan III", "IV": "Golongan IV"}.get(grp, grp)

        st.success(f"### {profile.get('icon','⚗️')} Kation Teridentifikasi: **{ion}** — {grp_label}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Golongan", grp_label)
        with col2:
            st.metric("Warna Endapan", profile.get("warna_endapan", "—"))

        st.subheader("⚗️ Reaksi Kimia yang Terjadi")
        for rxn in profile.get("reactions", []):
            st.code(rxn, language=None)

        st.info(f"✅ **Konfirmasi:** {profile.get('confirmasi', '—')}")

        grp_full = {"I": "Golongan I", "III": "Golongan III", "IV": "Golongan IV"}.get(grp, "")
        if grp_full in cation_data:
            with st.expander(f"📋 Lihat Prosedur Analisis Lengkap {grp_full}"):
                for i, step in enumerate(cation_data[grp_full]["steps"], 1):
                    st.markdown(f"**Langkah {i}:** {step['action']}")
                    st.write(f"→ {step['result']}")
                    if "confirm" in step:
                        st.success(step["confirm"])
                    st.divider()
        return

    # Current question
    curr_id = st.session_state.dig_current
    if curr_id not in DIG_Q_MAP:
        return

    q = DIG_Q_MAP[curr_id]
    total_q = len(DIG_QUESTIONS)
    answered = len(st.session_state.dig_history)

    st.progress(answered / total_q, text=f"Pertanyaan {answered+1} dari ~{total_q}")

    st.info(f"### 🔬 {q['text']}\n\n💡 *{q['hint']}*")

    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("✅  Ya — Teramati", use_container_width=True, key=f"yes_{curr_id}"):
            st.session_state.dig_history.append((curr_id, True))
            nxt = q["yes"]
            if nxt.startswith("confirm_") or nxt == "no_match":
                st.session_state.dig_result = nxt
            else:
                st.session_state.dig_current = nxt
            st.rerun()
    with col_no:
        if st.button("❌  Tidak — Tidak Teramati", use_container_width=True, key=f"no_{curr_id}"):
            st.session_state.dig_history.append((curr_id, False))
            nxt = q["no"]
            if nxt.startswith("confirm_") or nxt == "no_match":
                st.session_state.dig_result = nxt
            else:
                st.session_state.dig_current = nxt
            st.rerun()

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("⚗️ Analisis Kation")
st.sidebar.divider()
st.sidebar.markdown("### 📌 Menu")

page = st.sidebar.radio(
    "Navigasi:",
    ["🏠 Beranda", "🔍 Digitalisasi Kimia", "📊 Bagan Analisis", "🔬 Detail Reaksi", "📝 Kuis", "📚 Referensi"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.caption("Mencakup Golongan I, III, dan IV\nVersi 3.0 | 2026")
st.sidebar.caption(""" Created by : [Dwi Revani Tyas - 2560713]\n
                                    [Dyah Siti Wulandari - 2560615]\n
                                    [Raihan Jody Nur Alpian - 2560743]\n
                                    [Rizka Diana Putri - 2560762]\n
                                    [Yelsi - 2560807]
""")

# ============================================
# HALAMAN: BERANDA
# ============================================

if page == "🏠 Beranda":
    st.title("⚗️ Analisis Kation Golongan I, III, IV")
    st.caption("Sistem pembelajaran kimia analitik berbasis web — interaktif & komprehensif")
    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("🔬 Kation yang Dianalisis")
        data_tabel = {
            "Golongan": ["I", "III", "IV"],
            "Kation": ["Ag⁺, Pb²⁺, Hg₂²⁺", "Fe³⁺, Al³⁺, Cr³⁺", "Ba²⁺, Sr²⁺, Ca²⁺"],
            "Reagen Pengendap": ["HCl encer", "NH₄OH + NH₄Cl", "(NH₄)₂CO₃ + NH₄OH + NH₄Cl"],
            "Warna Endapan": ["Putih", "Coklat/Putih/Abu-abu", "Putih"],
        }
        st.table(data_tabel)

        st.warning("⚠️ **Catatan:** Golongan II dan V **tidak dibahas** dalam aplikasi ini. Golongan II (Cu²⁺, Cd²⁺, Bi³⁺, Hg²⁺, Sn²⁺, Sb³⁺, As³⁺) dilewati, dan Golongan V (Mg²⁺, K⁺, Na⁺, NH₄⁺) tidak tercakup.")

    with col2:
        st.subheader("🗂️ Fitur Aplikasi")
        features = [
            ("🔍", "Digitalisasi Kimia", "Identifikasi kation secara interaktif melalui tanya-jawab observasi lab"),
            ("📊", "Bagan Analisis", "Visualisasi alur analisis dari sampel hingga konfirmasi kation"),
            ("🔬", "Detail Reaksi", "Penjelasan step-by-step setiap reaksi kimia"),
            ("📝", "Kuis Interaktif", "Uji pemahaman dengan 10 soal acak per golongan"),
            ("📚", "Referensi", "Tabel warna endapan dan rangkuman reaksi lengkap"),
        ]
        for icon, title, desc in features:
            with st.container(border=True):
                st.markdown(f"**{icon} {title}**")
                st.caption(desc)

# ============================================
# HALAMAN: DIGITALISASI KIMIA
# ============================================

elif page == "🔍 Digitalisasi Kimia":
    render_digitalisasi()

# ============================================
# HALAMAN: BAGAN ANALISIS
# ============================================

elif page == "📊 Bagan Analisis":
    st.title("📊 Bagan Alur Analisis Kation")
    st.caption("Alur sistematis dari sampel hingga identifikasi kation")
    st.divider()

    # ── GOLONGAN I ──────────────────────────────────────────────
    st.subheader("⬛ Golongan I — Ag⁺, Pb²⁺, Hg₂²⁺")

    # Langkah 1
    with st.container(border=True):
        st.markdown("**🧪 SAMPEL** mengandung Ag⁺, Pb²⁺, Hg₂²⁺")
        st.markdown("⬇️ **+ HCl encer**")
        col_end, col_fil = st.columns(2)
        with col_end:
            with st.container(border=True):
                st.markdown("**ENDAPAN PUTIH**")
                st.markdown("AgCl, PbCl₂, Hg₂Cl₂")
        with col_fil:
            with st.container(border=True):
                st.markdown("**FILTRAT** → lanjut ke Golongan III")
                st.caption("(skip Golongan II)")

    # Langkah 2
    st.markdown("⬇️ Endapan + **H₂O panas**")
    col_pb, col_sisa = st.columns(2)
    with col_pb:
        with st.container(border=True):
            st.markdown("**FILTRAT PANAS: Pb²⁺** (larut)")
            st.markdown("⬇️ + K₂CrO₄")
            st.success("🟡 **PbCrO₄↓** — Kuning → **Pb²⁺ ✅**")
    with col_sisa:
        with st.container(border=True):
            st.markdown("**RESIDU: AgCl + Hg₂Cl₂** (tidak larut)")
            st.markdown("⬇️ + NH₄OH")

    # Langkah 3
    st.markdown("⬇️ Residu + **NH₄OH**")
    col_ag, col_hg = st.columns(2)
    with col_ag:
        with st.container(border=True):
            st.markdown("**FILTRAT: [Ag(NH₃)₂]⁺** (larut)")
            st.markdown("⬇️ + HNO₃")
            st.success("⚪ **AgCl↓** — Putih → **Ag⁺ ✅**")
    with col_hg:
        with st.container(border=True):
            st.markdown("**RESIDU: Hg₂Cl₂** (tidak larut dalam NH₄OH)")
            st.success("⚫ **Hg↓** (hitam) + **Hg(NH₂)Cl↓** (putih) → **Hg₂²⁺ ✅**")

    st.divider()

    # ── GOLONGAN III ─────────────────────────────────────────────
    st.subheader("🟦 Golongan III — Fe³⁺, Al³⁺, Cr³⁺")

    # Langkah 1
    with st.container(border=True):
        st.markdown("**FILTRAT dari Golongan I** mengandung Fe³⁺, Al³⁺, Cr³⁺")
        st.markdown("⬇️ **+ NH₄OH + NH₄Cl**")
        col_end3, col_fil3 = st.columns(2)
        with col_end3:
            with st.container(border=True):
                st.markdown("**ENDAPAN:**")
                st.markdown("🟤 Fe(OH)₃ — Coklat")
                st.markdown("⚪ Al(OH)₃ — Putih/Gel")
                st.markdown("🔘 Cr(OH)₃ — Abu-abu/Hijau")
        with col_fil3:
            with st.container(border=True):
                st.markdown("**FILTRAT** → lanjut ke Golongan IV")
                st.caption("Ba²⁺, Sr²⁺, Ca²⁺")

    # Langkah 2
    st.markdown("⬇️ Endapan + **NaOH berlebih + H₂O₂**")
    col_fe, col_alcr = st.columns(2)
    with col_fe:
        with st.container(border=True):
            st.markdown("**RESIDU: Fe(OH)₃** — tidak larut dalam basa")
            st.markdown("⬇️ + HCl → larutkan, lalu + KSCN")
            st.success("🔴 **[Fe(SCN)]²⁺** — Merah Darah → **Fe³⁺ ✅**")
    with col_alcr:
        with st.container(border=True):
            st.markdown("**FILTRAT: [Al(OH)₄]⁻ + CrO₄²⁻** — keduanya larut")

    # Langkah 3
    st.markdown("⬇️ Filtrat dipisah untuk konfirmasi Al³⁺ dan Cr³⁺")
    col_al, col_cr = st.columns(2)
    with col_al:
        with st.container(border=True):
            st.markdown("**[Al(OH)₄]⁻**")
            st.markdown("⬇️ + HCl perlahan (asamkan)")
            st.success("⚪ **Al(OH)₃↓** — Putih/Gel → **Al³⁺ ✅**")
    with col_cr:
        with st.container(border=True):
            st.markdown("**CrO₄²⁻** (filtrat berwarna kuning)")
            st.markdown("⬇️ + Pb(NO₃)₂")
            st.success("🟡 **PbCrO₄↓** — Kuning → **Cr³⁺ ✅**")

    st.divider()

    # ── GOLONGAN IV ──────────────────────────────────────────────
    st.subheader("🟨 Golongan IV — Ba²⁺, Sr²⁺, Ca²⁺")

    # Langkah 1
    with st.container(border=True):
        st.markdown("**FILTRAT dari Golongan III** mengandung Ba²⁺, Sr²⁺, Ca²⁺")
        st.markdown("⬇️ **+ (NH₄)₂CO₃ + NH₄OH + NH₄Cl**")
        col_end4, col_fil4 = st.columns(2)
        with col_end4:
            with st.container(border=True):
                st.markdown("**ENDAPAN PUTIH:**")
                st.markdown("BaCO₃, SrCO₃, CaCO₃")
        with col_fil4:
            with st.container(border=True):
                st.markdown("**FILTRAT** → Golongan V")
                st.caption("Mg²⁺, K⁺, Na⁺, NH₄⁺ — tidak dianalisis")

    # Langkah 2
    st.markdown("⬇️ Endapan + **CH₃COOH** → semua larut → + **K₂CrO₄**")
    col_ba, col_srcа = st.columns(2)
    with col_ba:
        with st.container(border=True):
            st.success("🟡 **BaCrO₄↓** — Kuning → **Ba²⁺ ✅**")
    with col_srcа:
        with st.container(border=True):
            st.markdown("**FILTRAT: Sr²⁺ + Ca²⁺** — tetap larut")

    # Langkah 3
    st.markdown("⬇️ Filtrat + **(NH₄)₂SO₄**")
    col_sr, col_ca = st.columns(2)
    with col_sr:
        with st.container(border=True):
            st.success("⚪ **SrSO₄↓** — Putih → **Sr²⁺ ✅**")
    with col_ca:
        with st.container(border=True):
            st.markdown("**FILTRAT: Ca²⁺** — tetap larut")
            st.markdown("⬇️ + (NH₄)₂C₂O₄")
            st.success("⚪ **CaC₂O₄↓** — Putih → **Ca²⁺ ✅**")

# ============================================
# HALAMAN: DETAIL REAKSI
# ============================================

elif page == "🔬 Detail Reaksi":
    st.title("🔬 Detail Reaksi Analisis")
    st.caption("Penjelasan langkah-demi-langkah setiap reaksi kimia")
    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "⬛ Golongan I  (Ag⁺, Pb²⁺, Hg₂²⁺)",
        "🟦 Golongan III  (Fe³⁺, Al³⁺, Cr³⁺)",
        "🟨 Golongan IV  (Ba²⁺, Sr²⁺, Ca²⁺)"
    ])

    def render_steps(group_key, reaksi_awal, catatan=None):
        with st.container(border=True):
            st.markdown(f"**🧪 Reagen:** {cation_data[group_key]['reagen']}")
            for rxn in reaksi_awal:
                st.code(rxn, language=None)
            if catatan:
                st.info(catatan)

        st.subheader("Langkah-langkah Analisis")
        for i, step in enumerate(cation_data[group_key]["steps"], 1):
            with st.expander(f"Langkah {i}: {step['action']}"):
                st.markdown(f"**Aksi:** {step['action']}")
                st.markdown(f"**Hasil:** {step['result']}")
                if "filtrate" in step:
                    st.markdown(f"**Filtrat:** {step['filtrate']}")
                if "residue" in step:
                    st.markdown(f"**Residu:** {step['residue']}")
                if "confirm" in step:
                    st.success(f"✅ {step['confirm']}")

    with tab1:
        render_steps(
            "Golongan I",
            [
                "Ag⁺ + Cl⁻ → AgCl↓ (Putih)",
                "Pb²⁺ + 2Cl⁻ → PbCl₂↓ (Putih)",
                "Hg₂²⁺ + 2Cl⁻ → Hg₂Cl₂↓ (Putih)"
            ]
        )

    with tab2:
        render_steps(
            "Golongan III",
            [
                "Fe³⁺ + 3OH⁻ → Fe(OH)₃↓ (Coklat/Merah)",
                "Al³⁺ + 3OH⁻ → Al(OH)₃↓ (Putih/Gel)",
                "Cr³⁺ + 3OH⁻ → Cr(OH)₃↓ (Abu-abu/Hijau)"
            ],
            catatan="⚠️ **NH₄Cl** berfungsi sebagai penyangga untuk menekan [OH⁻] agar Mg²⁺ tidak terendap."
        )

    with tab3:
        render_steps(
            "Golongan IV",
            [
                "Ba²⁺ + CO₃²⁻ → BaCO₃↓ (Putih)",
                "Sr²⁺ + CO₃²⁻ → SrCO₃↓ (Putih)",
                "Ca²⁺ + CO₃²⁻ → CaCO₃↓ (Putih)"
            ],
            catatan="💡 **NH₄Cl** mencegah pengendapan MgCO₃ yang tidak diinginkan."
        )

# ============================================
# HALAMAN: KUIS
# ============================================

elif page == "📝 Kuis":
    st.title("📝 Kuis Analisis Kation")
    st.caption("Uji pemahaman Anda — 10 soal acak per golongan")
    st.divider()

    selected_group = st.selectbox(
        "Pilih Golongan:",
        ["Golongan I", "Golongan III", "Golongan IV"]
    )

    quiz_key = f"quiz_state_{selected_group.replace(' ', '_')}"

    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = {
            'current_question': 0,
            'score': 0,
            'answered': False,
            'selected_option': None,
            'shuffled_questions': get_random_questions(selected_group, 10)
        }

    state = st.session_state[quiz_key]
    quiz_list = state['shuffled_questions']

    st.progress(
        state['current_question'] / len(quiz_list),
        text=f"Soal {state['current_question']+1} dari {len(quiz_list)}  |  Skor: {state['score']}"
    )

    if state['current_question'] < len(quiz_list):
        q = quiz_list[state['current_question']]

        with st.container(border=True):
            st.subheader(f"Soal {state['current_question']+1}")
            st.markdown(f"**{q['question']}**")

        for i, option in enumerate(q['options']):
            label = f"{chr(65+i)}.  {option}"
            if not state['answered']:
                if st.button(label, key=f"opt_{selected_group}_{i}_{state['current_question']}", use_container_width=True):
                    state['answered'] = True
                    state['selected_option'] = i
                    if i == q['correct']:
                        state['score'] += 1
                    st.rerun()
            else:
                if i == q['correct']:
                    st.success(f"✅ {label}")
                elif i == state['selected_option']:
                    st.error(f"❌ {label}")
                else:
                    st.button(label, key=f"opt_dis_{selected_group}_{i}_{state['current_question']}", use_container_width=True, disabled=True)

        if state['answered']:
            st.info(f"💡 **Penjelasan:** {q['explanation']}")
            if st.button("Soal Berikutnya →", type="primary", use_container_width=True):
                state['current_question'] += 1
                state['answered'] = False
                state['selected_option'] = None
                st.rerun()
    else:
        score_pct = (state['score'] / len(quiz_list)) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skor", f"{state['score']}/{len(quiz_list)}")
        with col2:
            st.metric("Persentase", f"{score_pct:.0f}%")
        with col3:
            st.metric("Golongan", selected_group)

        if score_pct >= 80:
            st.balloons()
            st.success("🏆 Luar biasa! Anda menguasai materi ini dengan sangat baik!")
        elif score_pct >= 60:
            st.info("👍 Bagus! Pemahaman Anda sudah cukup baik, tingkatkan lagi!")
        else:
            st.warning("📚 Perlu belajar lagi. Pelajari bagan dan detail reaksi dengan lebih teliti.")

        if st.button("🔄 Ulangi Kuis", type="primary", use_container_width=True):
            st.session_state[quiz_key] = {
                'current_question': 0,
                'score': 0,
                'answered': False,
                'selected_option': None,
                'shuffled_questions': get_random_questions(selected_group, 10)
            }
            st.rerun()

# ============================================
# HALAMAN: REFERENSI
# ============================================

elif page == "📚 Referensi":
    st.title("📚 Referensi & Tabel Ringkasan")
    st.caption("Warna endapan, larutan, dan rangkuman reaksi kimia")
    st.divider()

    st.subheader("🎨 Warna Endapan & Larutan")
    referensi_data = {
        "Senyawa": [
            "AgCl", "PbCl₂", "Hg₂Cl₂", "PbCrO₄",
            "Fe(OH)₃", "Al(OH)₃", "Cr(OH)₃", "[Fe(SCN)]²⁺", "PbCrO₄ (Gol.III)",
            "BaCrO₄", "SrSO₄", "CaC₂O₄"
        ],
        "Warna": [
            "Putih", "Putih", "Putih", "Kuning",
            "Coklat/Merah", "Putih/Gel", "Abu-abu/Hijau", "Merah Darah", "Kuning",
            "Kuning", "Putih", "Putih"
        ],
        "Keterangan": [
            "Larut dalam NH₄OH", "Larut dalam air panas", "Berubah hitam+putih dengan NH₄OH", "Konfirmasi Pb²⁺",
            "Tidak larut dalam basa berlebih", "Amfoter — larut dalam NaOH berlebih", "Dioksidasi → CrO₄²⁻ dengan H₂O₂", "Konfirmasi Fe³⁺ — sangat sensitif", "Konfirmasi Cr³⁺",
            "Konfirmasi Ba²⁺", "Konfirmasi Sr²⁺", "Konfirmasi Ca²⁺"
        ],
        "Golongan": [
            "I", "I", "I", "I",
            "III", "III", "III", "III", "III",
            "IV", "IV", "IV"
        ]
    }
    st.table(referensi_data)

    st.divider()
    st.subheader("⚗️ Rangkuman Reaksi Kimia")

    tab1, tab2, tab3 = st.tabs(["Golongan I", "Golongan III", "Golongan IV"])

    with tab1:
        reaksi_I = [
            "Pb²⁺ + 2Cl⁻ → PbCl₂↓  →  H₂O panas → larut  →  + K₂CrO₄  →  PbCrO₄↓ (Kuning)",
            "Ag⁺ + Cl⁻ → AgCl↓  →  + NH₄OH → [Ag(NH₃)₂]⁺  →  + HNO₃  →  AgCl↓ (Putih)",
            "Hg₂²⁺ + 2Cl⁻ → Hg₂Cl₂↓  →  + NH₄OH  →  Hg↓ (Hitam) + Hg(NH₂)Cl↓ (Putih)"
        ]
        for r in reaksi_I:
            st.code(r, language=None)

    with tab2:
        reaksi_III = [
            "Fe³⁺ + 3OH⁻ → Fe(OH)₃↓  →  + KSCN  →  [Fe(SCN)]²⁺ (Merah Darah)",
            "Al³⁺ + 3OH⁻ → Al(OH)₃↓  →  + NaOH berlebih → [Al(OH)₄]⁻  →  + HCl  →  Al(OH)₃↓ (Putih)",
            "Cr³⁺ + 3OH⁻ → Cr(OH)₃↓  →  + NaOH + H₂O₂ → CrO₄²⁻  →  + Pb(NO₃)₂  →  PbCrO₄↓ (Kuning)"
        ]
        for r in reaksi_III:
            st.code(r, language=None)

    with tab3:
        reaksi_IV = [
            "Ba²⁺ + CO₃²⁻ → BaCO₃↓  →  + CH₃COOH → Ba²⁺  →  + K₂CrO₄  →  BaCrO₄↓ (Kuning)",
            "Sr²⁺ + CO₃²⁻ → SrCO₃↓  →  + CH₃COOH → Sr²⁺  →  + (NH₄)₂SO₄  →  SrSO₄↓ (Putih)",
            "Ca²⁺ + CO₃²⁻ → CaCO₃↓  →  + CH₃COOH → Ca²⁺  →  + (NH₄)₂C₂O₄  →  CaC₂O₄↓ (Putih)"
        ]
        for r in reaksi_IV:
            st.code(r, language=None)
