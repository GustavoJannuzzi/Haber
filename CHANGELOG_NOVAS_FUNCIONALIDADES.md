# Changelog - Novas Funcionalidades Implementadas

## Resumo das Alterações

Este documento descreve as novas funcionalidades adicionadas ao sistema Haber conforme solicitado.

---

## 1. Página de Admin - Gestão de Usuários

### Características:
- **Acesso Restrito**: Apenas usuários com `role = 'admin'` podem acessar esta página
- **Visibilidade no Menu**: O item "Admin" só aparece no menu lateral para administradores
- **Ícone**: Shield-lock (🛡️) no menu

### Funcionalidades:

#### Visualização de Usuários
- Tabela com todas as informações dos usuários:
  - ID
  - Username
  - Nome
  - Email
  - Senha (oculta com "---")
  - Role
  - Data de criação
  - Último login
- Tema escuro consistente com o resto da aplicação

#### Edição de Usuários
- Modificar nome, email e role do usuário
- Alterar senha de usuário existente
- Validação de senha (mínimo 6 caracteres)
- Confirmação antes de deletar usuário
- Proteção: admin não pode deletar a própria conta

#### Adicionar Novos Usuários
- Formulário completo para criar novo usuário
- Campos: username, nome, email, senha, role
- Validação de todos os campos obrigatórios
- Prevenção de duplicação de username/email

### Arquivo Criado:
- `paginas/admin.py`

---

## 2. Página de Histórico Reformulada

A página de histórico foi completamente reformulada com visualizações profissionais e gráficos interativos.

### Seção 1: Histórico das Identificações
- **Tabela completa** com todas as detecções:
  - Data/Hora
  - Nome da doença
  - Confiança (formato decimal: 0.90000)
  - Cidade
  - Fonte da localização (GPS, IP, Manual)
- **Gradiente de cores verdes** nas células de confiança
  - Verde mais claro para valores menores
  - Verde mais escuro para valores maiores
- Fundo escuro consistente com o tema

### Seção 2: Quantidade por Doença
- **Gráfico de barras verticais** usando Plotly
- Mostra a contagem de cada doença detectada
- Barras com gradiente de verde (claro ao escuro)
- Valores exibidos acima das barras
- Eixos configurados:
  - Eixo Y: "Quantidade"
  - Eixo X: Nomes das doenças
- Fundo escuro do gráfico

### Seção 3: Confiança Média por Doença
- **Gráfico de dispersão (scatter/bubble chart)** usando Plotly
- Bolhas coloridas em tons de verde (cinza claro ao verde escuro)
- Tamanho das bolhas proporcional à quantidade de detecções
- Tooltip interativo mostrando:
  - Nome da doença
  - Confiança média
  - Total de detecções
- Eixos configurados:
  - Eixo Y: "Confiança Média"
  - Eixo X: Nomes das doenças
- Fundo escuro

### Seção 4: Mapa de Localizações
- **Mapa interativo** usando Folium
- Tema escuro (CartoDB dark_matter)
- Marcadores coloridos por tipo de doença
- Cores distintas para cada doença:
  - Mossaic Virus: Dourado
  - Southern Blight: Vermelho tomate
  - Sudden Death Syndrome: Marrom
  - Yellow Mosaic: Amarelo
  - Bacterial Blight: Azul royal
  - Brown Spot: Marrom siena
  - Crestamento: Vermelho laranja
  - Ferrugem: Dourado escuro
  - Powdery Mildew: Amarelo claro
  - Septoria: Cinza escuro
- **Legenda** no canto superior direito do mapa
- Popup com informações detalhadas ao clicar:
  - Nome da doença
  - Cidade
  - Data e hora da detecção
- Centralizado automaticamente na região com mais dados
- Zoom e navegação interativa

### Estatísticas no Rodapé
Três métricas principais em cards:
- Total de Análises
- Doenças Detectadas
- Confiança Média

