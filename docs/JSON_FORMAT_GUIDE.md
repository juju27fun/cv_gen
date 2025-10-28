# Guide de Génération JSON - Reactive Resume

## Vue d'ensemble

Ce guide explique comment structurer un JSON pour générer un CV avec Reactive Resume.

Structure racine :

```json
{
  "basics": { ... },
  "sections": { ... },
  "metadata": { ... }
}
```

---

## 1. BASICS - Informations personnelles

**Champs requis :**

```json
{
  "name": "Nom Prénom",
  "headline": "Titre professionnel",
  "email": "email@exemple.com",
  "phone": "+33 6 12 34 56 78",
  "location": "Ville, Pays",
  "url": {
    "label": "Mon Portfolio",
    "href": "https://monsite.com"
  },
  "customFields": [],
  "picture": {
    "url": "https://exemple.com/photo.jpg",
    "size": 120,
    "aspectRatio": 1,
    "borderRadius": 0,
    "effects": {
      "hidden": false,
      "border": false,
      "grayscale": false
    }
  }
}
```

---

## 2. SECTIONS - Contenu du CV

### Structure commune

Toutes les sections suivent ce format :

- `name` : Nom affiché
- `columns` : Nombre de colonnes (1-3)
- `visible` : true/false
- `id` : Identifiant unique
- `separateLinks` : true/false (sépare les liens des autres informations)
- `items` : Tableau d'éléments (sauf pour summary qui a `content`)

### 2.1 Summary (Résumé)

```json
{
  "summary": {
    "name": "Summary",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "summary",
    "content": "<p>Description du profil professionnel...</p>"
  }
}
```

### 2.2 Experience (Expériences)

```json
{
  "experience": {
    "name": "Experience",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "experience",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "company": "Entreprise SAS",
        "position": "Développeur Full-Stack",
        "location": "Paris, France",
        "date": "Jan 2020 - Présent",
        "summary": "<ul><li>Réalisation X</li><li>Réalisation Y</li></ul>",
        "url": {
          "label": "",
          "href": "https://entreprise.com"
        }
      }
    ]
  }
}
```

### 2.3 Education (Formation)

```json
{
  "education": {
    "name": "Education",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "education",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "institution": "Université",
        "studyType": "Master",
        "area": "Informatique",
        "score": "Mention TB",
        "date": "2018 - 2020",
        "summary": "Spécialisation IA",
        "url": {
          "label": "",
          "href": ""
        }
      }
    ]
  }
}
```

### 2.4 Skills (Compétences)

```json
{
  "skills": {
    "name": "Skills",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "skills",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "Développement Web",
        "description": "Avancé",
        "level": 0,
        "keywords": ["React", "Node.js", "TypeScript"]
      },
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "DevOps",
        "description": "Intermédiaire",
        "level": 0,
        "keywords": ["Docker", "Kubernetes", "CI/CD"]
      }
    ]
  }
}
```

### 2.5 Projects (Projets)

```json
{
  "projects": {
    "name": "Projects",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "projects",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "Projet E-Commerce",
        "description": "Lead Developer",
        "date": "2023",
        "summary": "<p>Plateforme e-commerce complète</p>",
        "keywords": ["React", "Stripe", "API"],
        "url": {
          "label": "GitHub",
          "href": "https://github.com/projet"
        }
      }
    ]
  }
}
```

### 2.6 Languages (Langues)

```json
{
  "languages": {
    "name": "Languages",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "languages",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "Français",
        "description": "Langue maternelle",
        "level": 0
      },
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "Anglais",
        "description": "Courant (C1)",
        "level": 0
      }
    ]
  }
}
```

### 2.7 Certifications

```json
{
  "certifications": {
    "name": "Certifications",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "certifications",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "AWS Certified Solutions Architect",
        "issuer": "Amazon Web Services",
        "date": "2023",
        "summary": "",
        "url": {
          "label": "",
          "href": ""
        }
      }
    ]
  }
}
```

### 2.8 Profiles (Profils réseaux sociaux)

```json
{
  "profiles": {
    "name": "Profiles",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "profiles",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "network": "LinkedIn",
        "username": "monprofil",
        "icon": "linkedin",
        "url": {
          "label": "",
          "href": "https://linkedin.com/in/monprofil"
        }
      },
      {
        "id": "uuid-unique",
        "visible": true,
        "network": "GitHub",
        "username": "monprofil",
        "icon": "github",
        "url": {
          "label": "",
          "href": "https://github.com/monprofil"
        }
      }
    ]
  }
}
```

### 2.9 Awards (Prix et distinctions)

```json
{
  "awards": {
    "name": "Awards",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "awards",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "title": "Meilleur Développeur 2023",
        "date": "2023",
        "awarder": "Entreprise XYZ",
        "summary": "Prix pour l'excellence technique",
        "url": {
          "label": "",
          "href": ""
        }
      }
    ]
  }
}
```

### 2.10 Volunteer (Bénévolat)

```json
{
  "volunteer": {
    "name": "Volunteering",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "volunteer",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "organization": "Association ABC",
        "position": "Développeur Volontaire",
        "location": "Paris, France",
        "date": "2020 - Présent",
        "summary": "<ul><li>Développement site web</li><li>Formation utilisateurs</li></ul>",
        "url": {
          "label": "",
          "href": "https://association-abc.org"
        }
      }
    ]
  }
}
```

### 2.11 Publications

