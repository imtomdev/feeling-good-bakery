# Estimation EcoIndex « après » — branche `eco/ecoindex`

> 25 octobre 2026. Rien n'est déployé : le score réel ne sera connu qu'après mise en production et analyse sur ecoindex.fr (procédure obligatoire, § 7). Ce document donne une **estimation chiffrée** à partir de la mesure locale et du biais de calibration mesuré à l'étape 1.

## 1. Tableau de synthèse

| Métrique | Avant (ecoindex.fr, prod, 25/10 11:34) | Après (local brut, ecoindex-cli) | Après (estimé ecoindex.fr) | Cible (plan) |
|---|---|---|---|---|
| DOM (éléments) | 321 | **215** (218 avec le badge) | **218** (badge compris) | 216–220 |
| Requêtes HTTP | 79 | **37** | **38** (37 + badge) | 37–40 |
| Poids transféré (Ko) | 7 205 | **6 634** | **≈ 2 340** (fourchette 1 940 – 6 740, § 3) | 2 000–2 500 |
| Score | 54,10 → **54** | 67,93 → **68** | **71,6 → 72** (fourchette 68 – 73, badge compris) | 72 ± 3 |
| Note | **D** | C | **B** (C si scénario pessimiste) | B |
| GES (gCO2e / vue) | 1,92 | 1,64 | ≈ 1,57 | |
| Eau (cl / vue) | 2,88 | 2,46 | ≈ 2,35 | |

Incertitude : ± 1 point sur le scénario central ; le seul risque de sortir de la cible est le traitement des vidéos par ecoindex.fr (§ 3.3), qui ferait tomber le score à 68 (C) dans le pire cas.

**Mesure de vérité du 26/10/2026 (§ 9) : 218 / 38 / 2 341,5 Ko → 72 B**, identique au scénario central.

## 2. Mesure locale brute (ecoindex-cli)

Même outil, même version, mêmes paramètres qu'à l'étape 1 : ecoindex-cli 2.32.0 (lib ecoindex 5.10.0, scraper 3.18.0, Camoufox 0.5.8), fenêtre 1920×1080, 3 s avant et après scroll. Site servi par `npm run build && npm run serve` (`vite preview`, port 4173) au commit `17a3597`.

```bash
<scratchpad>/venv/bin/ecoindex-cli analyze --url http://localhost:4173 --no-interaction --export-format json --output-file <scratchpad>/ecoindex-cli/final-runN.json
```

| Run | Heure | DOM | Requêtes | Poids (Ko) | Score | Note |
|---|---|---|---|---|---|---|
| 1 | 13:44:48 | 215 | 37 | 6 634,209 | 68 | C |
| 2 | 13:45:15 | 215 | 37 | 6 634,249 | 68 | C |
| 3 | 13:45:40 | 215 | 37 | 6 634,229 | 68 | C |
| **Médiane** | | **215** | **37** | **6 634,229** | **68** | **C** |

Pour mémoire, le même CLI sur le build local de la branche `dev` (avant) donne 321 / 79 / 30 084 Ko / 54 D, c'est-à-dire la même chose que sur la prod (321 / 78 / 30 407 / 54) à gtag.js près : le serveur local reproduit fidèlement le comportement du scraper.

Détail des 37 requêtes (poids transféré, Ko) :

| Ressource | Type | Ko |
|---|---|---|
| intro.mp4 | vidéo | 2 499,9 |
| video-centrale.mp4 | vidéo | 1 897,2 |
| gif.mp4 | vidéo | 403,1 |
| static.axept.io/sdk.js (tiers) | JS | 205,6 |
| / (HTML, SVG inlinés, gzip) | HTML | 128,8 |
| static.axept.io/datacenter-ranges.js (tiers) | JS | 92,0 |
| 9 cartes recettes .webp (carrousel) | images | 630,4 |
| 4 mosaïque .webp | images | 229,3 |
| carte-gmap, visuel-wookie, equipe, visuel-cookie-2, visuel-cookie-1, visuel-icecream .webp | images | 312,6 |
| chocolat-droite, chocolat-gauche .webp | images | 54,5 |
| eat-cookie.webp (loader) | image | 26,0 |
| carte-de-france.png | image | 12,9 |
| 5 polices .woff2 | polices | 100,9 |
| index.js (gzip) | JS | 28,5 |
| index.css (gzip) | CSS | 8,8 |
| client.axept.io … .json (tiers) | JSON | 3,7 |
| **Total** | **37 requêtes** | **6 634,2** |

Vite preview compresse HTML, JS et CSS (gzip), ce que nginx en prod ne fait que pour le HTML (§ 3.2).

## 3. Passage du local à ecoindex.fr : calcul

