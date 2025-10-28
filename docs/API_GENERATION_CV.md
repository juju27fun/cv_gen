# Génération de CV via API - Reactive Resume

## 📋 Vue d'ensemble

Ce document fournit une documentation complète pour générer des CV personnalisés en PDF via l'API Reactive Resume. L'API permet de créer des CV avec des données JSON et de les exporter en PDF de haute qualité.

## 🚀 Services et Ports

| Service | Port | URL |
|---------|------|-----|
| **Server API** | 3000 | `http://localhost:3000` |
| **Client Web** | 5175 | `http://localhost:5175` |
| **Artboard** | 6175 | `http://localhost:6175/artboard/` |

## 🔑 Prérequis

- Docker Compose démarré avec les services : `postgres`, `minio`, `chrome`, `adminer`
- Serveur de développement en cours d'exécution : `pnpm run dev`
- Authentification requise (JWT token)

## 📡 Endpoints API

### 1. Obtenir le schéma des données CV

```http
GET http://localhost:3000/api/resume/schema
```

**Réponse** : Schéma JSON complet pour valider les données CV.

### 2. Créer un CV depuis des données JSON

```http
POST http://localhost:3000/api/resume/import
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Corps de requête** :
```json
{
  "title": "Mon CV Personnalisé",
  "slug": "mon-cv-personnalise",
  "visibility": "private",
  "data": {
    "basics": { ... },
    "sections": { ... },
    "metadata": { ... }
  }
}
```

### 3. Générer le PDF du CV

```http
GET http://localhost:3000/api/resume/print/{resumeId}
Authorization: Bearer <jwt_token>
```

**Réponse** :
```json
{
  "url": "http://localhost:3000/api/storage/object/..."
}
```

## 📝 Structure des données CV

### Structure complète

```json
{
  "basics": {
    "name": "John Doe",
    "headline": "Développeur Web Innovant",
    "email": "john.doe@example.com",
    "phone": "(+33) 1 23 45 67 89",
    "location": "Paris, France",
    "url": {
      "label": "Portfolio",
      "href": "https://johndoe.me"
    },
    "customFields": [],
    "picture": {
      "url": "https://example.com/photo.jpg",
      "size": 120,
      "aspectRatio": 1,
      "borderRadius": 0,
      "effects": {
        "hidden": false,
        "border": false,
        "grayscale": false
      }
    }
  },
  "sections": {
    "summary": {
      "name": "Résumé",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "summary",
      "content": "<p>Résumé de votre profil professionnel...</p>"
    },
    "experience": {
      "name": "Expérience",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "experience",
      "items": [
        {
          "id": "exp1",
          "visible": true,
          "company": "Entreprise XYZ",
          "position": "Développeur Senior",
          "location": "Paris, France",
          "date": "2020 - Présent",
          "summary": "<ul><li><p>Description des responsabilités...</p></li></ul>",
          "url": {
            "label": "Site web",
            "href": "https://entreprise-xyz.com"
          }
        }
      ]
    },
    "education": {
      "name": "Formation",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "education",
      "items": [
        {
          "id": "edu1",
          "visible": true,
          "institution": "Université de Paris",
          "studyType": "Master en Informatique",
          "area": "Paris, France",
          "score": "Mention Très Bien",
          "date": "2018 - 2020",
          "summary": "",
          "url": {
            "label": "",
            "href": ""
          }
        }
      ]
    },
    "skills": {
      "name": "Compétences",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "skills",
      "items": [
        {
          "id": "skill1",
          "visible": true,
          "name": "Technologies Web",
          "description": "Expert",
          "level": 5,
          "keywords": ["React", "Vue.js", "Angular"]
        },
        {
          "id": "skill2",
          "visible": true,
          "name": "Backend",
          "description": "Intermédiaire",
          "level": 3,
          "keywords": ["Node.js", "Python", "PHP"]
        }
      ]
    },
    "projects": {
      "name": "Projets",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "projects",
      "items": [
        {
          "id": "proj1",
          "visible": true,
          "name": "Application E-commerce",
          "description": "Lead Developer",
          "date": "2022",
          "summary": "<p>Développement d'une plateforme e-commerce complète...</p>",
          "keywords": ["React", "Node.js", "MongoDB"],
          "url": {
            "label": "Voir le projet",
            "href": "https://github.com/johndoe/ecommerce"
          }
        }
      ]
    },
    "certifications": {
      "name": "Certifications",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "certifications",
      "items": [
        {
          "id": "cert1",
          "visible": true,
          "name": "AWS Certified Developer",
          "issuer": "Amazon Web Services",
          "date": "2021",
          "summary": "",
          "url": {
            "label": "",
            "href": ""
          }
        }
      ]
    },
    "languages": {
      "name": "Langues",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "languages",
      "items": [
        {
          "id": "lang1",
          "visible": true,
          "name": "Français",
          "description": "Langue maternelle",
          "level": 5,
          "keywords": []
        },
        {
          "id": "lang2",
          "visible": true,
          "name": "Anglais",
          "description": "Courant",
          "level": 4,
          "keywords": []
        }
      ]
    },
    "profiles": {
      "name": "Profils",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "profiles",
      "items": [
        {
          "id": "prof1",
          "visible": true,
          "network": "LinkedIn",
          "username": "johndoe",
          "icon": "linkedin",
          "url": {
            "label": "",
            "href": "https://linkedin.com/in/johndoe"
          }
        },
        {
          "id": "prof2",
          "visible": true,
          "network": "GitHub",
          "username": "johndoe",
          "icon": "github",
          "url": {
            "label": "",
            "href": "https://github.com/johndoe"
          }
        }
      ]
    }
  },
  "metadata": {
    "template": "glalie",
    "layout": [
      [
        ["summary", "experience", "education", "projects", "references"],
        [
          "profiles",
          "skills",
          "certifications",
          "interests",
          "languages",
          "awards",
          "volunteer",
          "publications"
        ]
      ]
    ],
    "css": {
      "value": "",
      "visible": false
    },
    "page": {
      "margin": 14,
      "format": "a4",
      "options": {
        "breakLine": true,
        "pageNumbers": true
      }
    },
    "theme": {
      "background": "#ffffff",
      "text": "#000000",
      "primary": "#ca8a04"
    },
    "typography": {
      "font": {
        "family": "Merriweather",
        "subset": "latin",
        "variants": ["regular"],
        "size": 13
      },
      "lineHeight": 1.75,
      "hideIcons": false,
      "underlineLinks": true
    },
    "notes": ""
  }
}
```

## 💡 Exemple d'utilisation complet

### Étape 1 : Créer un CV avec des données JSON

```bash
curl -X POST http://localhost:3000/api/resume/import \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CV Développeur Frontend",
    "slug": "cv-dev-frontend",
    "visibility": "private",
    "data": {
      "basics": {
        "name": "Alice Martin",
        "headline": "Développeuse Frontend Passionnée",
        "email": "alice.martin@example.com",
        "phone": "+33 6 12 34 56 78",
        "location": "Lyon, France",
        "url": {
          "label": "Portfolio",
          "href": "https://alice-martin.dev"
        },
        "customFields": [],
        "picture": {
          "url": "https://i.imgur.com/photo.jpg",
          "size": 120,
          "aspectRatio": 1,
          "borderRadius": 0,
          "effects": {
            "hidden": false,
            "border": false,
            "grayscale": false
          }
        }
      },
      "sections": {
        "summary": {
          "name": "Profil",
          "columns": 1,
          "separateLinks": true,
          "visible": true,
          "id": "summary",
          "content": "<p>Développeuse Frontend avec 4 ans d''expérience dans la création d''applications web modernes. Spécialisée en React et Vue.js, passionnée par l''UX/UI et les technologies web émergentes.</p>"
        },
        "experience": {
          "name": "Expérience Professionnelle",
          "columns": 1,
          "separateLinks": true,
          "visible": true,
          "id": "experience",
          "items": [
            {
              "id": "exp1",
              "visible": true,
              "company": "TechStart SAS",
              "position": "Développeuse Frontend Senior",
              "location": "Lyon, France",
              "date": "Janvier 2021 - Présent",
              "summary": "<ul><li><p>Développement d''applications React avec TypeScript pour des clients Fortune 500</p></li><li><p>Mentoring de 3 développeurs juniors et optimisation des performances (réduction de 40% du temps de chargement)</p></li></ul>",
              "url": {
                "label": "Site entreprise",
                "href": "https://techstart.fr"
              }
            }
          ]
        },
        "skills": {
          "name": "Compétences Techniques",
          "columns": 1,
          "separateLinks": true,
          "visible": true,
          "id": "skills",
          "items": [
            {
              "id": "skill1",
              "visible": true,
              "name": "Frontend",
              "description": "Expert",
              "level": 5,
              "keywords": ["React", "Vue.js", "Angular", "TypeScript", "JavaScript"]
            },
            {
              "id": "skill2",
              "visible": true,
              "name": "Outils",
              "description": "Expert",
              "level": 5,
              "keywords": ["Webpack", "Vite", "Git", "Jest", "Cypress"]
            }
          ]
        }
      },
      "metadata": {
        "template": "glalie",
        "layout": [
          [
            ["summary", "experience"],
            ["skills"]
          ]
        ],
        "theme": {
          "background": "#ffffff",
          "text": "#000000",
          "primary": "#6366f1"
        }
      }
    }'
