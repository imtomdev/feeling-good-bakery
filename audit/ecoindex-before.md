# Audit EcoIndex « avant » — feelinggoodbakery.fr

> Audit réalisé le dimanche 25 octobre 2026 (11:30–11:50, heure de Paris) sur la production `https://feelinggoodbakery.fr`.
> Tous les chiffres ci-dessous sont issus d'une sortie d'outil (ecoindex.fr, API ecoindex, ecoindex-cli, Lighthouse, Chrome via CDP, curl, ffprobe). Ce qui n'a pas pu être mesuré est signalé comme tel.

## 1. Résumé

| Indicateur | Valeur (ecoindex.fr) |
|---|---|
| **Score EcoIndex** | **54 / 100** |
| **Note** | **D** (« Hum, pas top. ») |
| Taille du DOM | 321 éléments (« Simple », médiane 693, cible 600) |
| Requêtes HTTP | 79 (« Trop de requêtes », médiane 78, cible 40) |
| Poids de la page | 7,205 Mo — 7 204,577 Ko selon l'API (« Trop lourde », médiane 2,41 Mo, cible 1,024 Mo) |
| Empreinte GES | 1,92 gCO2e par vue de page (affiché : 1,92 kgCO2e pour 1 000 visites) |
| Eau bleue | 2,88 cl par vue de page (affiché : 28,8 l pour 1 000 visites) |
| Classement | 289 676e sur 642 729 pages analysées |
| Date de l'analyse | 25/10/2026 à 11:34:10 (analyse fraîche, lancée pendant cet audit) |
| URL du résultat | https://www.ecoindex.fr/resultat/?id=0941c99b-2339-46c6-a19d-6e8256d0d2b0 |

Ce qu'il faut retenir :

- **Le poids est le principal problème mesuré.** Les images pèsent 4,98 Mo, soit 69 % du poids. Il s'agit surtout de 18 PNG produits/recettes, qui totalisent 3,7 Mo. Les vidéos ajoutent 1,4 Mo selon ecoindex.fr. **Dans un vrai navigateur, le poids réel dépasse 29 Mo** : la vidéo `intro.mp4` (20,2 Mo, 1920×1080 à 15,5 Mb/s) est téléchargée en entier par Chrome/Lighthouse et par ecoindex-cli en local. L'analyseur ecoindex.fr, lui, n'en compte que 785 octets.
- **Le nombre de requêtes (79) est plus pénalisant que le DOM.** 16 requêtes sont des doublons purs : 15 SVG chargés deux fois à cause de SVGInjector, plus la vidéo `gif.mp4` chargée deux fois. Les services tiers (Axeptio et Google Tag Manager) ajoutent 4 requêtes et 472 Ko.
- **Le DOM (321 nœuds comptés) est « simple ».** EcoIndex exclut les descendants des SVG, qui représentent 442 nœuds sur un total réel de 763.
- Aucune ressource statique n'a d'en-tête de cache. CSS, JS et SVG ne sont pas compressés, seul le HTML est en gzip. Le serveur (nginx/1.18.0 Ubuntu) ne sert que du HTTP/1.1.

## 2. Mesure de référence ecoindex.fr

### Procédure

1. `browser-use` (Chrome Beta local via CDP) : ouverture de `https://bff.ecoindex.fr/redirect/?url=https://feelinggoodbakery.fr`. **Cette URL n'a pas déclenché d'analyse** : elle a redirigé vers la page d'accueil `https://www.ecoindex.fr/`.
2. L'analyse a donc été lancée avec le formulaire de la page d'accueil (champ `#siteurl` = `https://feelinggoodbakery.fr`, bouton « Tester le site »). La page a affiché « L'analyse est en cours… 1 analyse actuellement en cours », puis a redirigé vers le résultat en moins d'une minute.
3. Le résultat est daté du jour (25/10/2026 11:34:10) : il ne s'agit donc pas d'un résultat en cache.
4. Les données ont été extraites du texte de la page, des tableaux (types, domaines, 79 requêtes) et de la section « Bonnes pratiques ». Elles ont été recoupées avec l'API publique `https://api.ecoindex.fr/v1/ecoindexes/0941c99b-2339-46c6-a19d-6e8256d0d2b0`.
5. Capture d'écran pleine page : `audit/screenshots/ecoindex-before.png`.

### Résultat brut de l'API

```json
{"requests":79,"id":"0941c99b-2339-46c6-a19d-6e8256d0d2b0","grade":"D","host":"feelinggoodbakery.fr",
 "url":"https://feelinggoodbakery.fr/","score":54.0,"version":1,"ges":1.92,"initial_ranking":289676,
 "width":1920,"water":2.88,"initial_total_results":642729,"ecoindex_version":"5.10.0","source":"ecoindex.fr",
 "height":1080,"size":7204.577,"date":"2026-10-25T11:34:10.806084","nodes":321,"page_type":null}
```

Points à noter : la fenêtre d'analyse est en **1920×1080** et la librairie de calcul est **ecoindex 5.10.0**. GES et eau sont exprimés par vue de page : 1,92 gCO2e et 2,88 cl. La page de résultat les affiche multipliés par le nombre de visites mensuelles choisi (1 000 par défaut), soit 1,92 kgCO2e et 28,8 l.

### Répartition par type (ecoindex.fr)

| Type | Requêtes | Poids | Part |
|---|---|---|---|
| HTML | 1 | 12,5 Ko | 0 % |
| CSS | 1 | 73,4 Ko | 1 % |
| JavaScript | 4 | 632,9 Ko | 9 % |
| Images | 55 | 4,98 Mo | 69 % |
| Vidéo | 4 | 1,4 Mo | 19 % |
| Autre (polices, JSON, SVG annulés) | 14 | 106,4 Ko | 1 % |
| **Total** | **79** | **7,2 Mo** | |

### Répartition par domaine (ecoindex.fr)

| Domaine | Requêtes | Poids |
|---|---|---|
| feelinggoodbakery.fr | 75 | 6,73 Mo |
| static.axept.io (tiers) | 2 | 297,6 Ko |
| www.googletagmanager.com (tiers) | 1 | 171 Ko |
| client.axept.io (tiers) | 1 | 3,7 Ko |

### Bonnes pratiques RWEB évaluées par ecoindex.fr (14 : 8 en échec, 1 à surveiller, 5 OK)

