"""Nederlands. Not yet checked by a native speaker: corrections are welcome on GitHub."""

MESSAGES = {
    # --- Steps, pages and buttons
    "Find videos": "Video's zoeken",
    "See the saving": "Besparing bekijken",
    "Convert": "Converteren",
    "Compare and clean up": "Vergelijken en opruimen",
    "Settings": "Instellingen",
    "{app} {version}: shrink videos, keep the quality": "{app} {version}: verklein video's, behoud de kwaliteit",
    "←  Back": "←  Terug",
    "Choose folder…": "Map kiezen…",
    "Choose the folder with your videos": "Kies de map met je video's",
    "No folder chosen": "Geen map gekozen",
    "Find your videos": "Zoek je video's",
    "Pick a folder. This tool looks through it and every folder inside it, and lists the H.264 videos it can shrink. Nothing is changed yet.":
        "Kies een map. Het programma doorzoekt die map en alle submappen, en toont de H.264-video's die het kan verkleinen. Er wordt nog niets gewijzigd.",
    "Next: see the saving  →": "Volgende: besparing bekijken  →",
    "Reading your videos…": "Je video's worden gelezen…",
    "File": "Bestand",
    "Folder": "Map",
    "Size": "Grootte",
    "Picture": "Beeld",
    "Length": "Duur",
    "State": "Status",
    "Ready": "Klaar",
    "Already has a conversion": "Heeft al een conversie",
    "GoPro low-res preview, off by default": "GoPro-voorbeeld in lage resolutie, standaard uit",
    "Already {codec}, skipped": "Al {codec}, overgeslagen",
    "(converted by this tool)": "(geconverteerd door dit programma)",
    "{n} could not be read and were skipped: {names}.": "{n} konden niet worden gelezen en zijn overgeslagen: {names}.",
    "No H.264 videos found in this folder or its subfolders.": "Geen H.264-video's gevonden in deze map of de submappen.",
    "Delete GoPro LRV files?": "GoPro LRV-bestanden verwijderen?",
    "An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera and its phone app can show quick previews. You don't need it if you have the original video, which is beside each of these.":
        "Een LRV-bestand is een kleine kopie in lage resolutie die een GoPro naast elke video opneemt, zodat de camera en de telefoonapp snel voorbeelden kunnen tonen. Je hebt het niet nodig als je de originele video hebt, en die staat naast elk van deze bestanden.",
    "Done": "Klaar",
    "Left in place:": "Blijven staan:",
    "Left as they are:": "Blijven zoals ze zijn:",

    # --- See the saving
    "See the saving before anything converts": "Bekijk de besparing voordat er iets wordt geconverteerd",
    "This makes short test encodes from a few of your own files and measures them. Your files are only read, and nothing appears in your folders.":
        "Dit maakt korte testcoderingen van een paar van je eigen bestanden en meet ze. Je bestanden worden alleen gelezen en er verschijnt niets in je mappen.",
    "Run the test encodes": "Testcoderingen uitvoeren",
    "Not measured yet": "Nog niet gemeten",
    "Click \"Run the test encodes\" to measure how much space you would save.":
        "Klik op \"Testcoderingen uitvoeren\" om te meten hoeveel ruimte je zou besparen.",
    "Measuring…": "Bezig met meten…",
    "Encoding samples of your files and comparing them with the originals.":
        "Fragmenten van je bestanden worden gecodeerd en met de originelen vergeleken.",
    "Could not measure": "Meten is niet gelukt",
    "The test encode stopped: {error}": "De testcodering is gestopt: {error}",
    "About {size} saved ({pct}%)": "Ongeveer {size} bespaard ({pct}%)",
    "Likely between {low} and {high}, out of {total}.": "Waarschijnlijk tussen {low} en {high}, van {total}.",
    "Converting everything should take {time}.": "Alles converteren duurt naar verwachting {time}.",
    "Sample from": "Fragment uit",
    "At": "Op",
    "Original": "Origineel",
    "VMAF average": "VMAF-gemiddelde",
    "VMAF worst 1%": "VMAF slechtste 1%",
    "Meets the quality target?": "Haalt het kwaliteitsdoel?",
    "Yes": "Ja",
    "⚠ No, would get a warning": "⚠ Nee, zou een waarschuwing krijgen",
    "Start converting  →": "Converteren starten  →",
    "Expected time: {time}. Your computer will not go to sleep while this runs.":
        "Verwachte tijd: {time}. Je computer gaat niet in slaapstand zolang dit loopt.",
    "The target: VMAF average at least {mean}, worst 1% of frames at least {p1}. Every full file is measured again after conversion.":
        "Het doel: VMAF-gemiddelde minstens {mean}, slechtste 1% van de beelden minstens {p1}. Elk volledig bestand wordt na de conversie opnieuw gemeten.",
    "{codec}. Change this in Settings.": "{codec}. Wijzig dit in Instellingen.",
    "{codec}, at most {size}. Change this in Settings.": "{codec}, hoogstens {size}. Wijzig dit in Instellingen.",

    # --- Convert
    "Files Processed": "Verwerkte bestanden",
    "Space Saved": "Bespaarde ruimte",
    "Current Batch": "Huidige reeks",
    "Time Remaining": "Resterende tijd",
    "Pause": "Pauzeren",
    "Resume": "Hervatten",
    "Paused": "Gepauzeerd",
    "Calculating…": "Berekenen…",
    "Overall Progress": "Totale voortgang",
    "Overall Progress: {pct}% ({done} of {total} files)": "Totale voortgang: {pct}% ({done} van {total} bestanden)",
    "Current File": "Huidig bestand",
    "Current File: {name}: {stage}": "Huidig bestand: {name}: {stage}",
    "Current File: none, the batch is finished": "Huidig bestand: geen, de reeks is klaar",
    "All": "Alle",
    "Completed": "Klaar",
    "Active": "Bezig",
    "Waiting": "Wachtend",
    "Before": "Voor",
    "After": "Na",
    "% Saved": "% bespaard",
    "Worst 1%": "Slechtste 1%",
    "Encoding": "Codering",
    "Next: compare and clean up  →": "Volgende: vergelijken en opruimen  →",
    "Finding the right quality": "De juiste kwaliteit zoeken",
    "Measuring every frame": "Elk beeld meten",
    "Finding quality": "Kwaliteit zoeken",
    "Measuring": "Meten",
    "Finished: {n} verified": "Klaar: {n} gecontroleerd",
    ", ⚠ {n} below target": ", ⚠ {n} onder het doel",
    ", {n} kept as original": ", {n} als origineel behouden",
    "(see next page)": "(zie volgende pagina)",
    "Nothing left to convert: every selected file is already finished.":
        "Niets meer te converteren: elk geselecteerd bestand is al klaar.",
    "The batch stopped": "De reeks is gestopt",
    "Files already verified are safe. Reopen the app to continue.":
        "Al gecontroleerde bestanden zijn veilig. Open de app opnieuw om verder te gaan.",
    "Continue where you left off?": "Verdergaan waar je gebleven was?",
    "Each conversion is saved beside its original with {suffix} added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Elke conversie wordt naast het origineel opgeslagen, met {suffix} toegevoegd aan de naam. Originelen worden alleen gelezen. Je kunt altijd pauzeren, en als de pc vastloopt, open je de app gewoon opnieuw.",
    "Each conversion is saved beside its original with {suffix} ({shrunk} if it was shrunk) added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Elke conversie wordt naast het origineel opgeslagen, met {suffix} ({shrunk} als ze verkleind is) toegevoegd aan de naam. Originelen worden alleen gelezen. Je kunt altijd pauzeren, en als de pc vastloopt, open je de app gewoon opnieuw.",
    "Stop converting?": "Converteren stoppen?",
    "The batch is still running. If you close now, the current file is restarted next time and finished files are kept. Close anyway?":
        "De reeks loopt nog. Als je nu sluit, begint het huidige bestand de volgende keer opnieuw en blijven klare bestanden behouden. Toch sluiten?",

    # --- Statuses
    "Working…": "Bezig…",
    "Verified": "Gecontroleerd",
    "⚠ Below target": "⚠ Onder het doel",
    "Resized": "Verkleind",
    "Verified at {mean} / {p1}": "Gecontroleerd op {mean} / {p1}",
    "Resized at {mean} / {p1}": "Verkleind op {mean} / {p1}",
    "Original kept": "Origineel behouden",
    "Failed, original kept": "Mislukt, origineel behouden",
    "Original in Recycle Bin": "Origineel in Prullenbak",
    "Done, has the original's name": "Klaar, heeft de naam van het origineel",
    "processor": "processor",

    # --- Compare and clean up
    "Play any original beside its conversion, in sync. When you are happy, you can send originals to the Recycle Bin. This step is optional. Click a column title to sort.":
        "Speel elk origineel synchroon af naast de conversie. Ben je tevreden, dan kun je originelen naar de Prullenbak sturen. Deze stap is optioneel. Klik op een kolomtitel om te sorteren.",
    "Select All": "Alles aanvinken",
    "Deselect All": "Alles uitvinken",
    "Select Recommended": "Aanbevolen aanvinken",
    "Deselect Recommended": "Aanbevolen uitvinken",
    "Recommended means the conversion met the quality target, with no warning sign.":
        "Aanbevolen betekent dat de conversie het kwaliteitsdoel haalde, zonder waarschuwing.",
    "Tip: Ctrl+click a row to tick it, Shift+click to tick a range, Ctrl+A to tick all. Right-click a row to open its folder.":
        "Tip: Ctrl+klik vinkt een rij aan, Shift+klik een reeks rijen, Ctrl+A alles. Klik met rechts op een rij om de map te openen.",
    "Delete?": "Verwijderen?",
    "Result": "Resultaat",
    "▶  Play selected side by side": "▶  Selectie naast elkaar afspelen",
    "Remove the added tags from names": "Toegevoegde labels uit namen halen",
    "Send ticked originals to Recycle Bin…": "Aangevinkte originelen naar Prullenbak…",
    "Tick originals above to delete them": "Vink hierboven originelen aan om ze te verwijderen",
    "Needs your attention": "Vraagt je aandacht",
    "Needs your attention ({n})": "Vraagt je aandacht ({n})",
    "Needs your attention: nothing": "Vraagt je aandacht: niets",
    "Every conversion passed.": "Elke conversie is geslaagd.",
    "Nothing converted yet.": "Nog niets geconverteerd.",
    "{size} can be saved once originals are removed": "{size} kan worden bespaard zodra de originelen weg zijn",
    "Available after an original has been sent to the Recycle Bin.": "Beschikbaar zodra een origineel naar de Prullenbak is gestuurd.",
    "Start Over": "Opnieuw beginnen",
    "Forget these files and go back to step 1. Your videos and reports aren't touched.":
        "Vergeet deze bestanden en ga terug naar stap 1. Je video's en rapporten blijven onaangeroerd.",
    "Open file location": "Bestandslocatie openen",
    "Pick a video": "Kies een video",
    "Click a row in the list first.": "Klik eerst op een rij in de lijst.",
    "Cannot compare": "Vergelijken kan niet",
    "This row needs both an original and a verified conversion on disk.":
        "Deze rij heeft zowel een origineel als een gecontroleerde conversie op de schijf nodig.",
    "Re-checking and removing": "Opnieuw controleren en verwijderen",
    "Renaming": "Hernoemen",
    "finishing": "afronden",
    "{action} {i} of {total}: {name}": "{action} {i} van {total}: {name}",
    "Remove the added tags from names?": "Toegevoegde labels uit namen halen?",
    "Only the name changes. If you later restore an original from the Recycle Bin, Windows will ask what to do about the same name.":
        "Alleen de naam verandert. Zet je later een origineel terug uit de Prullenbak, dan vraagt Windows wat het met de dubbele naam moet doen.",
    "Send originals to the Recycle Bin?": "Originelen naar de Prullenbak sturen?",
    "I understand. Send these originals to the Recycle Bin.": "Ik begrijp het. Stuur deze originelen naar de Prullenbak.",
    "Send to Recycle Bin": "Naar Prullenbak",
    "Keep them": "Behouden",
    "Below the quality target. Compare it with the original before removing the original.":
        "Onder het kwaliteitsdoel. Vergelijk het met het origineel voordat je het origineel verwijdert.",

    # --- Player
    "Side by side: {name}": "Naast elkaar: {name}",
    "Original (H.264)": "Origineel (H.264)",
    "Original (H.264), shrunk to match": "Origineel (H.264), verkleind om te passen",
    "Conversion ({codec})": "Conversie ({codec})",
    "Play": "Afspelen",
    "◀ Frame": "◀ Beeld",
    "Frame ▶": "Beeld ▶",
    "Whole picture": "Heel beeld",
    "Drag the picture to look around": "Sleep het beeld om rond te kijken",
    "VMAF average {mean}, worst 1% {p1}": "VMAF-gemiddelde {mean}, slechtste 1% {p1}",
    "Could not play": "Afspelen is niet gelukt",
    "Player": "Speler",

    # --- Settings
    "Language": "Taal",
    "The default settings suit most people, so you can leave this page alone. Change something only if you have a reason.":
        "De standaardinstellingen passen bij de meeste mensen, dus je kunt deze pagina laten zoals ze is. Wijzig alleen iets als je een reden hebt.",
    "Encode with": "Coderen met",
    "Graphics card (fast, recommended)": "Videokaart (snel, aanbevolen)",
    "Processor (slow, works on any PC)": "Processor (traag, werkt op elke pc)",
    "Graphics card (fast, recommended) ({card} detected)": "Videokaart (snel, aanbevolen) ({card} gevonden)",
    "Graphics card ({card} can't make this format)": "Videokaart ({card} kan dit formaat niet maken)",
    "Graphics card (no compatible graphics card detected)": "Videokaart (geen geschikte videokaart gevonden)",
    "NVIDIA card": "NVIDIA-kaart",
    "In use: your graphics card, making {codec} video.": "In gebruik: je videokaart, maakt {codec}-video.",
    "In use: your processor, making {codec} video.": "In gebruik: je processor, maakt {codec}-video.",
    "{card} was found, but it can't make {codec} video, so the processor is used.":
        "{card} is gevonden, maar kan geen {codec}-video maken, dus de processor wordt gebruikt.",
    "No compatible graphics card was found (only NVIDIA is supported), so the processor is used.":
        "Er is geen geschikte videokaart gevonden (alleen NVIDIA wordt ondersteund), dus de processor wordt gebruikt.",
    "Video format": "Videoformaat",
    "H.265 (recommended)": "H.265 (aanbevolen)",
    "AV1 files are usually smaller, but they play on fewer devices. Check that your TV or phone can play one first.":
        "AV1-bestanden zijn meestal kleiner, maar ze spelen op minder apparaten af. Controleer eerst of je tv of telefoon er een kan afspelen.",
    "Largest size": "Grootste formaat",
    "Keep the original resolution (recommended)": "Originele resolutie behouden (aanbevolen)",
    "This permanently lowers the detail in the conversions, and videos are never enlarged. They are checked against a smaller copy of the original and labelled Resized. Keep the originals if you might want the full detail later.":
        "Dit verlaagt het detail in de conversies voorgoed, en video's worden nooit vergroot. Ze worden vergeleken met een verkleinde kopie van het origineel en krijgen het label Verkleind. Bewaar de originelen als je later misschien het volle detail wilt.",
    "Show an Encoding column": "Kolom Codering tonen",
    "Format, quality setting, resolution and bitrate of each conversion.":
        "Formaat, kwaliteitsinstelling, resolutie en bitrate van elke conversie.",
    "Show the Welcome screen when the app opens": "Welkomstscherm tonen bij het openen van de app",
    "Advanced": "Geavanceerd",
    "Only change these if you know what you are doing: they can lower the quality of your videos.":
        "Wijzig deze alleen als je weet wat je doet: ze kunnen de kwaliteit van je video's verlagen.",
    "Read what each one does": "Lees wat elke instelling doet",
    "I've read this and understand what I'm doing": "Ik heb dit gelezen en begrijp wat ik doe",
    "Warn below": "Waarschuwen onder",
    "Also aim for these values when choosing quality": "Ook deze waarden nastreven bij het kiezen van de kwaliteit",
    "Ticked, lower values make smaller files with lower quality, and higher values make larger files. Not ticked, your files stay the same and only the warning moves.":
        "Aangevinkt geven lagere waarden kleinere bestanden met lagere kwaliteit, en hogere waarden grotere bestanden. Niet aangevinkt blijven je bestanden gelijk en verschuift alleen de waarschuwing.",
    "Don't keep a conversion below a minimum": "Geen conversie onder een minimum bewaren",
    "Below the minimum, nothing is kept and your original stays. Off by default, so every result that is smaller and matches is kept, with a warning if needed.":
        "Onder het minimum wordt niets bewaard en blijft je origineel staan. Standaard uit, dus elk resultaat dat kleiner is en klopt wordt bewaard, zo nodig met een waarschuwing.",
    "Back to the defaults": "Terug naar standaard",
    "Your target is {mean}.": "Jouw doel is {mean}.",
    "How close this video looks to the original, from 0 to 100. VMAF is a score made by Netflix, based on how people see video. At 95 or above, most people can't see a difference.":
        "Hoe dicht deze video bij het origineel ligt, van 0 tot 100. VMAF is een score van Netflix, gebaseerd op hoe mensen video zien. Vanaf 95 zien de meeste mensen geen verschil.",
    "The score of the worst moments: 1% of the video's frames score lower than this. It catches a short bad patch that a good average would hide. The target is {p1} or above.":
        "De score van de slechtste momenten: 1% van de beelden van de video scoort lager. Zo valt een kort slecht stuk op dat een goed gemiddelde zou verbergen. Het doel is {p1} of hoger.",

    # --- Welcome
    "Welcome to {app}": "Welkom bij {app}",
    "Shrink your videos, keep the quality.": "Verklein je video's, behoud de kwaliteit.",
    "Zero guesswork": "Geen giswerk",
    "No bitrates or codecs to configure. ClipShrink automatically finds the right compression balance for every video.":
        "Geen bitrates of codecs om in te stellen. ClipShrink vindt automatisch de juiste compressiebalans voor elke video.",
    "Measured frame-by-frame": "Beeld voor beeld gemeten",
    "Every result is scored against the original using Netflix's VMAF visual quality metric, and any clip that misses the target is clearly flagged.":
        "Elk resultaat wordt met het origineel vergeleken met VMAF, de beeldkwaliteitsmaat van Netflix, en elke clip die het doel mist, wordt duidelijk gemarkeerd.",
    "You stay in control": "Jij houdt de controle",
    "Conversions are saved as new files alongside your originals. Compare both versions side by side before deciding what to send to the Recycle Bin.":
        "Conversies worden als nieuwe bestanden naast je originelen opgeslagen. Vergelijk beide versies naast elkaar voordat je beslist wat naar de Prullenbak gaat.",
    "Don't show this again": "Niet meer tonen",

    # --- About
    "About {app}": "Over {app}",
    "{app} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion against its original with VMAF and warns you about any below the quality target. Your originals are only read during conversion, and nothing is sent anywhere.":
        "{app} verkleint H.264-video's naar H.265 of AV1 om schijfruimte vrij te maken. Het meet elke conversie met VMAF tegen het origineel en waarschuwt je voor elke conversie onder het kwaliteitsdoel. Je originelen worden tijdens het converteren alleen gelezen, en er wordt nergens iets heen gestuurd.",
    "Documentation:": "Documentatie:",
    "Open in your browser": "Openen in je browser",
    "Copy the link": "Link kopiëren",
    "Project:": "Project:",
    "Reports:": "Rapporten:",
    "Each batch leaves a CSV report here. They're only for your information. Once a batch is finished and you exit or click Start Over, the app forgets those files.":
        "Elke reeks laat hier een CSV-rapport achter, alleen ter informatie. Zodra een reeks klaar is en je afsluit of op Opnieuw beginnen klikt, vergeet de app die bestanden.",
    "Licence:": "Licentie:",
    "GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace.":
        "GPL-3.0. Zonder garantie, dus bewaar een back-up van beelden die je niet kunt vervangen.",
    "Built with:": "Gemaakt met:",
    "FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in THIRD_PARTY_NOTICES.md in the install folder and on the project page.":
        "FFmpeg, x265, SVT-AV1, VMAF, mpv en Qt. Hun licenties en links naar de broncode staan in THIRD_PARTY_NOTICES.md in de installatiemap en op de projectpagina.",
    "What does \"no quality loss\" mean?": "Wat betekent \"geen kwaliteitsverlies\"?",
    "Truly lossless H.265, where every pixel stays identical, usually makes files larger than the originals, so it would cost you space instead of saving it. This tool uses a measured definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure from Netflix of how a video looks to people, scored from 0 to 100. A conversion counts as recommended if the average score is at least 95 and the worst 1% of frames score at least 90, a level where differences are very hard to see. This is the quality target.\n\n"
    "If a file misses the target even at the best setting, it is still converted, and it gets a warning sign so you can decide for yourself. Use Select Recommended to leave those files out when cleaning up. If the result is not smaller, your original is simply kept and the file is listed in the report. Sound, any GoPro telemetry and capture dates are copied unchanged, and originals are never touched during conversion.\n\n"
    "If you choose a smaller resolution in Settings, the conversion is compared with a smaller copy of the original at the same size. So the score shows how clean the encoding is, not the detail lost by shrinking, and those files are labelled Resized rather than Verified.\n\n"
    "The advanced part of Settings can change these numbers. Files judged by other numbers show them in their label.":
        "Echt verliesvrije H.265, waarbij elke pixel identiek blijft, geeft meestal grotere bestanden dan de originelen: het zou je ruimte kosten in plaats van besparen. Dit programma gebruikt daarom een gemeten definitie.\n\n"
        "Na elke conversie vergelijkt het elk beeld met het origineel met VMAF, een open maat van Netflix voor hoe een video er voor mensen uitziet, met een score van 0 tot 100. Een conversie geldt als aanbevolen als de gemiddelde score minstens 95 is en de slechtste 1% van de beelden minstens 90 scoort, een niveau waarop verschillen heel moeilijk te zien zijn. Dat is het kwaliteitsdoel.\n\n"
        "Mist een bestand het doel zelfs met de beste instelling, dan wordt het toch geconverteerd en krijgt het een waarschuwingsteken, zodat je zelf kunt beslissen. Gebruik Aanbevolen aanvinken om die bestanden bij het opruimen over te slaan. Is het resultaat niet kleiner, dan blijft je origineel gewoon staan en staat het bestand in het rapport. Geluid, eventuele GoPro-telemetrie en opnamedatums worden ongewijzigd gekopieerd, en originelen worden tijdens het converteren nooit aangeraakt.\n\n"
        "Kies je in Instellingen een kleinere resolutie, dan wordt de conversie vergeleken met een verkleinde kopie van het origineel op hetzelfde formaat. De score toont dus hoe schoon de codering is, niet het detail dat door het verkleinen verloren gaat, en die bestanden krijgen het label Verkleind in plaats van Gecontroleerd.\n\n"
        "Het geavanceerde deel van Instellingen kan deze getallen wijzigen. Bestanden die met andere getallen zijn beoordeeld, tonen die in hun label.",

    # --- Sizes and times
    "bytes": "bytes",
    "KB": "KB",
    "MB": "MB",
    "GB": "GB",
    "TB": "TB",
    "~{m}m left": "~{m} min resterend",
    "~{h}h {m}m left": "~{h} u {m} min resterend",
    "under a minute": "minder dan een minuut",
    "about {h} h {m} min": "ongeveer {h} u {m} min",
    "about {d} days": "ongeveer {d} dagen",

    # --- Reasons
    "Could not convert, original kept: {error}": "Converteren is niet gelukt, origineel behouden: {error}",
    "This is {codec}, not H.264, so it was left alone.": "Dit is {codec}, geen H.264, dus het is niet aangeraakt.",
    "the encoder stopped: {detail}": "de encoder is gestopt: {detail}",
    "the encoder failed: {detail}": "de encoder is mislukt: {detail}",
    "could not write the file: {detail}": "het bestand kon niet worden geschreven: {detail}",
    "could not read a sample from the file: {detail}": "er kon geen fragment uit het bestand worden gelezen: {detail}",
    "the VMAF comparison could not run: {detail}": "de VMAF-vergelijking kon niet worden uitgevoerd: {detail}",
    "the VMAF comparison returned no frames": "de VMAF-vergelijking gaf geen beelden terug",
    "the original changed while it was being converted": "het origineel is gewijzigd tijdens het converteren",
    "Conversion is not smaller ({out} vs {src} bytes), original kept.": "De conversie is niet kleiner ({out} tegen {src} bytes), origineel behouden.",
    "Conversion did not match the original, original kept: {problems}": "De conversie kwam niet overeen met het origineel, origineel behouden: {problems}",
    "video is {codec}": "video is {codec}",
    "resolution differs": "resolutie verschilt",
    "pixel format differs ({out} vs {src})": "pixelformaat verschilt ({out} tegen {src})",
    "colour range differs": "kleurbereik verschilt",
    "audio tracks differ": "audiosporen verschillen",
    "duration differs ({out}s vs {src}s)": "duur verschilt ({out} s tegen {src} s)",
    "frame count differs ({out} vs {src})": "aantal beelden verschilt ({out} tegen {src})",
    "audio or telemetry tracks changed": "audio- of telemetriesporen zijn gewijzigd",
    "camera info changed": "camera-informatie is gewijzigd",
    "VMAF compared {frames} frames out of {total}, original kept.": "VMAF vergeleek {frames} van de {total} beelden, origineel behouden.",
    "VMAF short of what the search aims for.": "VMAF onder wat de zoektocht nastreeft.",
    "VMAF below your minimum: average {mean} (minimum {min_mean}), worst 1% {p1} (minimum {min_p1}). Nothing was kept, and your original is untouched.":
        "VMAF onder je minimum: gemiddelde {mean} (minimum {min_mean}), slechtste 1% {p1} (minimum {min_p1}). Er is niets bewaard en je origineel is onaangeroerd.",
    "VMAF below the target: average {mean} (target {warn_mean}), worst 1% {p1} (target {warn_p1}). Compare it before removing the original.":
        "VMAF onder het doel: gemiddelde {mean} (doel {warn_mean}), slechtste 1% {p1} (doel {warn_p1}). Vergelijk voordat je het origineel verwijdert.",
    "this file was never converted by this tool": "dit bestand is nooit door dit programma geconverteerd",
    "its original has not been sent to the Recycle Bin": "het origineel is niet naar de Prullenbak gestuurd",
    "the converted file is missing": "het geconverteerde bestand ontbreekt",
    "it already has the original's name": "het heeft al de naam van het origineel",
    "the converted file has changed since it was verified": "het geconverteerde bestand is gewijzigd sinds de controle",
    "another file already has that name": "een ander bestand heeft die naam al",
    "renaming was not confirmed": "hernoemen is niet bevestigd",
    "Windows refused the rename: {error}": "Windows weigerde het hernoemen: {error}",
    "it is not an LRV file": "het is geen LRV-bestand",
    "its full video is not beside it": "de volledige video staat er niet naast",
    "Windows did not move it to the Recycle Bin, so it was left in place": "Windows heeft het niet naar de Prullenbak verplaatst, dus het is blijven staan",
    "its conversion is not verified (status: {status})": "de conversie is niet gecontroleerd (status: {status})",
    "the original has changed since it was verified": "het origineel is gewijzigd sinds de controle",
    "the converted file's content does not match what was verified": "de inhoud van het geconverteerde bestand komt niet overeen met wat gecontroleerd is",
    "the converted file cannot be read: {error}": "het geconverteerde bestand kan niet worden gelezen: {error}",
    "the converted file is not H.265 or AV1": "het geconverteerde bestand is geen H.265 of AV1",
    "deletion was not confirmed": "verwijderen is niet bevestigd",
    "its conversion is below the default quality target, and that was not confirmed": "de conversie ligt onder het standaard kwaliteitsdoel, en dat is niet bevestigd",
    "its conversion has a lower resolution, and that was not confirmed": "de conversie heeft een lagere resolutie, en dat is niet bevestigd",

    # --- Report columns
    "Date": "Datum",
    "Reason": "Reden",
    "Before (bytes)": "Voor (bytes)",
    "After (bytes)": "Na (bytes)",
    "Saved %": "% bespaard",
    "Encoder": "Encoder",
    "Quality setting": "Kwaliteitsinstelling",
    "Conversion": "Conversie",
    "Codec": "Codec",
    "Output resolution": "Uitvoerresolutie",
    "Output bitrate (Mbit/s)": "Uitvoerbitrate (Mbit/s)",
    "Target average": "Doel gemiddelde",
    "Target worst 1%": "Doel slechtste 1%",
}

