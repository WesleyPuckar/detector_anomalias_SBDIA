import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore') 

# ---------------------------------------------------------
# 1. GERAÇÃO DO DATASET SIMULADO (MOCK DE LOGS DE API)
# ---------------------------------------------------------
np.random.seed(42) # Mantém a consistência dos resultados

# Simulação de tráfego normal (Horário comercial, baixo erro, payload padrão)
n_normal = 1000
dados_normais = pd.DataFrame({
    'hora_acesso': np.random.randint(8, 19, n_normal), # Entre 8h e 19h
    'taxa_requisicao_seg': np.random.normal(5, 2, n_normal), # Média de 5 req/s
    'tamanho_payload_bytes': np.random.normal(500, 100, n_normal), # ~500 bytes
    'status_erro_ratio': np.random.uniform(0.0, 0.05, n_normal) # Máximo 5% de erro
})

# Simulação de ataques/anomalias (Madrugada, alta taxa, payloads grandes - SQLi/DoS)
n_ataques = 20
dados_ataques = pd.DataFrame({
    'hora_acesso': np.random.choice([2, 3, 4, 23], n_ataques), # Fora do expediente
    'taxa_requisicao_seg': np.random.normal(50, 10, n_ataques), # Pico de requisições
    'tamanho_payload_bytes': np.random.normal(5000, 1500, n_ataques), # Payload massivo
    'status_erro_ratio': np.random.uniform(0.4, 0.9, n_ataques) # Alta taxa de erro (ex: 401/403)
})

# Unindo os dados e embaralhando para simular a ingestão contínua
logs_api = pd.concat([dados_normais, dados_ataques]).sample(frac=1).reset_index(drop=True)
# Adicionando IPs fictícios para o log
logs_api['ip_origem'] = [f"192.168.1.{np.random.randint(1, 255)}" for _ in range(len(logs_api))]

# ---------------------------------------------------------
# 2. CONFIGURAÇÃO E TREINAMENTO DA INTELIGÊNCIA ARTIFICIAL
# ---------------------------------------------------------
print("[INFO] Iniciando análise comportamental dos logs da API...")

# Selecionamos apenas as variáveis matemáticas para a IA analisar
features = ['hora_acesso', 'taxa_requisicao_seg', 'tamanho_payload_bytes', 'status_erro_ratio']
X = logs_api[features]

# Inicializando o Isolation Forest
# Defini uma estimativa de que apenas 2% do nosso tráfego total é malicioso.
modelo_ia = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)

# O modelo 'aprende' o padrão e já prevê quem está fora dele
logs_api['classificacao_ia'] = modelo_ia.fit_predict(X)

# O Isolation Forest retorna 1 para normal e -1 para anomalia. 
logs_api['status_seguranca'] = logs_api['classificacao_ia'].map({1: 'Tráfego Legítimo', -1: 'ANOMALIA DETECTADA (Possível Ataque)'})

# ---------------------------------------------------------
# 3. RESULTADOS EACIONAMENTO DO FLUXO DE RESPOSTA
# ---------------------------------------------------------
# Filtrando apenas as ameaças detectadas
ameacas = logs_api[logs_api['classificacao_ia'] == -1]

print("\n" + "="*60)
print("RELATÓRIO DO SISTEMA DE DETECÇÃO (SOAR)")
print("="*60)
print(f"Total de requisições analisadas: {len(logs_api)}")
print(f"Ameaças críticas bloqueadas: {len(ameacas)}")
print("-" * 60)

# Exibindo um resumo dos ataques pegos pela IA
for index, row in ameacas.head(5).iterrows():
    print(f"[BLOQUEIO] IP: {row['ip_origem']} | Hora: {row['hora_acesso']}h | Req/s: {row['taxa_requisicao_seg']:.1f} | Payload: {row['tamanho_payload_bytes']:.0f} bytes | Taxa Erro: {row['status_erro_ratio']:.2f}")

print("\n[AÇÃO AUTOMATIZADA] - Os IPs listados foram isolados e enviados para o Firewall (Null Routing).")
print("="*60)

print("\n[INFO] Gerando visualização gráfica do tráfego...")

plt.figure(figsize=(10, 6))

# Plotando o tráfego legítimo (Azul)
normais = logs_api[logs_api['classificacao_ia'] == 1]
plt.scatter(normais['hora_acesso'], normais['taxa_requisicao_seg'], 
            c='blue', label='Tráfego Normal', alpha=0.5, edgecolors='w', s=50)

# Plotando as anomalias detectadas (Vermelho)
plt.scatter(ameacas['hora_acesso'], ameacas['taxa_requisicao_seg'], 
            c='red', label='Anomalia / Ataque', edgecolors='k', s=100, marker='X')

# Configurando o visual do gráfico
plt.title('Detecção de Anomalias em APIs (Isolation Forest)', fontsize=14, fontweight='bold')
plt.xlabel('Horário do Acesso (0h - 23h)', fontsize=12)
plt.ylabel('Taxa de Requisições por Segundo', fontsize=12)
plt.xticks(np.arange(0, 24, 2)) 
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Exibe o gráfico na tela
plt.show()