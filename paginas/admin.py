# pages/admin.py

import streamlit as st
import pandas as pd
from utils.db_operations import (
    get_all_users,
    add_user,
    update_user,
    delete_user,
    update_user_password,
    is_user_admin
)
from utils.auth import get_user_id
from datetime import datetime

def display_content():
    st.title("🛡️ Gestão de Usuários")

    # Verifica se o usuário é admin
    user_id = get_user_id()
    if not user_id or not is_user_admin(user_id):
        st.error("❌ Acesso negado. Esta página é apenas para administradores.")
        return

    # Tabs para separar visualização de edição
    tab1, tab2 = st.tabs(["👥 Usuários", "➕ Adicionar Usuário"])

    with tab1:
        # Obtém todos os usuários
        users = get_all_users()

        if not users:
            st.info("Nenhum usuário encontrado.")
            return

        # Converte para DataFrame
        df = pd.DataFrame(users)

        # Formata as datas
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
        if 'last_login' in df.columns:
            df['last_login'] = pd.to_datetime(df['last_login']).dt.strftime('%d/%m/%Y %H:%M')
            df['last_login'] = df['last_login'].fillna('Nunca')

        # Oculta a senha
        df['password_display'] = '---'

        # Seleciona e renomeia as colunas
        display_df = df[['id', 'username', 'name', 'email', 'password_display', 'role', 'created_at', 'last_login']]
        display_df.columns = ['ID', 'Username', 'Nome', 'Email', 'Senha', 'Role', 'Criado em', 'Último Login']

        # Exibe a tabela com estilo
        st.markdown("""
        <style>
        .dataframe {
            background-color: #1E1E1E;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Seção de edição de usuários
        st.markdown("---")
        st.subheader("✏️ Editar ou Deletar Usuário")

        # Selecionar usuário para editar
        user_options = {f"{u['username']} ({u['name']})": u['id'] for u in users}
        selected_user_label = st.selectbox("Selecione um usuário:", list(user_options.keys()))
        selected_user_id = user_options[selected_user_label]

        # Busca os dados do usuário selecionado
        selected_user = next((u for u in users if u['id'] == selected_user_id), None)

        if selected_user:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Editar Informações**")
                edit_name = st.text_input("Nome:", value=selected_user['name'], key="edit_name")
                edit_email = st.text_input("Email:", value=selected_user['email'], key="edit_email")
                edit_role = st.selectbox("Role:", ['user', 'admin'],
                                        index=0 if selected_user['role'] == 'user' else 1,
                                        key="edit_role")

                if st.button("💾 Salvar Alterações", type="primary"):
                    if update_user(selected_user_id, edit_name, edit_email, edit_role):
                        st.success("✅ Usuário atualizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao atualizar usuário.")

            with col2:
                st.markdown("**Alterar Senha**")
                new_password = st.text_input("Nova Senha:", type="password", key="new_password")
                confirm_password = st.text_input("Confirmar Senha:", type="password", key="confirm_password")

                if st.button("🔑 Atualizar Senha"):
                    if not new_password:
                        st.error("❌ A senha não pode estar vazia.")
                    elif new_password != confirm_password:
                        st.error("❌ As senhas não coincidem.")
                    elif len(new_password) < 6:
                        st.error("❌ A senha deve ter pelo menos 6 caracteres.")
                    else:
                        if update_user_password(selected_user_id, new_password):
                            st.success("✅ Senha atualizada com sucesso!")
                        else:
                            st.error("❌ Erro ao atualizar senha.")

                st.markdown("---")
                st.markdown("**Deletar Usuário**")
                st.warning("⚠️ Esta ação não pode ser desfeita!")
                confirm_delete = st.checkbox("Confirmo que desejo deletar este usuário", key="confirm_delete")

                if st.button("🗑️ Deletar Usuário", type="secondary", disabled=not confirm_delete):
                    if selected_user_id == user_id:
                        st.error("❌ Você não pode deletar sua própria conta!")
                    else:
                        if delete_user(selected_user_id):
                            st.success("✅ Usuário deletado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao deletar usuário.")

    with tab2:
        st.subheader("Adicionar Novo Usuário")

        with st.form("add_user_form"):
            new_username = st.text_input("Username:", key="new_username")
            new_name = st.text_input("Nome Completo:", key="new_name")
            new_email = st.text_input("Email:", key="new_email")
            new_password = st.text_input("Senha:", type="password", key="new_user_password")
            new_role = st.selectbox("Role:", ['user', 'admin'], key="new_role")

            submitted = st.form_submit_button("➕ Adicionar Usuário", type="primary")

            if submitted:
                if not new_username or not new_name or not new_email or not new_password:
                    st.error("❌ Todos os campos são obrigatórios.")
                elif len(new_password) < 6:
                    st.error("❌ A senha deve ter pelo menos 6 caracteres.")
                else:
                    if add_user(new_username, new_name, new_email, new_password, new_role):
                        st.success(f"✅ Usuário '{new_username}' adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar usuário. Verifique se o username ou email já existe.")
