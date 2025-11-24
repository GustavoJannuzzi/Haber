# 🌿 Haber - Sistema de identificação de doenças em folhas de soja

Sistema web desenvolvido em Python/Streamlit para identificação automática de doenças em folhas de soja usando Deep Learning, com foco em usabilidade e precisão para produtores rurais.

## 🎯 Funcionalidades Principais

### 🔐 Sistema de Autenticação
- Login seguro com usuário e senha
- Sistema de cookies para sessão persistente
- Logout disponível na sidebar
- Usuários padrão configurados (joao/123456, maria/123456)

### 📸 Página Principal (Home)
- Upload de imagens de folhas de soja (jpg, jpeg, png)
- Visualização da imagem carregada
- Sistema de geolocalização inteligente
- Identificação automática de doenças
- Exibição de resultados com confiabilidade

### 📍 Sistema de Geolocalização
- Múltiplas opções de localização:
  - Extração de coordenadas EXIF da imagem
  - Seleção manual no mapa interativo
  - Baseado em IP
  - Digitação manual da cidade
- Visualização em mapa com marcador
- Exibição de coordenadas precisas
- Identificação automática da cidade/estado

### 🦠 Catálogo de Doenças
Identificação de 10 doenças comuns em soja:
- Mossaic Virus
- Southern Blight
- Sudden Death Syndrome
- Yellow Mosaic
- Bacterial Blight
- Brown Spot
- Crestamento
- Ferrugem
- Powdery Mildew
- Septoria

Para cada doença:
- Nome científico
- Descrição detalhada
- Agrotóxicos recomendados
- Cuidados preventivos

### 🤖 Página do Modelo
- Explicação técnica do modelo de IA
- Detalhes da arquitetura InceptionV3
- Métricas de desempenho
- Matriz de confusão
- Comparação com outros modelos

### 📊 Histórico de Análises
- Registro de análises anteriores
- Data e hora
- Tipo de praga identificada
- Localização (latitude/longitude)
- Usuário que realizou a análise

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.10+
- Streamlit para interface web
- PIL para processamento de imagens
- Folium para visualização geográfica
- InceptionV3 para deep learning

### Frontend
- Interface dark mode moderna
- Design responsivo para mobile
- Feedback visual em tempo real
- Mensagens de erro e sucesso
- Menu lateral com navegação

### Segurança
- Senhas criptografadas
- Sistema de cookies seguro
- Autenticação em camadas
- Proteção contra acessos não autorizados

## 📦 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Configuração do Ambiente
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/haber.git
cd haber
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando o Projeto
1. Inicie o servidor Streamlit:
```bash
streamlit run app.py
```

2. Acesse a aplicação em seu navegador:
```
http://localhost:8501
```

## 📁 Estrutura do Projeto

```
haber/
├── app.py                 # Arquivo principal da aplicação
├── requirements.txt       # Dependências do projeto
├── README.md             # Documentação do projeto
├── images/               # Imagens estáticas do sistema
├── utils/               # Módulos utilitários
│   ├── auth.py         # Autenticação
│   ├── auth_config.py  # Configuração de autenticação
│   ├── config.py       # Configurações gerais
│   ├── doencas.py      # Gerenciamento de doenças
│   ├── generate_hash.py # Geração de hashes
│   ├── generate_user.py # Geração de usuários
│   ├── image_processing.py # Processamento de imagens
│   └── location.py     # Funções de geolocalização
├── paginas/            # Páginas da aplicação
│   ├── doencas.py      # Página de catálogo de doenças
│   ├── modelo.py       # Página de informações do modelo
│   └── historico.py    # Página de histórico
└── database/          # Configurações do banco de dados
```

## 👥 Como Usar

1. Faça login com suas credenciais
2. Na página principal, faça upload da imagem da folha de soja
3. Aguarde a análise automática
4. Verifique o resultado e as recomendações
5. Consulte o histórico de análises anteriores
6. Explore o catálogo de doenças para mais informações

## 📝 Contribuição
Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de submeter pull requests.

## 📄 Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).

