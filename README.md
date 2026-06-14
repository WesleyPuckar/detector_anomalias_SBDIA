#  Defesa Proativa de APIs com IA e Big Data (Isolation Forest)

Este repositório contém o protótipo funcional desenvolvido para o desafio prático da disciplina de **Aplicações Avançadas de IA e Big Data na Segurança (SENAI)**. 

O projeto simula um ambiente de resposta automatizada a incidentes (SOAR) utilizando Machine Learning para detectar anomalias em logs de requisições de APIs críticas, mitigando ameaças fora do horário comercial.

##  Objetivo do Protótipo
Demonstrar a aplicação do algoritmo de aprendizado não supervisionado **Isolation Forest** para identificar desvios comportamentais em tráfego de rede (como ataques de Negação de Serviço, injeções de payload massivo e varreduras noturnas), sem a necessidade de assinaturas estáticas de antivírus ou firewalls tradicionais.

## ⚙️ Tecnologias e Bibliotecas Utilizadas
- **Linguagem:** Python 3
- **Manipulação de Dados:** `pandas`, `numpy` (Simulação da camada de ingestão de Big Data)
- **Machine Learning (IA):** `scikit-learn` (Algoritmo Isolation Forest)
- **Visualização de Dados:** `matplotlib` (Geração de gráficos de dispersão das anomalias)

##  Como executar o projeto

### 1. Pré-requisitos
Certifique-se de ter o Python 3 e o gerenciador de pacotes `pip` instalados no seu sistema operacional. Para distribuições Linux baseadas em Debian/Ubuntu, você pode garantir a instalação com:

```bash
sudo apt update
sudo apt install python3 python3-pip
````
### 2. Instalação das dependências
Clone este repositório e instale as bibliotecas necessárias executando o comando abaixo no terminal:

```bash
pip install pandas numpy scikit-learn matplotlib
```

### 3. Execução da Simulação
Para iniciar o script de simulação de logs e acionar o motor de Inteligência Artificial, execute:

```bash
python3 detector_anomalias.py
```
### 4. Resultados Esperados

Ao executar o script, o sistema realizará duas ações:

Saída no Terminal (CLI): Exibirá um relatório estilo "SOAR" demonstrando os IPs de origem bloqueados, o horário anômalo da requisição e o volume do payload malicioso.

Dashboard Visual: Abrirá uma janela gráfica plotando o tráfego legítimo em azul e destacando as ameaças contidas em vermelho, comprovando a eficácia matemática da separação de dados anômalos.
<img width="1918" height="678" alt="image" src="https://github.com/user-attachments/assets/750cc5a9-1c29-413a-b491-7a18012aff5b" />


Projeto desenvolvido como requisito acadêmico de cibersegurança.
