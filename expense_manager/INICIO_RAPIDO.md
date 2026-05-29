# 🚀 GUIA RÁPIDO - Comece Agora!

## Passo 1: Execute o Programa

### ✅ Windows
Clique duas vezes em `iniciar.bat`

### ✅ Linux/Mac
```bash
chmod +x iniciar.sh
./iniciar.sh
```

### ✅ Alternativa (todos os SO)
```bash
python main.py
# ou
python3 main.py
```

---

## Passo 2: Primeira Despesa

1. Clique na aba **"Lançar Despesa"**
2. Preencha:
   - **Descrição**: "Primeira Entrada"
   - **Valor**: "1000"
   - **Categoria**: "Outro"
3. Clique em **"Calcular"** para ver:
   - 20% para gastos: **R$ 200**
   - 80% disponível: **R$ 800**
4. Clique em **"Lançar Despesa"**

✅ Pronto! A despesa foi registrada.

---

## Passo 3: Solicitar Vale

1. Clique na aba **"Solicitar Vale"**
2. Preencha:
   - **Nome**: "João Silva"
   - **Valor**: "100"
   - **Motivo**: "Vale refeição"
   - **Email**: "joao@email.com"
3. O sistema mostrará:
   - Saldo disponível: **R$ 800**
   - Vales pendentes: **R$ 0**
4. Clique em **"Solicitar Vale"**

✅ Vale autorizado! Email foi enviado.

---

## Passo 4: Ver Relatório

1. Clique na aba **"Relatório"**
2. Você verá:
   - Saldo disponível atualizado
   - Histórico de despesas
   - Histórico de vales
3. Clique em **"Exportar"** para salvar em arquivo

---

## 📧 Configurar Email (Opcional)

Para enviar emails automáticos:

1. Abra `config.ini.example`
2. Copie todo o conteúdo
3. Crie um novo arquivo chamado `config.ini`
4. Cole o conteúdo
5. Edite com seus dados:

**Para Gmail:**
```
email = seu_email@gmail.com
password = sua_senha_app
admin_email = seu_email@gmail.com
```

[Crie uma senha de app do Google aqui](https://support.google.com/accounts/answer/185833)

---

## 🎯 O Que o Programa Faz

| Função | Como Usar |
|--------|-----------|
| **Lançar Despesa** | Registra entrada de dinheiro, calcula 20% automaticamente |
| **Solicitar Vale** | Autoriza vale para funcionário, desconta do saldo |
| **Email Automático** | Confirma operações por email (se configurado) |
| **Relatório** | Mostra resumo completo e histórico |
| **Dados Salvos** | Tudo é salvo em `expenses_data.json` |

---

## 💡 Exemplo Prático

```
Você recebe R$ 1.000

Sistema calcula automaticamente:
├─ R$ 200 (20%) → Reserva para gastos/operação
└─ R$ 800 (80%) → Disponível para vales

Você autoriza um vale de R$ 150 para João

Novo saldo: R$ 650
Vales pendentes: R$ 150
```

---

## ❓ Dúvidas?

- **"Não consigo rodar o programa"**: Instale Python em https://python.org
- **"Tkinter não funciona"**: Veja instruções no README.md
- **"Email não funciona"**: Verifique credenciais em config.ini
- **"Perdi meus dados"**: Estão em `expenses_data.json`

---

## 📂 Arquivos Importantes

| Arquivo | O Quê? |
|---------|--------|
| `main.py` | Programa principal |
| `expenses_data.json` | Seus dados salvos |
| `config.ini` | Configuração de email (você cria) |
| `relatório.txt` | Relatório exportado |

---

**Divirta-se gerenciando suas despesas! 🎉**
