# Recommandations côté hébergeur (hors scope du repo)

Constaté sur la prod le 25/10/2026 (`curl -sI`, Lighthouse, ecoindex.fr) : nginx/1.18.0 (Ubuntu), **HTTP/1.1 uniquement**, gzip sur `text/html` seulement, **aucun `Cache-Control` / `Expires`** sur les fichiers statiques (pourtant hashés par Vite), WOFF2 servi en `application/octet-stream`.

Ces trois points sont signalés en échec par ecoindex.fr (RWEB_0075 cache, RWEB_0076 compression, RWEB_0083 HTTP/2) mais ne pèsent que sur la métrique « poids » de la 1re visite, et seulement via la compression.

## Configuration nginx proposée

```nginx
server {
    listen 443 ssl http2;            # HTTP/2 (nginx < 1.25.1) ; sinon "http2 on;"
    # ...

    # Compression des ressources texte (le HTML l'est déjà)
    gzip on;
    gzip_comp_level 6;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/css application/javascript image/svg+xml application/json font/woff2;
    # Si le module ngx_brotli est disponible :
    # brotli on; brotli_comp_level 6;
    # brotli_types text/html text/css application/javascript image/svg+xml application/json;

    # Fichiers hashés par Vite : cache long, immutable
    location ~* ^/assets/.+\.(js|css|woff2|webp|png|svg|mp4)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # HTML : toujours revalidé
    location = /index.html {
        add_header Cache-Control "no-cache";
    }
}
```

Dans `/etc/nginx/mime.types`, vérifier :

```
font/woff2   woff2;
image/webp   webp;
```

## Effet attendu

| Mesure | Effet |
|---|---|
| Poids 1re visite (ecoindex.fr) | −89 Ko (JS + CSS gzippés) ; −120 Ko avec brotli (HTML compris) → ≈ +0,4 point |
| Visites suivantes | tout `/assets/` servi depuis le cache navigateur : 1 requête (HTML) au lieu de ~34 |
| HTTP/2 | multiplexage des ~34 requêtes first-party ; pas d'effet sur les métriques EcoIndex |
| RWEB | 0075, 0076, 0083 passent au vert |

Précompresser au build (`vite-plugin-compression` → `.gz`/`.br` + `gzip_static on;`) est une alternative si la compression à la volée n'est pas souhaitée ; elle demande aussi une ligne de configuration nginx.
