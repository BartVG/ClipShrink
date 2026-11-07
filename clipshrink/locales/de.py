"""Deutsch. Not yet checked by a native speaker: corrections are welcome on GitHub."""

MESSAGES = {
    # --- Steps, pages and buttons
    "Find videos": "Videos finden",
    "See the saving": "Ersparnis ansehen",
    "Convert": "Umwandeln",
    "Compare and clean up": "Vergleichen und aufräumen",
    "Settings": "Einstellungen",
    "{app} {version}: shrink videos, keep the quality": "{app} {version}: Videos verkleinern, Qualität behalten",
    "←  Back": "←  Zurück",
    "Choose folder…": "Ordner wählen…",
    "Choose the folder with your videos": "Wählen Sie den Ordner mit Ihren Videos",
    "No folder chosen": "Kein Ordner gewählt",
    "Find your videos": "Ihre Videos finden",
    "Pick a folder. This tool looks through it and every folder inside it, and lists the H.264 videos it can shrink. Nothing is changed yet.":
        "Wählen Sie einen Ordner. Das Programm durchsucht ihn und alle Unterordner und listet die H.264-Videos auf, die es verkleinern kann. Noch wird nichts verändert.",
    "Next: see the saving  →": "Weiter: Ersparnis ansehen  →",
    "Reading your videos…": "Ihre Videos werden gelesen…",
    "File": "Datei",
    "Folder": "Ordner",
    "Size": "Größe",
    "Picture": "Bild",
    "Length": "Dauer",
    "State": "Status",
    "Ready": "Bereit",
    "Already has a conversion": "Hat schon eine Umwandlung",
    "GoPro low-res preview, off by default": "GoPro-Vorschau in niedriger Auflösung, standardmäßig aus",
    "Already {codec}, skipped": "Schon {codec}, übersprungen",
    "(converted by this tool)": "(von diesem Programm umgewandelt)",
    "{n} could not be read and were skipped: {names}.": "{n} konnten nicht gelesen werden und wurden übersprungen: {names}.",
    "No H.264 videos found in this folder or its subfolders.": "Keine H.264-Videos in diesem Ordner oder seinen Unterordnern gefunden.",
    "Delete GoPro LRV files?": "GoPro-LRV-Dateien löschen?",
    "An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera and its phone app can show quick previews. You don't need it if you have the original video, which is beside each of these.":
        "Eine LRV-Datei ist eine kleine Kopie in niedriger Auflösung, die eine GoPro neben jedem Video aufnimmt, damit Kamera und Handy-App schnelle Vorschauen zeigen können. Sie brauchen sie nicht, wenn Sie das Originalvideo haben, und das liegt neben jeder dieser Dateien.",
    "Done": "Fertig",
    "Left in place:": "Liegen geblieben:",
    "Left as they are:": "Unverändert geblieben:",

    # --- See the saving
    "See the saving before anything converts": "Sehen Sie die Ersparnis, bevor etwas umgewandelt wird",
    "This makes short test encodes from a few of your own files and measures them. Your files are only read, and nothing appears in your folders.":
        "Dabei werden kurze Testkodierungen aus einigen Ihrer Dateien erstellt und gemessen. Ihre Dateien werden nur gelesen, und in Ihren Ordnern erscheint nichts.",
    "Run the test encodes": "Testkodierungen starten",
    "Not measured yet": "Noch nicht gemessen",
    "Click \"Run the test encodes\" to measure how much space you would save.":
        "Klicken Sie auf „Testkodierungen starten“, um zu messen, wie viel Platz Sie sparen würden.",
    "Measuring…": "Wird gemessen…",
    "Encoding samples of your files and comparing them with the originals.":
        "Ausschnitte Ihrer Dateien werden kodiert und mit den Originalen verglichen.",
    "Could not measure": "Messung nicht möglich",
    "The test encode stopped: {error}": "Die Testkodierung wurde abgebrochen: {error}",
    "About {size} saved ({pct}%)": "Etwa {size} gespart ({pct} %)",
    "Likely between {low} and {high}, out of {total}.": "Wahrscheinlich zwischen {low} und {high}, von {total}.",
    "Converting everything should take {time}.": "Alles umzuwandeln dauert voraussichtlich {time}.",
    "Sample from": "Ausschnitt aus",
    "At": "Bei",
    "Original": "Original",
    "VMAF average": "VMAF-Mittelwert",
    "VMAF worst 1%": "VMAF schlechteste 1 %",
    "Meets the quality target?": "Erreicht das Qualitätsziel?",
    "Yes": "Ja",
    "⚠ No, would get a warning": "⚠ Nein, bekäme eine Warnung",
    "Start converting  →": "Umwandlung starten  →",
    "Expected time: {time}. Your computer will not go to sleep while this runs.":
        "Erwartete Dauer: {time}. Ihr Computer geht währenddessen nicht in den Energiesparmodus.",
    "The target: VMAF average at least {mean}, worst 1% of frames at least {p1}. Every full file is measured again after conversion.":
        "Das Ziel: VMAF-Mittelwert mindestens {mean}, die schlechtesten 1 % der Bilder mindestens {p1}. Jede vollständige Datei wird nach der Umwandlung erneut gemessen.",
    "{codec}. Change this in Settings.": "{codec}. Änderbar in den Einstellungen.",
    "{codec}, at most {size}. Change this in Settings.": "{codec}, höchstens {size}. Änderbar in den Einstellungen.",

    # --- Convert
    "Files Processed": "Verarbeitete Dateien",
    "Space Saved": "Gesparter Platz",
    "Current Batch": "Aktueller Stapel",
    "Time Remaining": "Restzeit",
    "Pause": "Pause",
    "Resume": "Fortsetzen",
    "Paused": "Pausiert",
    "Calculating…": "Wird berechnet…",
    "Overall Progress": "Gesamtfortschritt",
    "Overall Progress: {pct}% ({done} of {total} files)": "Gesamtfortschritt: {pct} % ({done} von {total} Dateien)",
    "Current File": "Aktuelle Datei",
    "Current File: {name}: {stage}": "Aktuelle Datei: {name}: {stage}",
    "Current File: none, the batch is finished": "Aktuelle Datei: keine, der Stapel ist fertig",
    "All": "Alle",
    "Completed": "Fertig",
    "Active": "Aktiv",
    "Waiting": "Wartend",
    "Before": "Vorher",
    "After": "Nachher",
    "% Saved": "% gespart",
    "Worst 1%": "Schlechteste 1 %",
    "Encoding": "Kodierung",
    "Next: compare and clean up  →": "Weiter: vergleichen und aufräumen  →",
    "Finding the right quality": "Die richtige Qualität wird gesucht",
    "Measuring every frame": "Jedes Bild wird gemessen",
    "Finding quality": "Qualität suchen",
    "Measuring": "Messen",
    "Finished: {n} verified": "Fertig: {n} geprüft",
    ", ⚠ {n} below target": ", ⚠ {n} unter dem Ziel",
    ", {n} kept as original": ", {n} als Original behalten",
    "(see next page)": "(siehe nächste Seite)",
    "Nothing left to convert: every selected file is already finished.":
        "Nichts mehr umzuwandeln: Jede ausgewählte Datei ist schon fertig.",
    "The batch stopped": "Der Stapel wurde abgebrochen",
    "Files already verified are safe. Reopen the app to continue.":
        "Bereits geprüfte Dateien sind sicher. Öffnen Sie das Programm erneut, um fortzufahren.",
    "Continue where you left off?": "Dort weitermachen, wo Sie aufgehört haben?",
    "Each conversion is saved beside its original with {suffix} added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Jede Umwandlung wird neben ihrem Original gespeichert, mit {suffix} im Namen. Originale werden nur gelesen. Sie können jederzeit pausieren, und wenn der PC abstürzt, öffnen Sie das Programm einfach erneut.",
    "Each conversion is saved beside its original with {suffix} ({shrunk} if it was shrunk) added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Jede Umwandlung wird neben ihrem Original gespeichert, mit {suffix} ({shrunk}, wenn sie verkleinert wurde) im Namen. Originale werden nur gelesen. Sie können jederzeit pausieren, und wenn der PC abstürzt, öffnen Sie das Programm einfach erneut.",
    "Stop converting?": "Umwandlung beenden?",
    "The batch is still running. If you close now, the current file is restarted next time and finished files are kept. Close anyway?":
        "Der Stapel läuft noch. Wenn Sie jetzt schließen, wird die aktuelle Datei beim nächsten Mal neu begonnen, und fertige Dateien bleiben erhalten. Trotzdem schließen?",

    # --- Statuses
    "Working…": "In Arbeit…",
    "Verified": "Geprüft",
    "⚠ Below target": "⚠ Unter dem Ziel",
    "Resized": "Verkleinert",
    "Verified at {mean} / {p1}": "Geprüft bei {mean} / {p1}",
    "Resized at {mean} / {p1}": "Verkleinert bei {mean} / {p1}",
    "Original kept": "Original behalten",
    "Failed, original kept": "Fehlgeschlagen, Original behalten",
    "Original in Recycle Bin": "Original im Papierkorb",
    "Done, has the original's name": "Fertig, trägt den Namen des Originals",
    "processor": "Prozessor",

    # --- Compare and clean up
    "Play any original beside its conversion, in sync. When you are happy, you can send originals to the Recycle Bin. This step is optional. Click a column title to sort.":
        "Spielen Sie jedes Original synchron neben seiner Umwandlung ab. Wenn Sie zufrieden sind, können Sie Originale in den Papierkorb verschieben. Dieser Schritt ist freiwillig. Klicken Sie auf einen Spaltentitel, um zu sortieren.",
    "Select All": "Alle ankreuzen",
    "Deselect All": "Alle abwählen",
    "Select Recommended": "Empfohlene ankreuzen",
    "Deselect Recommended": "Empfohlene abwählen",
    "Recommended means the conversion met the quality target, with no warning sign.":
        "Empfohlen heißt: Die Umwandlung hat das Qualitätsziel erreicht, ohne Warnzeichen.",
    "Tip: Ctrl+click a row to tick it, Shift+click to tick a range, Ctrl+A to tick all. Right-click a row to open its folder.":
        "Tipp: Strg+Klick kreuzt eine Zeile an, Umschalt+Klick einen Bereich, Strg+A alle. Rechtsklick auf eine Zeile öffnet ihren Ordner.",
    "Delete?": "Löschen?",
    "Result": "Ergebnis",
    "▶  Play selected side by side": "▶  Auswahl nebeneinander abspielen",
    "Remove the added tags from names": "Angefügte Kennungen aus Namen entfernen",
    "Send ticked originals to Recycle Bin…": "Angekreuzte Originale in den Papierkorb…",
    "Tick originals above to delete them": "Kreuzen Sie oben Originale an, um sie zu löschen",
    "Needs your attention": "Braucht Ihre Aufmerksamkeit",
    "Needs your attention ({n})": "Braucht Ihre Aufmerksamkeit ({n})",
    "Needs your attention: nothing": "Braucht Ihre Aufmerksamkeit: nichts",
    "Every conversion passed.": "Jede Umwandlung hat bestanden.",
    "Nothing converted yet.": "Noch nichts umgewandelt.",
    "{size} can be saved once originals are removed": "{size} lassen sich sparen, sobald die Originale entfernt sind",
    "Available after an original has been sent to the Recycle Bin.": "Verfügbar, sobald ein Original im Papierkorb ist.",
    "Start Over": "Neu beginnen",
    "Forget these files and go back to step 1. Your videos and reports aren't touched.":
        "Diese Dateien vergessen und zu Schritt 1 zurückkehren. Ihre Videos und Berichte bleiben unberührt.",
    "Open file location": "Dateispeicherort öffnen",
    "Pick a video": "Wählen Sie ein Video",
    "Click a row in the list first.": "Klicken Sie zuerst auf eine Zeile in der Liste.",
    "Cannot compare": "Vergleich nicht möglich",
    "This row needs both an original and a verified conversion on disk.":
        "Diese Zeile braucht sowohl ein Original als auch eine geprüfte Umwandlung auf dem Datenträger.",
    "Re-checking and removing": "Erneut prüfen und entfernen",
    "Renaming": "Umbenennen",
    "finishing": "Abschluss",
    "{action} {i} of {total}: {name}": "{action} {i} von {total}: {name}",
    "Remove the added tags from names?": "Angefügte Kennungen aus Namen entfernen?",
    "Only the name changes. If you later restore an original from the Recycle Bin, Windows will ask what to do about the same name.":
        "Nur der Name ändert sich. Wenn Sie später ein Original aus dem Papierkorb wiederherstellen, fragt Windows, was mit dem gleichen Namen geschehen soll.",
    "Send originals to the Recycle Bin?": "Originale in den Papierkorb verschieben?",
    "I understand. Send these originals to the Recycle Bin.": "Ich habe verstanden. Diese Originale in den Papierkorb verschieben.",
    "Send to Recycle Bin": "In den Papierkorb",
    "Keep them": "Behalten",
    "Below the quality target. Compare it with the original before removing the original.":
        "Unter dem Qualitätsziel. Vergleichen Sie es mit dem Original, bevor Sie das Original entfernen.",

    # --- Player
    "Side by side: {name}": "Nebeneinander: {name}",
    "Original (H.264)": "Original (H.264)",
    "Original (H.264), shrunk to match": "Original (H.264), passend verkleinert",
    "Conversion ({codec})": "Umwandlung ({codec})",
    "Play": "Abspielen",
    "◀ Frame": "◀ Bild",
    "Frame ▶": "Bild ▶",
    "Whole picture": "Ganzes Bild",
    "Drag the picture to look around": "Ziehen Sie das Bild, um sich umzusehen",
    "VMAF average {mean}, worst 1% {p1}": "VMAF-Mittelwert {mean}, schlechteste 1 % {p1}",
    "Could not play": "Wiedergabe nicht möglich",
    "Player": "Player",

    # --- Settings
    "Language": "Sprache",
    "The default settings suit most people, so you can leave this page alone. Change something only if you have a reason.":
        "Die Standardeinstellungen passen für die meisten, Sie können diese Seite also so lassen. Ändern Sie nur etwas, wenn Sie einen Grund haben.",
    "Encode with": "Kodieren mit",
    "Graphics card (fast, recommended)": "Grafikkarte (schnell, empfohlen)",
    "Processor (slow, works on any PC)": "Prozessor (langsam, läuft auf jedem PC)",
    "Graphics card (fast, recommended) ({card} detected)": "Grafikkarte (schnell, empfohlen) ({card} erkannt)",
    "Graphics card ({card} can't make this format)": "Grafikkarte ({card} kann dieses Format nicht erzeugen)",
    "Graphics card (no compatible graphics card detected)": "Grafikkarte (keine passende Grafikkarte erkannt)",
    "NVIDIA card": "NVIDIA-Karte",
    "In use: your graphics card, making {codec} video.": "Verwendet: Ihre Grafikkarte, erzeugt {codec}-Video.",
    "In use: your processor, making {codec} video.": "Verwendet: Ihr Prozessor, erzeugt {codec}-Video.",
    "{card} was found, but it can't make {codec} video, so the processor is used.":
        "{card} wurde gefunden, kann aber kein {codec}-Video erzeugen, daher wird der Prozessor verwendet.",
    "No compatible graphics card was found (only NVIDIA is supported), so the processor is used.":
        "Keine passende Grafikkarte gefunden (nur NVIDIA wird unterstützt), daher wird der Prozessor verwendet.",
    "Video format": "Videoformat",
    "H.265 (recommended)": "H.265 (empfohlen)",
    "AV1 files are usually smaller, but they play on fewer devices. Check that your TV or phone can play one first.":
        "AV1-Dateien sind meist kleiner, laufen aber auf weniger Geräten. Prüfen Sie zuerst, ob Ihr Fernseher oder Handy eine abspielen kann.",
    "Largest size": "Größte Auflösung",
    "Keep the original resolution (recommended)": "Originalauflösung behalten (empfohlen)",
    "This permanently lowers the detail in the conversions, and videos are never enlarged. They are checked against a smaller copy of the original and labelled Resized. Keep the originals if you might want the full detail later.":
        "Das verringert die Details in den Umwandlungen dauerhaft, und Videos werden nie vergrößert. Sie werden mit einer verkleinerten Kopie des Originals verglichen und als Verkleinert gekennzeichnet. Behalten Sie die Originale, wenn Sie später vielleicht alle Details wollen.",
    "Show an Encoding column": "Spalte Kodierung anzeigen",
    "Format, quality setting, resolution and bitrate of each conversion.":
        "Format, Qualitätseinstellung, Auflösung und Bitrate jeder Umwandlung.",
    "Show the Welcome screen when the app opens": "Willkommensbildschirm beim Start anzeigen",
    "Advanced": "Erweitert",
    "Only change these if you know what you are doing: they can lower the quality of your videos.":
        "Ändern Sie diese Werte nur, wenn Sie wissen, was Sie tun: Sie können die Qualität Ihrer Videos verringern.",
    "Read what each one does": "Lesen, was jeder Wert bewirkt",
    "I've read this and understand what I'm doing": "Ich habe das gelesen und weiß, was ich tue",
    "Warn below": "Warnen unter",
    "Also aim for these values when choosing quality": "Diese Werte auch bei der Wahl der Qualität anstreben",
    "Ticked, lower values make smaller files with lower quality, and higher values make larger files. Not ticked, your files stay the same and only the warning moves.":
        "Angekreuzt ergeben niedrigere Werte kleinere Dateien mit geringerer Qualität und höhere Werte größere Dateien. Nicht angekreuzt bleiben Ihre Dateien gleich, und nur die Warnung verschiebt sich.",
    "Don't keep a conversion below a minimum": "Keine Umwandlung unter einem Minimum behalten",
    "Below the minimum, nothing is kept and your original stays. Off by default, so every result that is smaller and matches is kept, with a warning if needed.":
        "Unter dem Minimum wird nichts behalten, und Ihr Original bleibt. Standardmäßig aus, also wird jedes kleinere und passende Ergebnis behalten, bei Bedarf mit Warnung.",
    "Back to the defaults": "Zurück zu den Standardwerten",
    "Your target is {mean}.": "Ihr Ziel ist {mean}.",
    "How close this video looks to the original, from 0 to 100. VMAF is a score made by Netflix, based on how people see video. At 95 or above, most people can't see a difference.":
        "Wie nah dieses Video dem Original kommt, von 0 bis 100. VMAF ist ein Wert von Netflix, der darauf beruht, wie Menschen Video wahrnehmen. Ab 95 sehen die meisten Menschen keinen Unterschied.",
    "The score of the worst moments: 1% of the video's frames score lower than this. It catches a short bad patch that a good average would hide. The target is {p1} or above.":
        "Der Wert der schlechtesten Momente: 1 % der Bilder des Videos liegen darunter. So fällt eine kurze schlechte Stelle auf, die ein guter Mittelwert verbergen würde. Das Ziel ist {p1} oder mehr.",

    # --- Welcome
    "Welcome to {app}": "Willkommen bei {app}",
    "Shrink your videos, keep the quality.": "Verkleinern Sie Ihre Videos, behalten Sie die Qualität.",
    "Zero guesswork": "Kein Rätselraten",
    "No bitrates or codecs to configure. ClipShrink automatically finds the right compression balance for every video.":
        "Keine Bitraten oder Codecs einzustellen. ClipShrink findet für jedes Video automatisch das richtige Maß an Kompression.",
    "Measured frame-by-frame": "Bild für Bild gemessen",
    "Every result is scored against the original using Netflix's VMAF visual quality metric, and any clip that misses the target is clearly flagged.":
        "Jedes Ergebnis wird mit VMAF, dem Bildqualitätsmaß von Netflix, am Original gemessen, und jeder Clip, der das Ziel verfehlt, wird deutlich markiert.",
    "You stay in control": "Sie behalten die Kontrolle",
    "Conversions are saved as new files alongside your originals. Compare both versions side by side before deciding what to send to the Recycle Bin.":
        "Umwandlungen werden als neue Dateien neben Ihren Originalen gespeichert. Vergleichen Sie beide Fassungen nebeneinander, bevor Sie entscheiden, was in den Papierkorb kommt.",
    "Don't show this again": "Nicht mehr anzeigen",

    # --- About
    "About {app}": "Über {app}",
    "{app} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion against its original with VMAF and warns you about any below the quality target. Your originals are only read during conversion, and nothing is sent anywhere.":
        "{app} wandelt H.264-Videos in H.265 oder AV1 um, um Speicherplatz freizugeben. Es misst jede Umwandlung mit VMAF am Original und warnt Sie vor jeder unter dem Qualitätsziel. Ihre Originale werden beim Umwandeln nur gelesen, und nichts wird irgendwohin gesendet.",
    "Documentation:": "Dokumentation:",
    "Open in your browser": "Im Browser öffnen",
    "Copy the link": "Link kopieren",
    "Project:": "Projekt:",
    "Reports:": "Berichte:",
    "Each batch leaves a CSV report here. They're only for your information. Once a batch is finished and you exit or click Start Over, the app forgets those files.":
        "Jeder Stapel hinterlässt hier einen CSV-Bericht, nur zu Ihrer Information. Sobald ein Stapel fertig ist und Sie das Programm beenden oder auf Neu beginnen klicken, vergisst es diese Dateien.",
    "Licence:": "Lizenz:",
    "GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace.":
        "GPL-3.0. Ohne Gewähr, also bewahren Sie eine Sicherung von Aufnahmen auf, die Sie nicht ersetzen können.",
    "Built with:": "Erstellt mit:",
    "FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in THIRD_PARTY_NOTICES.md in the install folder and on the project page.":
        "FFmpeg, x265, SVT-AV1, VMAF, mpv und Qt. Ihre Lizenzen und Links zum Quellcode stehen in THIRD_PARTY_NOTICES.md im Installationsordner und auf der Projektseite.",
    "What does \"no quality loss\" mean?": "Was heißt „kein Qualitätsverlust“?",
    "Truly lossless H.265, where every pixel stays identical, usually makes files larger than the originals, so it would cost you space instead of saving it. This tool uses a measured definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure from Netflix of how a video looks to people, scored from 0 to 100. A conversion counts as recommended if the average score is at least 95 and the worst 1% of frames score at least 90, a level where differences are very hard to see. This is the quality target.\n\n"
    "If a file misses the target even at the best setting, it is still converted, and it gets a warning sign so you can decide for yourself. Use Select Recommended to leave those files out when cleaning up. If the result is not smaller, your original is simply kept and the file is listed in the report. Sound, any GoPro telemetry and capture dates are copied unchanged, and originals are never touched during conversion.\n\n"
    "If you choose a smaller resolution in Settings, the conversion is compared with a smaller copy of the original at the same size. So the score shows how clean the encoding is, not the detail lost by shrinking, and those files are labelled Resized rather than Verified.\n\n"
    "The advanced part of Settings can change these numbers. Files judged by other numbers show them in their label.":
        "Echt verlustfreies H.265, bei dem jedes Pixel gleich bleibt, ergibt meist größere Dateien als die Originale: Es würde Platz kosten, statt welchen zu sparen. Dieses Programm verwendet stattdessen eine gemessene Definition.\n\n"
        "Nach jeder Umwandlung vergleicht es jedes Bild mit dem Original, und zwar mit VMAF, einem offenen Maß von Netflix dafür, wie ein Video auf Menschen wirkt, mit Werten von 0 bis 100. Eine Umwandlung gilt als empfohlen, wenn der Mittelwert mindestens 95 beträgt und die schlechtesten 1 % der Bilder mindestens 90 erreichen, ein Niveau, auf dem Unterschiede sehr schwer zu sehen sind. Das ist das Qualitätsziel.\n\n"
        "Verfehlt eine Datei das Ziel selbst mit der besten Einstellung, wird sie trotzdem umgewandelt und bekommt ein Warnzeichen, damit Sie selbst entscheiden können. Mit Empfohlene ankreuzen lassen Sie diese Dateien beim Aufräumen aus. Ist das Ergebnis nicht kleiner, bleibt Ihr Original einfach erhalten, und die Datei steht im Bericht. Ton, eventuelle GoPro-Telemetrie und Aufnahmedaten werden unverändert übernommen, und Originale werden beim Umwandeln nie angetastet.\n\n"
        "Wählen Sie in den Einstellungen eine kleinere Auflösung, wird die Umwandlung mit einer verkleinerten Kopie des Originals in derselben Größe verglichen. Der Wert zeigt also, wie sauber die Kodierung ist, nicht die durch das Verkleinern verlorenen Details, und diese Dateien heißen Verkleinert statt Geprüft.\n\n"
        "Der erweiterte Teil der Einstellungen kann diese Zahlen ändern. Dateien, die nach anderen Zahlen beurteilt wurden, zeigen diese in ihrer Kennzeichnung.",

    # --- Sizes and times
    "bytes": "Bytes",
    "KB": "KB",
    "MB": "MB",
    "GB": "GB",
    "TB": "TB",
    "~{m}m left": "~{m} Min. übrig",
    "~{h}h {m}m left": "~{h} Std. {m} Min. übrig",
    "under a minute": "unter einer Minute",
    "about {h} h {m} min": "etwa {h} Std. {m} Min.",
    "about {d} days": "etwa {d} Tage",

    # --- Reasons
    "Could not convert, original kept: {error}": "Umwandlung nicht möglich, Original behalten: {error}",
    "This is {codec}, not H.264, so it was left alone.": "Das ist {codec}, nicht H.264, daher wurde es nicht angefasst.",
    "the encoder stopped: {detail}": "der Encoder wurde beendet: {detail}",
    "the encoder failed: {detail}": "der Encoder ist fehlgeschlagen: {detail}",
    "could not write the file: {detail}": "die Datei konnte nicht geschrieben werden: {detail}",
    "could not read a sample from the file: {detail}": "aus der Datei konnte kein Ausschnitt gelesen werden: {detail}",
    "the VMAF comparison could not run: {detail}": "der VMAF-Vergleich konnte nicht laufen: {detail}",
    "the VMAF comparison returned no frames": "der VMAF-Vergleich lieferte keine Bilder",
    "the original changed while it was being converted": "das Original hat sich während der Umwandlung geändert",
    "Conversion is not smaller ({out} vs {src} bytes), original kept.": "Die Umwandlung ist nicht kleiner ({out} gegenüber {src} Bytes), Original behalten.",
    "Conversion did not match the original, original kept: {problems}": "Die Umwandlung passte nicht zum Original, Original behalten: {problems}",
    "video is {codec}": "Video ist {codec}",
    "resolution differs": "Auflösung weicht ab",
    "pixel format differs ({out} vs {src})": "Pixelformat weicht ab ({out} gegenüber {src})",
    "colour range differs": "Farbbereich weicht ab",
    "audio tracks differ": "Tonspuren weichen ab",
    "duration differs ({out}s vs {src}s)": "Dauer weicht ab ({out} s gegenüber {src} s)",
    "frame count differs ({out} vs {src})": "Bildanzahl weicht ab ({out} gegenüber {src})",
    "audio or telemetry tracks changed": "Ton- oder Telemetriespuren haben sich geändert",
    "camera info changed": "Kamerainformationen haben sich geändert",
    "VMAF compared {frames} frames out of {total}, original kept.": "VMAF hat {frames} von {total} Bildern verglichen, Original behalten.",
    "VMAF short of what the search aims for.": "VMAF unter dem, was die Suche anstrebt.",
    "VMAF below your minimum: average {mean} (minimum {min_mean}), worst 1% {p1} (minimum {min_p1}). Nothing was kept, and your original is untouched.":
        "VMAF unter Ihrem Minimum: Mittelwert {mean} (Minimum {min_mean}), schlechteste 1 % {p1} (Minimum {min_p1}). Nichts wurde behalten, und Ihr Original ist unberührt.",
    "VMAF below the target: average {mean} (target {warn_mean}), worst 1% {p1} (target {warn_p1}). Compare it before removing the original.":
        "VMAF unter dem Ziel: Mittelwert {mean} (Ziel {warn_mean}), schlechteste 1 % {p1} (Ziel {warn_p1}). Vergleichen Sie, bevor Sie das Original entfernen.",
    "this file was never converted by this tool": "diese Datei wurde nie von diesem Programm umgewandelt",
    "its original has not been sent to the Recycle Bin": "ihr Original ist nicht im Papierkorb",
    "the converted file is missing": "die umgewandelte Datei fehlt",
    "it already has the original's name": "sie trägt schon den Namen des Originals",
    "the converted file has changed since it was verified": "die umgewandelte Datei hat sich seit der Prüfung geändert",
    "another file already has that name": "eine andere Datei trägt schon diesen Namen",
    "renaming was not confirmed": "das Umbenennen wurde nicht bestätigt",
    "Windows refused the rename: {error}": "Windows hat das Umbenennen verweigert: {error}",
    "it is not an LRV file": "es ist keine LRV-Datei",
    "its full video is not beside it": "das vollständige Video liegt nicht daneben",
    "Windows did not move it to the Recycle Bin, so it was left in place": "Windows hat sie nicht in den Papierkorb verschoben, daher ist sie geblieben",
    "its conversion is not verified (status: {status})": "ihre Umwandlung ist nicht geprüft (Status: {status})",
    "the original has changed since it was verified": "das Original hat sich seit der Prüfung geändert",
    "the converted file's content does not match what was verified": "der Inhalt der umgewandelten Datei entspricht nicht dem Geprüften",
    "the converted file cannot be read: {error}": "die umgewandelte Datei kann nicht gelesen werden: {error}",
    "the converted file is not H.265 or AV1": "die umgewandelte Datei ist weder H.265 noch AV1",
    "deletion was not confirmed": "das Löschen wurde nicht bestätigt",
    "its conversion is below the default quality target, and that was not confirmed": "ihre Umwandlung liegt unter dem Standard-Qualitätsziel, und das wurde nicht bestätigt",
    "its conversion has a lower resolution, and that was not confirmed": "ihre Umwandlung hat eine geringere Auflösung, und das wurde nicht bestätigt",

    # --- Report columns
    "Date": "Datum",
    "Reason": "Grund",
    "Before (bytes)": "Vorher (Bytes)",
    "After (bytes)": "Nachher (Bytes)",
    "Saved %": "% gespart",
    "Encoder": "Encoder",
    "Quality setting": "Qualitätseinstellung",
    "Conversion": "Umwandlung",
    "Codec": "Codec",
    "Output resolution": "Ausgabeauflösung",
    "Output bitrate (Mbit/s)": "Ausgabebitrate (Mbit/s)",
    "Target average": "Ziel Mittelwert",
    "Target worst 1%": "Ziel schlechteste 1 %",
}