### Arquivo Atualizado:
- `paginas/historico.py` (completamente reescrito)

---

## 3. Alterações no Banco de Dados

### Nova Coluna: `role`
- Adicionada coluna `role` na tabela `users`
- Tipo: VARCHAR(20)
- Valor padrão: 'user'
- Valores possíveis: 'user', 'admin'

### Usuário Admin Padrão
- Usuário `joao` definido como admin
- Pode ser alterado através do script de migração

### Arquivos Criados:
- `database/add_role.sql` - Script SQL para migração manual
- `migrate_add_role.py` - Script Python para migração automatizada

---

## 4. Funções Adicionadas em `db_operations.py`

### Funções para Histórico:
- `get_all_scans_detailed()` - Obtém todas as análises com detalhes
- `get_confidence_by_disease()` - Calcula confiança média por doença
- `get_all_scan_locations()` - Obtém todas as localizações das detecções

### Funções para Admin:
- `get_all_users()` - Lista todos os usuários
- `is_user_admin(user_id)` - Verifica se usuário é admin
- `add_user()` - Adiciona novo usuário
- `update_user()` - Atualiza informações do usuário
- `delete_user()` - Remove usuário
- `update_user_password()` - Atualiza senha do usuário

---

## 5. Alterações no `app.py`

### Menu Dinâmico
- Menu adaptado baseado no role do usuário
- Item "Admin" só aparece para administradores
- Ícone shield-lock para página Admin

### Importações Adicionadas
- `is_user_admin` de `db_operations`
- Importação dinâmica da página admin

### Roteamento
- Adicionado roteamento para página "Admin"
- Correção na importação da página de histórico

---

## 6. Dependências Adicionadas

### requirements.txt
- **plotly** - Para gráficos interativos e profissionais

---

## Como Usar as Novas Funcionalidades

### 1. Executar a Migração do Banco de Dados
```bash
python migrate_add_role.py
```

### 2. Acessar como Admin
- Login: `joao`
- Senha: `123456`

### 3. Página Admin
- Após login como admin, clique em "Admin" no menu lateral
- Gerencie usuários, adicione novos, edite ou delete existentes

### 4. Página de Histórico
- Acesse "Histórico" no menu lateral
- Visualize gráficos interativos
- Explore o mapa de localizações
- Analise estatísticas detalhadas

---

## Arquivos Modificados

1. `app.py` - Menu dinâmico e roteamento
2. `paginas/historico.py` - Completamente reescrito
3. `utils/db_operations.py` - Novas funções adicionadas
4. `requirements.txt` - Plotly adicionado

## Arquivos Criados

1. `paginas/admin.py` - Nova página de administração
2. `database/add_role.sql` - Script SQL de migração
3. `migrate_add_role.py` - Script Python de migração
4. `CHANGELOG_NOVAS_FUNCIONALIDADES.md` - Este documento

---

## URLs de Acesso

- **Aplicação Principal**: http://haber.hml.local:8501
- **Banco de Dados**: haber3.hml.local:3306
- **Database**: haber_db

---

## Observações Técnicas

1. **Segurança**: Senhas são criptografadas usando pbkdf2_sha256
2. **Tema**: Todas as visualizações usam fundo escuro (#0E1117, #1E1E1E, #2D2D2D)
3. **Cores**: Esquema de cores verde consistente com a aplicação
4. **Performance**: Gráficos Plotly são interativos e responsivos
5. **Responsividade**: Layout adaptado para diferentes tamanhos de tela

---

## Próximos Passos Sugeridos

1. Testar todas as funcionalidades no ambiente de produção
2. Verificar permissões de usuários
3. Popular o banco com dados de teste para visualizar os gráficos
4. Ajustar cores e estilos conforme necessário
5. Considerar adicionar exportação de dados em Excel/CSV

---

**Data da Implementação**: 2025-11-10
**Desenvolvido por**: Claude Code
