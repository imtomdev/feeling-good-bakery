# Plan d'optimisation EcoIndex — feelinggoodbakery.fr

> Rédigé le 25 octobre 2026 à partir de `audit/ecoindex-before.md` (mesure ecoindex.fr du 25/10/2026 11:34, résultat `https://www.ecoindex.fr/resultat/?id=0941c99b-2339-46c6-a19d-6e8256d0d2b0`) et de la lecture du repo (`index.html`, `src/`, `assets/`, `package.json`, build Vite 2.9.15 testé en local).
>
> Contrainte : zéro changement visuel ou fonctionnel (hors badge EcoIndex final). Chaque item porte un niveau de risque de régression : **nul** / **faible** / **à vérifier**.

## 1. Point de départ

| Métrique | Valeur ecoindex.fr | Quantile (sur 20) | Part de la pénalité |
|---|---|---|---|
| DOM | 321 éléments | 5,38 | 29 % (poids ×3 dans la formule) |
| Requêtes | 79 | 10,13 | 37 % (poids ×2) |
| Poids | 7 205 Ko | 18,68 | 34 % (poids ×1) |
| **Score** | **54,10 → 54 / D** | | |

Formule (ecoindex 5.10.0, vérifiée dans le source cnumr) : `score = 100 − 5 × (3·q_dom + 2·q_req + q_size) / 6`. Autour des valeurs actuelles, une requête vaut ≈ 0,19 point, un nœud DOM ≈ 0,04 point, et le poids ne compte presque plus au-delà de 5 Mo (quantiles très larges). **Conséquence : les requêtes et le DOM rapportent beaucoup plus que le poids**, tant qu'on reste au-dessus de ~2 Mo.

Deux faits mesurés qui orientent le plan :

1. **ecoindex.fr ne télécharge pas `intro.mp4` ni `video-centrale.mp4`** (785 et 781 octets comptés sur 20,2 Mo et 3,2 Mo réels). Seul `gif.mp4` (698 Ko, ×2) est compté en entier. Le ré-encodage des vidéos est donc indispensable pour les visiteurs réels et pour Lighthouse, mais rapporte peu sur le score ecoindex.fr. Corollaire : **rester en H.264/MP4** et ne pas passer en WebM/VP9, que le Firefox d'ecoindex.fr décoderait nativement et téléchargerait probablement en entier (+1,8 Mo comptés, ≈ −2 points).
2. **Le scraper compte `nb(*) − nb(descendants de <svg>)`** : inliner les SVG dans le HTML ne coûte rien en DOM, et le contenu d'un `<template>` n'est pas dans le document (non compté).

## 2. Score cible

| Scénario | DOM | Requêtes | Poids (Ko) | Score calculé | Grade |
|---|---|---|---|---|---|
| Actuel | 321 | 79 | 7 205 | 54,1 | D |
| Lot A seul (requêtes : SVG inline, doublon vidéo, gtag) | 321 | 47 | 6 164 | 61,8 | C |
| Lot A + B (images WebP, JS modulaire) | 321 | 47 | 4 461 | 62,7 | C |
| Lot A + B + C (modales en `<template>`) | 216 | 37 | 2 428 | 71,7 | B |
| + lot D optionnel (lazy slides Swiper) | 216 | 31 | 2 080 | 74,3 | B |

**Cible retenue : grade B, score 72 ± 3** (lots A + B + C). Hypothèses : DOM ≈ 216 (−105 nœuds de modales, +2 `<template>`… arrondi 216–220), requêtes ≈ 37–40, poids ≈ 2 000–2 500 Ko. La marge couvre : le poids réel du HTML une fois les SVG inlinés et gzippés (estimé ~100 Ko), le comportement d'ecoindex.fr sur les MP4 ré-encodés, et ±2 requêtes de tiers (Axeptio). Le lot D peut amener à 74–76 mais demande une vérification visuelle du carrousel.

Réduction attendue par métrique :

| Métrique | Avant | Après (cible) | Réduction | Points gagnés (approx.) |
|---|---|---|---|---|
| Requêtes | 79 | 37–40 | −50 % | ≈ +8 |
| DOM | 321 | ~216–220 | −32 % | ≈ +4 |
| Poids | 7 205 Ko | ~2 000–2 500 Ko | −68 % | ≈ +5,5 |

