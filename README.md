# Gerenciador de Despesas e Vales

Um programa desktop para gerenciar despesas da empresa e vales de funcionários com envio automático de emails.

## 🎯 Funcionalidades

✅ **Lançar Despesas**
- Registrar despesas com descrição, valor e categoria
- Cálculo automático de 20% para gastos/reserva
- Visualizar saldo disponível em tempo real

✅ **Solicitar Vales**
- Autorizar vales para funcionários
- Desconto automático do saldo disponível
- Controle de vales pendentes e descontados

✅ **Notificações por Email**
- Confirmação automática de despesas registradas
- Notificação ao funcionário quando vale é autorizado
- Cópia para administrador

✅ **Relatórios**
- Visualizar resumo financeiro
- Histórico de despesas
- Histórico de vales
- Exportar relatório para arquivo

## 📋 Requisitos

- Python 3.7 ou superior
- Tkinter (já vem com Python)

## 🚀 Como Usar

### 1. Instalação

```bash
# Clone ou baixe a pasta do projeto
cd expense_manager

# Instale dependências (se houver)
pip install -r requirements.txt
```

### 2. Configurar Email (Opcional)

Para enviar emails automáticos:

1. Copie `config.ini.example` para `config.ini`
2. Abra `config.ini` e configure:
   - **Gmail**: Use seu email e [senha de app](https://support.google.com/accounts/answer/185833)
   - **Outlook/Yahoo**: Confira as configurações SMTP correspondentes

Se não configurar, os emails serão exibidos no console.

### 3. Executar o Programa

**Windows:**
```bash
python main.py
```

**Linux/Mac:**
```bash
python3 main.py
```

## 📖 Guia de Uso

### Aba "Lançar Despesa"

1. Preencha **Descrição** (ex: "Compra de Materiais")
2. Insira o **Valor** em reais (ex: 1000)
3. Escolha a **Categoria** (Salário, Insumos, Aluguel, etc.)
4. Clique em **Calcular** para ver a divisão:
   - 20% vai para reserva de gastos
   - 80% fica disponível para vales
5. Clique em **Lançar Despesa** para registrar
6. Um email de confirmação será enviado

### Aba "Solicitar Vale"

1. Digite o **Nome do Funcionário**
2. Insira o **Valor do Vale** desejado
3. Indique o **Motivo** (ex: "Vale refeição")
4. Insira o **Email do Funcionário**
5. O sistema mostra:
   - Saldo disponível (80% da última entrada)
   - Total de vales pendentes
6. Clique em **Solicitar Vale**
7. O funcionário receberá email de confirmação

### Aba "Relatório"

- Clique em **Atualizar** para ver dados atualizados
- Clique em **Exportar** para salvar em `relatório.txt`

## 💾 Dados Armazenados

Todos os dados são salvos em `expenses_data.json`:

```json
{
  "total_balance": 1000,
  "expenses": [
    {
      "id": 1,
      "date": "2024-05-29T10:30:00",
      "description": "Compra de Materiais",
      "value": 1000,
      "category": "Insumos",
      "percentage_20": 200,
      "available": 800
    }
  ],
  "vales": [
    {
      "id": 1,
      "date": "2024-05-29T10:35:00",
      "employee_name": "João Silva",
      "value": 200,
      "reason": "Vale refeição",
      "email": "joao@email.com",
      "status": "approved"
    }
  ],
  "gastos_reserve": 200
}
```

## 🧮 Lógica Financeira

### Quando você lança uma despesa:

```
Valor Lançado: R$ 1.000

├─ 20% para Gastos/Custos: R$ 200
└─ 80% para Vales/Saldo:   R$ 800
```

### Quando você autoriza um vale:

```
Saldo Disponível: R$ 800
   │
   ├─ Vale Autorizado:  -R$ 200
   │
   └─ Novo Saldo:       R$ 600
```

## ⚙️ Configurações de Email

### Gmail (recomendado)

1. Ative [verificação de 2 etapas](https://myaccount.google.com/security)
2. Crie [senha de app](https://support.google.com/accounts/answer/185833)
3. Use essa senha no `config.ini`

### Outlook

```ini
smtp_server = smtp-mail.outlook.com
smtp_port = 587
```

### Yahoo

```ini
smtp_server = smtp.mail.yahoo.com
smtp_port = 587
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'tkinter'"

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

### Emails não estão sendo enviados

1. Verifique se `config.ini` foi criado
2. Teste as credenciais do email
3. Ative acesso para "[Aplicativos menos seguros](https://myaccount.google.com/lesssecureapps)" no Gmail (se aplicável)
4. Verifique a porta SMTP da sua provedora

### Dados desaparecendo

- Verifique se o arquivo `expenses_data.json` existe
- Não altere o arquivo manualmente (pode corromper dados)

## 📝 Estrutura de Pastas

```
expense_manager/
├── main.py                    # Programa principal (interface)
├── expense_manager.py         # Lógica de negócio
├── email_service.py           # Serviço de emails
├── config.ini.example         # Exemplo de configuração
├── config.ini                 # Configuração real (você cria)
├── expenses_data.json         # Dados salvos (criado automaticamente)
├── requirements.txt           # Dependências
└── README.md                  # Este arquivo
```

## 💡 Dicas

1. **Backup Regular**: Copie `expenses_data.json` regularmente
2. **Validação**: Sempre confira os valores antes de clicar em "Lançar"
3. **Relatórios**: Exporte relatórios regularmente para histórico
4. **Email**: Teste a configuração com uma despesa pequena primeiro

## 🔒 Segurança

⚠️ **Importante:**
- Nunca compartilhe `config.ini` com suas credenciais
- Use [Senha de App do Google](https://support.google.com/accounts/answer/185833), não sua senha real
- Faça backup regular de `expenses_data.json`
- Não edite manualmente JSON (pode corromper dados)

## 📞 Suporte

Se encontrar problemas:

1. Verifique se Python 3.7+ está instalado: `python --version`
2. Verifique se Tkinter está disponível: `python -m tkinter`
3. Revise a configuração de email
4. Verifique os logs no console

## 📄 Licença

Livre para uso pessoal e comercial.

---

**Desenvolvido para gerenciamento eficiente de despesas empresariais.**
