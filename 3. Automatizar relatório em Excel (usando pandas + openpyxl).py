import pandas as pd
from plyer import notification

def analisar_vendas(arquivo_csv):
    # Carregar o arquivo CSV
    df = pd.read_csv(arquivo_csv)
    
    # Verificar se o arquivo possui as colunas esperadas
    if not {'Produto', 'Quantidade', 'Total'}.issubset(df.columns):
        raise ValueError("O arquivo CSV deve conter as colunas: Produto, Quantidade e Total")
    
    # Agrupar por produto
    resumo_vendas = df.groupby('Produto').agg({'Quantidade': 'sum', 'Total': 'sum'}).reset_index()
    
    # Produto mais vendido
    produto_mais_vendido = resumo_vendas.loc[resumo_vendas['Quantidade'].idxmax(), 'Produto']
    
    # Total geral de vendas
    total_vendas = df['Total'].sum()
    
    return resumo_vendas, produto_mais_vendido, total_vendas

def salvar_relatorio(resumo_vendas, arquivo_excel):
    with pd.ExcelWriter(arquivo_excel, engine='openpyxl') as writer:
        resumo_vendas.to_excel(writer, sheet_name='Resumo de Vendas', index=False)

def enviar_notificacao(produto, total):
    mensagem = f"Produto mais vendido: {produto}\nTotal de vendas: R$ {total:,.2f}"
    notification.notify(
        title="Resumo de Vendas",
        message=mensagem,
        timeout=10
    )

if __name__ == "__main__":
    try:
        arquivo_csv = "vendas.csv"  # Substitua pelo nome correto do arquivo
        arquivo_excel = "relatorio.xlsx"
        resumo, produto, total = analisar_vendas(arquivo_csv)
        salvar_relatorio(resumo, arquivo_excel)
        enviar_notificacao(produto, total)
    except Exception as e:
        print(f"Erro: {e}")

