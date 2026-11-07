"""Italiano. Not yet checked by a native speaker: corrections are welcome on GitHub."""

MESSAGES = {
    # --- Steps, pages and buttons
    "Find videos": "Trova i video",
    "See the saving": "Vedi il risparmio",
    "Convert": "Converti",
    "Compare and clean up": "Confronta e pulisci",
    "Settings": "Impostazioni",
    "{app} {version}: shrink videos, keep the quality": "{app} {version}: riduci i video, mantieni la qualità",
    "←  Back": "←  Indietro",
    "Choose folder…": "Scegli cartella…",
    "Choose the folder with your videos": "Scegli la cartella con i tuoi video",
    "No folder chosen": "Nessuna cartella scelta",
    "Find your videos": "Trova i tuoi video",
    "Pick a folder. This tool looks through it and every folder inside it, and lists the H.264 videos it can shrink. Nothing is changed yet.":
        "Scegli una cartella. Il programma la esamina insieme a tutte le sottocartelle ed elenca i video H.264 che può ridurre. Per ora non viene modificato nulla.",
    "Next: see the saving  →": "Avanti: vedi il risparmio  →",
    "Reading your videos…": "Lettura dei tuoi video…",
    "File": "File",
    "Folder": "Cartella",
    "Size": "Dimensione",
    "Picture": "Immagine",
    "Length": "Durata",
    "State": "Stato",
    "Ready": "Pronto",
    "Already has a conversion": "Ha già una conversione",
    "GoPro low-res preview, off by default": "Anteprima GoPro a bassa risoluzione, esclusa di default",
    "Already {codec}, skipped": "Già in {codec}, saltato",
    "(converted by this tool)": "(convertito da questo programma)",
    "{n} could not be read and were skipped: {names}.": "{n} non sono leggibili e sono stati saltati: {names}.",
    "No H.264 videos found in this folder or its subfolders.": "Nessun video H.264 trovato in questa cartella o nelle sue sottocartelle.",
    "Delete GoPro LRV files?": "Eliminare i file LRV della GoPro?",
    "An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera and its phone app can show quick previews. You don't need it if you have the original video, which is beside each of these.":
        "Un file LRV è una piccola copia a bassa risoluzione che una GoPro registra accanto a ogni video, così la videocamera e la sua app per telefono possono mostrare anteprime rapide. Non ti serve se hai il video originale, che si trova accanto a ciascuno di essi.",
    "Done": "Fatto",
    "Left in place:": "Rimasti al loro posto:",
    "Left as they are:": "Rimasti come sono:",

    # --- See the saving
    "See the saving before anything converts": "Vedi il risparmio prima di convertire",
    "This makes short test encodes from a few of your own files and measures them. Your files are only read, and nothing appears in your folders.":
        "Vengono fatte brevi codifiche di prova da alcuni dei tuoi file, poi misurate. I tuoi file vengono solo letti e nelle tue cartelle non compare nulla.",
    "Run the test encodes": "Avvia le codifiche di prova",
    "Not measured yet": "Non ancora misurato",
    "Click \"Run the test encodes\" to measure how much space you would save.":
        "Fai clic su «Avvia le codifiche di prova» per misurare quanto spazio risparmieresti.",
    "Measuring…": "Misurazione…",
    "Encoding samples of your files and comparing them with the originals.":
        "Codifica di spezzoni dei tuoi file e confronto con gli originali.",
    "Could not measure": "Misurazione non riuscita",
    "The test encode stopped: {error}": "La codifica di prova si è interrotta: {error}",
    "About {size} saved ({pct}%)": "Circa {size} risparmiati ({pct}%)",
    "Likely between {low} and {high}, out of {total}.": "Probabilmente tra {low} e {high}, su {total}.",
    "Converting everything should take {time}.": "Convertire tutto dovrebbe richiedere {time}.",
    "Sample from": "Spezzone da",
    "At": "A",
    "Original": "Originale",
    "VMAF average": "VMAF medio",
    "VMAF worst 1%": "VMAF peggior 1%",
    "Meets the quality target?": "Raggiunge l'obiettivo di qualità?",
    "Yes": "Sì",
    "⚠ No, would get a warning": "⚠ No, avrebbe un avviso",
    "Start converting  →": "Avvia la conversione  →",
    "Expected time: {time}. Your computer will not go to sleep while this runs.":
        "Tempo previsto: {time}. Il computer non andrà in sospensione nel frattempo.",
    "The target: VMAF average at least {mean}, worst 1% of frames at least {p1}. Every full file is measured again after conversion.":
        "L'obiettivo: VMAF medio almeno {mean}, peggior 1% dei fotogrammi almeno {p1}. Ogni file completo viene misurato di nuovo dopo la conversione.",
    "{codec}. Change this in Settings.": "{codec}. Puoi cambiarlo nelle Impostazioni.",
    "{codec}, at most {size}. Change this in Settings.": "{codec}, al massimo {size}. Puoi cambiarlo nelle Impostazioni.",

    # --- Convert
    "Files Processed": "File elaborati",
    "Space Saved": "Spazio risparmiato",
    "Current Batch": "Lotto attuale",
    "Time Remaining": "Tempo rimanente",
    "Pause": "Pausa",
    "Resume": "Riprendi",
    "Paused": "In pausa",
    "Calculating…": "Calcolo…",
    "Overall Progress": "Avanzamento totale",
    "Overall Progress: {pct}% ({done} of {total} files)": "Avanzamento totale: {pct}% ({done} di {total} file)",
    "Current File": "File attuale",
    "Current File: {name}: {stage}": "File attuale: {name}: {stage}",
    "Current File: none, the batch is finished": "File attuale: nessuno, il lotto è finito",
    "All": "Tutti",
    "Completed": "Completati",
    "Active": "In corso",
    "Waiting": "In attesa",
    "Before": "Prima",
    "After": "Dopo",
    "% Saved": "% risparmiato",
    "Worst 1%": "Peggior 1%",
    "Encoding": "Codifica",
    "Next: compare and clean up  →": "Avanti: confronta e pulisci  →",
    "Finding the right quality": "Ricerca della qualità giusta",
    "Measuring every frame": "Misurazione di ogni fotogramma",
    "Finding quality": "Ricerca qualità",
    "Measuring": "Misurazione",
    "Finished: {n} verified": "Finito: {n} verificati",
    ", ⚠ {n} below target": ", ⚠ {n} sotto l'obiettivo",
    ", {n} kept as original": ", {n} tenuti come originale",
    "(see next page)": "(vedi la pagina successiva)",
    "Nothing left to convert: every selected file is already finished.":
        "Non resta nulla da convertire: tutti i file selezionati sono già finiti.",
    "The batch stopped": "Il lotto si è interrotto",
    "Files already verified are safe. Reopen the app to continue.":
        "I file già verificati sono al sicuro. Riapri l'app per continuare.",
    "Continue where you left off?": "Riprendere da dove avevi lasciato?",
    "Each conversion is saved beside its original with {suffix} added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Ogni conversione viene salvata accanto al suo originale, con {suffix} aggiunto al nome. Gli originali vengono solo letti. Puoi mettere in pausa in qualsiasi momento e, se il PC si blocca, basta riaprire l'app.",
    "Each conversion is saved beside its original with {suffix} ({shrunk} if it was shrunk) added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Ogni conversione viene salvata accanto al suo originale, con {suffix} ({shrunk} se è stata ridotta) aggiunto al nome. Gli originali vengono solo letti. Puoi mettere in pausa in qualsiasi momento e, se il PC si blocca, basta riaprire l'app.",
    "Stop converting?": "Interrompere la conversione?",
    "The batch is still running. If you close now, the current file is restarted next time and finished files are kept. Close anyway?":
        "Il lotto è ancora in corso. Se chiudi ora, il file attuale ripartirà la prossima volta e i file finiti restano. Chiudere comunque?",

    # --- Statuses
    "Working…": "In lavorazione…",
    "Verified": "Verificato",
    "⚠ Below target": "⚠ Sotto l'obiettivo",
    "Resized": "Ridimensionato",
    "Verified at {mean} / {p1}": "Verificato a {mean} / {p1}",
    "Resized at {mean} / {p1}": "Ridimensionato a {mean} / {p1}",
    "Original kept": "Originale tenuto",
    "Failed, original kept": "Non riuscito, originale tenuto",
    "Original in Recycle Bin": "Originale nel Cestino",
    "Done, has the original's name": "Fatto, ha il nome dell'originale",
    "processor": "processore",

    # --- Compare and clean up
    "Play any original beside its conversion, in sync. When you are happy, you can send originals to the Recycle Bin. This step is optional. Click a column title to sort.":
        "Riproduci qualsiasi originale accanto alla sua conversione, in sincrono. Quando sei soddisfatto, puoi spostare gli originali nel Cestino. Questo passaggio è facoltativo. Fai clic sul titolo di una colonna per ordinare.",
    "Select All": "Seleziona tutto",
    "Deselect All": "Deseleziona tutto",
    "Select Recommended": "Seleziona i consigliati",
    "Deselect Recommended": "Deseleziona i consigliati",
    "Recommended means the conversion met the quality target, with no warning sign.":
        "Consigliato significa che la conversione ha raggiunto l'obiettivo di qualità, senza avvisi.",
    "Tip: Ctrl+click a row to tick it, Shift+click to tick a range, Ctrl+A to tick all. Right-click a row to open its folder.":
        "Suggerimento: Ctrl+clic seleziona una riga, Maiusc+clic un intervallo, Ctrl+A tutto. Clic destro su una riga per aprirne la cartella.",
    "Delete?": "Eliminare?",
    "Result": "Risultato",
    "▶  Play selected side by side": "▶  Riproduci la selezione affiancata",
    "Remove the added tags from names": "Togli i suffissi aggiunti ai nomi",
    "Send ticked originals to Recycle Bin…": "Sposta gli originali selezionati nel Cestino…",
    "Tick originals above to delete them": "Seleziona sopra gli originali da eliminare",
    "Needs your attention": "Da controllare",
    "Needs your attention ({n})": "Da controllare ({n})",
    "Needs your attention: nothing": "Da controllare: niente",
    "Every conversion passed.": "Tutte le conversioni sono riuscite.",
    "Nothing converted yet.": "Ancora nulla di convertito.",
    "{size} can be saved once originals are removed": "{size} risparmiabili una volta rimossi gli originali",
    "Available after an original has been sent to the Recycle Bin.": "Disponibile dopo che un originale è stato spostato nel Cestino.",
    "Start Over": "Ricomincia",
    "Forget these files and go back to step 1. Your videos and reports aren't touched.":
        "Dimentica questi file e torna al passaggio 1. I tuoi video e i rapporti non vengono toccati.",
    "Open file location": "Apri percorso file",
    "Pick a video": "Scegli un video",
    "Click a row in the list first.": "Fai prima clic su una riga dell'elenco.",
    "Cannot compare": "Confronto impossibile",
    "This row needs both an original and a verified conversion on disk.":
        "Questa riga richiede sia un originale sia una conversione verificata sul disco.",
    "Re-checking and removing": "Ricontrollo e rimozione",
    "Renaming": "Ridenominazione",
    "finishing": "completamento",
    "{action} {i} of {total}: {name}": "{action} {i} di {total}: {name}",
    "Remove the added tags from names?": "Togliere i suffissi aggiunti ai nomi?",
    "Only the name changes. If you later restore an original from the Recycle Bin, Windows will ask what to do about the same name.":
        "Cambia solo il nome. Se in seguito ripristini un originale dal Cestino, Windows ti chiederà cosa fare con il nome uguale.",
    "Send originals to the Recycle Bin?": "Spostare gli originali nel Cestino?",
    "I understand. Send these originals to the Recycle Bin.": "Ho capito. Sposta questi originali nel Cestino.",
    "Send to Recycle Bin": "Sposta nel Cestino",
    "Keep them": "Tienili",
    "Below the quality target. Compare it with the original before removing the original.":
        "Sotto l'obiettivo di qualità. Confrontalo con l'originale prima di rimuovere l'originale.",

    # --- Player
    "Side by side: {name}": "Affiancati: {name}",
    "Original (H.264)": "Originale (H.264)",
    "Original (H.264), shrunk to match": "Originale (H.264), ridotto per corrispondere",
    "Conversion ({codec})": "Conversione ({codec})",
    "Play": "Riproduci",
    "◀ Frame": "◀ Fotogramma",
    "Frame ▶": "Fotogramma ▶",
    "Whole picture": "Immagine intera",
    "Drag the picture to look around": "Trascina l'immagine per esplorarla",
    "VMAF average {mean}, worst 1% {p1}": "VMAF medio {mean}, peggior 1% {p1}",
    "Could not play": "Riproduzione non riuscita",
    "Player": "Lettore",

    # --- Settings
    "Language": "Lingua",
    "The default settings suit most people, so you can leave this page alone. Change something only if you have a reason.":
        "Le impostazioni predefinite vanno bene per la maggior parte delle persone, quindi puoi lasciare questa pagina com'è. Cambia qualcosa solo se hai un motivo.",
    "Encode with": "Codifica con",
    "Graphics card (fast, recommended)": "Scheda video (veloce, consigliata)",
    "Processor (slow, works on any PC)": "Processore (lento, funziona su ogni PC)",
    "Graphics card (fast, recommended) ({card} detected)": "Scheda video (veloce, consigliata) ({card} rilevata)",
    "Graphics card ({card} can't make this format)": "Scheda video ({card} non può creare questo formato)",
    "Graphics card (no compatible graphics card detected)": "Scheda video (nessuna scheda video compatibile rilevata)",
    "NVIDIA card": "scheda NVIDIA",
    "In use: your graphics card, making {codec} video.": "In uso: la tua scheda video, crea video {codec}.",
    "In use: your processor, making {codec} video.": "In uso: il tuo processore, crea video {codec}.",
    "{card} was found, but it can't make {codec} video, so the processor is used.":
        "È stata trovata {card}, ma non può creare video {codec}, quindi si usa il processore.",
    "No compatible graphics card was found (only NVIDIA is supported), so the processor is used.":
        "Nessuna scheda video compatibile trovata (è supportata solo NVIDIA), quindi si usa il processore.",
    "Video format": "Formato video",
    "H.265 (recommended)": "H.265 (consigliato)",
    "AV1 files are usually smaller, but they play on fewer devices. Check that your TV or phone can play one first.":
        "I file AV1 sono di solito più piccoli, ma si riproducono su meno dispositivi. Controlla prima che il tuo televisore o telefono possa riprodurli.",
    "Largest size": "Dimensione massima",
    "Keep the original resolution (recommended)": "Mantieni la risoluzione originale (consigliato)",
    "This permanently lowers the detail in the conversions, and videos are never enlarged. They are checked against a smaller copy of the original and labelled Resized. Keep the originals if you might want the full detail later.":
        "Questo riduce per sempre il dettaglio delle conversioni, e i video non vengono mai ingranditi. Sono confrontati con una copia ridotta dell'originale e contrassegnati come Ridimensionato. Tieni gli originali se in futuro potresti volere tutto il dettaglio.",
    "Show an Encoding column": "Mostra una colonna Codifica",
    "Format, quality setting, resolution and bitrate of each conversion.":
        "Formato, impostazione di qualità, risoluzione e bitrate di ogni conversione.",
    "Show the Welcome screen when the app opens": "Mostra la schermata di benvenuto all'apertura",
    "Advanced": "Avanzate",
    "Only change these if you know what you are doing: they can lower the quality of your videos.":
        "Cambia questi valori solo se sai cosa stai facendo: possono ridurre la qualità dei tuoi video.",
    "Read what each one does": "Leggi a cosa serve ciascuno",
    "I've read this and understand what I'm doing": "Ho letto e capisco cosa sto facendo",
    "Warn below": "Avvisa sotto",
    "Also aim for these values when choosing quality": "Punta anche a questi valori nella scelta della qualità",
    "Ticked, lower values make smaller files with lower quality, and higher values make larger files. Not ticked, your files stay the same and only the warning moves.":
        "Se selezionato, valori più bassi danno file più piccoli e di qualità inferiore, e valori più alti file più grandi. Se non selezionato, i tuoi file restano uguali e si sposta solo l'avviso.",
    "Don't keep a conversion below a minimum": "Non tenere una conversione sotto un minimo",
    "Below the minimum, nothing is kept and your original stays. Off by default, so every result that is smaller and matches is kept, with a warning if needed.":
        "Sotto il minimo non si tiene nulla e il tuo originale resta. Disattivato di default, quindi ogni risultato più piccolo e conforme viene tenuto, con un avviso se serve.",
    "Back to the defaults": "Torna ai valori predefiniti",
    "Your target is {mean}.": "Il tuo obiettivo è {mean}.",
    "How close this video looks to the original, from 0 to 100. VMAF is a score made by Netflix, based on how people see video. At 95 or above, most people can't see a difference.":
        "Quanto questo video somiglia all'originale, da 0 a 100. VMAF è un punteggio creato da Netflix, basato su come le persone vedono il video. Da 95 in su, la maggior parte delle persone non vede differenze.",
    "The score of the worst moments: 1% of the video's frames score lower than this. It catches a short bad patch that a good average would hide. The target is {p1} or above.":
        "Il punteggio dei momenti peggiori: l'1% dei fotogrammi del video ha un punteggio inferiore. Rivela un breve tratto difettoso che una buona media nasconderebbe. L'obiettivo è {p1} o più.",

    # --- Welcome
    "Welcome to {app}": "Benvenuto in {app}",
    "Shrink your videos, keep the quality.": "Riduci i tuoi video, mantieni la qualità.",
    "Zero guesswork": "Niente tentativi",
    "No bitrates or codecs to configure. ClipShrink automatically finds the right compression balance for every video.":
        "Nessun bitrate o codec da configurare. ClipShrink trova automaticamente il giusto equilibrio di compressione per ogni video.",
    "Measured frame-by-frame": "Misurato fotogramma per fotogramma",
    "Every result is scored against the original using Netflix's VMAF visual quality metric, and any clip that misses the target is clearly flagged.":
        "Ogni risultato viene valutato rispetto all'originale con VMAF, la metrica di qualità visiva di Netflix, e ogni clip che manca l'obiettivo viene segnalata chiaramente.",
    "You stay in control": "Il controllo resta a te",
    "Conversions are saved as new files alongside your originals. Compare both versions side by side before deciding what to send to the Recycle Bin.":
        "Le conversioni vengono salvate come nuovi file accanto ai tuoi originali. Confronta le due versioni affiancate prima di decidere cosa spostare nel Cestino.",
    "Don't show this again": "Non mostrare più",

    # --- About
    "About {app}": "Informazioni su {app}",
    "{app} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion against its original with VMAF and warns you about any below the quality target. Your originals are only read during conversion, and nothing is sent anywhere.":
        "{app} riduce i video H.264 in H.265 o AV1 per liberare spazio su disco. Misura ogni conversione rispetto al suo originale con VMAF e ti avvisa di quelle sotto l'obiettivo di qualità. I tuoi originali vengono solo letti durante la conversione, e non viene inviato nulla da nessuna parte.",
    "Documentation:": "Documentazione:",
    "Open in your browser": "Apri nel browser",
    "Copy the link": "Copia il link",
    "Project:": "Progetto:",
    "Reports:": "Rapporti:",
    "Each batch leaves a CSV report here. They're only for your information. Once a batch is finished and you exit or click Start Over, the app forgets those files.":
        "Ogni lotto lascia qui un rapporto CSV, solo a titolo informativo. Quando un lotto è finito ed esci o fai clic su Ricomincia, l'app dimentica quei file.",
    "Licence:": "Licenza:",
    "GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace.":
        "GPL-3.0. È fornito senza garanzia, quindi tieni un backup delle riprese che non potresti sostituire.",
    "Built with:": "Realizzato con:",
    "FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in THIRD_PARTY_NOTICES.md in the install folder and on the project page.":
        "FFmpeg, x265, SVT-AV1, VMAF, mpv e Qt. Le loro licenze e i link al codice sorgente sono in THIRD_PARTY_NOTICES.md, nella cartella di installazione e sulla pagina del progetto.",
    "What does \"no quality loss\" mean?": "Che cosa significa «nessuna perdita di qualità»?",
    "Truly lossless H.265, where every pixel stays identical, usually makes files larger than the originals, so it would cost you space instead of saving it. This tool uses a measured definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure from Netflix of how a video looks to people, scored from 0 to 100. A conversion counts as recommended if the average score is at least 95 and the worst 1% of frames score at least 90, a level where differences are very hard to see. This is the quality target.\n\n"
    "If a file misses the target even at the best setting, it is still converted, and it gets a warning sign so you can decide for yourself. Use Select Recommended to leave those files out when cleaning up. If the result is not smaller, your original is simply kept and the file is listed in the report. Sound, any GoPro telemetry and capture dates are copied unchanged, and originals are never touched during conversion.\n\n"
    "If you choose a smaller resolution in Settings, the conversion is compared with a smaller copy of the original at the same size. So the score shows how clean the encoding is, not the detail lost by shrinking, and those files are labelled Resized rather than Verified.\n\n"
    "The advanced part of Settings can change these numbers. Files judged by other numbers show them in their label.":
        "Un H.265 davvero senza perdita, in cui ogni pixel resta identico, di solito produce file più grandi degli originali: ti costerebbe spazio invece di fartene risparmiare. Per questo il programma usa una definizione misurata.\n\n"
        "Dopo ogni conversione confronta ogni fotogramma con l'originale usando VMAF, una misura aperta di Netflix di come un video appare alle persone, con un punteggio da 0 a 100. Una conversione è consigliata se il punteggio medio è almeno 95 e il peggior 1% dei fotogrammi ottiene almeno 90, un livello in cui le differenze sono molto difficili da vedere. Questo è l'obiettivo di qualità.\n\n"
        "Se un file manca l'obiettivo anche con l'impostazione migliore, viene comunque convertito e riceve un segnale di avviso, così puoi decidere tu. Usa Seleziona i consigliati per escludere quei file durante la pulizia. Se il risultato non è più piccolo, il tuo originale viene semplicemente tenuto e il file compare nel rapporto. L'audio, l'eventuale telemetria GoPro e le date di ripresa vengono copiati senza modifiche, e gli originali non vengono mai toccati durante la conversione.\n\n"
        "Se nelle Impostazioni scegli una risoluzione più piccola, la conversione viene confrontata con una copia ridotta dell'originale alla stessa dimensione. Il punteggio mostra quindi quanto è pulita la codifica, non il dettaglio perso nella riduzione, e quei file sono contrassegnati come Ridimensionato invece di Verificato.\n\n"
        "La parte avanzata delle Impostazioni può cambiare questi numeri. I file valutati con altri numeri li mostrano nella loro etichetta.",

    # --- Sizes and times
    "bytes": "byte",
    "KB": "KB",
    "MB": "MB",
    "GB": "GB",
    "TB": "TB",
    "~{m}m left": "~{m} min rimanenti",
    "~{h}h {m}m left": "~{h} h {m} min rimanenti",
    "under a minute": "meno di un minuto",
    "about {h} h {m} min": "circa {h} h {m} min",
    "about {d} days": "circa {d} giorni",

    # --- Reasons
    "Could not convert, original kept: {error}": "Conversione non riuscita, originale tenuto: {error}",
    "This is {codec}, not H.264, so it was left alone.": "Questo è {codec}, non H.264, quindi non è stato toccato.",
    "the encoder stopped: {detail}": "l'encoder si è fermato: {detail}",
    "the encoder failed: {detail}": "l'encoder non è riuscito: {detail}",
    "could not write the file: {detail}": "impossibile scrivere il file: {detail}",
    "could not read a sample from the file: {detail}": "impossibile leggere uno spezzone del file: {detail}",
    "the VMAF comparison could not run: {detail}": "impossibile eseguire il confronto VMAF: {detail}",
    "the VMAF comparison returned no frames": "il confronto VMAF non ha restituito fotogrammi",
    "the original changed while it was being converted": "l'originale è cambiato durante la conversione",
    "Conversion is not smaller ({out} vs {src} bytes), original kept.": "La conversione non è più piccola ({out} contro {src} byte), originale tenuto.",
    "Conversion did not match the original, original kept: {problems}": "La conversione non corrispondeva all'originale, originale tenuto: {problems}",
    "video is {codec}": "il video è {codec}",
    "resolution differs": "la risoluzione è diversa",
    "pixel format differs ({out} vs {src})": "il formato pixel è diverso ({out} contro {src})",
    "colour range differs": "la gamma di colori è diversa",
    "audio tracks differ": "le tracce audio sono diverse",
    "duration differs ({out}s vs {src}s)": "la durata è diversa ({out} s contro {src} s)",
    "frame count differs ({out} vs {src})": "il numero di fotogrammi è diverso ({out} contro {src})",
    "audio or telemetry tracks changed": "sono cambiate tracce audio o di telemetria",
    "camera info changed": "sono cambiate le informazioni della videocamera",
    "VMAF compared {frames} frames out of {total}, original kept.": "VMAF ha confrontato {frames} fotogrammi su {total}, originale tenuto.",
    "VMAF short of what the search aims for.": "VMAF sotto quanto cerca la ricerca.",
    "VMAF below your minimum: average {mean} (minimum {min_mean}), worst 1% {p1} (minimum {min_p1}). Nothing was kept, and your original is untouched.":
        "VMAF sotto il tuo minimo: media {mean} (minimo {min_mean}), peggior 1% {p1} (minimo {min_p1}). Non è stato tenuto nulla e il tuo originale è intatto.",
    "VMAF below the target: average {mean} (target {warn_mean}), worst 1% {p1} (target {warn_p1}). Compare it before removing the original.":
        "VMAF sotto l'obiettivo: media {mean} (obiettivo {warn_mean}), peggior 1% {p1} (obiettivo {warn_p1}). Confrontalo prima di rimuovere l'originale.",
    "this file was never converted by this tool": "questo file non è mai stato convertito da questo programma",
    "its original has not been sent to the Recycle Bin": "il suo originale non è stato spostato nel Cestino",
    "the converted file is missing": "il file convertito manca",
    "it already has the original's name": "ha già il nome dell'originale",
    "the converted file has changed since it was verified": "il file convertito è cambiato dopo la verifica",
    "another file already has that name": "un altro file ha già quel nome",
    "renaming was not confirmed": "la ridenominazione non è stata confermata",
    "Windows refused the rename: {error}": "Windows ha rifiutato la ridenominazione: {error}",
    "it is not an LRV file": "non è un file LRV",
    "its full video is not beside it": "il suo video completo non è accanto",
    "Windows did not move it to the Recycle Bin, so it was left in place": "Windows non l'ha spostato nel Cestino, quindi è rimasto al suo posto",
    "its conversion is not verified (status: {status})": "la sua conversione non è verificata (stato: {status})",
    "the original has changed since it was verified": "l'originale è cambiato dopo la verifica",
    "the converted file's content does not match what was verified": "il contenuto del file convertito non corrisponde a quello verificato",
    "the converted file cannot be read: {error}": "il file convertito non è leggibile: {error}",
    "the converted file is not H.265 or AV1": "il file convertito non è né H.265 né AV1",
    "deletion was not confirmed": "l'eliminazione non è stata confermata",
    "its conversion is below the default quality target, and that was not confirmed": "la sua conversione è sotto l'obiettivo di qualità predefinito, e non è stato confermato",
    "its conversion has a lower resolution, and that was not confirmed": "la sua conversione ha una risoluzione inferiore, e non è stato confermato",

    # --- Report columns
    "Date": "Data",
    "Reason": "Motivo",
    "Before (bytes)": "Prima (byte)",
    "After (bytes)": "Dopo (byte)",
    "Saved %": "% risparmiato",
    "Encoder": "Encoder",
    "Quality setting": "Impostazione di qualità",
    "Conversion": "Conversione",
    "Codec": "Codec",
    "Output resolution": "Risoluzione in uscita",
    "Output bitrate (Mbit/s)": "Bitrate in uscita (Mbit/s)",
    "Target average": "Obiettivo medio",
    "Target worst 1%": "Obiettivo peggior 1%",
}

