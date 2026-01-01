# 📋 SPYBNB - DIRECTIVES DE DÉVELOPPEMENT

> Ce fichier contient TOUTES les règles à suivre pour ce projet.
> **À LIRE AVANT CHAQUE SESSION DE DÉVELOPPEMENT**

---

## 🏗️ ARCHITECTURE DU PROJET

```
/opt/spybnb/
├── DIRECTIVES.md          # CE FICHIER - Règles à suivre
├── TASKS.md               # Todo list - MàJ à chaque tâche terminée
├── .env                   # Variables d'environnement (NE PAS COMMIT)
├── backend/               # API FastAPI (Python)
│   ├── main.py            # Point d'entrée
│   ├── config.py          # Configuration
│   ├── services/          # Services métier
│   │   ├── apify_service.py
│   │   └── supabase_service.py
│   ├── models/            # Pydantic models
│   │   └── schemas.py
│   └── requirements.txt
├── frontend/              # Next.js
└── docs/                  # Documentation
```

---

## 🚨 ERREURS À NE JAMAIS COMMETTRE

### 1. Fichiers et Nommage
- ❌ **JAMAIS** de majuscules dans les noms de fichiers (sauf DIRECTIVES.md, TASKS.md, README.md)
- ❌ **JAMAIS** d'espaces dans les noms → utiliser `_` ou `-`
- ❌ **JAMAIS** de caractères spéciaux (accents, ç, etc.)
- ✅ Format : `mon_fichier.py`, `mon-composant.tsx`

### 2. Credentials et Sécurité
- ❌ **JAMAIS** de tokens/passwords en dur dans le code
- ❌ **JAMAIS** commit le fichier `.env`
- ✅ Toujours utiliser `os.getenv("MA_VARIABLE")`
- ✅ Fichier `.env.example` avec les noms de variables (sans valeurs)

### 3. Code Python
- ❌ **JAMAIS** de `print()` pour debug → utiliser `logging`
- ❌ **JAMAIS** de `from module import *`
- ✅ Toujours typer les fonctions
- ✅ Toujours valider les données entrantes (Pydantic)

### 4. API et Routes
- ❌ **JAMAIS** de verbes dans les URLs (`/getUsers`, `/createListing`)
- ✅ REST correct : `GET /users`, `POST /listings`

### 5. Git et Versioning
- ❌ **JAMAIS** de commits sans message descriptif
- ✅ Format commit : `type(scope): description`
  - `feat(api): add listing scan endpoint`
  - `fix(scraper): handle empty results`
  - `docs(readme): update installation`

---

## 📝 CONVENTIONS DE NOMMAGE

### Python (Backend)
| Élément | Convention | Exemple |
|---------|------------|---------|
| Fichiers | snake_case | `apify_service.py` |
| Classes | PascalCase | `ApifyService` |
| Fonctions | snake_case | `get_listings()` |
| Variables | snake_case | `listing_count` |
| Constantes | UPPER_SNAKE | `MAX_LISTINGS` |

### TypeScript (Frontend)
| Élément | Convention | Exemple |
|---------|------------|---------|
| Fichiers composants | PascalCase | `ListingCard.tsx` |
| Fichiers utils | camelCase | `formatPrice.ts` |
| Composants | PascalCase | `ListingCard` |
| Fonctions | camelCase | `formatPrice()` |

---

## 🔧 STACK TECHNIQUE

| Composant | Technologie |
|-----------|-------------|
| Backend | FastAPI |
| Python | 3.11+ |
| Scraping | Apify SDK |
| Database | Supabase |
| Frontend | Next.js 14 |
| Styling | Tailwind CSS |
| Auth | Supabase Auth |
| Paiements | Stripe |

---

## 🔑 VARIABLES D'ENVIRONNEMENT

```bash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_KEY=xxx
APIFY_API_TOKEN=apify_api_xxx
STRIPE_SECRET_KEY=sk_test_xxx
APP_ENV=development
```

---

## 📊 WORKFLOW

1. **Avant de coder** : Lire DIRECTIVES.md et TASKS.md
2. **Pendant** : Suivre les conventions
3. **Après chaque tâche** : Mettre à jour TASKS.md
4. **Avant commit** : Vérifier qu'aucun secret n'est exposé

---

## 🚀 COMMANDES UTILES

```bash
# Backend
cd /opt/spybnb/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

---

## 📅 DERNIÈRE MISE À JOUR
- Date: 2026-01-01
- Version: 1.0.0
