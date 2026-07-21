import streamlit as st
import ClassesContasST
from ListaDeExercicios import lista_de_exercicios,lista_de_contas
from ListaDeDefContas import lista_de_contas_def

#----- Inicializando Variaveis que vão ficar com valores salvos na sessão
if 'lista_contas_deb' not in st.session_state:
    st.session_state.lista_contas_deb = []
    st.session_state.lista_contas_cred = []
    st.session_state.conta_selecionada = 0
    st.session_state.id_conta = 0
    st.session_state.conta_selecionada_tipo = ""
    st.session_state.id_questao = 0
    st.session_state.mostrar_modal_aviso = True
    st.session_state.conta_nome = ""

#Configuração da página
st.set_page_config(page_title="UFF | Contabilidade", layout="wide",page_icon="logouff_vertical_azul-1.png")
st.logo("logouff_vertical_azul-1.png")
st.markdown("""
<style>
.texto-scroll {
    height: 180px;          /* altura fixa */
    overflow-y: auto;       /* scroll vertical */
    padding: 0px;
    border-radius: 8px;
    white-space: pre-wrap;  /* respeita as quebras de linha */
}
</style>
""", unsafe_allow_html=True)


#----------------------Modal de apresentação
@st.dialog("AVISO")
def AvisoInicial():
    st.text("Olá, seja bem-vindo! Só uns avisos:"
            "\n- O site ainda em está em versão de testes, então algumas funcionalidades talvez não funcionem como deveriam."
            "\n- O foco do conteúdo são os alunos que estão començando na contabilidade."
            "\n- Sugestões de melhoria podem ser enviadas para: xxxxx"
            "\nObrigado!!!")

#------------------------Modal de Criar Conta
@st.dialog("Criar Conta")
def CasdastrarConta():
    st.text("Criar conta")
    nome_conta = st.selectbox("Nome: ", (lista_de_contas))
    tipo_conta = st.selectbox("Tipo de Conta: ",("Débito","Crédito"))
    valor_conta = st.number_input(
        "Valor",
        min_value=0.0,
        value=0.0,
        step=100.0
    )
    if st.button("Adicionar Conta",key="btn_AddConta", type="primary"):
        st.session_state.id_conta += 1
        conta_teste = ClassesContasST.Conta_ST(nome_conta, tipo_conta, valor_conta,st.session_state.id_conta)
        print('teste')
        if tipo_conta == "Débito":
            st.session_state.lista_contas_deb.append(conta_teste)
        elif tipo_conta == "Crédito":
            st.session_state.lista_contas_cred.append(conta_teste)
        st.rerun()

#-----------------------Modal de Criar  Lançamentos
@st.dialog("Fazer lançamentos")
def FazerLancamentos():
    tipo_lancamento = st.selectbox("Tipo de Lançamento: ",("Débito","Crédito"))
    valor_lacamento = st.number_input(
                "Valor",
                min_value=0.0,
                value=0.0,
                step=100.0)

    if st.button("Adicionar Lançamento", key="btn_Lancar", type="primary"):
        id_conta = st.session_state.conta_selecionada
        tipo_conta = st.session_state.conta_selecionada_tipo
        if tipo_conta == "Débito":
            conta_selecionada = next((c for c in st.session_state.lista_contas_deb if c.id_conta == id_conta), None)
        elif tipo_conta == "Crédito":
            conta_selecionada = next((c for c in st.session_state.lista_contas_cred if c.id_conta == id_conta), None)
        conta_selecionada.LancamentoConta(valor_lacamento, tipo_lancamento)
        st.rerun()
#--------------Lançamentos para mais de 1 conta
@st.dialog("Fazer lançamentos +")
def FazerLancamentosMais():
    st.text("Fazer Lançamentos:")
    tipo_conta_deb = st.selectbox("Conta (Débito): ", (lista_de_contas))
    tipo_conta_cred = st.selectbox("Conta (Crédito): ", (lista_de_contas))
    tipo_lancamento_deb = st.number_input(
        "Débito (Valor):",
        min_value=0.0,
        value=0.0,
        step=100.0
    )
    tipo_lancamento_cred = st.number_input(
        "Crédito (Valor):",
        min_value=0.0,
        value=0.0,
        step=100.0
    )
    if st.button("Fazer Lançamento", type="primary"):
        st.rerun()

