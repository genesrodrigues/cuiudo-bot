# Guia de Contribuição

Bah tchê! Obrigado por querer contribuir com o Cuiudo!

## Como Contribuir

### Reportar Bugs
- Use a aba Issues no GitHub
- Descreva o problema claramente
- Inclua passos para reproduzir
- Informe versão do Python e dependências

### Sugerir Melhorias
- Novas gírias gaúchas
- Atividades adicionais
- Melhorias na personalidade
- Novos comandos

### Adicionar Gírias

Para adicionar novas gírias autênticas:

1. Edite `personalidade.py`
2. Adicione na categoria apropriada em `GIRIAS`
3. Se for vocabulário, adicione em `VOCABULARIO`
4. Teste com `python test_cuiudo.py`

Exemplo:
```python
'cumprimento': [
    'Bah tchê!',
    'Nova gíria aqui!',  # <-- Sua contribuição
]
```

### Adicionar Atividades

Para adicionar atividades do colono:

1. Edite `atividades.py`
2. Adicione na categoria de período do dia apropriada
3. Use emojis para deixar visual

Exemplo:
```python
'tarde': [
    '🧉 Cevando uns mates',
    '🎣 Pescando no açude',  # <-- Sua contribuição
]
```

## Diretrizes

### Autenticidade
- Use gírias reais do Rio Grande do Sul
- Evite estereótipos exagerados
- Mantenha o tom amigável e hospitaleiro

### Código
- Siga PEP 8
- Adicione docstrings
- Teste suas alterações
- Comente código não-óbvio

### Segurança
- NUNCA adicione comandos de sistema
- NUNCA exponha informações técnicas da máquina
- Mantenha filtros de segurança

## Processo de Pull Request

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-giria`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova gíria'`)
4. Push para a branch (`git push origin feature/nova-giria`)
5. Abra um Pull Request

## Testes

Antes de submeter, rode os testes:

```bash
python test_cuiudo.py
```

Todos devem passar!

## Dúvidas?

Abra uma Issue ou entre em contato.

---

**Tri obrigado pela contribuição tchê!** 🧉
