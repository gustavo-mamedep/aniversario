from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import init_db, salvar_presenca

app = Flask(__name__)
app.secret_key = "chave-super-secreta"  # só pro flash funcionar (pode trocar)

# --------- CONFIGURAÇÕES DA FESTA ---------
NOME_ANIVERSARIANTE = "Ana Luíza"
DATA_FESTA = "2025-12-06 15:00:00"  # AAAA-MM-DD HH:MM:SS
LOCAL_NOME = "Condominio Morada do Sol"
LOCAL_ENDERECO = "Rua Tamarindos, 600"
LINK_MAPS = "https://www.google.com/maps/place/R.+Tamarindos,+60...55r!5m1!1e4?entry=ttu&g_ep=EgoyMDI1MTExNy4wIKXMDSoASAFQAw%3D%3D"

# --------- INICIAR BANCO ---------
init_db()


# --------- ROTA PÁGINA INICIAL ---------
@app.route("/")
def index():
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


# --------- ROTA DO FORMULÁRIO DE PRESENÇA ---------
@app.route("/presenca", methods=["GET", "POST"])
def presenca():
    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        telefone = (request.form.get("telefone") or "").strip()
        motorista = (request.form.get("motorista") or "").strip()
        cpf_motorista = (request.form.get("cpf_motorista") or "").strip()
        qtde = (request.form.get("qtde_pessoas") or "").strip()

        erros = []

        if not nome:
            erros.append("Nome é obrigatório.")
        if not telefone:
            erros.append("Telefone é obrigatório.")
        if not qtde:
            erros.append("Quantidade de pessoas é obrigatória.")

        try:
            qtde_int = int(qtde)
            if qtde_int <= 0:
                erros.append("Quantidade de pessoas deve ser maior que zero.")
        except ValueError:
            erros.append("Quantidade de pessoas inválida.")
            qtde_int = 1

        if erros:
            # Se tiver erro, mostra mensagem e volta pro formulário
            for e in erros:
                flash(e, "erro")
            return render_template(
                "presenca.html",
                nome_aniversariante=NOME_ANIVERSARIANTE,
                form_data=request.form,
            )

        # Se passou pelas validações, salva no banco
        salvar_presenca(
            nome=nome,
            telefone=telefone,
            motorista=motorista,
            cpf_motorista=cpf_motorista,
            qtde_pessoas=qtde_int,
        )

        return redirect(url_for("confirmado"))

    # GET: mostra o formulário vazio
    return render_template(
        "presenca.html",
        nome_aniversariante=NOME_ANIVERSARIANTE,
        form_data={},
    )


# --------- ROTA PÁGINA "PRESENÇA CONFIRMADA" ---------
@app.route("/presenca/confirmada")
def confirmado():
    return render_template(
        "confirmado.html",
        nome_aniversariante=NOME_ANIVERSARIANTE,
    )


if __name__ == "__main__":
    app.run(debug=True)
