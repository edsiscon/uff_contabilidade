import streamlit as st
import ClassesContasST

#----- Inicializando Variaveis que vão ficar com valores salvos na sessão
if 'lista_contas_deb' not in st.session_state:
    st.session_state.lista_contas_deb = []
    st.session_state.lista_contas_cred = []
    st.session_state.conta_selecionada = 0
    st.session_state.id_conta = 0
    st.session_state.conta_selecionada_tipo = ""

#Configuração da página
st.set_page_config(page_title="UFF | Contabilidade", layout="wide",page_icon="logouff_vertical_azul-1.png")
st.logo("logouff_vertical_azul-1.png")

#------------------------Modal de Criar Conta
@st.dialog("Criar Conta")
def CasdastrarConta():
    st.text("Criar conta")
    nome_conta = st.text_input("Nome do Conta", value="Conta")
    tipo_conta = st.selectbox("Tipo de Conta: ",("Débito","Crédito"))
    valor_conta = st.number_input(
        "Valor",
        min_value=0.0,
        value=0.0,
        step=100.0
    )
    if st.button("Adicionar Conta",key="btn_AddConta"):
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

    if st.button("Adicionar Lançamento", key="btn_Lancar"):
        id_conta = st.session_state.conta_selecionada
        tipo_conta = st.session_state.conta_selecionada_tipo
        if tipo_conta == "Débito":
            conta_selecionada = next((c for c in st.session_state.lista_contas_deb if c.id_conta == id_conta), None)
        elif tipo_conta == "Crédito":
            conta_selecionada = next((c for c in st.session_state.lista_contas_cred if c.id_conta == id_conta), None)
        conta_selecionada.LancamentoConta(valor_lacamento, tipo_lancamento)
        st.rerun()

#-------------- Modal do balancete
@st.dialog("Balancete de Verificação")
def GerarBalanceteVerificao():
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
        else:
            linha_balancete = {
                "Nome da Conta": conta.nome_conta,
                "Débito": 0,
                "Crédito": valor_conta
            }
        balancete_df.append(linha_balancete)
    st.dataframe(balancete_df)
@st.dialog("Excluir Conta")
def ExcluirConta():
    st.text("Deseja excluir essa Conta?")
    if st.button("Excluir Conta", use_container_width=True):
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

#--------------Inicio do codigo 2 colunas para questãoes e botões
with st.container(border=True):
    col_questao, col_botoes = st.columns([8,2])

    with col_questao:
        st.text("No dia primeiro de setembro do ano corrente, a empresa Locadora Sul S.A. celebra um contrato de arrendamento mercantil de um caminhão por 36 meses. O caminhão será utilizado no transporte de equipamentos da entidade. A vida útil do caminhão é de 10 anos, e seu valor justo é de R$ 200.000,00. A taxa de juros implícita no contrato é de 1,5% ao mês. O contrato implica em prestações iguais de R$ 6.500,00. Elabore os lançamentos contábeis no reconhecimento inicial e no primeiro mês, considerando a apropriação da despesa financeira e que os pagamentos são realizados ao final de cada mês.")

    with col_botoes:
        st.button("Criar Conta", use_container_width=True, on_click=CasdastrarConta,key="btn_CriarConta")
        st.button("Vizualizar Balancete", use_container_width=True, on_click=GerarBalanceteVerificao,key="btn_GerarBalanceteVerificao")

#------------Container do razonetes
with st.container():
    col_d, col_c = st.columns(2)
    with col_d:
        for conta in st.session_state.lista_contas_deb:
            conta.render()
    with col_c:
        for conta in st.session_state.lista_contas_cred:
            conta.render()