PLURALS = {
    "Found {n} GoPro LRV file ({size}).": ("Trovato {n} file LRV GoPro ({size}).", "Trovati {n} file LRV GoPro ({size})."),
    "Measured on {n} file using your graphics card.": ("Misurato su {n} file con la tua scheda video.", "Misurato su {n} file con la tua scheda video."),
    "Measured on {n} file using your processor.": ("Misurato su {n} file con il tuo processore.", "Misurato su {n} file con il tuo processore."),
    "Remove the added tags from {n} name…": ("Togli i suffissi aggiunti da {n} nome…", "Togli i suffissi aggiunti da {n} nomi…"),
    "Send it to the Recycle Bin?": ("Spostarlo nel Cestino?", "Spostarli nel Cestino?"),
    "Send {n} ticked original to Recycle Bin…": ("Sposta {n} originale selezionato nel Cestino…", "Sposta {n} originali selezionati nel Cestino…"),
    "about {n} minute": ("circa {n} minuto", "circa {n} minuti"),
    "{n} H.264 video, {size}.": ("{n} video H.264, {size}.", "{n} video H.264, {size}."),
    "{n} LRV file moved to the Recycle Bin.": ("{n} file LRV spostato nel Cestino.", "{n} file LRV spostati nel Cestino."),
    "{n} conversion whose original is in the Recycle Bin will take the original's name, for example {name}.":
        ("{n} conversione il cui originale è nel Cestino prenderà il nome dell'originale, per esempio {name}.",
         "{n} conversioni il cui originale è nel Cestino prenderanno il nome dell'originale, per esempio {name}."),
    "{n} file renamed.": ("{n} file rinominato.", "{n} file rinominati."),
    "{n} original ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, and you can restore originals from the Recycle Bin.":
        ("{n} originale ({size}) andrà nel Cestino di Windows. Ogni conversione viene prima ricontrollata, e puoi ripristinare gli originali dal Cestino.",
         "{n} originali ({size}) andranno nel Cestino di Windows. Ogni conversione viene prima ricontrollata, e puoi ripristinare gli originali dal Cestino."),
    "{n} original moved to the Recycle Bin.": ("{n} originale spostato nel Cestino.", "{n} originali spostati nel Cestino."),
    "{n} other LRV file will stay, because the original video isn't beside it.":
        ("{n} altro file LRV resterà, perché il video originale non è accanto.",
         "{n} altri file LRV resteranno, perché il video originale non è accanto."),
    "{n} video already in H.265, skipped.": ("{n} video già in H.265, saltato.", "{n} video già in H.265, saltati."),
    "{n} video from your last batch is not finished. Files already verified will not be converted again. Continue now?":
        ("{n} video del tuo ultimo lotto non è finito. I file già verificati non verranno riconvertiti. Continuare ora?",
         "{n} video del tuo ultimo lotto non sono finiti. I file già verificati non verranno riconvertiti. Continuare ora?"),
    "{n} video in another format, skipped.": ("{n} video in un altro formato, saltato.", "{n} video in un altro formato, saltati."),
    "{n} video, {size}.": ("{n} video, {size}.", "{n} video, {size}."),
    "⚠ {n} of these has a conversion at a lower resolution. Once the original is gone from the Recycle Bin, that detail is gone for good.":
        ("⚠ {n} di questi ha una conversione a risoluzione inferiore. Quando l'originale non sarà più nel Cestino, quel dettaglio sarà perso per sempre.",
         "⚠ {n} di questi hanno una conversione a risoluzione inferiore. Quando l'originale non sarà più nel Cestino, quel dettaglio sarà perso per sempre."),
    "⚠ {n} of these has a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). Once the original is gone from the Recycle Bin, that lost quality can't be recovered.":
        ("⚠ {n} di questi ha una conversione sotto la qualità consigliata (VMAF medio {mean}, peggior 1% {p1}). Quando l'originale non sarà più nel Cestino, quella qualità persa non potrà essere recuperata.",
         "⚠ {n} di questi hanno una conversione sotto la qualità consigliata (VMAF medio {mean}, peggior 1% {p1}). Quando l'originale non sarà più nel Cestino, quella qualità persa non potrà essere recuperata."),
}