PLURALS = {
    "Found {n} GoPro LRV file ({size}).": ("{n} GoPro-LRV-Datei gefunden ({size}).", "{n} GoPro-LRV-Dateien gefunden ({size})."),
    "Measured on {n} file using your graphics card.": ("Gemessen an {n} Datei mit Ihrer Grafikkarte.", "Gemessen an {n} Dateien mit Ihrer Grafikkarte."),
    "Measured on {n} file using your processor.": ("Gemessen an {n} Datei mit Ihrem Prozessor.", "Gemessen an {n} Dateien mit Ihrem Prozessor."),
    "Remove the added tags from {n} name…": ("Angefügte Kennungen aus {n} Namen entfernen…", "Angefügte Kennungen aus {n} Namen entfernen…"),
    "Send it to the Recycle Bin?": ("In den Papierkorb verschieben?", "In den Papierkorb verschieben?"),
    "Send {n} ticked original to Recycle Bin…": ("{n} angekreuztes Original in den Papierkorb…", "{n} angekreuzte Originale in den Papierkorb…"),
    "about {n} minute": ("etwa {n} Minute", "etwa {n} Minuten"),
    "{n} H.264 video, {size}.": ("{n} H.264-Video, {size}.", "{n} H.264-Videos, {size}."),
    "{n} LRV file moved to the Recycle Bin.": ("{n} LRV-Datei in den Papierkorb verschoben.", "{n} LRV-Dateien in den Papierkorb verschoben."),
    "{n} conversion whose original is in the Recycle Bin will take the original's name, for example {name}.":
        ("{n} Umwandlung, deren Original im Papierkorb ist, erhält den Namen des Originals, zum Beispiel {name}.",
         "{n} Umwandlungen, deren Original im Papierkorb ist, erhalten den Namen des Originals, zum Beispiel {name}."),
    "{n} file renamed.": ("{n} Datei umbenannt.", "{n} Dateien umbenannt."),
    "{n} original ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, and you can restore originals from the Recycle Bin.":
        ("{n} Original ({size}) kommt in den Windows-Papierkorb. Jede Umwandlung wird zuerst erneut geprüft, und Sie können Originale aus dem Papierkorb wiederherstellen.",
         "{n} Originale ({size}) kommen in den Windows-Papierkorb. Jede Umwandlung wird zuerst erneut geprüft, und Sie können Originale aus dem Papierkorb wiederherstellen."),
    "{n} original moved to the Recycle Bin.": ("{n} Original in den Papierkorb verschoben.", "{n} Originale in den Papierkorb verschoben."),
    "{n} other LRV file will stay, because the original video isn't beside it.":
        ("{n} weitere LRV-Datei bleibt, weil das Originalvideo nicht daneben liegt.",
         "{n} weitere LRV-Dateien bleiben, weil das Originalvideo nicht daneben liegt."),
    "{n} video already in H.265, skipped.": ("{n} Video schon in H.265, übersprungen.", "{n} Videos schon in H.265, übersprungen."),
    "{n} video from your last batch is not finished. Files already verified will not be converted again. Continue now?":
        ("{n} Video aus Ihrem letzten Stapel ist nicht fertig. Bereits geprüfte Dateien werden nicht erneut umgewandelt. Jetzt fortfahren?",
         "{n} Videos aus Ihrem letzten Stapel sind nicht fertig. Bereits geprüfte Dateien werden nicht erneut umgewandelt. Jetzt fortfahren?"),
    "{n} video in another format, skipped.": ("{n} Video in einem anderen Format, übersprungen.", "{n} Videos in einem anderen Format, übersprungen."),
    "{n} video, {size}.": ("{n} Video, {size}.", "{n} Videos, {size}."),
    "⚠ {n} of these has a conversion at a lower resolution. Once the original is gone from the Recycle Bin, that detail is gone for good.":
        ("⚠ {n} davon hat eine Umwandlung mit geringerer Auflösung. Sobald das Original aus dem Papierkorb verschwunden ist, sind diese Details für immer weg.",
         "⚠ {n} davon haben eine Umwandlung mit geringerer Auflösung. Sobald das Original aus dem Papierkorb verschwunden ist, sind diese Details für immer weg."),
    "⚠ {n} of these has a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). Once the original is gone from the Recycle Bin, that lost quality can't be recovered.":
        ("⚠ {n} davon hat eine Umwandlung unter der empfohlenen Qualität (VMAF-Mittelwert {mean}, schlechteste 1 % {p1}). Sobald das Original aus dem Papierkorb verschwunden ist, lässt sich diese verlorene Qualität nicht zurückholen.",
         "⚠ {n} davon haben eine Umwandlung unter der empfohlenen Qualität (VMAF-Mittelwert {mean}, schlechteste 1 % {p1}). Sobald das Original aus dem Papierkorb verschwunden ist, lässt sich diese verlorene Qualität nicht zurückholen."),
}