Grade A (> 80) n'est **pas atteignable sans concession visuelle/fonctionnelle** (voir § 5) : il faudrait descendre vers 25 requêtes / 1 Mo / 200 nœuds, ce qui impose de supprimer des polices, le bandeau Axeptio ou des images.

## 3. Changements proposés, classés par gain/effort

Légende effort : S (< 1 h), M (1–3 h), L (> 3 h). Gain exprimé sur les métriques ecoindex.fr ; « réel » = ce que paie un visiteur Chrome.

### Lot A — Requêtes (gain fort, effort faible)

| # | Changement | Fichiers | Gain estimé | Risque |
|---|---|---|---|---|
| A1 | **Inliner les 15 SVG au build** au lieu de SVGInjector (`<img class="js-inject-me">` + XHR = 31 requêtes pour 16 fichiers). Petit plugin Vite `transformIndexHtml` qui remplace chaque `<img class="js-inject-me" src="x.svg" title=… alt=…>` par le contenu du SVG, en recopiant `class`, `title`, `alt` sur la balise `<svg>` (SVGInjector fait exactement ça, les sélecteurs CSS `svg[title^="facebook-"]`, `svg[title="burger-icon"]`, `.cls-1`, `svg path` continuent de matcher). Suppression de `svg-injector` et de `functions.js`. Nettoyer la balise `<h1>` invalide présente dans `hero-titre.svg` (non rendue aujourd'hui ; en HTML inline elle casserait le parseur) → remplacée par `<title>`. | `index.html`, `vite.config.js` (nouveau), `src/js/main.js`, `src/js/functions.js` (supprimé), `package.json`, `assets/img/hero-titre.svg` | **−30 requêtes** (31 → favicon seul). Poids : −272 Ko de fichiers SVG, +~100 Ko de HTML (le HTML est la seule ressource gzippée par nginx ; les SVG partent aujourd'hui en clair). JS : −4,6 Ko (svg-injector). DOM : 0 (les descendants de `<svg>` ne sont pas comptés). | **faible** — même DOM final que SVGInjector ; à contrôler : les icônes qui changent de couleur au survol (flèches Swiper, réseaux sociaux) et l'opacité burger/croix. Pas de flash d'image avant injection : amélioration invisible. |
| A2 | **Ne charger qu'une fois `gif.mp4`** : la `<video class="gif mobile">` (masquée en desktop) télécharge quand même la vidéo. Remplacer `src` par `data-src` sur les deux `<video>` « gif » et ajouter 15 lignes de JS : au chargement et au changement de `matchMedia("(max-width: 1024px)")`, affecter `src` à la vidéo dont `display !== "none"` et appeler `play()`. | `index.html`, `src/js/main.js` (ou nouveau `src/js/videos.js`) | **−1 requête, −698 Ko** (−~300 Ko après ré-encodage B5) | **faible** — la vidéo visible démarre exactement comme avant (autoplay muted) ; la vidéo cachée n'est plus téléchargée. |
| A3 | **Charger `gtag.js` seulement après consentement Axeptio.** Aujourd'hui `<script async src="…gtag/js">` est dans le `<head>` et se charge avant tout consentement ; seul `gtag('config')` attend le callback. Déplacer la création du `<script>` dans le callback `cookies:complete` quand `choices.google_analytics` est vrai. | `index.html` | **−1 requête, −171 Ko** sur ecoindex.fr (Axeptio y est chargé, mais personne ne consent) | **nul visuellement** — fonctionnel : identique pour un visiteur qui consent (GA se charge puis `config`) ; conforme RGPD. |
| A4 | **`cross-modal.png`** (11 occurrences, 1 requête de 186 o) : devient inutile côté requêtes avec C1 (chargé à l'ouverture). Alternative sans C1 : l'inliner en data-URI (`<img src="data:image/png;base64,…">`, 11 × 250 o dans le HTML). | `index.html` | −1 requête | nul |

Sous-total lot A : **−33 requêtes**, −~1 040 Ko.

### Lot B — Poids (gain moyen sur le score, fort pour les visiteurs)

| # | Changement | Fichiers | Gain estimé | Risque |
|---|---|---|---|---|
| B1 | **Convertir les 20 PNG photographiques en WebP** (9 recettes du carrousel, 9 produits des modales, chocolat gauche/droite), **sans redimensionner** (ils sont affichés à ~1,4× leur taille CSS sur écran Retina ; réduire baisserait la netteté). Encodage `cwebp -q 85 -m 6 -sharp_yuv -alpha_q 100` ; conversions test faites (q 80) : recettes 1 684 Ko → ~530 Ko, produits 2 033 Ko → ~580 Ko, chocolats 248 Ko → 46 Ko. `<img src="x.webp">` simple : WebP est supporté par tous les navigateurs depuis 2020 (Safari 14) ; pas de `<picture>`, qui ajouterait 2 nœuds par image (+54 nœuds = −2 points). AVIF écarté pour la même raison (gain supplémentaire ~250 Ko, insuffisant face au coût DOM d'un `<picture>`). | `assets/img/recipes/*.png` → `.webp`, `assets/img/chocolat-*.png` → `.webp`, `index.html` | **−2 800 Ko** environ (dont 1 450 Ko sur les 9 produits si C1 n'est pas retenu ; avec C1 ces 9 images ne sont plus comptées du tout) | **à vérifier** — compression lossy avec alpha : visuellement indiscernable à q 85 mais pas identique au pixel. Je fournirai une comparaison DSSIM par image et des captures côte à côte. Si tu veux du strictement sans perte : WebP lossless (gain ~30 % seulement). |
| B2 | **Convertir les 10 JPG en WebP** (visuels, mosaïque, équipe, carte Google Maps en CSS). Test q 80 : 700 Ko → ~440 Ko. `carte-de-france.png` (12 Ko) et `ellipse.png` (1 Ko) : laisser. | `assets/img/*.jpg` → `.webp`, `index.html`, `src/scss/style.scss` | **−260 Ko** | **à vérifier** (même remarque que B1, re-compression d'un JPG déjà compressé : q 85 recommandé) |
| B3 | **Swiper modulaire** : `import Swiper, { Navigation } from "swiper"` + `swiper/css` + `swiper/css/navigation` au lieu de `swiper/bundle` + `swiper-bundle.css`. Mesuré avec esbuild : Swiper core + Navigation + AOS = 81,5 Ko contre 164 Ko pour le bundle actuel. CSS : 16 Ko → 7 Ko. | `src/js/recipes.js` | **−80 Ko JS, −9 Ko CSS** (ressources non gzippées par nginx, donc gain plein) | **faible** — mêmes options (`loop`, `navigation`, `allowTouchMove:false`), même version 8.4.4. Le CSS de la police d'icônes `swiper-icons` (data-URI) disparaît : non utilisée (les flèches sont des SVG maison). |
| B4 | **Purger le CSS d'AOS** : `aos.css` (28 Ko) contient ~40 animations ; le site utilise `fade-up/down/left/right` uniquement. Option a) importer uniquement les règles nécessaires via une copie locale réduite (`src/scss/vendor/_aos.scss`) ; option b) PurgeCSS avec safelist `aos-*`. Je recommande a) (déterministe). | `src/js/main.js`, `src/scss/vendor/_aos.scss` (nouveau) | **−22 Ko CSS** | **à vérifier** — les 4 animations, `duration:600`, easing et `[data-aos][data-aos-duration]` doivent rester identiques ; test visuel des sections animées. |
| B5 | **Ré-encoder les 3 MP4** en H.264 (rester en MP4, cf. § 1), même définition, même cadence, sans piste audio (les vidéos sont `muted`), `+faststart` : `intro.mp4` 20 163 Ko → **2 500 Ko à CRF 24** (1 814 Ko à CRF 26) ; `video-centrale.mp4` 3 209 Ko → **1 897 Ko à CRF 26** ; `gif.mp4` (4 images à 1 i/s) 698 Ko → **403 Ko à CRF 28** (317 Ko à CRF 30). Encodages test déjà faits (ffmpeg 9, libx264 preset slow). | `assets/videos/*.mp4` | ecoindex.fr : **−300 Ko** (seul `gif.mp4` est compté). **Réel : −19 000 Ko**, LCP mobile 21,7 s → ~3 s, et ecoindex-cli local redevient comparable. | **à vérifier** — qualité perçue : CRF 24 sur une vidéo 1080p déjà compressée est en pratique transparent ; je fournis les deux CRF pour arbitrage sur captures d'images fixes (frames identiques, pas de recadrage). |
| B6 | **Loader GIF → WebP animé** (`eat-cookie.gif` 32 Ko, 2 images) : `gif2webp` conserve les délais d'image ; 28 Ko en lossy q 90, ~30 Ko en lossless. Règle la pratique RWEB_0099 « limiter les GIF animés ». | `assets/videos/eat-cookie.gif` → `assets/img/eat-cookie.webp`, `index.html` | −4 Ko, +1 bonne pratique RWEB | faible (lossless : identique) |
| B7 | **Polices** : ne garder que `woff2` dans les `@font-face` (le `woff` n'est jamais demandé par un navigateur moderne : 0 requête gagnée, mais nettoyage) ; supprimer les déclarations jamais utilisées (`bodoni-book`, `bodoni-bold`, `poppins-medium` : 500 déclaré dans le SCSS mais jamais téléchargé en prod). Sous-setter `bodoni-book-italic.woff2` (35 Ko) en Latin-1 + ponctuation typographique → ~15 Ko. | `src/scss/_fonts.scss`, `assets/fonts/` | −20 Ko (sous-set) | sous-set : **à vérifier** (risque de glyphe manquant : « » ’ … œ) ; le reste : nul |

Sous-total lot B : −~3 200 Ko sur ecoindex.fr (−~22 000 Ko réels), −1 requête (gif).

### Lot C — DOM (gain fort, effort moyen)

| # | Changement | Fichiers | Gain estimé | Risque |
|---|---|---|---|---|
| C1 | **Modales dans `<template>`** : les 9 modales produits (`section.modals`, 67 nœuds) et les 2 modales du footer (mentions légales + RGPD, 38 nœuds) sont rendues dans le DOM avec `opacity:0`. Les placer dans un `<template>` par groupe (2 nœuds au total) ; `modal.js` clone la modale à la première ouverture puis la réutilise (même markup, mêmes classes `.modal.open`, même `section.bg`, même transition 0,3 s). Les 9 PNG produits ne sont alors chargés qu'à l'ouverture. **Pour éviter toute latence visible à la première ouverture**, précharger l'image au `mouseenter` / `focus` / `touchstart` du bouton « Découvrez son histoire » (une `new Image()` de ~60 Ko WebP, soit < 100 ms sur 4G, masqués par la transition de 300 ms). | `index.html`, `src/js/components/modal.js`, `src/js/recipes.js` (le bouton lit `data-id` de la slide active : inchangé) | **−103 nœuds DOM** (−105 + 2) ≈ **+4 points** ; **−10 requêtes** (9 PNG produits + `cross-modal.png`) ; **−2 033 Ko** (−580 Ko si B1 fait avant) | **faible** — fonctionnel : la modale et son texte sont identiques ; seule différence possible : première ouverture sans survol préalable (clavier, lecteur d'écran) → l'image apparaît ~100 ms après le texte. À signaler si tu veux l'interdire ; dans ce cas, variante C1-bis : garder les images en chargement immédiat (gain DOM identique, −1 requête seulement). |
| C2 | Doublons mobiles (`h2.mobile` : 3 nœuds, `div.mobile` de la mosaïque : 5 nœuds, `video.gif.mobile` : 1) | — | −9 nœuds | **non retenu** : nécessiterait de réordonner le DOM par CSS (`order`, grid) avec risque de décalage ; gain 0,35 point. Listé pour mémoire. |
| C3 | Clones Swiper (`loop:true`, 2 slides dupliquées = 4 nœuds) | — | −4 nœuds | **non retenu** : `loop` fait partie du comportement (navigation circulaire). |

### Lot D — Optionnel, à vérifier visuellement

| # | Changement | Fichiers | Gain estimé | Risque |
|---|---|---|---|---|
| D1 | **`loading="lazy"` sur les 9 images du carrousel** (seules la slide active et ses voisines sont dans la zone de préchargement de Chrome/Firefox). | `index.html` | −5 à −6 requêtes, −300 Ko | **à vérifier** — au clic sur une flèche, la slide suivante doit être déjà chargée (Chrome précharge à 1 250 px, Firefox à ~ 1 écran) ; sinon, flash d'image blanche pendant la transition. Test Camoufox/Firefox obligatoire puisque c'est le moteur d'ecoindex.fr. Si le test montre un flash : abandon. |
| D2 | **`loading="lazy"` + `decoding="async"`** sur les images sous la ligne de flottaison (mosaïque, saison, carte) | `index.html` | 0 sur ecoindex.fr (le scraper scrolle jusqu'en bas et attend 3 s : tout se charge). Gain réel pour les visiteurs qui ne scrollent pas. | **nul** visuellement (images chargées ~1 écran avant d'apparaître) |
| D3 | **Vidéos `video-centrale` et `gif` sous la ligne de flottaison** : `preload="none"` + `data-src`, `src` affecté par IntersectionObserver avec `rootMargin: 100%`. `intro.mp4` (hero) reste immédiat. | `index.html`, `src/js/videos.js` | 0 sur ecoindex.fr. Réel : −2,3 Mo pour un visiteur qui ne scrolle pas. | **faible** — démarrage de la lecture un écran avant d'arriver dessus ; comportement identique à l'œil si la connexion suit (fichiers de 0,4 et 1,9 Mo après B5). |
| D4 | **`width`/`height` explicites** sur les `<img>` (CLS 0,565 en desktop, 0,302 en mobile). Nécessite une règle `img { height: auto }` globale pour que les largeurs CSS existantes gardent le ratio. | `index.html`, `src/scss/style.scss` | 0 sur EcoIndex ; Lighthouse CLS → ~0 | **à vérifier** — toute image dont la CSS fixe une hauteur (`.mosaic .mobile img { height:100% }`) doit être contrôlée ; comparaison pixel avant/après indispensable. |
| D5 | **SVGO** sur les 16 SVG (chocolat 69 → 45 Ko, sac-blé 42 → 35 Ko, œufs 36 → 31 Ko, hero 85 → 77 Ko) avec config conservatrice (ne pas toucher aux IDs/classes, précision 3). | `assets/img/**/*.svg` | −45 Ko sur le HTML inliné (~−15 Ko gzippés) | **à vérifier** — rendu vectoriel : comparaison de rendu raster avant/après à 2× ; gain faible, je le mets en dernier. |
| D6 | **Feuille `@media print`** minimale (masquer vidéos, loader, bandeau) : règle RWEB_0031 « fournir une CSS print » | `src/scss/_print.scss` | 0 sur le score, +1 bonne pratique | nul à l'écran |
| D7 | **Externaliser le JS inline** (snippet gtag/Axeptio/loader → dans `main.js`) : RWEB_0042. Les deux JSON-LD restent inline (données SEO). | `index.html`, `src/js/main.js` | 0 sur le score, +1 bonne pratique ; le `setTimeout(5000)` du loader et l'init Axeptio passent dans le module (différé) | **faible** — l'init Axeptio se fait quelques dizaines de ms plus tard ; le fallback loader 5 s doit rester. |

### Hygiène du repo (aucun effet sur le score, demandé dans la mission)

Mettre de côté (liste dans `audit/removed-assets.md`, pas de suppression définitive) les fichiers d'`assets/` jamais référencés par `index.html` ni le SCSS — Vite ne les copie déjà pas dans `dist/` :

- doublons PNG des JPG : `carte-gmap.png`, `equipe.png`, `mosaique-cookie-{1,2,3,4}.png`, `visuel-cookie-{1,2}.png`, `visuel-icecream.png`, `visuel-wookie.png` (≈ 4,5 Mo) ;
- `video1titre.png` (331 Ko, 4284×1634), `intro.gif` (1,1 Mo), `chouchou-beignet.png` + `chouchou-beignet-recette.png` (recette absente du site) ;
- sources de polices : `Bodoni 72.ttc` (418 Ko), `Poppins-*.ttf` (5 × ~260 Ko), et les `.woff` si B7 est retenu ;
- après B1/B2/B5 : les PNG/JPG/MP4 d'origine remplacés par les WebP/MP4 ré-encodés (conservés pour pouvoir ré-encoder à une autre qualité).

Corriger aussi le double slash `./assets//img/visuel-*.jpg` (cosmétique).

## 4. Hors scope / côté hébergeur (à documenter, pas à faire ici)

Mesuré sur la prod : nginx/1.18.0, **HTTP/1.1 uniquement**, gzip sur `text/html` seulement, **aucun `Cache-Control`/`Expires`** malgré des noms de fichiers hashés par Vite, WOFF2 servi en `application/octet-stream`. Recommandations à passer à l'hébergeur (fichier `audit/server-recommendations.md` à produire à l'étape 5) :

```nginx
http2 on;                                   # ou "listen 443 ssl http2;" selon la version
gzip on; gzip_types text/css application/javascript image/svg+xml font/woff2 application/json;
# brotli_static / brotli on; brotli_types ... (module ngx_brotli si disponible)
location ~* \.(?:js|css|woff2|webp|png|jpg|svg|mp4)$ { expires 1y; add_header Cache-Control "public, immutable"; }
types { font/woff2 woff2; image/webp webp; }
```

Effet attendu sur ecoindex.fr (1re visite, cache vide) : compression du JS/CSS/SVG restants ≈ −60 Ko (après lot B les ressources texte ne pèsent plus que ~90 Ko) ; le cache n'agit que sur les visites suivantes ; HTTP/2 ne change ni requêtes ni poids. Ces trois points règlent les pratiques RWEB_0075, RWEB_0076 et RWEB_0083 affichées en échec sur ecoindex.fr, mais **pas le score**.

Également hors scope car ils changeraient le rendu ou le fonctionnement :

- bandeau Axeptio (3 requêtes, 301 Ko) : obligatoire pour le consentement GA ;
- Google Analytics lui-même ;
- réduire le nombre de graisses de polices (5 fichiers) ;
- supprimer le carrousel, les vidéos d'ambiance, le loader de 5 s ;
- mise à jour de Vite : le build 2.9.15 fonctionne sous Node 26 sans avertissement, la CI Travis est en Node 18 ; une montée en Vite 5/6 n'apporte rien de mesurable sur ce site et touche la CI → non proposée.

## 5. Peut-on faire mieux ? (pour information, non réalisé)

Gains restants qui **exigent une concession** visuelle ou fonctionnelle :

| Levier | Gain | Concession |
|---|---|---|
| Supprimer Axeptio + GA | −4 requêtes, −470 Ko ≈ +1,5 pt | plus de statistiques de fréquentation |
| Passer à 2 graisses de Poppins au lieu de 4 | −2 requêtes, −32 Ko ≈ +0,5 pt | typographie modifiée |
| Supprimer la vidéo `gif.mp4` ou la remplacer par une image fixe | −1 requête, −400 Ko | contenu modifié |
| Supprimer le loader de 5 s | −1 requête, −28 Ko | comportement modifié |
| Charger les slides du carrousel à la demande (Swiper virtual) | −6 à −8 requêtes | flash possible à la navigation |

Avec tout cela, on approcherait 80 (grade A limite). Sans concession, le plafond réaliste est **B, 72–76**.

## 6. Ordre d'exécution proposé (étape 3)

1. Branche `eco/ecoindex`, captures de référence `audit/screenshots/before/` (desktop 1920×1080 et mobile 390×844, page entière + chaque section).
2. Lot A (A1 → A2 → A3 → A4), un commit par item ; build ; captures intermédiaires.
3. Lot B (B5 vidéos, B1/B2 images, B3 Swiper, B4 AOS, B6 loader, B7 polices).
4. Lot C1.
5. Lot D selon ton arbitrage.
6. Hygiène repo + `audit/removed-assets.md`.
7. Vérification (étape 4) : build sans warning, captures `after/`, diff pixel, interactions, console.

## 7. Décisions attendues

1. **C1 (modales en `<template>`)** : OK avec le préchargement au survol ? Ou variante C1-bis (images chargées immédiatement, gain DOM seul) ?
2. **B1/B2 (WebP lossy)** : q 85 avec comparaison DSSIM fournie, ou lossless uniquement ?
3. **B5 (vidéos)** : CRF 24 (2,5 Mo) ou 26 (1,8 Mo) pour `intro.mp4` ; CRF 26 ou 28 pour `video-centrale` ; CRF 28 ou 30 pour `gif.mp4` ? Je peux fournir des frames extraites côte à côte avant de trancher.
4. **Lot D** : lesquels inclure (D1 carrousel lazy, D2/D3 lazy sous la ligne de flottaison, D4 width/height, D5 SVGO, D6 print, D7 JS externalisé) ?
5. **B7** : sous-setter Bodoni (gain 20 Ko, risque glyphe) ou laisser ?

## 8. Décisions prises (25/10/2026)

| Question | Décision |
|---|---|
| C1 modales | **Oui** : modales en `<template>`, créées au clic, image préchargée au survol/focus/touch du bouton |
| B1/B2 WebP | **Qualité 85** (lossy), captures avant/après fournies |
| B5 vidéos | **Qualité haute** : intro CRF 24 (~2,5 Mo), video-centrale CRF 26 (~1,9 Mo), gif CRF 28 (~0,4 Mo) |
| Lot D | **D1, D2, D3, D4, D6, D7 retenus**. D5 (SVGO) et B7 sous-set Bodoni écartés : gain < 0,2 point, risque de rendu non nul |