#-------------- Modal do balancete
@st.dialog("Balancete de Verificação")
def GerarBalanceteVerificao():
    todos_lancamentos_cred = 0
    todos_lancamentos_deb = 0
    balancete_df = []
    listas_todas_contas = st.session_state.lista_contas_deb + st.session_state.lista_contas_cred
    for conta in listas_todas_contas:
        valor_conta = sum(conta.lista_lancamentos_deb) - sum(conta.lista_lancamentos_cred)
        if valor_conta > 0:
            linha_balancete = {
                "Nome da Conta": conta.nome_conta,
                "Débito": valor_conta,
                "Crédito": 0
            }
            todos_lancamentos_deb = valor_conta + todos_lancamentos_deb
        else:
            valor_conta = valor_conta *-1
            linha_balancete = {
                "Nome da Conta": conta.nome_conta,
                "Débito": 0,
                "Crédito": valor_conta
            }
            todos_lancamentos_cred = valor_conta + todos_lancamentos_cred
        balancete_df.append(linha_balancete)
    balancete_df.append({
                "Nome da Conta": "Total",
                "Débito": todos_lancamentos_deb,
                "Crédito": todos_lancamentos_cred
            })
    st.dataframe(balancete_df)
    if todos_lancamentos_deb != todos_lancamentos_cred:
        st.error("Balancete não bate!")
    else:
        st.success("Balancete bate!")

#-------------Trocar De Questão
def TrocarQuestaoDir():
    st.session_state.id_questao += 1
    st.session_state.lista_contas_cred = []
    st.session_state.lista_contas_deb = []
def TrocarQuestaoEsq():
    st.session_state.id_questao -= 1
    st.session_state.lista_contas_cred = []
    st.session_state.lista_contas_deb = []

@st.dialog("Excluir Conta")
def ExcluirConta():
    st.text("Deseja excluir essa Conta?")
    if st.button("Excluir Conta", use_container_width=True, type="primary"):
        id_conta = st.session_state.conta_selecionada
        tipo_conta = st.session_state.conta_selecionada_tipo
        if tipo_conta == "Débito":
            conta_selecionada = next((c for c in st.session_state.lista_contas_deb if c.id_conta == id_conta), None)
            st.session_state.lista_contas_deb.remove(conta_selecionada)
        else:
            conta_selecionada = next((c for c in st.session_state.lista_contas_cred if c.id_conta == id_conta), None)
            st.session_state.lista_contas_cred.remove(conta_selecionada)
        st.rerun()
    if st.button("Cancelar", use_container_width=True):
        st.rerun()
#-------------- Ai vai o caralho das explicações
@st.dialog("Explicação")
def CardDeExplicaçao():
    conta_selecionada = next((conta for conta in lista_de_contas_def if conta["conta"] == st.session_state.conta_nome ), None)
    st.markdown(f'''
        <div style="
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-left: 4px solid #28a745;
    border-radius: 0.5rem;
    padding: 1rem;
    color: #155724;
    font-size: 0.95rem;
    line-height: 1.6;
    ">
    <strong>Conta:</strong> {conta_selecionada["conta"]}<br>
    <strong>Grupo:</strong> {conta_selecionada["grupo"]}<br>
    <strong>Natureza:</strong> {conta_selecionada["natureza"]}<br>
    <strong>Tipo:</strong> {conta_selecionada["tipo"]}<br>
    <strong>Aumenta:</strong>{conta_selecionada["aumenta"]}<br>
   <strong> Descrição:</strong> {conta_selecionada["descricao"]}
</div>''', unsafe_allow_html=True)


#--------------Inicio do codigo 2 colunas para questãoes e botões
if st.session_state.mostrar_modal_aviso:
    pass
with st.container(border=True):
    col_questao, col_botoes = st.columns([8,2],gap="small")

    with col_questao:
        st.markdown(
            f""" <div class="texto-scroll">{lista_de_exercicios[st.session_state.id_questao]["questao"]}</div>""",
            unsafe_allow_html=True
        )
    with col_botoes:
        st.button("Criar Conta", use_container_width=True, on_click=CasdastrarConta,key="btn_CriarConta", type="primary")
        st.button("Fazer Lançamento", use_container_width=True, on_click=FazerLancamentosMais, key="btn_FazerLancamento", type="primary")
        st.button("Vizualizar Balancete", use_container_width=True, on_click=GerarBalanceteVerificao,key="btn_GerarBalanceteVerificao", type="primary")
        col_1, col_2 = st.columns(2)
        with col_1:
            st.button("◀", use_container_width=True, on_click=TrocarQuestaoEsq, key="btn_trocar_esq", type="primary")
        with col_2:
            st.button("▶", use_container_width=True, on_click=TrocarQuestaoDir, key="btn_trocar_dir", type="primary")
#------------Container do razonetes
with st.container():
    col_d, col_c = st.columns(2,gap="small")
    with col_d:
        for conta in st.session_state.lista_contas_deb:
            conta.render()
    with col_c:
        for conta in st.session_state.lista_contas_cred:
            conta.render()