### 3.1 Biais de calibration de l'étape 1

| Métrique | ecoindex.fr (prod) | ecoindex-cli (prod) | Écart | Cause identifiée |
|---|---|---|---|---|
| DOM | 321 | 321 | 0 | — |
| Requêtes | 79 | 78 | +1 | gtag.js bloqué par uBlock Origin dans le CLI |
| Poids | 7 204,6 Ko | 30 407,2 Ko | −23 202,6 Ko | intro.mp4 (−20 163,4), video-centrale.mp4 (−3 208,3) non téléchargés par ecoindex.fr (≈ 0,8 Ko chacun), gtag.js (+171,0) |

Le biais n'est pas un ratio global : il se décompose ressource par ressource. On l'applique donc **ressource par ressource** aux nouvelles valeurs.

### 3.2 Application

| Étape | Requêtes | Poids (Ko) |
|---|---|---|
| Local brut (médiane) | 37 | 6 634,2 |
| gtag.js : n'est plus chargé du tout (après consentement seulement) → écart de calibration devenu nul | +0 | +0 |
| intro.mp4 : ecoindex.fr n'en télécharge que ~0,8 Ko (comportement observé à l'étape 1, même conteneur MP4/H.264, `+faststart`) | 0 | −2 499,9 + 0,8 |
| video-centrale.mp4 : idem | 0 | −1 897,2 + 0,8 |
| gif.mp4 : comptée en entier à l'étape 1 → on la garde en entier (403,1) | 0 | 0 |
| **Sous-total après calibration** | **37** | **2 238,7** |
| nginx prod : HTML en gzip niveau 1 (141,5 Ko mesuré avec `gzip -1`) au lieu du gzip de vite preview (128,8) | 0 | +12,7 |
| nginx prod : JS **non compressé** (90,9 Ko au lieu de 28,5) | 0 | +62,4 |
| nginx prod : CSS **non compressé** (35,5 Ko au lieu de 8,8) | 0 | +26,7 |
| Badge EcoIndex dans le footer (étape 6) : 1 requête tierce, SVG de 643 o servi en brotli | +1 | +0,7 |
| **Estimé ecoindex.fr** | **38** | **≈ 2 341** |

Hypothèses : pas de cache (1re visite), Axeptio chargé comme à l'étape 1 (3 requêtes, 301 Ko), pas de consentement donc pas de GA.

### 3.3 Ce que le local ne reproduit pas, et dans quel sens

- **Compression serveur** : nginx ne gzippe que le HTML. L'estimation ci-dessus l'intègre (+102 Ko par rapport au local), elle est donc **pessimiste** sur ce point par rapport à un hébergeur bien configuré (−89 Ko, +0,4 point si gzip/brotli étaient activés sur JS/CSS, voir `audit/server-recommendations.md`).
- **Cache** : aucun en-tête `Cache-Control` en prod. Sans effet sur une 1re visite (ce que mesure ecoindex.fr), donc sans effet sur l'estimation.
- **Vidéos** : c'est la seule vraie inconnue. À l'étape 1, ecoindex.fr a compté `gif.mp4` en entier mais pas `intro.mp4` ni `video-centrale.mp4` (≈ 0,8 Ko) ; la cause exacte n'a pas pu être établie (les profils H.264 ne l'expliquent pas : gif et centrale étaient tous deux en profil Main). Les trois fichiers ont été ré-encodés (profil High, `+faststart`), le comportement peut donc changer dans un sens ou dans l'autre :
  - **scénario central** (même comportement qu'à l'étape 1, fichier par fichier) : 2 341 Ko → **72 B** ;
  - **scénario optimiste** (gif.mp4 non comptée non plus) : 1 940 Ko → 72,9 → **73 B** ;
  - **scénario pessimiste** (les 3 vidéos comptées en entier, comme le CLI local) : 6 737 Ko → 67,7 → **68 C**.
  Dans tous les cas, le poids réellement téléchargé par un visiteur Chrome passe de ≈ 29 Mo à ≈ 6,7 Mo.

## 4. Contre-vérification à la main (formule officielle EcoIndex 5.10.0)

`score = 100 − 5 × (3·q_dom + 2·q_req + q_size) / 6`, quantile = `i − 1 + (valeur − Q[i−1]) / (Q[i] − Q[i−1])` sur les tables officielles (source `cnumr/ecoindex_python_fullstack`, reprise dans `audit/scripts/ecoindex_score.py`).

Scénario central (215 nœuds, 38 requêtes, 2 341 Ko) :

