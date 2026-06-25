# 📊 Tabela Periódica Interativa

Uma aplicação Streamlit interativa para visualizar e gerenciar a tabela periódica com funcionalidades de marcação de elementos já estudados e agregador de vídeos.

## ✨ Funcionalidades

- **Tabela Periódica Colorida**: Elementos categorizados por cor (metais, não-metais, gases nobres, etc.)
- **Marcação de Elementos**: Marque os elementos que já foram estudados - eles ficarão com risco e esmaecidos
- **Progresso de Estudo**: Acompanhe quantos elementos você já estudou
- **Agregador de Vídeos**: Adicione links de vídeos para cada elemento
- **Gerenciamento de Vídeos**: Organize, visualize e delete vídeos por elemento
- **Persistência de Dados**: Dados são mantidos durante a sessão

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Senha de Administrador

Para deixar a aplicação pública apenas para visualização, defina a variável `ADMIN_PASSWORD`.

No PowerShell, antes de iniciar a aplicação:

```powershell
$env:ADMIN_PASSWORD="sua-senha-aqui"
```

Quem acessar sem essa senha poderá visualizar a tabela e os links cadastrados, mas não poderá marcar elementos, resetar progresso, adicionar vídeos ou remover vídeos.

As edições feitas pelo administrador são salvas no arquivo `dados_tabela.json`, criado automaticamente na primeira alteração.

### 3. Executar a Aplicação

```bash
streamlit run Tabelaperiodica.py
```

A aplicação abrirá no seu navegador padrão em `http://localhost:8501`

## 📋 Guia de Uso

### Tabela Periódica
- Clique no botão **"Marcar"** de cada elemento para marcá-lo como estudado
- Elementos marcados aparecem com risco e ficarão esmaecidos
- A cor de fundo indica a categoria do elemento

### Agregador de Vídeos
1. Selecione um elemento na caixa de seleção
2. Cole a URL do vídeo (YouTube, Vimeo, etc.)
3. Adicione uma descrição do vídeo
4. Clique em **"➕ Adicionar Vídeo"**
5. Os vídeos aparecem em uma lista expansível
6. Clique no link do vídeo para abrir em uma nova aba
7. Use o botão 🗑️ para remover um vídeo

### Controles
- **🔄 Resetar Elementos Falados**: Limpa todas as marcações
- **Progresso**: Visualize quantos elementos foram estudados

## 🎨 Categorias de Elementos

- 🟢 **Verde**: Não-metais
- 🔴 **Vermelho**: Gases nobres
- 🟡 **Amarelo**: Metais alcalinos
- 🟠 **Laranja**: Metais alcalinoterrosos
- 🔵 **Azul**: Semimetais
- 🟣 **Roxo**: Halogênios
- ⚪ **Cinza**: Metais

## 📝 Notas

- A aplicação suporta até 18 elementos (você pode expandir a lista `ELEMENTOS_PERIODICOS`)
- Os dados são salvos durante a sessão (recarregar a página mantém os dados)
- Para expandir, adicione mais elementos ao dicionário `ELEMENTOS_PERIODICOS`

## 🔄 Próximas Melhorias Sugeridas

- Adicionar toda a tabela periódica (118 elementos)
- Salvar dados em banco de dados para persistência permanente
- Adicionar informações mais detalhadas dos elementos
- Integração com APIs de vídeos do YouTube
- Sistema de quiz/testes
- Exportar relatório de progresso

## 📧 Desenvolvido com ❤️

Usando Streamlit para criar interfaces web interativas em Python
