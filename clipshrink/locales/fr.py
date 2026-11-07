"""Français. Not yet checked by a native speaker: corrections are welcome on GitHub."""

MESSAGES = {
    # --- Steps, pages and buttons
    "Find videos": "Trouver les vidéos",
    "See the saving": "Voir le gain",
    "Convert": "Convertir",
    "Compare and clean up": "Comparer et nettoyer",
    "Settings": "Paramètres",
    "{app} {version}: shrink videos, keep the quality": "{app} {version} : réduisez vos vidéos, gardez la qualité",
    "←  Back": "←  Retour",
    "Choose folder…": "Choisir un dossier…",
    "Choose the folder with your videos": "Choisissez le dossier contenant vos vidéos",
    "No folder chosen": "Aucun dossier choisi",
    "Find your videos": "Trouvez vos vidéos",
    "Pick a folder. This tool looks through it and every folder inside it, and lists the H.264 videos it can shrink. Nothing is changed yet.":
        "Choisissez un dossier. L'outil le parcourt, ainsi que tous ses sous-dossiers, et liste les vidéos H.264 qu'il peut réduire. Rien n'est encore modifié.",
    "Next: see the saving  →": "Suivant : voir le gain  →",
    "Reading your videos…": "Lecture de vos vidéos…",
    "File": "Fichier",
    "Folder": "Dossier",
    "Size": "Taille",
    "Picture": "Image",
    "Length": "Durée",
    "State": "État",
    "Ready": "Prête",
    "Already has a conversion": "A déjà une conversion",
    "GoPro low-res preview, off by default": "Aperçu GoPro basse résolution, décoché par défaut",
    "Already {codec}, skipped": "Déjà en {codec}, ignorée",
    "(converted by this tool)": "(convertie par cet outil)",
    "{n} could not be read and were skipped: {names}.": "{n} n'ont pas pu être lues et ont été ignorées : {names}.",
    "No H.264 videos found in this folder or its subfolders.": "Aucune vidéo H.264 trouvée dans ce dossier ni dans ses sous-dossiers.",
    "Delete GoPro LRV files?": "Supprimer les fichiers LRV de la GoPro ?",
    "An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera and its phone app can show quick previews. You don't need it if you have the original video, which is beside each of these.":
        "Un fichier LRV est une petite copie en basse résolution qu'une GoPro enregistre à côté de chaque vidéo, pour que la caméra et son application mobile affichent des aperçus rapides. Vous n'en avez pas besoin si vous avez la vidéo originale, qui se trouve à côté de chacun d'eux.",
    "Done": "Terminé",
    "Left in place:": "Laissés en place :",
    "Left as they are:": "Laissés tels quels :",

    # --- See the saving
    "See the saving before anything converts": "Voyez le gain avant toute conversion",
    "This makes short test encodes from a few of your own files and measures them. Your files are only read, and nothing appears in your folders.":
        "L'outil fait de courts encodages d'essai à partir de quelques-uns de vos fichiers et les mesure. Vos fichiers sont seulement lus, et rien n'apparaît dans vos dossiers.",
    "Run the test encodes": "Lancer les encodages d'essai",
    "Not measured yet": "Pas encore mesuré",
    "Click \"Run the test encodes\" to measure how much space you would save.":
        "Cliquez sur « Lancer les encodages d'essai » pour mesurer l'espace que vous gagneriez.",
    "Measuring…": "Mesure en cours…",
    "Encoding samples of your files and comparing them with the originals.":
        "Encodage d'extraits de vos fichiers et comparaison avec les originaux.",
    "Could not measure": "Mesure impossible",
    "The test encode stopped: {error}": "L'encodage d'essai s'est arrêté : {error}",
    "About {size} saved ({pct}%)": "Environ {size} gagnés ({pct} %)",
    "Likely between {low} and {high}, out of {total}.": "Probablement entre {low} et {high}, sur {total}.",
    "Converting everything should take {time}.": "Tout convertir devrait prendre {time}.",
    "Sample from": "Extrait de",
    "At": "À",
    "Original": "Original",
    "VMAF average": "VMAF moyen",
    "VMAF worst 1%": "VMAF pire 1 %",
    "Meets the quality target?": "Atteint l'objectif de qualité ?",
    "Yes": "Oui",
    "⚠ No, would get a warning": "⚠ Non, aurait un avertissement",
    "Start converting  →": "Lancer la conversion  →",
    "Expected time: {time}. Your computer will not go to sleep while this runs.":
        "Durée prévue : {time}. Votre ordinateur ne se mettra pas en veille pendant ce temps.",
    "The target: VMAF average at least {mean}, worst 1% of frames at least {p1}. Every full file is measured again after conversion.":
        "L'objectif : VMAF moyen d'au moins {mean}, et au moins {p1} pour le pire 1 % des images. Chaque fichier complet est mesuré à nouveau après la conversion.",
    "{codec}. Change this in Settings.": "{codec}. Modifiable dans les Paramètres.",
    "{codec}, at most {size}. Change this in Settings.": "{codec}, au plus {size}. Modifiable dans les Paramètres.",

    # --- Convert
    "Files Processed": "Fichiers traités",
    "Space Saved": "Espace gagné",
    "Current Batch": "Lot en cours",
    "Time Remaining": "Temps restant",
    "Pause": "Pause",
    "Resume": "Reprendre",
    "Paused": "En pause",
    "Calculating…": "Calcul…",
    "Overall Progress": "Progression globale",
    "Overall Progress: {pct}% ({done} of {total} files)": "Progression globale : {pct} % ({done} fichiers sur {total})",
    "Current File": "Fichier en cours",
    "Current File: {name}: {stage}": "Fichier en cours : {name} : {stage}",
    "Current File: none, the batch is finished": "Fichier en cours : aucun, le lot est terminé",
    "All": "Tous",
    "Completed": "Terminés",
    "Active": "En cours",
    "Waiting": "En attente",
    "Before": "Avant",
    "After": "Après",
    "% Saved": "% gagné",
    "Worst 1%": "Pire 1 %",
    "Encoding": "Encodage",
    "Next: compare and clean up  →": "Suivant : comparer et nettoyer  →",
    "Finding the right quality": "Recherche de la bonne qualité",
    "Measuring every frame": "Mesure de chaque image",
    "Finding quality": "Recherche de qualité",
    "Measuring": "Mesure",
    "Finished: {n} verified": "Terminé : {n} vérifiées",
    ", ⚠ {n} below target": ", ⚠ {n} sous l'objectif",
    ", {n} kept as original": ", {n} gardées en original",
    "(see next page)": "(voir la page suivante)",
    "Nothing left to convert: every selected file is already finished.":
        "Plus rien à convertir : tous les fichiers sélectionnés sont déjà terminés.",
    "The batch stopped": "Le lot s'est arrêté",
    "Files already verified are safe. Reopen the app to continue.":
        "Les fichiers déjà vérifiés sont en sécurité. Rouvrez l'application pour continuer.",
    "Continue where you left off?": "Reprendre là où vous en étiez ?",
    "Each conversion is saved beside its original with {suffix} added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Chaque conversion est enregistrée à côté de son original, avec {suffix} ajouté au nom. Les originaux sont seulement lus. Vous pouvez mettre en pause à tout moment, et si le PC plante, rouvrez simplement l'application.",
    "Each conversion is saved beside its original with {suffix} ({shrunk} if it was shrunk) added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Chaque conversion est enregistrée à côté de son original, avec {suffix} ({shrunk} si elle a été réduite) ajouté au nom. Les originaux sont seulement lus. Vous pouvez mettre en pause à tout moment, et si le PC plante, rouvrez simplement l'application.",
    "Stop converting?": "Arrêter la conversion ?",
    "The batch is still running. If you close now, the current file is restarted next time and finished files are kept. Close anyway?":
        "Le lot est toujours en cours. Si vous fermez maintenant, le fichier en cours sera recommencé la prochaine fois et les fichiers terminés sont conservés. Fermer quand même ?",

    # --- Statuses
    "Working…": "En cours…",
    "Verified": "Vérifiée",
    "⚠ Below target": "⚠ Sous l'objectif",
    "Resized": "Redimensionnée",
    "Verified at {mean} / {p1}": "Vérifiée à {mean} / {p1}",
    "Resized at {mean} / {p1}": "Redimensionnée à {mean} / {p1}",
    "Original kept": "Original conservé",
    "Failed, original kept": "Échec, original conservé",
    "Original in Recycle Bin": "Original dans la Corbeille",
    "Done, has the original's name": "Terminé, porte le nom de l'original",
    "processor": "processeur",

    # --- Compare and clean up
    "Play any original beside its conversion, in sync. When you are happy, you can send originals to the Recycle Bin. This step is optional. Click a column title to sort.":
        "Lisez n'importe quel original à côté de sa conversion, en synchronisé. Quand vous êtes satisfait, vous pouvez envoyer les originaux à la Corbeille. Cette étape est facultative. Cliquez sur un titre de colonne pour trier.",
    "Select All": "Tout cocher",
    "Deselect All": "Tout décocher",
    "Select Recommended": "Cocher les recommandées",
    "Deselect Recommended": "Décocher les recommandées",
    "Recommended means the conversion met the quality target, with no warning sign.":
        "Recommandée signifie que la conversion a atteint l'objectif de qualité, sans avertissement.",
    "Tip: Ctrl+click a row to tick it, Shift+click to tick a range, Ctrl+A to tick all. Right-click a row to open its folder.":
        "Astuce : Ctrl+clic coche une ligne, Maj+clic coche une plage, Ctrl+A coche tout. Clic droit sur une ligne pour ouvrir son dossier.",
    "Delete?": "Supprimer ?",
    "Result": "Résultat",
    "▶  Play selected side by side": "▶  Lire la sélection côte à côte",
    "Remove the added tags from names": "Retirer les suffixes ajoutés aux noms",
    "Send ticked originals to Recycle Bin…": "Envoyer les originaux cochés à la Corbeille…",
    "Tick originals above to delete them": "Cochez des originaux ci-dessus pour les supprimer",
    "Needs your attention": "À vérifier",
    "Needs your attention ({n})": "À vérifier ({n})",
    "Needs your attention: nothing": "À vérifier : rien",
    "Every conversion passed.": "Toutes les conversions ont réussi.",
    "Nothing converted yet.": "Rien n'a encore été converti.",
    "{size} can be saved once originals are removed": "{size} peuvent être gagnés une fois les originaux supprimés",
    "Available after an original has been sent to the Recycle Bin.": "Disponible une fois qu'un original a été envoyé à la Corbeille.",
    "Start Over": "Recommencer",
    "Forget these files and go back to step 1. Your videos and reports aren't touched.":
        "Oublier ces fichiers et revenir à l'étape 1. Vos vidéos et vos rapports ne sont pas touchés.",
    "Open file location": "Ouvrir l'emplacement du fichier",
    "Pick a video": "Choisissez une vidéo",
    "Click a row in the list first.": "Cliquez d'abord sur une ligne de la liste.",
    "Cannot compare": "Comparaison impossible",
    "This row needs both an original and a verified conversion on disk.":
        "Cette ligne doit avoir à la fois un original et une conversion vérifiée sur le disque.",
    "Re-checking and removing": "Revérification et suppression",
    "Renaming": "Renommage",
    "finishing": "finalisation",
    "{action} {i} of {total}: {name}": "{action} {i} sur {total} : {name}",
    "Remove the added tags from names?": "Retirer les suffixes ajoutés aux noms ?",
    "Only the name changes. If you later restore an original from the Recycle Bin, Windows will ask what to do about the same name.":
        "Seul le nom change. Si vous restaurez plus tard un original depuis la Corbeille, Windows vous demandera quoi faire du nom identique.",
    "Send originals to the Recycle Bin?": "Envoyer les originaux à la Corbeille ?",
    "I understand. Send these originals to the Recycle Bin.": "J'ai compris. Envoyer ces originaux à la Corbeille.",
    "Send to Recycle Bin": "Envoyer à la Corbeille",
    "Keep them": "Les garder",
    "Below the quality target. Compare it with the original before removing the original.":
        "Sous l'objectif de qualité. Comparez-la avec l'original avant de supprimer l'original.",

    # --- Player
    "Side by side: {name}": "Côte à côte : {name}",
    "Original (H.264)": "Original (H.264)",
    "Original (H.264), shrunk to match": "Original (H.264), réduit pour correspondre",
    "Conversion ({codec})": "Conversion ({codec})",
    "Play": "Lecture",
    "◀ Frame": "◀ Image",
    "Frame ▶": "Image ▶",
    "Whole picture": "Image entière",
    "Drag the picture to look around": "Faites glisser l'image pour l'explorer",
    "VMAF average {mean}, worst 1% {p1}": "VMAF moyen {mean}, pire 1 % {p1}",
    "Could not play": "Lecture impossible",
    "Player": "Lecteur",

    # --- Settings
    "Language": "Langue",
    "The default settings suit most people, so you can leave this page alone. Change something only if you have a reason.":
        "Les réglages par défaut conviennent à la plupart des gens : vous pouvez laisser cette page telle quelle. Ne changez quelque chose que si vous avez une raison.",
    "Encode with": "Encoder avec",
    "Graphics card (fast, recommended)": "Carte graphique (rapide, recommandé)",
    "Processor (slow, works on any PC)": "Processeur (lent, fonctionne sur tout PC)",
    "Graphics card (fast, recommended) ({card} detected)": "Carte graphique (rapide, recommandé) ({card} détectée)",
    "Graphics card ({card} can't make this format)": "Carte graphique ({card} ne sait pas faire ce format)",
    "Graphics card (no compatible graphics card detected)": "Carte graphique (aucune carte graphique compatible détectée)",
    "NVIDIA card": "carte NVIDIA",
    "In use: your graphics card, making {codec} video.": "Utilisé : votre carte graphique, en vidéo {codec}.",
    "In use: your processor, making {codec} video.": "Utilisé : votre processeur, en vidéo {codec}.",
    "{card} was found, but it can't make {codec} video, so the processor is used.":
        "{card} a été trouvée, mais elle ne sait pas faire de vidéo {codec}, donc le processeur est utilisé.",
    "No compatible graphics card was found (only NVIDIA is supported), so the processor is used.":
        "Aucune carte graphique compatible n'a été trouvée (seule NVIDIA est prise en charge), donc le processeur est utilisé.",
    "Video format": "Format vidéo",
    "H.265 (recommended)": "H.265 (recommandé)",
    "AV1 files are usually smaller, but they play on fewer devices. Check that your TV or phone can play one first.":
        "Les fichiers AV1 sont souvent plus petits, mais ils sont lus par moins d'appareils. Vérifiez d'abord que votre téléviseur ou votre téléphone peut en lire un.",
    "Largest size": "Taille maximale",
    "Keep the original resolution (recommended)": "Garder la résolution d'origine (recommandé)",
    "This permanently lowers the detail in the conversions, and videos are never enlarged. They are checked against a smaller copy of the original and labelled Resized. Keep the originals if you might want the full detail later.":
        "Cela réduit définitivement le niveau de détail des conversions, et les vidéos ne sont jamais agrandies. Elles sont comparées à une copie réduite de l'original et marquées Redimensionnée. Gardez les originaux si vous pourriez vouloir tout le détail plus tard.",
    "Show an Encoding column": "Afficher une colonne Encodage",
    "Format, quality setting, resolution and bitrate of each conversion.":
        "Format, réglage de qualité, résolution et débit de chaque conversion.",
    "Show the Welcome screen when the app opens": "Afficher l'écran d'accueil à l'ouverture",
    "Advanced": "Avancé",
    "Only change these if you know what you are doing: they can lower the quality of your videos.":
        "Ne modifiez ces valeurs que si vous savez ce que vous faites : elles peuvent réduire la qualité de vos vidéos.",
    "Read what each one does": "Lire à quoi sert chacune",
    "I've read this and understand what I'm doing": "J'ai lu ceci et je comprends ce que je fais",
    "Warn below": "Avertir sous",
    "Also aim for these values when choosing quality": "Viser aussi ces valeurs pour choisir la qualité",
    "Ticked, lower values make smaller files with lower quality, and higher values make larger files. Not ticked, your files stay the same and only the warning moves.":
        "Coché, des valeurs plus basses donnent des fichiers plus petits et de moindre qualité, et des valeurs plus hautes des fichiers plus gros. Non coché, vos fichiers ne changent pas et seul l'avertissement bouge.",
    "Don't keep a conversion below a minimum": "Ne pas garder une conversion sous un minimum",
    "Below the minimum, nothing is kept and your original stays. Off by default, so every result that is smaller and matches is kept, with a warning if needed.":
        "Sous le minimum, rien n'est gardé et votre original reste. Désactivé par défaut : tout résultat plus petit et conforme est gardé, avec un avertissement si besoin.",
    "Back to the defaults": "Revenir aux valeurs par défaut",
    "Your target is {mean}.": "Votre objectif est {mean}.",
    "How close this video looks to the original, from 0 to 100. VMAF is a score made by Netflix, based on how people see video. At 95 or above, most people can't see a difference.":
        "À quel point cette vidéo ressemble à l'original, de 0 à 100. VMAF est un score créé par Netflix, fondé sur la façon dont les gens perçoivent la vidéo. À partir de 95, la plupart des gens ne voient aucune différence.",
    "The score of the worst moments: 1% of the video's frames score lower than this. It catches a short bad patch that a good average would hide. The target is {p1} or above.":
        "Le score des pires moments : 1 % des images de la vidéo ont un score plus bas. Il repère un court passage raté qu'une bonne moyenne cacherait. L'objectif est {p1} ou plus.",

    # --- Welcome
    "Welcome to {app}": "Bienvenue dans {app}",
    "Shrink your videos, keep the quality.": "Réduisez vos vidéos, gardez la qualité.",
    "Zero guesswork": "Zéro tâtonnement",
    "No bitrates or codecs to configure. ClipShrink automatically finds the right compression balance for every video.":
        "Aucun débit ni codec à régler. ClipShrink trouve automatiquement le bon équilibre de compression pour chaque vidéo.",
    "Measured frame-by-frame": "Mesuré image par image",
    "Every result is scored against the original using Netflix's VMAF visual quality metric, and any clip that misses the target is clearly flagged.":
        "Chaque résultat est noté par rapport à l'original avec VMAF, la mesure de qualité visuelle de Netflix, et toute vidéo qui manque l'objectif est clairement signalée.",
    "You stay in control": "Vous gardez la main",
    "Conversions are saved as new files alongside your originals. Compare both versions side by side before deciding what to send to the Recycle Bin.":
        "Les conversions sont enregistrées comme nouveaux fichiers à côté de vos originaux. Comparez les deux versions côte à côte avant de décider quoi envoyer à la Corbeille.",
    "Don't show this again": "Ne plus afficher",

    # --- About
    "About {app}": "À propos de {app}",
    "{app} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion against its original with VMAF and warns you about any below the quality target. Your originals are only read during conversion, and nothing is sent anywhere.":
        "{app} convertit les vidéos H.264 en H.265 ou AV1 pour libérer de l'espace disque. Il mesure chaque conversion par rapport à son original avec VMAF et vous avertit de toute conversion sous l'objectif de qualité. Vos originaux sont seulement lus pendant la conversion, et rien n'est envoyé nulle part.",
    "Documentation:": "Documentation :",
    "Open in your browser": "Ouvrir dans votre navigateur",
    "Copy the link": "Copier le lien",
    "Project:": "Projet :",
    "Reports:": "Rapports :",
    "Each batch leaves a CSV report here. They're only for your information. Once a batch is finished and you exit or click Start Over, the app forgets those files.":
        "Chaque lot laisse ici un rapport CSV, uniquement pour votre information. Une fois un lot terminé, quand vous quittez ou cliquez sur Recommencer, l'application oublie ces fichiers.",
    "Licence:": "Licence :",
    "GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace.":
        "GPL-3.0. Elle est fournie sans garantie : gardez une sauvegarde des vidéos que vous ne pourriez pas remplacer.",
    "Built with:": "Conçu avec :",
    "FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in THIRD_PARTY_NOTICES.md in the install folder and on the project page.":
        "FFmpeg, x265, SVT-AV1, VMAF, mpv et Qt. Leurs licences et les liens vers leur code source se trouvent dans THIRD_PARTY_NOTICES.md, dans le dossier d'installation et sur la page du projet.",
    "What does \"no quality loss\" mean?": "Que veut dire « sans perte de qualité » ?",
    "Truly lossless H.265, where every pixel stays identical, usually makes files larger than the originals, so it would cost you space instead of saving it. This tool uses a measured definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure from Netflix of how a video looks to people, scored from 0 to 100. A conversion counts as recommended if the average score is at least 95 and the worst 1% of frames score at least 90, a level where differences are very hard to see. This is the quality target.\n\n"
    "If a file misses the target even at the best setting, it is still converted, and it gets a warning sign so you can decide for yourself. Use Select Recommended to leave those files out when cleaning up. If the result is not smaller, your original is simply kept and the file is listed in the report. Sound, any GoPro telemetry and capture dates are copied unchanged, and originals are never touched during conversion.\n\n"
    "If you choose a smaller resolution in Settings, the conversion is compared with a smaller copy of the original at the same size. So the score shows how clean the encoding is, not the detail lost by shrinking, and those files are labelled Resized rather than Verified.\n\n"
    "The advanced part of Settings can change these numbers. Files judged by other numbers show them in their label.":
        "Un H.265 vraiment sans perte, où chaque pixel reste identique, donne en général des fichiers plus gros que les originaux : vous perdriez de la place au lieu d'en gagner. Cet outil utilise donc une définition mesurée.\n\n"
        "Après chaque conversion, il compare chaque image à l'original avec VMAF, une mesure ouverte de Netflix qui note de 0 à 100 l'aspect d'une vidéo pour l'œil humain. Une conversion est recommandée si le score moyen est d'au moins 95 et si le pire 1 % des images obtient au moins 90, un niveau où les différences sont très difficiles à voir. C'est l'objectif de qualité.\n\n"
        "Si un fichier manque l'objectif même au meilleur réglage, il est quand même converti, avec un signe d'avertissement pour que vous décidiez vous-même. Utilisez Cocher les recommandées pour écarter ces fichiers lors du nettoyage. Si le résultat n'est pas plus petit, votre original est simplement conservé et le fichier figure dans le rapport. Le son, la télémétrie GoPro éventuelle et les dates de prise de vue sont copiés tels quels, et les originaux ne sont jamais modifiés pendant la conversion.\n\n"
        "Si vous choisissez une résolution plus petite dans les Paramètres, la conversion est comparée à une copie réduite de l'original, à la même taille. Le score montre donc la propreté de l'encodage, pas le détail perdu en réduisant, et ces fichiers sont marqués Redimensionnée plutôt que Vérifiée.\n\n"
        "La partie avancée des Paramètres peut changer ces chiffres. Les fichiers jugés selon d'autres chiffres les affichent dans leur libellé.",

    # --- Sizes and times
    "bytes": "octets",
    "KB": "Ko",
    "MB": "Mo",
    "GB": "Go",
    "TB": "To",
    "~{m}m left": "~{m} min restantes",
    "~{h}h {m}m left": "~{h} h {m} restantes",
    "under a minute": "moins d'une minute",
    "about {h} h {m} min": "environ {h} h {m} min",
    "about {d} days": "environ {d} jours",

    # --- Reasons
    "Could not convert, original kept: {error}": "Conversion impossible, original conservé : {error}",
    "This is {codec}, not H.264, so it was left alone.": "Ce fichier est en {codec}, pas en H.264 : il n'a pas été touché.",
    "the encoder stopped: {detail}": "l'encodeur s'est arrêté : {detail}",
    "the encoder failed: {detail}": "l'encodeur a échoué : {detail}",
    "could not write the file: {detail}": "impossible d'écrire le fichier : {detail}",
    "could not read a sample from the file: {detail}": "impossible de lire un extrait du fichier : {detail}",
    "the VMAF comparison could not run: {detail}": "la comparaison VMAF n'a pas pu se faire : {detail}",
    "the VMAF comparison returned no frames": "la comparaison VMAF n'a renvoyé aucune image",
    "the original changed while it was being converted": "l'original a changé pendant sa conversion",
    "Conversion is not smaller ({out} vs {src} bytes), original kept.": "La conversion n'est pas plus petite ({out} contre {src} octets), original conservé.",
    "Conversion did not match the original, original kept: {problems}": "La conversion ne correspondait pas à l'original, original conservé : {problems}",
    "video is {codec}": "la vidéo est en {codec}",
    "resolution differs": "la résolution diffère",
    "pixel format differs ({out} vs {src})": "le format de pixel diffère ({out} contre {src})",
    "colour range differs": "la plage de couleurs diffère",
    "audio tracks differ": "les pistes audio diffèrent",
    "duration differs ({out}s vs {src}s)": "la durée diffère ({out} s contre {src} s)",
    "frame count differs ({out} vs {src})": "le nombre d'images diffère ({out} contre {src})",
    "audio or telemetry tracks changed": "des pistes audio ou de télémétrie ont changé",
    "camera info changed": "les informations de la caméra ont changé",
    "VMAF compared {frames} frames out of {total}, original kept.": "VMAF a comparé {frames} images sur {total}, original conservé.",
    "VMAF short of what the search aims for.": "VMAF en dessous de ce que vise la recherche.",
    "VMAF below your minimum: average {mean} (minimum {min_mean}), worst 1% {p1} (minimum {min_p1}). Nothing was kept, and your original is untouched.":
        "VMAF sous votre minimum : moyenne {mean} (minimum {min_mean}), pire 1 % {p1} (minimum {min_p1}). Rien n'a été gardé, et votre original n'est pas touché.",
    "VMAF below the target: average {mean} (target {warn_mean}), worst 1% {p1} (target {warn_p1}). Compare it before removing the original.":
        "VMAF sous l'objectif : moyenne {mean} (objectif {warn_mean}), pire 1 % {p1} (objectif {warn_p1}). Comparez-la avant de supprimer l'original.",
    "this file was never converted by this tool": "ce fichier n'a jamais été converti par cet outil",
    "its original has not been sent to the Recycle Bin": "son original n'a pas été envoyé à la Corbeille",
    "the converted file is missing": "le fichier converti est introuvable",
    "it already has the original's name": "il porte déjà le nom de l'original",
    "the converted file has changed since it was verified": "le fichier converti a changé depuis sa vérification",
    "another file already has that name": "un autre fichier porte déjà ce nom",
    "renaming was not confirmed": "le renommage n'a pas été confirmé",
    "Windows refused the rename: {error}": "Windows a refusé le renommage : {error}",
    "it is not an LRV file": "ce n'est pas un fichier LRV",
    "its full video is not beside it": "sa vidéo complète n'est pas à côté",
    "Windows did not move it to the Recycle Bin, so it was left in place": "Windows ne l'a pas déplacé dans la Corbeille, il est donc resté en place",
    "its conversion is not verified (status: {status})": "sa conversion n'est pas vérifiée (état : {status})",
    "the original has changed since it was verified": "l'original a changé depuis sa vérification",
    "the converted file's content does not match what was verified": "le contenu du fichier converti ne correspond pas à ce qui a été vérifié",
    "the converted file cannot be read: {error}": "le fichier converti est illisible : {error}",
    "the converted file is not H.265 or AV1": "le fichier converti n'est ni en H.265 ni en AV1",
    "deletion was not confirmed": "la suppression n'a pas été confirmée",
    "its conversion is below the default quality target, and that was not confirmed": "sa conversion est sous l'objectif de qualité par défaut, et cela n'a pas été confirmé",
    "its conversion has a lower resolution, and that was not confirmed": "sa conversion a une résolution plus basse, et cela n'a pas été confirmé",

    # --- Report columns
    "Date": "Date",
    "Reason": "Raison",
    "Before (bytes)": "Avant (octets)",
    "After (bytes)": "Après (octets)",
    "Saved %": "% gagné",
    "Encoder": "Encodeur",
    "Quality setting": "Réglage de qualité",
    "Conversion": "Conversion",
    "Codec": "Codec",
    "Output resolution": "Résolution de sortie",
    "Output bitrate (Mbit/s)": "Débit de sortie (Mbit/s)",
    "Target average": "Objectif moyen",
    "Target worst 1%": "Objectif pire 1 %",
}

