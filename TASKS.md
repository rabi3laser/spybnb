# ✅ SPYBNB - LISTE DES TÂCHES

> **Dernière mise à jour** : 2026-01-01 23:30 UTC
> **Status global** : 🟢 Backend complet (35%)

---

## 📊 PROGRESSION

```
[███████░░░░░░░░░░░░░] 35% - Backend API complet!
```

| Phase | Status | Progression |
|-------|--------|-------------|
| 1. Setup | ✅ Terminé | 100% |
| 2. Backend | ✅ Terminé | 100% |
| 3. Database | ⚪ Non démarré | 0% |
| 4. Frontend | ⚪ Non démarré | 0% |
| 5. Tests | ⚪ Non démarré | 0% |
| 6. Déploiement | ⚪ Non démarré | 0% |

---

## 🎯 PHASE 1 : SETUP INITIAL ✅

### Infrastructure
- [x] Créer dossier projet `/opt/spybnb`
- [x] Créer fichier `DIRECTIVES.md`
- [x] Créer fichier `TASKS.md`
- [x] Créer structure dossiers (backend/, frontend/, docs/)
- [x] Créer fichier `.env.example`
- [x] Créer fichier `.gitignore`
- [x] Créer fichier `.env` avec vrais tokens
- [x] Initialiser Git
- [x] Créer repo GitHub `spybnb`
- [x] Push sur GitHub

---

## 🎯 PHASE 2 : BACKEND (FastAPI) ✅

### Structure
- [x] Créer `backend/main.py`
- [x] Créer `backend/config.py`
- [x] Créer `backend/models/schemas.py`
- [x] Créer `backend/services/`

### Services
- [x] `services/apify_service.py` - Intégration Apify
- [x] `services/supabase_service.py` - Intégration DB

### Models
- [x] `models/schemas.py` - Tous les modèles Pydantic

### Routes API
- [x] `POST /api/scan` - Lancer un scan
- [x] `GET /api/scan/{id}` - Récupérer résultats scan
- [x] `GET /api/scans` - Liste des scans utilisateur
- [x] `POST /api/alerts` - Créer une alerte
- [x] `GET /api/alerts` - Liste des alertes
- [x] `DELETE /api/alerts/{id}` - Supprimer alerte

---

## 🎯 PHASE 3 : BASE DE DONNÉES (Supabase)

### Tables
- [ ] Table `users`
- [ ] Table `scans`
- [ ] Table `listings`
- [ ] Table `alerts`
- [ ] Table `subscriptions`

### RLS (Row Level Security)
- [ ] Policies pour `scans`
- [ ] Policies pour `alerts`

---

## 🎯 PHASE 4 : FRONTEND (Next.js)

### Pages
- [ ] Landing page `/`
- [ ] Dashboard `/dashboard`
- [ ] Scan `/dashboard/scan`
- [ ] Résultats `/dashboard/results/{id}`
- [ ] Alertes `/dashboard/alerts`
- [ ] Pricing `/pricing`

### Composants
- [ ] `ListingCard`
- [ ] `PriceChart`
- [ ] `ScanForm`
- [ ] `AlertForm`
- [ ] `Navbar`
- [ ] `Footer`

---

## 🎯 PHASE 5 : FONCTIONNALITÉS MVP

- [ ] Scan de listings par localisation
- [ ] Affichage des résultats
- [ ] Alertes email
- [ ] Export CSV
- [ ] Historique des scans

---

## 🎯 PHASE 6 : DÉPLOIEMENT

- [ ] Build production
- [ ] Configuration nginx
- [ ] SSL/HTTPS
- [ ] Domaine

---

## 📝 HISTORIQUE DES MISES À JOUR

| Date | Heure | Tâches complétées |
|------|-------|-------------------|
| 2026-01-01 | 22:47 | Setup initial |
| 2026-01-01 | 22:55 | Services + Models |
| 2026-01-01 | 23:29 | main.py + Push GitHub complet |