```

### Étape 2 : Générer le PDF

```bash
curl -X GET http://localhost:3000/api/resume/print/RESUME_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Réponse** :
```json
{
  "url": "http://localhost:3000/api/storage/object/user_id/resumes/fichier.pdf"
}
```

### Étape 3 : Télécharger le PDF

```bash
curl -X GET "http://localhost:3000/api/storage/object/user_id/resumes/fichier.pdf" \
  --output "mon-cv.pdf"
```

## 🎨 Templates disponibles

Les templates par défaut incluent :
- `rhyhorn` (défaut)
- `glalie`
- `pikachu`
- `chikorita`
- `azurill`
- `bronzor`
- `gengar`
- `glalie`
- `kakuna`
- `leafish`
- `nosepass`
- `onyx`
- `ditto`

## 🔧 Personnalisation avancée

### CSS personnalisé
```json
{
  "metadata": {
    "css": {
      "value": "* { outline: 1px solid red !important; }",
      "visible": true
    }
  }
}
```

### Layout personnalisé
```json
{
  "metadata": {
    "layout": [
      [
        ["summary", "experience", "education"],
        ["skills", "projects", "certifications"]
      ]
    ]
  }
}
```

### Configuration de page
```json
{
  "metadata": {
    "page": {
      "margin": 20,
      "format": "a4",
      "options": {
        "breakLine": true,
        "pageNumbers": true
      }
    }
  }
}
```

## 🚨 Erreurs courantes

1. **Erreur 401** : JWT token manquant ou invalide
2. **Erreur 400** : Données JSON invalides selon le schéma
3. **Erreur 500** : Service Chrome indisponible ou erreur de génération PDF
4. **Timeout** : Le service de génération peut prendre du temps pour des CV complexes

## 🔗 URLs utiles

- **API Documentation** : `http://localhost:3000/api/docs`
- **Adminer (Base de données)** : `http://localhost:5555`
- **Minio Console** : `http://localhost:9001` (minioadmin/minioadmin)
- **Health Check** : `http://localhost:3000/api/health`

---

Cette documentation vous permet de générer facilement des CV personnalisés via l'API Reactive Resume. Pour toute question, consultez les logs du serveur ou la documentation Swagger interactive.