- `q_dom(215) = 3 + (215 − 159) / (233 − 159) = 3,757`
- `q_req(38) = 4 + (38 − 34) / (42 − 34) = 4,500`
- `q_size(2341) = 13 + (2341 − 2142,06) / (2465,37 − 2142,06) = 13,615`
- `score = 100 − 5 × (3 × 3,757 + 2 × 4,500 + 13,615) / 6 = 100 − 5 × 33,886 / 6 = 71,76` → **72, B** (B = score > 70)
- GES = 2 + 2 × (50 − 71,76) / 100 = **1,56 gCO2e** ; eau = 3 + 3 × (50 − 71,76) / 100 = **2,35 cl**

Vérification du même calcul sur les valeurs locales (215 / 37 / 6 634,2) : `q_req = 4,375`, `q_size = 18,468`, score 67,93 → 68 C, identique à la sortie du CLI. Et sur la référence prod (321 / 79 / 7 205) : 54,10 → 54 D, identique à ecoindex.fr.

Contribution de chaque métrique à la pénalité (scénario central) : DOM 11,27 (33 %), requêtes 9,00 (27 %), poids 13,62 (40 %). **Le poids est redevenu la première composante** : c'est là que se trouvent les gains restants.

## 5. Cible atteinte ?

Cible du plan : B, 72 ± 3. Scénario central : **72 B, atteinte**. Scénario pessimiste : 68 C, cible manquée de 1 point à cause d'une seule chose : les 4,4 Mo des deux vidéos `intro.mp4` et `video-centrale.mp4` si ecoindex.fr se met à les télécharger. Rien d'autre ne peut faire basculer le résultat : DOM et requêtes sont mesurés à l'identique en local et sur ecoindex.fr (vérifié à l'étape 1).

## 6. Peut-on faire mieux ?

### 6.1 Sans concession visuelle ni fonctionnelle (gains restants)

| Levier | Gain estimé | Points | Remarque |
|---|---|---|---|
| Activer gzip/brotli sur JS, CSS (hébergeur, `audit/server-recommendations.md`) | −89 Ko (−120 Ko en brotli, HTML compris) | +0,4 | hors repo |
| Réduire encore `video-centrale.mp4` (CRF 28 : 1,5 Mo) et `gif.mp4` (CRF 30 : 0,3 Mo) | −0,5 Mo réels ; −0,1 Mo sur ecoindex.fr | +0,05 (scénario central) / +0,4 (pessimiste) | à juger à l'œil |
| SVGO conservateur sur les 16 SVG inlinés (chocolat 69 → 45 Ko, etc.) | −45 Ko bruts, ≈ −15 Ko gzip | +0,07 | rendu vectoriel à vérifier |
| Sous-setter `bodoni-book-italic.woff2` (35 Ko → ~15 Ko) | −20 Ko | +0,1 | risque de glyphe manquant |
| Carte Google Maps : recadrer `carte-gmap.webp` à la zone réellement affichée (1481×459 pour une zone de 46 rem de haut) | −30 Ko | +0,15 | à vérifier au pixel |
| 9 nœuds DOM : doublons mobiles (`h2.mobile`, `div.mobile` de la mosaïque, `video.gif.mobile`) remplacés par une seule version réordonnée en CSS | −9 nœuds | +0,3 | risque de décalage, non retenu dans le plan |
| HTTP/2, `Cache-Control`, `font/woff2` (hébergeur) | 0 sur la 1re visite | 0 | bonnes pratiques RWEB_0075/0083, visites suivantes |

Total réaliste sans concession : ≈ +1 point (73). Le grade A (> 80) reste hors d'atteinte : il faudrait ≈ 25 requêtes et ≈ 1 Mo.

### 6.2 Avec concession visuelle ou fonctionnelle (non réalisés, pour information)