PLURALS = {
    "Found {n} GoPro LRV file ({size}).": ("{n} fichier LRV GoPro trouvé ({size}).", "{n} fichiers LRV GoPro trouvés ({size})."),
    "Measured on {n} file using your graphics card.": ("Mesuré sur {n} fichier avec votre carte graphique.", "Mesuré sur {n} fichiers avec votre carte graphique."),
    "Measured on {n} file using your processor.": ("Mesuré sur {n} fichier avec votre processeur.", "Mesuré sur {n} fichiers avec votre processeur."),
    "Remove the added tags from {n} name…": ("Retirer les suffixes ajoutés de {n} nom…", "Retirer les suffixes ajoutés de {n} noms…"),
    "Send it to the Recycle Bin?": ("L'envoyer à la Corbeille ?", "Les envoyer à la Corbeille ?"),
    "Send {n} ticked original to Recycle Bin…": ("Envoyer {n} original coché à la Corbeille…", "Envoyer {n} originaux cochés à la Corbeille…"),
    "about {n} minute": ("environ {n} minute", "environ {n} minutes"),
    "{n} H.264 video, {size}.": ("{n} vidéo H.264, {size}.", "{n} vidéos H.264, {size}."),
    "{n} LRV file moved to the Recycle Bin.": ("{n} fichier LRV déplacé dans la Corbeille.", "{n} fichiers LRV déplacés dans la Corbeille."),
    "{n} conversion whose original is in the Recycle Bin will take the original's name, for example {name}.":
        ("{n} conversion dont l'original est dans la Corbeille prendra le nom de l'original, par exemple {name}.",
         "{n} conversions dont l'original est dans la Corbeille prendront le nom de l'original, par exemple {name}."),
    "{n} file renamed.": ("{n} fichier renommé.", "{n} fichiers renommés."),
    "{n} original ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, and you can restore originals from the Recycle Bin.":
        ("{n} original ({size}) ira dans la Corbeille de Windows. Chaque conversion est d'abord revérifiée, et vous pouvez restaurer les originaux depuis la Corbeille.",
         "{n} originaux ({size}) iront dans la Corbeille de Windows. Chaque conversion est d'abord revérifiée, et vous pouvez restaurer les originaux depuis la Corbeille."),
    "{n} original moved to the Recycle Bin.": ("{n} original déplacé dans la Corbeille.", "{n} originaux déplacés dans la Corbeille."),
    "{n} other LRV file will stay, because the original video isn't beside it.":
        ("{n} autre fichier LRV restera, car la vidéo originale n'est pas à côté.",
         "{n} autres fichiers LRV resteront, car la vidéo originale n'est pas à côté."),
    "{n} video already in H.265, skipped.": ("{n} vidéo déjà en H.265, ignorée.", "{n} vidéos déjà en H.265, ignorées."),
    "{n} video from your last batch is not finished. Files already verified will not be converted again. Continue now?":
        ("{n} vidéo de votre dernier lot n'est pas terminée. Les fichiers déjà vérifiés ne seront pas reconvertis. Continuer maintenant ?",
         "{n} vidéos de votre dernier lot ne sont pas terminées. Les fichiers déjà vérifiés ne seront pas reconvertis. Continuer maintenant ?"),
    "{n} video in another format, skipped.": ("{n} vidéo dans un autre format, ignorée.", "{n} vidéos dans un autre format, ignorées."),
    "{n} video, {size}.": ("{n} vidéo, {size}.", "{n} vidéos, {size}."),
    "⚠ {n} of these has a conversion at a lower resolution. Once the original is gone from the Recycle Bin, that detail is gone for good.":
        ("⚠ {n} d'entre eux a une conversion en résolution plus basse. Une fois l'original sorti de la Corbeille, ce détail est perdu pour de bon.",
         "⚠ {n} d'entre eux ont une conversion en résolution plus basse. Une fois l'original sorti de la Corbeille, ce détail est perdu pour de bon."),
    "⚠ {n} of these has a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). Once the original is gone from the Recycle Bin, that lost quality can't be recovered.":
        ("⚠ {n} d'entre eux a une conversion sous la qualité recommandée (VMAF moyen {mean}, pire 1 % {p1}). Une fois l'original sorti de la Corbeille, cette qualité perdue ne peut pas être récupérée.",
         "⚠ {n} d'entre eux ont une conversion sous la qualité recommandée (VMAF moyen {mean}, pire 1 % {p1}). Une fois l'original sorti de la Corbeille, cette qualité perdue ne peut pas être récupérée."),
}
