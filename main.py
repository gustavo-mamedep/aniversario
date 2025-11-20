from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# --------- CONFIGURAÇÕES DA FESTA ---------
NOME_ANIVERSARIANTE = "Ana Luíza"
DATA_FESTA = "2025-12-06 18:00:00"  # AAAA-MM-DD HH:MM:SS
LOCAL_NOME = "Condominio Morada do Sol"
LOCAL_ENDERECO = "Rua Tamarindos, 600"
LINK_MAPS = "https://www.google.com/maps?q=Buffet+Espaco+Festas"

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
    )


if __name__ == "__main__":
    app.run(debug=True)
