# Vérification de non-régression — branche `eco/ecoindex`

> 25 octobre 2026. Build Vite 2.9.15 sous Node 26.7 (CI : Node 18). Référence = build de la branche `dev` (commit `0b2a7b0`) servi sur `localhost:4174` ; version optimisée = `eco/ecoindex` (commit `ce66cc3`) servie sur `localhost:4173` via `npm run build && npm run serve`.

## 1. Build

| | Avant (`dev`) | Après (`eco/ecoindex`) |
|---|---|---|
| `npm run build` | 0 erreur, 0 warning | 0 erreur, 0 warning (même sortie) |
| `dist/` | 28 Mo | 7,3 Mo |
| `index.html` | 39,8 Ko (12,5 Ko gzip) | 300 Ko (SVG inlinés) — 127 Ko gzip |
| JS | 164 Ko (48 Ko gzip) | 88,5 Ko (27 Ko gzip) |
| CSS | 73 Ko (12,5 Ko gzip) | 34,6 Ko (8,3 Ko gzip) |
| Vidéos | 24 071 Ko | 4 800 Ko |
| Images raster | 4 980 Ko | 2 150 Ko |
| Dépendances | swiper, aos, svg-injector | swiper, aos |

## 2. Captures d'écran avant / après

Méthode (script `shoot.py`, Playwright Chromium 151, identique pour les deux builds) :

