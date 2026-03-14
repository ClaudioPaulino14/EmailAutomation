🚀 AutoMail.ai | Triagem Inteligente de E-mails e Documentos
Assistente de Operações Financeiras Sênior desenvolvido para o desafio de automação. O sistema utiliza Inteligência Artificial (Gemini 3 Flash) para triar, resumir e redigir respostas para comunicações corporativas e documentos financeiros (PDF/TXT).

📂 Estrutura do Repositório
O repositório está organizado da seguinte forma:
📂 app.py: Script principal da aplicação (Interface Streamlit e Lógica de IA).
📂 requirements.txt: Lista de dependências para instalação do ambiente.
📂 data_examples/: Pasta contendo arquivos de exemplo (PDF de boletos e extratos) para teste da ferramenta.
📂 assets/: Imagens e capturas de tela da interface (Light/Dark Mode).

🛠️ Tecnologias e Bibliotecas
Linguagem: Python 3.10+
IA Generativa: google-genai (Modelo Gemini 3 Flash)
Interface: streamlit
Análise de Dados: pandas
Gráficos: plotly

🌟 Diferenciais Técnicos
Engenharia de Prompt: Implementação de técnicas de Few-Shot Prompting e delimitação estruturada para garantir que a IA processe corretamente documentos densos (extratos e boletos).
Tratamento de Erros Multimodal: Lógica de processamento para lidar com inconsistências em arquivos PDF e fallbacks de conexão.
UI Adaptativa: Design focado em scannability com cards coloridos que se adaptam automaticamente aos temas Light e Dark do Streamlit.
