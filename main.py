from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# --------- CONFIGURAÇÕES DA FESTA ---------
NOME_ANIVERSARIANTE = "Ana Luíza"
DATA_FESTA = "2025-12-06 18:00:00"  # AAAA-MM-DD HH:MM:SS
LOCAL_NOME = "Condominio Morada do Sol"
LOCAL_ENDERECO = "Rua Tamarindos, 600"
LINK_MAPS = "https://www.google.com/maps/place/R.+Tamarindos,+600+-+Morada+do+Sol,+Uberl%C3%A2ndia+-+MG,+38415-474/@-18.8952451,-48.3473766,206m/data=!3m1!1e3!4m6!3m5!1s0x94a44164977b417d:0x39f7cd92e11fd7e1!8m2!3d-18.8954859!4d-48.3474985!16s%2Fg%2F11lcc6s55r!5m1!1e4?entry=ttu&g_ep=EgoyMDI1MTExNy4wIKXMDSoASAFQAw%3D%3D"

# --------- ROTAS ---------
@app.route("/")
def index():
    # transforma a string em data/hora
    data_dt = datetime.strptime(DATA_FESTA, "%Y-%m-%d %H:%M:%S")
    data_formatada = data_dt.strftime("%d/%m/%Y")
    hora_formatada = data_dt.strftime("%H:%M")

    return render_template(
        "index.html",
        nome_aniversariante=NOME_ANIVERSARIANTE,
        local_nome=LOCAL_NOME,
        local_endereco=LOCAL_ENDERECO,
        link_maps=LINK_MAPS,
        data_formatada=data_formatada,
        hora_formatada=hora_formatada,
        data_festa_iso=DATA_FESTA,
    )


if __name__ == "__main__":
    app.run(debug=True)