| Statut | Réf. | Pratique | Valeur mesurée | Seuils |
|---|---|---|---|---|
| Échec | RWEB_0075 | Ajouter des en-têtes Expires ou Cache-Control | 1/69 ressource statique avec en-têtes de cache (68 sans) | échec > 0 |
| Échec | RWEB_0076 | Compresser CSS, JS, HTML et SVG | 20 ressources compressibles non compressées | échec > 0 |
| Échec | RWEB_0042 | Externaliser CSS et JavaScript | 4 blocs inline (0 CSS, 4 JS) | alerte 1 · échec 2 |
| Échec | RWEB_0047 | Limiter le nombre de requêtes HTTP | 79 | alerte 26 · échec 40 |
| Échec | RWEB_0083 | Préférer HTTP/2 à HTTP/1 | 75/79 requêtes en HTTP/1.1 | échec > 0 |
| Échec | RWEB_0032 | Préférer les polices standards | 5 polices téléchargées | alerte 1 · échec 2 |
| Échec | RWEB_0099 | Limiter les GIF animés | 1 GIF | échec > 0 |
| Échec | RWEB_0031 | Fournir une CSS print | aucune feuille print | échec si absente |
| À surveiller | RWEB_0082 | Limiter le nombre de domaines | 4 domaines | alerte 3 · échec 5 |
| OK | RWEB_0112 | Éviter les redirections | 0 | |
| OK | RWEB_0035 | Limiter le nombre de CSS | 1 feuille | alerte 7 · échec 10 |
| OK | RWEB_0059 | Remplacer les boutons officiels de partage | aucun bouton officiel | |
| OK | RWEB_0081 | Ressources statiques sur domaine sans cookie | aucun cookie envoyé | |
| OK | (catégorie Datacenter) | 14e pratique, affichée « 1 OK » dans la catégorie Datacenter | — | |

Le libellé exact de la 14e pratique (catégorie Datacenter) n'a pas pu être extrait du DOM. Seules 13 références RWEB y apparaissent.

## 3. Calibration avec ecoindex-cli

### Installation et version

- `pipx` n'était pas installé. Le fallback `python3 -m venv` a échoué : le Python système est en 3.14.7 et la compilation de Pillow échoue (`Failed to build 'Pillow'`).
- Installation retenue (avec uv, déjà présent) :
  ```bash
  uv venv --python 3.12 <scratchpad>/venv
  VIRTUAL_ENV=<scratchpad>/venv uv pip install ecoindex-cli
  ```
- Versions installées : **ecoindex-cli 2.32.0**, qui embarque `ecoindex` (calcul) **5.10.0** — la même version qu'ecoindex.fr d'après l'API — et le scraper **3.18.0**. S'y ajoutent **camoufox 0.5.8** et **playwright 1.62.0**.
- Navigateur réellement utilisé : **Camoufox**, un Firefox headless modifié, et non Chromium. Au premier lancement, Camoufox télécharge son propre binaire et l'extension **uBlock Origin** (« Downloading addon (UBO) » dans `run1.log`). La commande `playwright install chromium` a été lancée mais n'est pas utilisée par le scraper.

### Commande exacte (à rejouer telle quelle en local)

```bash
<scratchpad>/venv/bin/ecoindex-cli analyze --url https://feelinggoodbakery.fr --no-interaction --export-format json --output-file <scratchpad>/ecoindex-cli/runN.json
```

Les autres paramètres restent à leur valeur par défaut, lue dans `--help` : `--window-size 1920,1080`, `--wait-before-scroll 3` (s), `--wait-after-scroll 3` (s), `--no-recursive`, `--max-workers` = nombre de cœurs. Pour localhost, il suffit de remplacer `--url`.

Le scraper (`ecoindex/scraper/scrap.py`) procède ainsi :

1. `goto` puis `wait_for_load_state` ;
2. attente de 3 s, capture, touche `ArrowDown`, puis `scrollTo(bottom, smooth)` ;
3. nouvelle attente de 3 s, puis comptage du DOM ;
4. le poids est la somme des `_transferSize` du HAR, divisée par 1000.

Le DOM compté est `nb(*) − nb(descendants de <svg>)`. Le scraper amont le plus récent (v3.20.0, publié le 07/10/2026) conserve le même moteur Camoufox et la même logique de scroll. Il ajoute le moteur de bonnes pratiques RWEB affiché par ecoindex.fr.

### 3 runs

| Run | Heure | DOM | Requêtes | Poids (Ko) | Score | Note | GES (g) | Eau (cl) |
|---|---|---|---|---|---|---|---|---|
| 1 | 11:36:09 | 321 | 78 | 30 407,201 | 54 | D | 1,92 | 2,88 |
| 2 | 11:36:36 | 321 | 78 | 30 407,189 | 54 | D | 1,92 | 2,88 |
| 3 | 11:36:59 | 321 | 78 | 30 405,262 | 54 | D | 1,92 | 2,88 |
| **Médiane** | | **321** | **78** | **30 407,189** | **54** | **D** | 1,92 | 2,88 |

Un 4e run a été fait via l'API Python du même scraper, avec les mêmes paramètres, pour obtenir le détail des requêtes (`detail-run.json`). Il donne des résultats identiques : 321 / 78 / 30 407,21 Ko / 54.

### Tableau d'écart

| Métrique | ecoindex.fr | ecoindex-cli (médiane) | Écart absolu | Écart % |
|---|---|---|---|---|
| Score | 54 | 54 | 0 | 0 % |
| Note | D | D | — | — |
| DOM | 321 | 321 | 0 | 0 % |
| Requêtes | 79 | 78 | −1 | −1,3 % |
| Poids (Ko) | 7 204,577 | 30 407,189 | +23 202,6 | **+322 %** |

Score brut non arrondi, recalculé avec la librairie locale : 54,10 avec les métriques ecoindex.fr (q_dom 5,383, q_req 10,125, q_size 18,684) et 53,96 avec les métriques du CLI (q_size 19,104). L'énorme écart de poids ne change pas le score arrondi, pour deux raisons : le poids ne pèse que 1/6 de la formule, et les deux valeurs tombent dans les derniers quantiles.

### Explication de l'écart (vérifiée ressource par ressource)

La comparaison de la liste des 79 requêtes d'ecoindex.fr avec les 78 requêtes du HAR local (`detail-run.json`) fait apparaître exactement trois différences :

| Ressource | ecoindex.fr | ecoindex-cli local | Écart |
|---|---|---|---|
| `intro.74c04010.mp4` | 785 o (206) | 20 164,2 Ko (206) | +20 163,4 Ko |
| `video-centrale.fd857fac.mp4` | 781 o (206) | 3 209,1 Ko (206) | +3 208,3 Ko |
| `googletagmanager.com/gtag/js` | 171,0 Ko | absente | −171,0 Ko, −1 requête |

Après neutralisation de ces trois lignes, les poids concordent à ~2 Ko près : 7 204,577 − 171,0 − 0,785 − 0,781 = 7 032,0 Ko côté ecoindex.fr, contre 30 407,2 − 20 164,2 − 3 209,1 = 7 033,9 Ko côté CLI. Toutes les autres ressources ont le même poids, à l'octet près, dans les deux mesures.

Causes probables :

