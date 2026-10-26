# La Vita Spa Sousse — site web (FR + AR) modernisé

Un seul projet : les pages finales sont déjà générées (`index.html`, `ar/`, `hijama/`, `massage-sousse/`…), avec `build.py`, le CSS, le JavaScript et les photos.

## Contenu du dossier

| Élément | Rôle |
|---|---|
| `index.html`, `ar/`, `hijama/`, `massage-*`, `hammam-sousse-sahloul/`, `contact/` | Les pages du site (FR + AR), prêtes à publier |
| `assets/style.css` | Design : dégradés, animations, cartes, galerie, mobile |
| `assets/main.js` | Animations au défilement, menu mobile, agrandissement des photos |
| `assets/images/` | Vos photos (matériel, accueil, soins, hammam) |
| `build.py` | Génère toutes les pages (textes, villes, SEO) |
| `rebuild.bat` / `rebuild.sh` | Lance `build.py` d'un double-clic |
| `.github/workflows/deploy.yml` | Option : publication via GitHub Actions |

## Publier sur GitHub (méthode simple)

1. Créez un dépôt sur GitHub, puis **Add file → Upload files** et glissez tout le contenu du dossier.
2. **Settings → Pages → Deploy from a branch → main / (root) → Save**.
3. Le site est en ligne après 1 à 2 minutes : `https://VOTRE-COMPTE.github.io/NOM-DU-DEPOT/`

## Mettre vos vraies adresses (important pour Google)

Ouvrez `build.py`, ligne `SITE_URL = …`, remplacez `VOTRE-COMPTE` et le nom du dépôt par les vôtres (ou votre domaine), puis lancez `rebuild.bat` (Windows) ou `./rebuild.sh`. Python 3 est nécessaire. Renvoyez ensuite les fichiers modifiés sur GitHub. Vous pouvez aussi modifier ici le téléphone, l'adresse exacte et les coordonnées GPS (`BUSINESS`).

## Changer les photos

Remplacez les fichiers de `assets/images/` en gardant les mêmes noms :
`outils-massage.jpg`, `spa-sousse-accueil.jpg`, `spa-sousse-soins.jpg`, `hammam-turc-sahloul.jpg`, `hammam-individuel-sousse.jpg`.
Pour changer les descriptions (texte alternatif, utile au SEO), modifiez `PHOTOS` dans `build.py`.

## Option : GitHub Actions

Si vous préférez que GitHub reconstruise le site seul : **Settings → Pages → Source : GitHub Actions**, puis lancez le workflow « Deploy site to GitHub Pages » depuis l'onglet Actions.

## Checklist SEO après la mise en ligne

1. **Google Business Profile** (fiche Google Maps) à Sahloul, mêmes téléphones que le site, zone de service : Monastir, Nabeul, Mahdia, Hammamet. C'est le levier n°1.
2. **Google Search Console** : ajoutez le site et envoyez `sitemap.xml`.
3. **Avis clients Google** (vrais avis uniquement).
4. Mettez l'adresse du site dans la bio Instagram @la_vita_spa_sousse.
5. Gardez le même nom, adresse et téléphone partout (site, Google, Instagram, Facebook).
6. Ajoutez des articles régulièrement (bienfaits du massage, hijama et précautions…).

## Notes

- La page hijama mentionne les contre-indications (grossesse, anticoagulants…) et ne promet aucune guérison.
- Les polices viennent de Google Fonts (connexion internet nécessaire pour les voir) ; les icônes sont intégrées au site.
- Aucun prix n'est affiché ; ajoutez-les dans `SERVICES` si vous le souhaitez.
