# Arquitetura do UniMarket (Fase 1)

## Visão geral

Aplicação Django monolítica (templates renderizados no servidor) com uma API REST em `/api/v1/` e base de dados MySQL.

```
Navegador ──HTTP──► Django (config/urls.py)
                      ├── Páginas HTML  → views → templates/ (+ static/css, static/js)
                      ├── API REST      → DRF viewsets → serializers
                      └── Admin Django  → /admin/
                                  │
                              Django ORM ──► MySQL (utf8mb4)
```

- **Páginas HTML**: as views consultam o ORM e entregam templates Django. O JavaScript só trata do menu móvel.
- **API REST**: usa os mesmos modelos. Documentação Swagger em `/api/docs/` e esquema OpenAPI em `/api/schema/`.
- **Segurança**: validação sempre no servidor; segredos só no `.env`.

## Estrutura de diretórios

```
unimarket/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── config/                  # Configuração do projeto
│   ├── settings/ (base.py, dev.py, prod.py)
│   ├── urls.py, wsgi.py, asgi.py
├── apps/
│   ├── core/                # Página inicial, context processor
│   └── products/            # Category e Product, páginas e API de categorias
├── templates/ (base.html, core/, products/, partials/)
├── static/ (css/, js/, img/)
├── docs/ARCHITECTURE.md
└── .github/ (ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md)
```

## Decisões desta fase

| Decisão | Justificação |
|---|---|
| Apenas `core` e `products` | Só existem se tiverem comportamento real. As restantes apps chegam nas fases seguintes. |
| `Product` sem loja nem vendedor | A relação com `stores` é criada na Fase 3. |
| Settings divididos em base/dev/prod | Separa configurações seguras de produção (HTTPS, cookies seguros, HSTS). |
| `DB_ENGINE=sqlite` opcional | Só para testes rápidos sem MySQL. O padrão e o alvo é MySQL. |
| `django-environ` | Lê o `.env` sem expor segredos no código. |
| Utilizador personalizado | **Decisão pendente** (ver abaixo): deve ser tomada antes da primeira migração da Fase 2. |

## Decisões que precisam da sua aprovação

1. **Modelo de utilizador personalizado**: recomendo criar já na Fase 2 um `accounts.User` próprio (herdando `AbstractUser`) com campo de papel (comprador/vendedor). Alterá-lo depois de existirem migrações é difícil.
2. **Comprador e vendedor**: uma única conta que pode abrir loja (recomendado, mais simples) ou contas separadas?
3. **Pagamento no MVP**: apenas dinheiro na entrega/levantamento, deixando M-Pesa e e-Mola para depois?
4. **Entrega**: levantamento no campus, entrega, ou ambos?
5. **Idioma da interface**: português apenas (como agora)?