- **Vidéos** : le moteur est le même (Camoufox) des deux côtés. Sur le serveur ecoindex.fr, les vidéos `intro` et `video-centrale` s'arrêtent après ~780 octets. En local (macOS), elles sont lues et téléchargées en entier pendant les ~6 s d'attente. Seule `gif.mp4` (698 Ko) est complète des deux côtés.
  - Hypothèse non vérifiable d'ici : l'environnement serveur (Linux/Docker) diffère pour le décodage H.264 ou la lecture automatique (autoplay).
  - Fait vérifié : **Chrome (Lighthouse) télécharge aussi `intro.mp4` en entier** (19 691 KiB). Le chiffre local est donc plus proche de ce que paie un vrai visiteur.
- **gtag.js** : le CLI local charge l'extension uBlock Origin fournie par Camoufox, qui bloque très probablement `googletagmanager.com`. Le blocage n'a pas pu être confirmé dans les logs. ecoindex.fr, lui, mesure bien gtag.js.
- Facteurs écartés : la fenêtre (1920×1080 des deux côtés), la version de calcul (5.10.0 des deux côtés), le lazy-load (aucun sur le site, voir § 5) et le bandeau cookies (Axeptio est chargé dans les deux cas).

**Conséquence pour le suivi en local :** pour la comparaison avant/après, il faut comparer **CLI contre CLI**, et ne pas comparer le CLI à ecoindex.fr. Le DOM et les requêtes se transposent à l'identique (avec −1 requête pour gtag). Le poids local sera gonflé tant que les vidéos `intro` et `video-centrale` restent en lecture automatique (autoplay).

## 4. Lighthouse (performance)

Lighthouse **12.8.2** (`npx -y lighthouse@12`), Chrome headless (`--headless=new`). Mesures prises le 25/10/2026 vers 11:39.

| Métrique | Mobile (défaut) | Desktop (`--preset=desktop`) |
|---|---|---|
| Score performance | **54** | **58** |
| FCP | 2,4 s | 0,5 s |
| LCP | **21,7 s** | 3,5 s |
| TBT | 120 ms | 0 ms |
| CLS | 0,302 | **0,565** |
| Speed Index | 4,2 s | 1,3 s |
| Time to Interactive | 22,2 s | 3,6 s |
| Poids total transféré | **28 938 KiB** | **29 175 KiB** |
| Éléments DOM (SVG inclus) | 750 | 750 |
| Temps de réponse serveur (document) | 40 ms | 40 ms |

L'élément LCP est, en mobile comme en desktop, `<video src="/assets/intro.74c04010.mp4" autoplay muted loop playsinline>`.

### Opportunités principales

| Audit | Desktop | Mobile | Détail |
|---|---|---|---|
| Formats d'image modernes | ~3 147 KiB | ~3 147 KiB | 18 PNG produits/recettes en tête (ex. peanut-better.png : 470 KiB, gain estimé 422 KiB) |
| Images correctement dimensionnées | ~1 250 KiB | ~2 742 KiB | PNG produits de 500 px environ affichés à 350 px |
| Images hors écran (lazy-load) | — | ~454 KiB | chocolat-droite/gauche, james-brownie-recette, visuel-cookie-1/2 |
| Compression texte | ~172 KiB | ~172 KiB | index.js : 160 KiB, gain 113 KiB ; index.css : 71,5 KiB, gain 59 KiB |
| JS inutilisé | ~315 KiB | ~314 KiB | axept sdk.js : 131 KiB inutilisés ; gtag.js : 97 KiB ; index.js : 88 KiB |
| CSS inutilisé | ~54 KiB | ~46 KiB | index.css |
| JS legacy | ~35 KiB | ~35 KiB | essentiellement axept sdk.js (34 KiB) |
| Politique de cache | 52 ressources | 53 ressources | TTL = 0 sur toutes les ressources first-party ; « cache-insight » estime 28 816 KiB réutilisables |
| HTTP/2 | 59 requêtes HTTP/1.1 | idem | |
| Ressources bloquantes | ~50–100 ms | ~470–630 ms | index.css et module JS dans `<head>` |
| Preconnect | ~90 ms | ~150 ms | origines tierces |
| Images sans width/height | oui | oui | contribue au CLS |

Remarque : le `<body>` porte la classe `--loading`, retirée par un `setTimeout(..., 5000)` inline. Un loader (GIF) s'affiche donc 5 s quel que soit l'état du chargement.

## 5. Inventaire des ressources

### Chargement initial et après scroll

Mesure faite dans Chrome via `browser-use` :

- nouvel onglet, cache désactivé (`Network.setCacheDisabled`), fenêtre 1920×1080 ;
- scroll jusqu'en bas par pas de 800 px, sur une hauteur de page de 9 492 px ;
- lecture de `performance.getEntriesByType('resource')`.

| Moment | Entrées Resource Timing | DOM (`*`) | dont descendants SVG |
|---|---|---|---|
| Après chargement (+3 s) | 74 | 763 | — |
| Après scroll complet (+4 s) | 74 | 763 | 442 |

