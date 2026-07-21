import streamlit as st
from appST import FazerLancamentos,ExcluirConta,CardDeExplicaçao

class Conta_ST:
    #Construtor da classe Contas
    def __init__(self, nome_conta, tipo_conta, valor_conta,id_conta):
        self.nome_conta = nome_conta
        self.tipo_conta = tipo_conta
        self.valor_conta = valor_conta
        self.lista_lancamentos_deb = [0]
        self.lista_lancamentos_cred = [0]
        self.id_conta = id_conta

        if tipo_conta == "Débito":
            self.lista_lancamentos_deb[0] = self.valor_conta
        else:
            self.lista_lancamentos_cred[0] = self.valor_conta

    #Rederizar o razonete
    def render(self):
        with st.container(border=True):
            col_texto, col_botao = st.columns([7, 3])

            with col_texto:
                st.markdown(
                    f"<p style='text-align:center; font-size: 18px;'><strong>{self.nome_conta} - {self.tipo_conta}</strong></p>",
                    unsafe_allow_html=True
                )

            with col_botao:
                col_btn1, col_btn2,col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button("📝",key=f"chave_editar{self.id_conta}",use_container_width=True):
                        st.session_state.conta_selecionada = self.id_conta
                        st.session_state.conta_selecionada_tipo = self.tipo_conta
                        FazerLancamentos()
                with col_btn2:
                    if st.button("❌", key=f"chave_excluir{self.id_conta}",use_container_width=True):
                        st.session_state.conta_selecionada_tipo = self.tipo_conta
                        st.session_state.conta_selecionada = self.id_conta
                        ExcluirConta()
                with col_btn3:
                    if st.button("🔍", key=f"chave_informacao{self.id_conta}",use_container_width=True):
                        st.session_state.conta_nome = self.nome_conta
                        CardDeExplicaçao()
            st.dataframe({"Débito": self.lista_lancamentos_deb,"Crédito": self.lista_lancamentos_cred})

    #Adicionar os lançamentos no razonete
    def LancamentoConta(self,valor_lancamento,tipo_lancamento):
        if self.tipo_conta == "Débito":
            if(tipo_lancamento=="Débito"):
                self.valor_conta += valor_lancamento
                self.lista_lancamentos_deb.append(valor_lancamento)
                self.lista_lancamentos_cred.append(0)
            elif(tipo_lancamento=="Crédito"):
                self.valor_conta -= valor_lancamento
                self.lista_lancamentos_cred.append(valor_lancamento)
                self.lista_lancamentos_deb.append(0)
            else:
                print("Erro de tipo de conta")
        elif self.tipo_conta == "Crédito":
            if(tipo_lancamento=="Débito"):
                self.valor_conta -= valor_lancamento
                self.lista_lancamentos_deb.append(valor_lancamento)
                self.lista_lancamentos_cred.append(0)
            elif(tipo_lancamento=="Crédito"):
                self.valor_conta += valor_lancamento
                self.lista_lancamentos_cred.append(valor_lancamento)
                self.lista_lancamentos_deb.append(0)
            else:
                print("Erro de tipo de conta")