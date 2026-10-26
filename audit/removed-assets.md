# Assets mis de côté

Aucun fichier n'a été supprimé : tout ce qui n'est plus servi par le site a été déplacé dans `archive/` (conservé dans le dépôt, hors du build Vite qui ne copie que les fichiers référencés par `index.html` et le SCSS). Pour revenir en arrière sur un fichier, il suffit de le remettre dans `assets/` et de rétablir sa référence.

## Remplacés par une version optimisée (original conservé)

| Original (archive/) | Remplacé par (assets/) | Avant | Après |
|---|---|---|---|
| `videos/intro.mp4` (1080p, 15,7 Mb/s, piste audio) | `videos/intro.mp4` (1080p H.264 CRF 24, sans audio) | 20 164 Ko | 2 500 Ko |
| `videos/video-centrale.mp4` | `videos/video-centrale.mp4` (CRF 26) | 3 209 Ko | 1 897 Ko |
| `videos/gif.mp4` | `videos/gif.mp4` (CRF 28) | 698 Ko | 403 Ko |
| `videos/eat-cookie.gif` (loader) | `img/eat-cookie.webp` (WebP animé sans perte) | 32 Ko | 26 Ko |
| `img/recipes/*-recette.png` (9 cartes du carrousel) | `img/recipes/*-recette.webp` (q 85) | 1 684 Ko | 628 Ko |
| `img/recipes/{nom}.png` (9 cookies des modales) | `img/recipes/{nom}.webp` (q 92) | 2 033 Ko | 984 Ko |
| `img/chocolat-droite.png`, `img/chocolat-gauche.png` | `.webp` (q 85) | 248 Ko | 54 Ko |
| `img/*.jpg` (10 visuels : équipe, cookies, mosaïque, saison, carte) | `.webp` (q 85) | 700 Ko | 539 Ko |

## Jamais référencés par le site (doublons et sources)

| Fichier (archive/) | Taille | Raison |
|---|---|---|
| `img/carte-gmap.png`, `img/equipe.png`, `img/mosaique-cookie-{1,2,3,4}.png`, `img/visuel-cookie-{1,2}.png`, `img/visuel-icecream.png`, `img/visuel-wookie.png` | 4 340 Ko | doublons PNG des JPG utilisés |
| `img/video1titre.png` (4284×1634) | 331 Ko | non référencé |
| `img/recipes/chouchou-beignet.png`, `img/recipes/chouchou-beignet-recette.png` | 275 Ko | recette absente du site |
| `videos/intro.gif` | 1 145 Ko | non référencé (doublon GIF de `gif.mp4`) |
| `fonts/bodoni-72/Bodoni 72.ttc`, `fonts/poppins/Poppins-*.ttf` (5 fichiers) | 1 756 Ko | sources des polices, non servies |
| `fonts/bodoni-72/*.woff`, `fonts/poppins/*.woff` (8 fichiers) | 296 Ko | fallback WOFF jamais demandé par un navigateur moderne (WOFF2 conservé) |
| `fonts/bodoni-72/bodoni-book.woff2`, `fonts/bodoni-72/bodoni-bold.woff2`, `fonts/poppins/poppins-medium-webfont.woff2` | 79 Ko | déclarés en `@font-face` mais jamais utilisés par un texte de la page (prod : 5 polices chargées, pas celles-ci) |

## Dépendance npm retirée

- `svg-injector` : remplacé par l'inlining des SVG au build (`vite.config.js`).

## Bilan

`assets/` : 36 Mo → 7,2 Mo. `dist/` (build) : 28 Mo → 7,3 Mo (dont 6,2 Mo de vidéos et images).