```json
{
  "publications": {
    "name": "Publications",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "publications",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "Article sur l'IA",
        "publisher": "Revue Tech",
        "date": "2023",
        "summary": "Analyse des tendances IA",
        "url": {
          "label": "Lire",
          "href": "https://revuetech.com/article-ia"
        }
      }
    ]
  }
}
```

### 2.12 References (Références)

```json
{
  "references": {
    "name": "References",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "references",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "Jean Dupont",
        "description": "Manager chez Entreprise XYZ",
        "summary": "Disponible sur demande",
        "url": {
          "label": "",
          "href": ""
        }
      }
    ]
  }
}
```

### 2.13 Interests (Centres d'intérêt)

```json
{
  "interests": {
    "name": "Interests",
    "columns": 1,
    "separateLinks": true,
    "visible": true,
    "id": "interests",
    "items": [
      {
        "id": "uuid-unique",
        "visible": true,
        "name": "Photographie",
        "keywords": ["Portrait", "Paysage"]
      }
    ]
  }
}
```

### 2.14 Custom (Section personnalisée)

```json
{
  "custom": {}
}
```

---

## 3. METADATA - Configuration

```json
{
  "metadata": {
    "template": "pikachu",
    "layout": [
      [
        ["summary", "experience", "education", "projects"],
        [
          "profiles",
          "skills",
          "certifications",
          "languages",
          "references",
          "interests",
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
        "family": "Titillium Web",
        "subset": "latin",
        "variants": ["regular"],
        "size": 13.8
      },
      "lineHeight": 1.5,
      "hideIcons": false,
      "underlineLinks": false
    },
    "notes": ""
  }
}
```

---

## Utilisation

### Templates disponibles

- pikachu, gengar, glalie, bronzor, azurill, chikorita
- ditto, kakuna, leafish, nosepass, onyx, rhyhorn

### Exemples complets

- `apps/client/public/templates/json/pikachu.json`
- `apps/client/public/templates/json/gengar.json`
- `libs/schema/src/sample.ts`

### Génération d'UUID

```javascript
const { randomUUID } = require("crypto");

// Générer un ID unique pour chaque item
const id = randomUUID();
```

### Génération du résumé

```javascript
const generateSummaryHTML = (text) => {
  return `<p>${text}</p>`;
};

const generateBulletsHTML = (points) => {
  const bullets = points.map((p) => `<li><p>${p}</p></li>`).join("");
  return `<ul>${bullets}</ul>`;
};
```

---

## Checklist

- [ ] Toutes les sections ont un `id` unique
- [ ] Tous les items ont un `id` unique
- [ ] `visible` est défini pour chaque section/item
- [ ] Le template est spécifié dans metadata
- [ ] Layout correspond aux sections utilisées
- [ ] URL sont valides (ou vides `""`)
- [ ] HTML utilisé pour summary et descriptions

---

## Exemple de JSON complet

```json
{
  "basics": {
    "name": "Jean Dupont",
    "headline": "Développeur Full-Stack",
    "email": "jean.dupont@email.com",
    "phone": "+33 6 12 34 56 78",
    "location": "Paris, France",
    "url": {
      "label": "Mon Portfolio",
      "href": "https://mondportfolio.com"
    },
    "customFields": [],
    "picture": {
      "url": "https://exemple.com/photo.jpg",
      "size": 140,
      "aspectRatio": 1,
      "borderRadius": 4,
      "effects": {
        "hidden": false,
        "border": false,
        "grayscale": false
      }
    }
  },
  "sections": {
    "summary": {
      "name": "Summary",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "summary",
      "content": "<p>Développeur passionné avec 5 ans d'expérience...</p>"
    },
    "experience": {
      "name": "Experience",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "experience",
      "items": []
    },
    "education": {
      "name": "Education",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "education",
      "items": []
    },
    "skills": {
      "name": "Skills",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "skills",
      "items": []
    },
    "projects": {
      "name": "Projects",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "projects",
      "items": []
    },
    "languages": {
      "name": "Languages",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "languages",
      "items": []
    },
    "certifications": {
      "name": "Certifications",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "certifications",
      "items": []
    },
    "profiles": {
      "name": "Profiles",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "profiles",
      "items": []
    },
    "awards": {
      "name": "Awards",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "awards",
      "items": []
    },
    "volunteer": {
      "name": "Volunteering",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "volunteer",
      "items": []
    },
    "publications": {
      "name": "Publications",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "publications",
      "items": []
    },
    "references": {
      "name": "References",
      "columns": 1,
      "separateLinks": true,
      "visible": false,
      "id": "references",
      "items": []
    },
    "interests": {
      "name": "Interests",
      "columns": 1,
      "separateLinks": true,
      "visible": true,
      "id": "interests",
      "items": []
    },
    "custom": {}
  },
  "metadata": {
    "template": "pikachu",
    "layout": [
      [
        ["summary", "experience", "education", "projects"],
        [
          "profiles",
          "skills",
          "certifications",
          "languages",
          "references",
          "interests",
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
        "family": "Titillium Web",
        "subset": "latin",
        "variants": ["regular"],
        "size": 13.8
      },
      "lineHeight": 1.5,
      "hideIcons": false,
      "underlineLinks": false
    },
    "notes": ""
  }
}
```

---

## Endpoint Reactive Resume

**URL :** `http://localhost:3000/api/resume/import`

**Méthode :** POST

**Body :** Structure avec `{title, slug, visibility, data}` où data contient le JSON complet

**Réponse :** ID du CV créé pour génération PDF

**Génération PDF :** `GET http://localhost:3000/api/resume/print/{resumeId}`