- desktop 1920×1080 (DPR 1) et mobile 390×844 (DPR 2, touch) ;
- scripts tiers (Axeptio, GTM) bloqués pour que le bandeau cookies ne perturbe pas la mise en page ; loader retiré ; scroll pas à pas jusqu'en bas pour déclencher toutes les animations AOS, retour en haut ;
- `<video>` masquées en magenta (le timing des frames n'est pas déterministe ; les vidéos sont contrôlées à part, § 4) ; transitions CSS gelées avant capture ;
- 32 captures par build : page entière, chaque section, 3 modales (produit, mentions légales, RGPD), menu mobile ouvert, carrousel après un clic « suivant ».

Comparaison pixel à pixel (`compare.py`, seuil 16/255 par canal) :

| Capture | Taille | Pixels différents |
|---|---|---|
| desktop-00-bandeau-header.png | 1920x1018 | 0,000 % |
| desktop-01-introduction.png | 1920x990 | 0,000 % |
| desktop-02-description.png | 1920x1145 | 0,000 % |
| desktop-03-cookies.png | 1920x955 | 0,000 % |
| desktop-04-recipes.png | 1920x854 | 0,030 % |
| desktop-05-season-products.png | 1920x696 | 0,000 % |
| desktop-06-map-container.png | 1536x950 | 0,000 % |
| desktop-07-mosaic.png | 1920x1171 | 0,000 % |
| desktop-08-informations.png | 1920x890 | 0,000 % |
| desktop-09-footer.png | 1920x57 | 0,000 % |
| desktop-full.png | 1920x9494 | 0,003 % |
| desktop-modal-james-brownie.png | 1920x1080 | 0,000 % |
| desktop-modal-mentions-legales.png | 1920x1080 | 0,000 % |
| desktop-modal-rgpd.png | 1920x1080 | 0,000 % |
| desktop-recipes-slide2.png | 1920x854 | 0,007 % |
| mobile-00-bandeau-header.png | 780x1612 | 0,000 % |
| mobile-01-introduction.png | 780x2698 | 0,000 % |
| mobile-02-description.png | 780x1404 | 0,000 % |
| mobile-03-cookies.png | 780x2132 | 0,000 % |
| mobile-04-recipes.png | 780x932 | 0,025 % |
| mobile-05-season-products.png | 780x2650 | 0,000 % |
| mobile-06-map-container.png | 780x1512 | 0,000 % |
| mobile-07-mosaic.png | 780x2116 | 0,000 % |
| mobile-08-informations.png | 780x1998 | 0,000 % |
| mobile-09-footer.png | 780x332 | 0,000 % |
| mobile-full.png | 780x18488 | 0,001 % |
| mobile-menu-open.png | 780x1688 | 0,000 % |
| mobile-modal-james-brownie.png | 780x1688 | 0,000 % |
| mobile-modal-mentions-legales.png | 780x1688 | 0,000 % |
| mobile-modal-rgpd.png | 780x1688 | 0,000 % |
| mobile-recipes-slide2.png | 780x932 | 0,002 % |

- Les dimensions de toutes les captures sont identiques (aucun décalage de mise en page, hauteur de page 9 494 px desktop / 9 244 px mobile dans les deux cas).
- Les seules différences (≤ 0,03 % des pixels) sont dans la carte recette du carrousel : bruit de compression WebP q 85 (pixels isolés sur la photo du cookie et les bords du texte), aucune différence structurelle. Images de diff (pixels changés en rouge) dans `audit/screenshots/diff/`. Les captures elles-mêmes sont dans `audit/screenshots/before/` et `after/` (non versionnées, 28 Mo chacune).
- Hauteur de page mesurée **avant** le chargement des images lazy = hauteur finale, en desktop comme en mobile : les attributs `width`/`height` évitent tout saut de mise en page. (Deux cas ont dû être traités : la mosaïque, dont le conteneur flex est dimensionné par les images — elles restent en chargement immédiat — et la vidéo « gif » mobile, qui reçoit `height: auto`.)

## 3. DOM

| | Avant | Après |
|---|---|---|
| Éléments (`*`) | 763 | 656 |
| dont descendants de `<svg>` | 442 | 441 (le `<h1>` invalide de `hero-titre.svg` a été retiré) |
| **DOM EcoIndex** | **321** | **215** |

Les 105 nœuds des 11 modales sont dans deux `<template>` (2 nœuds), les 3 `<script>` inline ont disparu.

## 4. Interactions (script `interactions.py`, Chromium, desktop et mobile)

26 vérifications par viewport, **52/52 OK** sur la version optimisée (et le même script passe sur la version d'origine, aux 2 vérifications près qui décrivent le nouveau comportement des vidéos) :

- loader retiré après chargement ; vidéo hero en lecture dès le chargement ;
- menu burger : ouverture, fermeture, fermeture au scroll ; ancres de navigation avec scroll fluide jusqu'à la bonne section (position identique au pixel à l'original) ;
- carrousel : slide active/suivante/précédente chargées au repos ; 9 clics « suivant » à 450 ms d'intervalle sans jamais tomber sur une slide non chargée ; retour « précédent » ; le bouton « Découvrez son histoire » suit la slide active ;
- modales : ouverture par le bouton, image et texte présents, fermeture par la croix et par clic sur le fond ; les 9 modales produits et les 2 modales du footer (dans le `<footer>`, même CSS) ;
- AOS : 13/13 éléments animés après scroll ;
- vidéos : chacune des 3 vidéos visibles est en lecture (`readyState` 4, non en pause) une fois dans la vue ; la copie mobile cachée de `gif.mp4` n'est jamais téléchargée (`readyState` 0) en desktop, et inversement ;
- toutes les images visibles hors carrousel chargées après scroll ;
- **console : 0 erreur, 0 requête en échec / 404** (les seuls messages du harnais sont les scripts tiers bloqués volontairement).

Firefox (Camoufox 0.5.8, le moteur d'ecoindex-cli et d'ecoindex.fr) : même test du carrousel, 18 clics à 350 ms, aucune slide non chargée ; vidéos en lecture ; DOM EcoIndex 215. Un premier essai avec le lazy-load natif seul montrait 2 slides non prêtes dans Firefox : d'où le préchargement des deux slides voisines ajouté dans `recipes.js`.

## 5. Requêtes et poids (Chromium, cache vide, scroll complet)

| | Avant | Après |
|---|---|---|
| Requêtes desktop | 79 (74 first-party + 5 tiers) | 47 (43 first-party + 4 tiers) |
| Requêtes mobile | 79 | 44 |
| gtag.js chargé sans consentement | oui | non |

La mesure de référence (ecoindex-cli, médiane de 3 runs, et estimation ecoindex.fr) est l'objet de l'étape 5 (`audit/ecoindex-after.md`).

## 6. Différences de comportement assumées (non visibles)

| Changement | Avant | Après |
|---|---|---|
| Google Analytics | `gtag.js` téléchargé dès le `<head>` pour tout le monde, `config` après consentement | script injecté **et** configuré après consentement Axeptio (même résultat pour un visiteur qui consent) |
| Vidéos « gif » et « centrale » | `autoplay` dès le chargement | lecture déclenchée un écran avant d'arriver dessus (`IntersectionObserver`, `rootMargin: 100%`) ; `preload="none"` sinon |
| Modales | présentes dans le DOM dès le départ, images chargées au démarrage | créées à la première ouverture ; images préchargées au survol / focus / touch du bouton. Ouverture au clavier sans survol préalable : l'image peut arriver ~100 ms après le texte (masqué par la transition de 300 ms) |
| Carrousel | 9 images chargées au démarrage | 5 chargées (active ± 2), les autres au fur et à mesure |
| Scripts inline | 3 blocs JS inline | 0 (le fallback « loader 5 s » est dans le module) |

## 7. À regarder pendant ta passe visuelle

1. **Qualité des images WebP** (q 85, q 92 pour les cookies des modales) : cartes du carrousel, photos des modales, mosaïque, produits de saison, carte Google Maps. SSIM (sur fond blanc) entre 0,92 et 0,99 selon l'image (détail dans le message du commit `4cc3c97`). Si une image te semble dégradée, elle peut être ré-encodée à une qualité plus haute ou en WebP sans perte, l'original est dans `archive/`.
2. **Qualité des 3 vidéos** ré-encodées (SSIM 0,982 / 0,983 / 0,972 par rapport à l'original) : hero, « gif » (photos qui défilent), vidéo centrale.
3. **Démarrage des vidéos** « gif » et centrale pendant le scroll (elles démarrent un écran avant d'être visibles).
4. **Première ouverture d'une modale** au clavier (Tab + Entrée sur « Découvrez son histoire », puis Mentions légales / RGPD).
5. Le carrousel en cliquant vite sur les flèches, dans ton navigateur habituel.
6. Le menu mobile, les liens d'ancre, la fermeture des modales au clic sur le fond.

## 8. Reproduire

```bash
# version optimisée
npm ci && npm run build && npm run serve          # http://localhost:4173
# scripts de vérification (Python 3.12, playwright, Pillow)
python -I <scratchpad>/scripts/shoot.py http://localhost:4173 audit/screenshots/after
python -I <scratchpad>/scripts/compare.py audit/screenshots/before audit/screenshots/after audit/screenshots/diff
python -I <scratchpad>/scripts/interactions.py http://localhost:4173 chromium
```

Les trois scripts sont copiés dans `audit/scripts/` pour pouvoir être rejoués.