| Levier | Gain | Points | Concession |
|---|---|---|---|
| Supprimer Axeptio + Google Analytics | −3 requêtes, −301 Ko | +1,3 | plus de statistiques de fréquentation (ou GA sans bandeau n'est pas conforme) |
| Remplacer `gif.mp4` (4 photos qui défilent) par une image fixe ou un `<picture>` | −1 requête, −403 Ko | +1,4 (scénario central) | animation supprimée |
| Supprimer la vidéo centrale (1,9 Mo réels) | −1 requête ; 0 Ko sur ecoindex.fr, −1,9 Mo réels | +0,2 (+5 dans le scénario pessimiste) | contenu supprimé |
| 2 graisses Poppins au lieu de 4 (light + semibold) | −2 requêtes, −33 Ko | +0,5 | typographie modifiée |
| Supprimer le loader animé | −1 requête, −26 Ko | +0,3 | comportement modifié |
| Carrousel sans `loop` (pas de clones) | −4 nœuds | +0,15 | navigation non circulaire |
| Carte Google Maps en lien texte sans image | −1 requête, −69 Ko | +0,5 | visuel supprimé |

Tout cumulé : ≈ 77–78, toujours B. Le A demanderait en plus de renoncer aux polices personnalisées et au carrousel.

## 7. Après déploiement : mesure de vérité

1. Ouvrir `https://bff.ecoindex.fr/redirect/?url=https://feelinggoodbakery.fr` (à l'étape 1 cette URL a renvoyé sur l'accueil d'ecoindex.fr sans lancer l'analyse ; dans ce cas, lancer l'analyse depuis le formulaire de l'accueil avec `https://feelinggoodbakery.fr`).
2. Relever sur `https://www.ecoindex.fr/resultat/?id=…` : score, note, DOM, requêtes, poids, GES, eau, date, et l'URL du résultat.
3. Comparer au tableau du § 1 : DOM attendu 215 (218 avec le badge, § 8), requêtes 38, poids ≈ 2,3 Mo. Si le poids est à ≈ 6,7 Mo, c'est le scénario pessimiste (vidéos comptées) : la marge de manœuvre est alors le § 6.1 (vidéos plus compressées) ou, avec concession, la suppression de la vidéo centrale.

## 8. Badge EcoIndex (étape 6)

Le badge officiel (`https://bff.ecoindex.fr/badge/?theme=light&url=https://feelinggoodbakery.fr`) est ajouté dans le footer, thème `light` (fond blanc du footer). Il affiche la **dernière analyse connue** d'ecoindex.fr pour l'URL : aujourd'hui la note D du 25/10/2026 ; il ne montrera le nouveau score qu'après déploiement et nouvelle analyse de la prod sur ecoindex.fr (§ 7). Impact mesuré en local avec ecoindex-cli (run du 25/10 13:52, build avec badge) : 218 nœuds (+3 : `li`, `a`, `img`), 38 requêtes (+1, `bff.ecoindex.fr`, SVG de 694 o transférés, brotli, `cache-control: public, max-age=604800`), 6 635,1 Ko (+0,9), score brut 67,62 (−0,31 point), arrondi inchangé à 68. Dans le scénario central ecoindex.fr : 218 / 38 / 2 341 Ko → 71,6 → **72 B** (inclus dans le § 1). Accessibilité : `alt` explicite, lien avec `title`, anneau de focus visible (`:focus-visible`, contour marron 2 px), contraste du badge officiel inchangé.

## 9. Mesure de vérité (26/10/2026)

Déploiement manuel de `master` (`5a27479`) sur la prod le 26/10/2026 (rsync identique à `ci/deploy-production` ; Travis ne recevait plus les pushes), puis analyse lancée depuis le formulaire d'ecoindex.fr (le redirect `bff.ecoindex.fr/redirect/` renvoie le résultat en cache du 25/10). Résultat confirmé par l'API (`https://api.ecoindex.fr/v1/ecoindexes/e2883aa8-7b25-4859-ab4c-85c49312d89f`, `url` = `https://feelinggoodbakery.fr/`, moteur 5.10.0, 1920×1080).

URL du résultat : <https://www.ecoindex.fr/resultat/?id=e2883aa8-7b25-4859-ab4c-85c49312d89f> (calculé le lundi 26 octobre 2026 à 14:31:11).

| Métrique | Avant (25/10) | Estimé (§ 1) | **Mesuré (26/10)** | Écart estimé → mesuré |
|---|---|---|---|---|
| DOM (éléments) | 321 | 218 | **218** | 0 |
| Requêtes HTTP | 79 | 38 | **38** | 0 |
| Poids transféré (Ko) | 7 205 | ≈ 2 340 | **2 341,5** | +1,5 |
| Score | 54 | 71,6 → 72 | **72,0** | 0 |
| Note | D | B | **B** | — |
| GES (gCO2e / vue) | 1,92 | ≈ 1,57 | **1,56** | −0,01 |
| Eau (cl / vue) | 2,88 | ≈ 2,35 | **2,34** | −0,01 |
| Classement | 289 676 / 642 729 | | **140 423 / 643 003** | |

Lecture : le scénario central du § 3 était le bon, les deux MP4 lazy (`intro`, `video-centrale`) ne sont pas téléchargés par le navigateur d'ecoindex.fr, comme à l'étape 1. Cible du plan (B, 72 ± 3) atteinte au point près. Les leviers restants sont inchangés (§ 6.1 : compression côté serveur ≈ +0,4, vidéos plus compressées, etc.).

Badge : à 14:35 le badge `bff.ecoindex.fr/badge/` renvoie encore « D » ; il est servi avec `cache-control: max-age=604800` (7 jours), il basculera sur « B » au plus tard à l'expiration de ce cache.