**Le scroll ne déclenche aucun chargement supplémentaire : tout est chargé dès l'arrivée sur la page.** Aucune `<img>` n'a `loading="lazy"` (0 sur 45). Les 4 `<video>` ont `autoplay muted loop playsinline` (donc `preload` vaut « metadata » par défaut, mais l'autoplay force le chargement).

Limites de cette mesure :

- Resource Timing ne liste pas les requêtes des `<video>`.
- Les tiers (Axeptio, GTM) y apparaissent avec une taille de 0, faute d'en-tête `Timing-Allow-Origin`.
- L'onglet étant en arrière-plan, les vidéos y sont restées en pause. Leur poids réel vient donc de Lighthouse, du CLI et de ffprobe.

### Tableau (79 requêtes, ordre décroissant)

Sources des colonnes :

- La liste et le « Transféré » viennent d'ecoindex.fr.
- « Décompressé LH » est le `resourceSize` de Lighthouse desktop, converti en Ko. Pour les vidéos, il s'agit de la taille téléchargée par Chrome, qui correspond au fichier complet.
- Les en-têtes ont été vérifiés par `curl -sI -H 'Accept-Encoding: br, gzip' --http2` sur le HTML, le CSS, le JS, hero-titre.svg, peanut-better.png, mosaique-cookie-3.jpg, les 3 MP4, poppins-regular.woff2 et les 3 scripts tiers.
- Pour les autres ressources first-party, les colonnes cache et compression sont déduites de la configuration nginx observée sur l'échantillon. Elles sont confirmées par RWEB_0075 (68/69 sans cache) et RWEB_0076 (20 ressources texte non compressées).

| # | URL | Type (ecoindex.fr) | Statut | Transféré (Ko) | Décompressé LH (Ko) | Cache-Control | Content-Encoding |
|---|---|---|---|---|---|---|---|
| 1 | `/assets/gif.2b9dad88.mp4` | Vidéo | 206 | 698.3 | 698.1 | absent | aucune |
| 2 | `/assets/gif.2b9dad88.mp4` | Vidéo | 206 | 698.3 | 698.1 | absent | aucune |
| 3 | `/assets/peanut-better.cf9df111.png` | Images | 200 | 481.7 | 481.4 | absent | aucune |
| 4 | `/assets/mamma-damia.bb2cfabc.png` | Images | 200 | 437.2 | 437.0 | absent | aucune |
| 5 | `/assets/pecan-express-recette.7a79e46b.png` | Images | 200 | 355.3 | 355.1 | absent | aucune |
| 6 | `/assets/dandy-recette.c7533679.png` | Images | 200 | 335.7 | 335.5 | absent | aucune |
| 7 | `/assets/mamma-damia-recette.b65af38b.png` | Images | 200 | 259.5 | 259.2 | absent | aucune |
| 8 | `/assets/peanut-better-recette.1b359741.png` | Images | 200 | 254.0 | 253.7 | absent | aucune |
| 9 | `https://static.axept.io/sdk.js` | JavaScript | 200 | 205.6 | 726.8 | absent | br |
| 10 | `/assets/matchaman.d810b99b.png` | Images | 200 | 181.0 | 180.7 | absent | aucune |
| 11 | `/assets/pecan-express.16134336.png` | Images | 200 | 171.1 | 170.9 | absent | aucune |
| 12 | `https://www.googletagmanager.com/gtag/js` | JavaScript | 200 | 171.0 | 501.4 | private, max-age=900 | br |
| 13 | `/assets/s-more.cf60db58.png` | Images | 200 | 166.8 | 166.6 | absent | aucune |
| 14 | `/assets/index.1f64aba1.js` | JavaScript | 200 | 164.2 | 164.0 | absent | aucune |
| 15 | `/assets/dandy.f64df760.png` | Images | 200 | 159.1 | 158.9 | absent | aucune |
| 16 | `/assets/roudoudou.1c97eb10.png` | Images | 200 | 153.5 | 153.2 | absent | aucune |
| 17 | `/assets/naoned.83866eb8.png` | Images | 200 | 152.2 | 151.9 | absent | aucune |
| 18 | `/assets/james-brownie.73f9ef06.png` | Images | 200 | 130.0 | 129.7 | absent | aucune |
| 19 | `/assets/chocolat-droite.dcb73684.png` | Images | 200 | 126.8 | 126.6 | absent | aucune |
| 20 | `/assets/chocolat-gauche.915420b9.png` | Images | 200 | 121.5 | 121.2 | absent | aucune |
| 21 | `/assets/carte-gmap.ae584f76.jpg` | Images | 200 | 100.0 | 99.7 | absent | aucune |
| 22 | `/assets/naoned-recette.baec126c.png` | Images | 200 | 99.1 | 98.8 | absent | aucune |
| 23 | `/assets/s-more-recette.8d9b8afc.png` | Images | 200 | 99.0 | 98.8 | absent | aucune |
| 24 | `/assets/matchaman-recette.2a7a8e52.png` | Images | 200 | 96.9 | 96.7 | absent | aucune |
| 25 | `/assets/mosaique-cookie-3.2a9d6e54.jpg` | Images | 200 | 95.9 | 95.7 | absent | aucune |
| 26 | `/assets/james-brownie-recette.2ee17ddd.png` | Images | 200 | 95.7 | 95.4 | absent | aucune |
| 27 | `https://static.axept.io/datacenter-ranges.js` | JavaScript | 200 | 92.0 | 634.3 | absent | br |
| 28 | `/assets/roudoudou-recette.bbee86b4.png` | Images | 200 | 89.2 | 89.0 | absent | aucune |
| 29 | `/assets/hero-titre.4bea38b8.svg` | Images | 200 | 84.9 | 84.7 | absent | aucune |
| 30 | `/assets/visuel-wookie.e0b3d750.jpg` | Images | 200 | 81.0 | 80.8 | absent | aucune |
| 31 | `/assets/mosaique-cookie-4.b7fe64d5.jpg` | Images | 200 | 77.9 | 77.7 | absent | aucune |
| 32 | `/assets/visuel-cookie-2.2074d782.jpg` | Images | 200 | 74.3 | 74.1 | absent | aucune |
| 33 | `/assets/index.78af96fe.css` | CSS | 200 | 73.4 | 73.2 | absent | aucune |
| 34 | `/assets/chocolat.6bff7264.svg` | Images | 200 | 69.2 | 68.9 | absent | aucune |
| 35 | `/assets/mosaique-cookie-1.83186a26.jpg` | Images | 200 | 59.1 | 58.8 | absent | aucune |
| 36 | `/assets/equipe.b594c358.jpg` | Images | 200 | 58.6 | 58.4 | absent | aucune |
| 37 | `/assets/mosaique-cookie-2.bb3931e4.jpg` | Images | 200 | 54.8 | 54.5 | absent | aucune |
| 38 | `/assets/visuel-icecream.62b15886.jpg` | Images | 200 | 50.7 | 50.5 | absent | aucune |
| 39 | `/assets/visuel-cookie-1.ff3f7eab.jpg` | Images | 200 | 48.1 | 47.9 | absent | aucune |
| 40 | `/assets/sac-ble.f2f6df2f.svg` | Images | 200 | 42.3 | 42.1 | absent | aucune |
| 41 | `/assets/oeufs.cf47c3d5.svg` | Images | 200 | 36.7 | 36.4 | absent | aucune |
| 42 | `/assets/bodoni-book-italic.6208c871.woff2` | Autre | 200 | 35.1 | 34.9 | absent | aucune |
| 43 | `/assets/eat-cookie.1a62902f.gif` | Images | 200 | 32.2 | 32.0 | absent | aucune |
| 44 | `/assets/poppins-regular-webfont.4916abbc.woff2` | Autre | 200 | 16.5 | 16.3 | absent | aucune |
| 45 | `/assets/poppins-semibold-webfont.68a37b9e.woff2` | Autre | 200 | 16.5 | 16.2 | absent | aucune |
| 46 | `/assets/poppins-light-webfont.25124084.woff2` | Autre | 200 | 16.3 | 16.0 | absent | aucune |
| 47 | `/assets/poppins-bold-webfont.047e27d1.woff2` | Autre | 200 | 16.3 | 16.0 | absent | aucune |
| 48 | `/assets/soucoupe.b5d45e5a.svg` | Images | 200 | 14.3 | 14.0 | absent | aucune |
| 49 | `/assets/carte-de-france.92061cb2.png` | Images | 200 | 12.9 | 12.6 | absent | aucune |
| 50 | `/` | HTML | 200 | 12.5 | 39.8 | absent | gzip |
| 51 | `/assets/beurre.92e82dba.svg` | Images | 200 | 7.7 | 7.5 | absent | aucune |
| 52 | `/assets/ustensiles-2.ef819421.svg` | Images | 200 | 4.5 | 4.3 | absent | aucune |
| 53 | `https://client.axept.io/projectconfigurations/brands/60a53c9b6cd349769a41d8cb.json` | Autre | 200 | 3.7 | 5.9 | absent | br |
| 54 | `/assets/recettes.cd3b247a.svg` | Images | 200 | 2.6 | 2.3 | absent | aucune |
| 55 | `/assets/ustensiles.b848ad99.svg` | Images | 200 | 1.9 | 1.6 | absent | aucune |
| 56 | `/assets/instagram.ce41677c.svg` | Images | 200 | 1.6 | 1.3 | absent | aucune |
| 57 | `/assets/intro.74c04010.mp4` | Vidéo | 206 | 0.8 | 20163.9 | absent | aucune |
| 58 | `/assets/video-centrale.fd857fac.mp4` | Vidéo | 206 | 0.8 | 3208.8 | absent | aucune |
| 59 | `/assets/cross.3a900517.svg` | Images | 200 | 0.8 | 0.5 | absent | aucune |
| 60 | `/assets/burger.2163b538.svg` | Images | 200 | 0.7 | 0.5 | absent | aucune |
| 61 | `/assets/arrow-right.e0f65b90.svg` | Images | 200 | 0.6 | 0.4 | absent | aucune |
| 62 | `/assets/arrow-right.e0f65b90.svg` | Images | 200 | 0.6 | 0.4 | absent | aucune |
| 63 | `/assets/arrow-left.92ac8e76.svg` | Images | 200 | 0.6 | 0.4 | absent | aucune |
| 64 | `/assets/facebook.a8aee3ff.svg` | Images | 200 | 0.6 | 0.4 | absent | aucune |
| 65 | `/assets/favicon.ba841369.svg` | Images | 200 | 0.5 | 0.3 | absent | aucune |
| 66 | `/assets/beurre.92e82dba.svg` | Autre | -1 | 0.3 | 7.5 | absent | aucune |
| 67 | `/assets/soucoupe.b5d45e5a.svg` | Autre | -1 | 0.3 | 14.0 | absent | aucune |
| 68 | `/assets/oeufs.cf47c3d5.svg` | Autre | -1 | 0.3 | 36.4 | absent | aucune |
| 69 | `/assets/sac-ble.f2f6df2f.svg` | Autre | -1 | 0.3 | 42.1 | absent | aucune |
| 70 | `/assets/chocolat.6bff7264.svg` | Autre | -1 | 0.3 | 68.9 | absent | aucune |
| 71 | `/assets/ustensiles.b848ad99.svg` | Autre | -1 | 0.3 | 1.6 | absent | aucune |
| 72 | `/assets/recettes.cd3b247a.svg` | Autre | -1 | 0.3 | 2.3 | absent | aucune |
| 73 | `/assets/ustensiles-2.ef819421.svg` | Autre | -1 | 0.3 | 4.3 | absent | aucune |
| 74 | `/assets/facebook.a8aee3ff.svg` | Images | 200 | 0.0 | 0.4 | absent | aucune |
| 75 | `/assets/instagram.ce41677c.svg` | Images | 200 | 0.0 | 1.3 | absent | aucune |
| 76 | `/assets/burger.2163b538.svg` | Images | 200 | 0.0 | 0.5 | absent | aucune |
| 77 | `/assets/cross.3a900517.svg` | Images | 200 | 0.0 | 0.5 | absent | aucune |
| 78 | `/assets/hero-titre.4bea38b8.svg` | Images | 200 | 0.0 | 84.7 | absent | aucune |
| 79 | `/assets/arrow-left.92ac8e76.svg` | Images | 200 | 0.0 | 0.4 | absent | aucune |
| | **Total** | | | **7204.4** | | | |
Notes sur le tableau :

- Les lignes à `-1` (252 o) et à `0 o` sont les doublons des 15 SVG injectés par **SVGInjector** : chacun est chargé une fois en `<img>`, puis une seconde fois en XHR pour être inliné. Au total, **31 requêtes SVG pour 16 fichiers distincts**.
- `gif.2b9dad88.mp4` est chargé **2 fois** (2 × 698,3 Ko dans ecoindex.fr et dans le CLI) : une `<video class="gif">` pour le desktop, plus une `<video class="gif mobile">` masquée (0×0 en desktop) mais chargée quand même. Dans Chrome/Lighthouse, la 2e requête ne pèse que 0,3 Ko.
- Poids réels des fichiers vidéo, d'après `curl` (`Content-Length`) et ffprobe :

| Fichier | Taille | Définition | Codec | Durée | Débit | Piste audio |
|---|---|---|---|---|---|---|
| `intro.74c04010.mp4` | 20 163 872 o | 1920×1080 | H.264, 23,976 i/s | 10,26 s | 15,7 Mb/s | oui (AAC, alors que la vidéo est `muted`) |
| `video-centrale.fd857fac.mp4` | 3 208 836 o | 1280×720 | H.264, 30 i/s | 11,27 s | 2,28 Mb/s | non |
| `gif.2b9dad88.mp4` | 698 055 o | 560×884 | H.264, 1 i/s | 4,0 s | 1,4 Mb/s | non |

- GIF : `eat-cookie.1a62902f.gif` (32,2 Ko, 145×132 affiché en 70×64) sert de loader.
- Polices : 5 WOFF2 auto-hébergées (4 graisses de Poppins à 16,3–16,5 Ko + Bodoni Book Italic à 35,1 Ko, soit 100,7 Ko), servies en `application/octet-stream`. La CSS embarque en plus une police `swiper-icons` en data-URI (`data:application/font-woff`). Pas de Google Fonts.
- Doublons d'images dans le DOM (sans requête supplémentaire) : `mosaique-cookie-2` et `mosaique-cookie-4` apparaissent deux fois (variantes desktop et mobile masquée). `mamma-damia-recette` et `james-brownie-recette` apparaissent deux fois (clones Swiper).
- Pas de doublon PNG/JPG détecté entre fichiers différents : chaque visuel n'existe qu'en un seul format.

### Agrégats (poids ecoindex.fr)

| Groupe | Fichiers | Poids |
|---|---|---|
| PNG produits (dans les modales, invisibles au chargement) | 9 | 2 032,6 Ko |
| PNG recettes (carrousel Swiper) | 9 | 1 684,4 Ko |
| MP4 (ecoindex.fr) — réel Chrome/CLI ≈ 24 769 Ko | 4 requêtes / 3 fichiers | 1 398,2 Ko |
| JPG (visuels, mosaïque, carte) | 10 | 700,4 Ko |
| SVG | 31 requêtes / 16 fichiers | 272,3 Ko |
| Autres PNG (chocolat gauche/droite, carte de France) | 3 | 261,2 Ko |
| JS tiers (axept sdk + datacenter-ranges + gtag) | 3 | 468,6 Ko |
| JS first-party (`index.1f64aba1.js`) | 1 | 164,2 Ko |
| Polices WOFF2 | 5 | 100,7 Ko |
| CSS | 1 | 73,4 Ko |
| GIF | 1 | 32,2 Ko |
| HTML | 1 | 12,5 Ko (39,8 Ko décompressé) |
| JSON Axeptio | 1 | 3,7 Ko |

### En-têtes serveur (`headers.txt`)

| Ressource | HTTP | Server | Content-Encoding | Cache-Control | Expires | ETag | Last-Modified |
|---|---|---|---|---|---|---|---|
| `/` (HTML) | 1.1 | nginx/1.18.0 (Ubuntu) | gzip | absent | absent | `W/"6386456f-9ba3"` | 29/11/2022 |
| `index.78af96fe.css` | 1.1 | nginx/1.18.0 (Ubuntu) | **aucune** | absent | absent | `"6386456f-11de5"` | 29/11/2022 |
| `index.1f64aba1.js` | 1.1 | nginx/1.18.0 (Ubuntu) | **aucune** | absent | absent | `"6386456f-28079"` | 29/11/2022 |
| `hero-titre.4bea38b8.svg` | 1.1 | nginx/1.18.0 (Ubuntu) | **aucune** | absent | absent | `"6386456f-14aae"` | 29/11/2022 |
| `peanut-better.cf9df111.png` | 1.1 | nginx/1.18.0 (Ubuntu) | aucune | absent | absent | `"6386456f-7587b"` | 29/11/2022 |
| `mosaique-cookie-3.2a9d6e54.jpg` | 1.1 | nginx/1.18.0 (Ubuntu) | aucune | absent | absent | `"6386456f-175a8"` | 29/11/2022 |
| `intro / video-centrale / gif .mp4` | 1.1 | nginx/1.18.0 (Ubuntu) | aucune | absent | absent | présents | 29/11/2022 |
| `poppins-regular-webfont.woff2` | 1.1 | nginx/1.18.0 (Ubuntu) | aucune | absent | absent | `"6386456f-3f90"` | 29/11/2022 |
| `static.axept.io/sdk.js`, `datacenter-ranges.js` | 2 | AmazonS3 | br | absent | absent | — | — |
| `googletagmanager.com/gtag/js` | 2 | Google Tag Manager | br | `private, max-age=900` | +15 min | — | — |

Constats :

- `curl --http2` négocie du **HTTP/1.1** : pas de h2 côté nginx.
- La compression (gzip) ne s'applique qu'à `text/html`, ce qui correspond à la configuration par défaut de nginx (`gzip_types`). CSS, JS et SVG partent en clair.
- **Aucun `Cache-Control` ni `Expires`**, alors que les noms de fichiers Vite sont hashés. Seule la revalidation par ETag / Last-Modified est possible.
- Le WOFF2 est servi en `application/octet-stream` au lieu de `font/woff2`.

## 6. Ressources tierces

| Domaine | Rôle | Requêtes | Poids transféré | Poids décompressé (LH) | Remarques |
|---|---|---|---|---|---|
| static.axept.io | CMP Axeptio (bandeau cookies) : `sdk.js` | 1 | 205,6 Ko | 709,8 KiB | 131 KiB de JS inutilisé, 34 KiB de JS legacy (LH) |
| static.axept.io | Axeptio : `datacenter-ranges.js` | 1 | 92,0 Ko | 619,4 KiB | |
| client.axept.io | Axeptio : configuration projet (JSON) | 1 | 3,7 Ko | 5,8 KiB | |
| www.googletagmanager.com | Google Analytics 4 (`gtag/js?id=G-MC0HGGF759`) | 1 | 171,0 Ko | 489,6 KiB | Chargé en `async` **dès le `<head>`, avant le consentement**. Seul `gtag('config')` attend le consentement Axeptio. 97 KiB inutilisés (LH) |
| **Total tiers** | | **4** | **472,3 Ko** (6,6 % du poids) | | 3 domaines tiers ; temps main-thread : axept 68 ms, GTM 30 ms (LH desktop) |

Les services suivants ne sont pas utilisés : Google Fonts, Google Maps (la carte est une image statique, `carte-gmap.ae584f76.jpg`, 100 Ko), CDN tiers, iframes (0) et boutons sociaux officiels (les liens Facebook/Instagram sont de simples SVG). Aucune requête de collecte GA (`/g/collect`) n'a été observée sans consentement.

## 7. Analyse du DOM

Le total est de 763 éléments (`document.getElementsByTagName('*')`), dont 442 descendants de `<svg>`. Le comptage EcoIndex donne 763 − 442 = **321**, identique à ecoindex.fr. Lighthouse en compte 750.

### Par section (enfants directs de `<body>`)

Les colonnes comptent les descendants, sans l'élément section lui-même.

| Section | Descendants | dont dans des SVG | Comptés EcoIndex |
|---|---|---|---|
| `section.loader` | 1 | 0 | 1 |
| `section.bg` | 0 | 0 | 0 |
| `section.bandeau-header` (header + hero) | 152 | 124 | 28 |
| ↳ `header` | 32 | 21 | 11 |
| ↳ `section.hero` (SVG titre inline) | 105 | 103 | 2 |
| `section#notre-histoire.introduction` | 9 | 0 | 9 |
| `section.description` | 10 | 0 | 10 |
| `section.cookies` | 7 | 0 | 7 |
| `section#nos-cookies.recipes` (carrousel Swiper) | 45 | 12 | 33 |
| `section.modals` (9 modales produits) | 66 | 0 | **66** |
| `section.season-products` | 19 | 0 | 19 |
| `section#nos-fournisseurs.map-container` | 322 | 287 | 35 |
| `section.mosaic` | 14 | 0 | 14 |
| `section#ou-nous-trouver.informations` | 38 | 19 | 19 |
| `footer` | 51 | 0 | **51** |
| 3 `<script>` en fin de body | 0 | 0 | 0 |

Le reste (16 enfants de body, `html`/`head`/`body`, balises du `<head>`) complète jusqu'à 321.

Répartition par balise (hors descendants SVG) : DIV 81, P 46, IMG 45, SPAN 19, H2 19, LI 17, svg 15, H3 14, SECTION 13, BR 13, A 11, SCRIPT 7, VIDEO 4, UL 4.

### SVG inline

Les 15 `<svg class="injected-svg js-inject-me">` sont injectés par SVGInjector, qui remplace des `<img>` par le SVG récupéré en XHR. Ils représentent 442 nœuds au total.

| Emplacement | Nœuds | Taille du markup |
|---|---|---|
| `section.hero` (hero-titre.svg) | 103 | 85,2 Ko |
| `#nos-fournisseurs` (5 SVG, appariés par taille : chocolat 195 nœuds / 70,2 Ko, sac-blé 56 / 42,4 Ko, soucoupe 30 / 14,3 Ko, œufs 3 / 36,5 Ko, beurre 3 / 7,5 Ko) | 287 | 170,9 Ko |
| `#ou-nous-trouver` (3 SVG) | 8 + 6 + 5 = 19 | 4,4 + 2,4 + 1,7 Ko |
| `#nos-cookies` (2 flèches) | 6 + 6 = 12 | 0,4 + 0,4 Ko |
| header (4 icônes : réseaux sociaux, burger, croix) | 5 + 7 + 5 + 4 = 21 | 0,5–1,4 Ko |

Les descendants SVG ne comptent pas dans le DOM EcoIndex. En revanche, l'injection **double les requêtes** (15 requêtes en plus) et alourdit le DOM réel (442 nœuds, utile pour Lighthouse et le rendu).

### Éléments cachés, clones, contenus non affichés

- **9 modales produits** (`section.modals > div.modal`, `opacity: 0`, `display: block`) : 66 nœuds EcoIndex, et 9 PNG produits **chargés au démarrage**, soit 2 032,6 Ko, alors qu'ils ne s'affichent qu'au clic.
- **Clones Swiper (mode loop)** : 11 `.swiper-slide` au lieu de 9, dont 2 `.swiper-slide-duplicate` (mamma-damia-recette, james-brownie-recette).
- **Variantes « mobile » masquées en desktop** (12 éléments non rendus au total, dont 3 `<script>`) :
  - `video.gif.mobile`, qui provoque la 2e requête `gif.mp4` ;
  - `h2.mobile` ;
  - `div.mobile` de la mosaïque, avec 2 `<img>` en double (mosaique-cookie-4 et -2).
- **Loader** : `section.loader` (GIF) affiché pendant 5 s fixes, puis caché.
- **Scripts inline** : 4 blocs JS (gtag/Axeptio/loader de 539 caractères, 2 JSON-LD de 339 et 320 caractères, 1 bloc de 373 caractères), ce qui correspond à RWEB_0042.

## 8. Bonnes pratiques GreenIT non respectées

Le CLI GreenIT-Analysis n'a pas pu être exécuté : les paquets `greenit-cli`, `greenit-analysis-cli`, `@cnumr/greenit-cli` et `greenit` renvoient tous une erreur 404 sur le registre npm. L'outil cnumr n'est distribué que sous forme de dépôt GitHub à construire (Puppeteer), ce qui a été écarté. Le tableau ci-dessous combine donc les 14 pratiques RWEB évaluées par ecoindex.fr et les constats mesurés ci-dessus.

Sur les colonnes d'impact : elles indiquent l'effet attendu sur chacune des 3 métriques EcoIndex d'une première visite (cache vide), telles que les mesure le scraper. Ce sont des estimations qualitatives, mais elles reposent sur les volumes mesurés.

| Pratique | Constat mesuré | DOM | Requêtes | Poids |
|---|---|---|---|---|
| Optimiser les images (format adapté) | 18 PNG photographiques (produits + recettes) = 3 717 Ko ; LH « modern formats » ≈ 3 147 KiB de gain | — | — | **Fort** |
| Redimensionner les images (taille d'affichage) | PNG produits de ~500 px affichés en 350 px ; LH ≈ 1 250 KiB (desktop) / 2 742 KiB (mobile) | — | — | **Fort** |
| Ne charger que le contenu affiché (lazy-load, contenu à la demande) | 0 `<img loading="lazy">` sur 45 ; 9 PNG de modales invisibles chargés (2 032,6 Ko) ; variantes mobiles masquées chargées | Moyen (66 nœuds de modales) | Moyen (9 modales + doublons mobiles) | **Fort** |
| Éviter les vidéos / fonds vidéo en autoplay | intro.mp4 de 20,2 Mo (1080p, 15,7 Mb/s, piste audio inutile), video-centrale de 3,2 Mo, gif.mp4 de 698 Ko ×2 ; ecoindex.fr en compte 1,4 Mo, Chrome et le CLI local ≈ 24,8 Mo | — | Faible (4 req.) | **Fort** (réel), moyen (sur ecoindex.fr) |
| RWEB_0047 Limiter le nombre de requêtes HTTP | 79 requêtes (échec au-delà de 40) | — | **Fort** | — |
| Éviter les doublons de requêtes (SVG injectés) | 15 SVG chargés en `<img>` + XHR (SVGInjector) : 31 requêtes pour 16 fichiers ; gif.mp4 ×2 | Nul (SVG exclus) | **Fort** (16 requêtes redondantes) | Faible |
| RWEB_0076 Compresser CSS, JS, HTML, SVG | 20 ressources non compressées : JS 164 Ko, CSS 73 Ko, SVG 272 Ko ; LH ≈ 172 KiB de gain sur JS + CSS seuls | — | — | Moyen |
| Limiter les scripts tiers / services superflus | Axeptio 301 Ko (3 req.) + GTM 171 Ko (1 req.), GTM chargé avant consentement ; LH : ≈ 228 KiB de JS tiers inutilisé | — | Faible (4) | Moyen (472 Ko) |
| Supprimer le JS/CSS inutilisé | index.js : 88 KiB inutilisés ; index.css : 54 KiB inutilisés (LH desktop) | — | — | Faible à moyen |
| RWEB_0032 Préférer les polices standards | 5 WOFF2 (100,7 Ko) + police swiper-icons inline | — | Faible (5) | Faible |
| Éviter les carrousels | Swiper : 2 slides clonées, 9 PNG recettes (1 684 Ko) tous chargés | Faible | Faible | Moyen |
| RWEB_0099 Limiter les GIF animés | eat-cookie.gif de 32,2 Ko (loader de 5 s) | Faible | Faible (1) | Faible |
| RWEB_0042 Externaliser CSS et JS | 4 blocs JS inline (dont 2 JSON-LD légitimes) | Nul | Nul | Nul |
| RWEB_0075 Ajouter Cache-Control / Expires | 68/69 ressources statiques sans en-tête de cache, malgré des noms hashés | Nul | Nul (1re visite) | Nul (1re visite), fort sur les visites suivantes |
| RWEB_0083 Préférer HTTP/2 | nginx sert du HTTP/1.1 uniquement (75/79 requêtes) | Nul | Nul | Nul (léger sur les en-têtes) |
| RWEB_0082 Limiter le nombre de domaines | 4 domaines (seuil d'alerte : 3) | — | Faible | Faible |
| RWEB_0031 Fournir une CSS print | aucune règle `@media print` | Nul | Nul | Nul |
| Dimensionner les images (`width`/`height`) | images sans dimensions explicites, CLS de 0,565 (desktop) | Nul | Nul | Nul |
| Servir les bons types MIME | WOFF2 en `application/octet-stream` | Nul | Nul | Nul |

## 9. Synthèse des principaux leviers (classés par impact)

D'après la formule EcoIndex 5.10.0 (`100 − 5 × (3·q_dom + 2·q_req + q_size) / 6`), les contributions actuelles se répartissent ainsi :

| Composante | Calcul | Valeur | Part de la pénalité |
|---|---|---|---|
| Requêtes | 2 × q_req = 2 × 10,125 | 20,25 | 37 % |
| Poids | 1 × q_size | 18,68 | 34 % |
| DOM | 3 × q_dom = 3 × 5,383 | 16,15 | 29 % |

Le score brut est de 54,10, arrondi à 54.

Leviers, du plus fort au plus faible effet sur les métriques mesurées :

1. **Images PNG photographiques** : 18 fichiers, 3 717 Ko, soit 52 % du poids mesuré par ecoindex.fr. Elles sont au mauvais format et surdimensionnées. C'est le levier le plus lourd sur la métrique « poids », qui est dans le 19e quantile sur 20.
2. **Contenu chargé mais non affiché** : 9 PNG de modales (2 033 Ko), images et vidéo des variantes mobiles masquées, aucun lazy-load. Ce levier joue à la fois sur le poids et sur les requêtes.
3. **Requêtes redondantes** : 16 requêtes en double (15 SVG via SVGInjector, plus gif.mp4). Combinées aux 18 PNG et aux 5 polices, elles expliquent l'essentiel des 79 requêtes, la composante la plus pénalisante du score.
4. **Vidéos en autoplay** : 1,4 Mo comptés par ecoindex.fr, mais ≈ 24,8 Mo réellement téléchargés par Chrome et par le CLI local, dont 20,2 Mo pour intro.mp4 (1080p à 15,7 Mb/s, avec une piste audio alors que la vidéo est muette). Ce levier est le plus important pour l'empreinte réelle et pour le suivi local avec le CLI. Il pèse peu sur le score ecoindex.fr actuel.
5. **Compression et cache serveur** : nginx ne compresse que le HTML (CSS, JS et SVG ≈ 510 Ko en clair) et n'envoie aucun Cache-Control. Le gain sur le score de 1re visite est modéré (poids), mais fort pour les visites répétées. HTTP/2 n'est pas activé.
6. **Scripts tiers** : 472 Ko et 4 requêtes (Axeptio, GTM), avec GTM chargé avant le consentement.
7. **DOM** : 321 nœuds, c'est déjà « simple ». Les marges restantes viennent des modales pré-rendues (66 nœuds), du footer (51), des clones Swiper et des doublons mobiles. Le levier est le plus faible des trois en valeur absolue, mais chaque nœud compte triple dans la formule.

## 10. Annexe — commandes et fichiers bruts

Scratchpad : `/private/tmp/claude-501/-Users-thomas-dev-feeling-good-bakery/98457f49-2bfa-4084-a169-3bcfd387c0a9/scratchpad` (noté `<SP>` ci-dessous).

### Commandes

```bash
# ecoindex.fr (browser-use, Chrome Beta via CDP)
browser-use <<'PY'
new_tab("https://bff.ecoindex.fr/redirect/?url=https://feelinggoodbakery.fr")   # -> redirected to home, no analysis
PY
# then: fill #siteurl with https://feelinggoodbakery.fr, click "Tester le site", poll until /resultat/?id=...
browser-use < <SP>/scripts/extract_ecoindex.py     # tables (types, domains, 79 requests)
browser-use < <SP>/scripts/extract_bp.py           # best practices (raw)
browser-use < <SP>/scripts/bp_struct.py            # best practices (structured)
curl -s https://api.ecoindex.fr/v1/ecoindexes/0941c99b-2339-46c6-a19d-6e8256d0d2b0 > <SP>/ecoindex-fr-api.json

# ecoindex-cli
uv venv --python 3.12 <SP>/venv && VIRTUAL_ENV=<SP>/venv uv pip install ecoindex-cli
<SP>/venv/bin/playwright install chromium     # not used by the Camoufox-based scraper
for i in 1 2 3; do
  <SP>/venv/bin/ecoindex-cli analyze --url https://feelinggoodbakery.fr --no-interaction \
    --export-format json --output-file <SP>/ecoindex-cli/run$i.json
done
<SP>/venv/bin/python -I <SP>/scripts/scrape_detail.py <SP>/ecoindex-cli/detail-run.json   # per-request detail + score sensitivity

# Lighthouse 12.8.2
npx -y lighthouse@12 https://feelinggoodbakery.fr --only-categories=performance --preset=desktop \
  --output=json --output-path=<SP>/lh-desktop.json --chrome-flags="--headless=new"
npx -y lighthouse@12 https://feelinggoodbakery.fr --only-categories=performance \
  --output=json --output-path=<SP>/lh-mobile.json --chrome-flags="--headless=new"

# Headers / video probe
curl -sI -H 'Accept-Encoding: br, gzip' --http2 -w 'http_version=%{http_version}\n' <url>
ffprobe -v error -show_entries format=duration,bit_rate,size:stream=codec_name,codec_type,width,height,r_frame_rate,bit_rate -of compact <mp4 url>

# Browser (resource timing after scroll, DOM breakdown)
browser-use < <SP>/scripts/site_scroll.py
browser-use < <SP>/scripts/dom_breakdown.py
python3 -I <SP>/scripts/inventory.py <SP>                 # builds inventory.md

# GreenIT CLI (failed: E404 on all names)
npm view greenit-cli / greenit-analysis-cli / @cnumr/greenit-cli / greenit
```

### Fichiers bruts conservés

| Fichier | Contenu |
|---|---|
| `<SP>/ecoindex-fr-result.txt` | texte complet de la page de résultat ecoindex.fr |
| `<SP>/ecoindex-fr-tables.txt` | tableaux types / domaines / 79 requêtes |
| `<SP>/ecoindex-fr-bp.txt` | section bonnes pratiques (texte brut) |
| `<SP>/ecoindex-fr-api.json` | résultat API ecoindex.fr |
| `audit/screenshots/ecoindex-before.png` | capture pleine page du résultat |
| `<SP>/ecoindex-cli/run1.json` … `run3.json`, `run*.log` | 3 runs ecoindex-cli |
| `<SP>/ecoindex-cli/detail-run.json` | 4e run, détail des 78 requêtes du CLI |
| `<SP>/lh-desktop.json`, `<SP>/lh-mobile.json`, `<SP>/lh.log` | rapports Lighthouse |
| `<SP>/headers.txt` | en-têtes HTTP (curl) |
| `<SP>/ffprobe.txt` | caractéristiques des 3 MP4 |
| `<SP>/browser-resources.json` | Resource Timing + DOM avant/après scroll (Chrome) |
| `<SP>/dom-breakdown.json` | DOM par section, SVG, vidéos, images, éléments cachés |
| `<SP>/index.html` | HTML servi (décompressé) |
| `<SP>/inventory.md` | inventaire généré (repris au § 5) |
| `<SP>/scripts/*.py` | scripts utilisés |
| `<SP>/pip.log`, `<SP>/pw-install.log` | logs d’installation (uv / playwright ; le log de l’échec pip sous Python 3.14 a été écrasé) |