PLURALS = {
    "Found {n} GoPro LRV file ({size}).": ("{n} GoPro LRV-bestand gevonden ({size}).", "{n} GoPro LRV-bestanden gevonden ({size})."),
    "Measured on {n} file using your graphics card.": ("Gemeten op {n} bestand met je videokaart.", "Gemeten op {n} bestanden met je videokaart."),
    "Measured on {n} file using your processor.": ("Gemeten op {n} bestand met je processor.", "Gemeten op {n} bestanden met je processor."),
    "Remove the added tags from {n} name…": ("Toegevoegde labels uit {n} naam halen…", "Toegevoegde labels uit {n} namen halen…"),
    "Send it to the Recycle Bin?": ("Naar de Prullenbak sturen?", "Ze naar de Prullenbak sturen?"),
    "Send {n} ticked original to Recycle Bin…": ("{n} aangevinkt origineel naar Prullenbak…", "{n} aangevinkte originelen naar Prullenbak…"),
    "about {n} minute": ("ongeveer {n} minuut", "ongeveer {n} minuten"),
    "{n} H.264 video, {size}.": ("{n} H.264-video, {size}.", "{n} H.264-video's, {size}."),
    "{n} LRV file moved to the Recycle Bin.": ("{n} LRV-bestand naar de Prullenbak verplaatst.", "{n} LRV-bestanden naar de Prullenbak verplaatst."),
    "{n} conversion whose original is in the Recycle Bin will take the original's name, for example {name}.":
        ("{n} conversie waarvan het origineel in de Prullenbak staat, krijgt de naam van het origineel, bijvoorbeeld {name}.",
         "{n} conversies waarvan het origineel in de Prullenbak staat, krijgen de naam van het origineel, bijvoorbeeld {name}."),
    "{n} file renamed.": ("{n} bestand hernoemd.", "{n} bestanden hernoemd."),
    "{n} original ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, and you can restore originals from the Recycle Bin.":
        ("{n} origineel ({size}) gaat naar de Windows-Prullenbak. Elke conversie wordt eerst opnieuw gecontroleerd, en je kunt originelen terugzetten uit de Prullenbak.",
         "{n} originelen ({size}) gaan naar de Windows-Prullenbak. Elke conversie wordt eerst opnieuw gecontroleerd, en je kunt originelen terugzetten uit de Prullenbak."),
    "{n} original moved to the Recycle Bin.": ("{n} origineel naar de Prullenbak verplaatst.", "{n} originelen naar de Prullenbak verplaatst."),
    "{n} other LRV file will stay, because the original video isn't beside it.":
        ("{n} ander LRV-bestand blijft staan, omdat de originele video er niet naast staat.",
         "{n} andere LRV-bestanden blijven staan, omdat de originele video er niet naast staat."),
    "{n} video already in H.265, skipped.": ("{n} video al in H.265, overgeslagen.", "{n} video's al in H.265, overgeslagen."),
    "{n} video from your last batch is not finished. Files already verified will not be converted again. Continue now?":
        ("{n} video uit je laatste reeks is niet klaar. Al gecontroleerde bestanden worden niet opnieuw geconverteerd. Nu verdergaan?",
         "{n} video's uit je laatste reeks zijn niet klaar. Al gecontroleerde bestanden worden niet opnieuw geconverteerd. Nu verdergaan?"),
    "{n} video in another format, skipped.": ("{n} video in een ander formaat, overgeslagen.", "{n} video's in een ander formaat, overgeslagen."),
    "{n} video, {size}.": ("{n} video, {size}.", "{n} video's, {size}."),
    "⚠ {n} of these has a conversion at a lower resolution. Once the original is gone from the Recycle Bin, that detail is gone for good.":
        ("⚠ {n} hiervan heeft een conversie met een lagere resolutie. Zodra het origineel uit de Prullenbak weg is, is dat detail voorgoed verloren.",
         "⚠ {n} hiervan hebben een conversie met een lagere resolutie. Zodra het origineel uit de Prullenbak weg is, is dat detail voorgoed verloren."),
    "⚠ {n} of these has a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). Once the original is gone from the Recycle Bin, that lost quality can't be recovered.":
        ("⚠ {n} hiervan heeft een conversie onder de aanbevolen kwaliteit (VMAF-gemiddelde {mean}, slechtste 1% {p1}). Zodra het origineel uit de Prullenbak weg is, is die verloren kwaliteit niet meer terug te halen.",
         "⚠ {n} hiervan hebben een conversie onder de aanbevolen kwaliteit (VMAF-gemiddelde {mean}, slechtste 1% {p1}). Zodra het origineel uit de Prullenbak weg is, is die verloren kwaliteit niet meer terug te halen."),
}
