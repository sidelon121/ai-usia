import os
from groq import Groq
from flask import Flask, render_template, request, send_from_directory
from datetime import datetime
from dotenv import load_dotenv 
app = Flask(__name__)

load_dotenv()  
AI_KEY = os.getenv("GROQ_API_KEY")  

if not AI_KEY:
    raise ValueError("❌ API key tidak ditemukan! Pastikan file .env sudah dibuat dan berisi GROQ_API_KEY.")


client = Groq(api_key=AI_KEY)

def ai_call(year):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Anda adalah asisten yang ahli dalam memberikan fakta menarik di bidang Politik, Ekonomi, dan Teknologi."
                },
                {
                    "role": "user",
                    "content": (
                        f"Berikan fakta-fakta menarik bidang Politik, Ekonomi, dan Teknologi dunia pada tahun {year}. "
                        "Format setiap fakta dengan huruf kapital di judulnya, kelompokkan per bidang, "
                        "misal Ekonomi 3 fakta, Politik 3 fakta, Teknologi 3 fakta. "
                        "Berikan penjelasan singkat, padat, dan mendalam dalam bahasa Indonesia."
                    )
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=3000,
            stream=False,
        )

        ai_output = chat_completion.choices[0].message.content
        return ai_output

    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        return f"Maaf, AI tidak tersedia saat ini. Error: {error_msg[:100]}"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/usia', methods=['GET', 'POST'])
def cek_usia():
    if request.method == 'POST':
        try:
            tahun_lahir = int(request.form['tahun_lahir'])
        except ValueError:
            return render_template('cek_usia.html', error="Input tahun lahir harus berupa angka.")

        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir
        ai_output = ai_call(tahun_lahir)

        return render_template('cek_usia.html', usia=usia, tahun_lahir=tahun_lahir, ai_output=ai_output)

    return render_template('cek_usia.html', usia=None, tahun_lahir=None)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.png',
        mimetype='image/png'
    )

if __name__ == "__main__":
    app.run(debug=True)