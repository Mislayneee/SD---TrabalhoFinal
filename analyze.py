import pandas as pd
import matplotlib.pyplot as plt

# 1) Lê o CSV contendo média e desvio para cada cenário
#    Ajuste o caminho se necessário (por exemplo: "logs/exp_results.csv")
df = pd.read_csv("logs/tempos.csv")

# 2) Define eixo X como a coluna “taxa”
x = df["taxa"]

# 3) Identifica cenários a partir dos nomes de coluna que terminam em "_média"
cenarios = []
for col in df.columns:
    if col.endswith("_média"):
        # extrai o prefixo antes de "_média"
        cenarios.append(col[:-len("_média")])

# 4) Para cada cenário, plota média ± desvio como linha com barras de erro
plt.figure(figsize=(10, 6))
for cen in cenarios:
    media_col = f"{cen}_média"
    desvio_col = f"{cen}_desvio"
    plt.errorbar(
        x,
        df[media_col],
        yerr=df[desvio_col],
        fmt="-o",
        capsize=4,
        label=cen.replace("_", " ").title()
    )

# 5) Personaliza o gráfico
plt.title("MRT vs Taxa de Geração para Diferentes Cenários")
plt.xlabel("Taxa de Geração (req/s)")
plt.ylabel("Tempo Médio de Resposta (s)")
plt.xticks(x)  # garante um marcador para cada valor de taxa
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# 6) Salva o gráfico em PNG
plt.savefig("grafico_MRT_multisscenarios.png")
print("Gráfico salvo como: grafico_MRT_multisscenarios.png")
