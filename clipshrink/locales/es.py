"""Español. Not yet checked by a native speaker: corrections are welcome on GitHub."""

MESSAGES = {
    # --- Steps, pages and buttons
    "Find videos": "Buscar vídeos",
    "See the saving": "Ver el ahorro",
    "Convert": "Convertir",
    "Compare and clean up": "Comparar y limpiar",
    "Settings": "Ajustes",
    "{app} {version}: shrink videos, keep the quality": "{app} {version}: reduce tus vídeos, conserva la calidad",
    "←  Back": "←  Atrás",
    "Choose folder…": "Elegir carpeta…",
    "Choose the folder with your videos": "Elige la carpeta con tus vídeos",
    "No folder chosen": "Ninguna carpeta elegida",
    "Find your videos": "Busca tus vídeos",
    "Pick a folder. This tool looks through it and every folder inside it, and lists the H.264 videos it can shrink. Nothing is changed yet.":
        "Elige una carpeta. El programa la recorre junto con todas sus subcarpetas y muestra los vídeos H.264 que puede reducir. Todavía no se cambia nada.",
    "Next: see the saving  →": "Siguiente: ver el ahorro  →",
    "Reading your videos…": "Leyendo tus vídeos…",
    "File": "Archivo",
    "Folder": "Carpeta",
    "Size": "Tamaño",
    "Picture": "Imagen",
    "Length": "Duración",
    "State": "Estado",
    "Ready": "Listo",
    "Already has a conversion": "Ya tiene una conversión",
    "GoPro low-res preview, off by default": "Vista previa GoPro de baja resolución, desmarcada por defecto",
    "Already {codec}, skipped": "Ya en {codec}, omitido",
    "(converted by this tool)": "(convertido por este programa)",
    "{n} could not be read and were skipped: {names}.": "{n} no se pudieron leer y se omitieron: {names}.",
    "No H.264 videos found in this folder or its subfolders.": "No se encontraron vídeos H.264 en esta carpeta ni en sus subcarpetas.",
    "Delete GoPro LRV files?": "¿Eliminar los archivos LRV de GoPro?",
    "An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera and its phone app can show quick previews. You don't need it if you have the original video, which is beside each of these.":
        "Un archivo LRV es una copia pequeña de baja resolución que una GoPro graba junto a cada vídeo, para que la cámara y su aplicación móvil muestren vistas previas rápidas. No lo necesitas si tienes el vídeo original, que está junto a cada uno de ellos.",
    "Done": "Hecho",
    "Left in place:": "Se quedan donde están:",
    "Left as they are:": "Se quedan como están:",

    # --- See the saving
    "See the saving before anything converts": "Mira el ahorro antes de convertir nada",
    "This makes short test encodes from a few of your own files and measures them. Your files are only read, and nothing appears in your folders.":
        "Esto hace codificaciones de prueba breves con algunos de tus archivos y las mide. Tus archivos solo se leen y no aparece nada en tus carpetas.",
    "Run the test encodes": "Hacer las codificaciones de prueba",
    "Not measured yet": "Aún sin medir",
    "Click \"Run the test encodes\" to measure how much space you would save.":
        "Haz clic en «Hacer las codificaciones de prueba» para medir cuánto espacio ahorrarías.",
    "Measuring…": "Midiendo…",
    "Encoding samples of your files and comparing them with the originals.":
        "Codificando fragmentos de tus archivos y comparándolos con los originales.",
    "Could not measure": "No se pudo medir",
    "The test encode stopped: {error}": "La codificación de prueba se detuvo: {error}",
    "About {size} saved ({pct}%)": "Unos {size} ahorrados ({pct} %)",
    "Likely between {low} and {high}, out of {total}.": "Probablemente entre {low} y {high}, de {total}.",
    "Converting everything should take {time}.": "Convertirlo todo debería llevar {time}.",
    "Sample from": "Fragmento de",
    "At": "En",
    "Original": "Original",
    "VMAF average": "VMAF medio",
    "VMAF worst 1%": "VMAF peor 1 %",
    "Meets the quality target?": "¿Cumple el objetivo de calidad?",
    "Yes": "Sí",
    "⚠ No, would get a warning": "⚠ No, tendría un aviso",
    "Start converting  →": "Empezar a convertir  →",
    "Expected time: {time}. Your computer will not go to sleep while this runs.":
        "Tiempo previsto: {time}. Tu ordenador no entrará en suspensión mientras tanto.",
    "The target: VMAF average at least {mean}, worst 1% of frames at least {p1}. Every full file is measured again after conversion.":
        "El objetivo: VMAF medio de al menos {mean} y al menos {p1} en el peor 1 % de los fotogramas. Cada archivo completo se vuelve a medir después de la conversión.",
    "{codec}. Change this in Settings.": "{codec}. Puedes cambiarlo en Ajustes.",
    "{codec}, at most {size}. Change this in Settings.": "{codec}, como máximo {size}. Puedes cambiarlo en Ajustes.",

    # --- Convert
    "Files Processed": "Archivos procesados",
    "Space Saved": "Espacio ahorrado",
    "Current Batch": "Lote actual",
    "Time Remaining": "Tiempo restante",
    "Pause": "Pausa",
    "Resume": "Reanudar",
    "Paused": "En pausa",
    "Calculating…": "Calculando…",
    "Overall Progress": "Progreso total",
    "Overall Progress: {pct}% ({done} of {total} files)": "Progreso total: {pct} % ({done} de {total} archivos)",
    "Current File": "Archivo actual",
    "Current File: {name}: {stage}": "Archivo actual: {name}: {stage}",
    "Current File: none, the batch is finished": "Archivo actual: ninguno, el lote ha terminado",
    "All": "Todos",
    "Completed": "Terminados",
    "Active": "En curso",
    "Waiting": "En espera",
    "Before": "Antes",
    "After": "Después",
    "% Saved": "% ahorrado",
    "Worst 1%": "Peor 1 %",
    "Encoding": "Codificación",
    "Next: compare and clean up  →": "Siguiente: comparar y limpiar  →",
    "Finding the right quality": "Buscando la calidad adecuada",
    "Measuring every frame": "Midiendo cada fotograma",
    "Finding quality": "Buscando calidad",
    "Measuring": "Midiendo",
    "Finished: {n} verified": "Terminado: {n} verificados",
    ", ⚠ {n} below target": ", ⚠ {n} bajo el objetivo",
    ", {n} kept as original": ", {n} conservados como original",
    "(see next page)": "(ver la página siguiente)",
    "Nothing left to convert: every selected file is already finished.":
        "No queda nada por convertir: todos los archivos seleccionados ya están terminados.",
    "The batch stopped": "El lote se detuvo",
    "Files already verified are safe. Reopen the app to continue.":
        "Los archivos ya verificados están a salvo. Vuelve a abrir la aplicación para continuar.",
    "Continue where you left off?": "¿Seguir donde lo dejaste?",
    "Each conversion is saved beside its original with {suffix} added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Cada conversión se guarda junto a su original, con {suffix} añadido al nombre. Los originales solo se leen. Puedes pausar cuando quieras y, si el PC se bloquea, basta con volver a abrir la aplicación.",
    "Each conversion is saved beside its original with {suffix} ({shrunk} if it was shrunk) added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Cada conversión se guarda junto a su original, con {suffix} ({shrunk} si se redujo) añadido al nombre. Los originales solo se leen. Puedes pausar cuando quieras y, si el PC se bloquea, basta con volver a abrir la aplicación.",
    "Stop converting?": "¿Detener la conversión?",
    "The batch is still running. If you close now, the current file is restarted next time and finished files are kept. Close anyway?":
        "El lote sigue en marcha. Si cierras ahora, el archivo actual se empezará de nuevo la próxima vez y los archivos terminados se conservan. ¿Cerrar de todos modos?",

    # --- Statuses
    "Working…": "Trabajando…",
    "Verified": "Verificado",
    "⚠ Below target": "⚠ Bajo el objetivo",
    "Resized": "Redimensionado",
    "Verified at {mean} / {p1}": "Verificado a {mean} / {p1}",
    "Resized at {mean} / {p1}": "Redimensionado a {mean} / {p1}",
    "Original kept": "Original conservado",
    "Failed, original kept": "Error, original conservado",
    "Original in Recycle Bin": "Original en la Papelera",
    "Done, has the original's name": "Hecho, tiene el nombre del original",
    "processor": "procesador",

    # --- Compare and clean up
    "Play any original beside its conversion, in sync. When you are happy, you can send originals to the Recycle Bin. This step is optional. Click a column title to sort.":
        "Reproduce cualquier original junto a su conversión, sincronizados. Cuando estés conforme, puedes enviar los originales a la Papelera de reciclaje. Este paso es opcional. Haz clic en el título de una columna para ordenar.",
    "Select All": "Marcar todo",
    "Deselect All": "Desmarcar todo",
    "Select Recommended": "Marcar recomendados",
    "Deselect Recommended": "Desmarcar recomendados",
    "Recommended means the conversion met the quality target, with no warning sign.":
        "Recomendado significa que la conversión cumplió el objetivo de calidad, sin aviso.",
    "Tip: Ctrl+click a row to tick it, Shift+click to tick a range, Ctrl+A to tick all. Right-click a row to open its folder.":
        "Consejo: Ctrl+clic marca una fila, Mayús+clic marca un rango, Ctrl+A marca todo. Clic derecho en una fila para abrir su carpeta.",
    "Delete?": "¿Eliminar?",
    "Result": "Resultado",
    "▶  Play selected side by side": "▶  Reproducir la selección lado a lado",
    "Remove the added tags from names": "Quitar las etiquetas añadidas a los nombres",
    "Send ticked originals to Recycle Bin…": "Enviar los originales marcados a la Papelera…",
    "Tick originals above to delete them": "Marca originales arriba para eliminarlos",
    "Needs your attention": "Requiere tu atención",
    "Needs your attention ({n})": "Requiere tu atención ({n})",
    "Needs your attention: nothing": "Requiere tu atención: nada",
    "Every conversion passed.": "Todas las conversiones han superado la prueba.",
    "Nothing converted yet.": "Aún no se ha convertido nada.",
    "{size} can be saved once originals are removed": "Se pueden ahorrar {size} cuando se eliminen los originales",
    "Available after an original has been sent to the Recycle Bin.": "Disponible cuando un original se haya enviado a la Papelera.",
    "Start Over": "Empezar de nuevo",
    "Forget these files and go back to step 1. Your videos and reports aren't touched.":
        "Olvidar estos archivos y volver al paso 1. Tus vídeos e informes no se tocan.",
    "Open file location": "Abrir ubicación del archivo",
    "Pick a video": "Elige un vídeo",
    "Click a row in the list first.": "Primero haz clic en una fila de la lista.",
    "Cannot compare": "No se puede comparar",
    "This row needs both an original and a verified conversion on disk.":
        "Esta fila necesita un original y una conversión verificada en el disco.",
    "Re-checking and removing": "Volviendo a comprobar y eliminando",
    "Renaming": "Renombrando",
    "finishing": "terminando",
    "{action} {i} of {total}: {name}": "{action} {i} de {total}: {name}",
    "Remove the added tags from names?": "¿Quitar las etiquetas añadidas a los nombres?",
    "Only the name changes. If you later restore an original from the Recycle Bin, Windows will ask what to do about the same name.":
        "Solo cambia el nombre. Si más adelante restauras un original desde la Papelera, Windows te preguntará qué hacer con el nombre repetido.",
    "Send originals to the Recycle Bin?": "¿Enviar los originales a la Papelera de reciclaje?",
    "I understand. Send these originals to the Recycle Bin.": "Lo entiendo. Enviar estos originales a la Papelera de reciclaje.",
    "Send to Recycle Bin": "Enviar a la Papelera",
    "Keep them": "Conservarlos",
    "Below the quality target. Compare it with the original before removing the original.":
        "Bajo el objetivo de calidad. Compáralo con el original antes de eliminar el original.",

    # --- Player
    "Side by side: {name}": "Lado a lado: {name}",
    "Original (H.264)": "Original (H.264)",
    "Original (H.264), shrunk to match": "Original (H.264), reducido para coincidir",
    "Conversion ({codec})": "Conversión ({codec})",
    "Play": "Reproducir",
    "◀ Frame": "◀ Fotograma",
    "Frame ▶": "Fotograma ▶",
    "Whole picture": "Imagen completa",
    "Drag the picture to look around": "Arrastra la imagen para recorrerla",
    "VMAF average {mean}, worst 1% {p1}": "VMAF medio {mean}, peor 1 % {p1}",
    "Could not play": "No se pudo reproducir",
    "Player": "Reproductor",

    # --- Settings
    "Language": "Idioma",
    "The default settings suit most people, so you can leave this page alone. Change something only if you have a reason.":
        "Los ajustes por defecto sirven para la mayoría, así que puedes dejar esta página como está. Cambia algo solo si tienes un motivo.",
    "Encode with": "Codificar con",
    "Graphics card (fast, recommended)": "Tarjeta gráfica (rápida, recomendada)",
    "Processor (slow, works on any PC)": "Procesador (lento, funciona en cualquier PC)",
    "Graphics card (fast, recommended) ({card} detected)": "Tarjeta gráfica (rápida, recomendada) ({card} detectada)",
    "Graphics card ({card} can't make this format)": "Tarjeta gráfica ({card} no puede crear este formato)",
    "Graphics card (no compatible graphics card detected)": "Tarjeta gráfica (no se detectó ninguna tarjeta gráfica compatible)",
    "NVIDIA card": "tarjeta NVIDIA",
    "In use: your graphics card, making {codec} video.": "En uso: tu tarjeta gráfica, creando vídeo {codec}.",
    "In use: your processor, making {codec} video.": "En uso: tu procesador, creando vídeo {codec}.",
    "{card} was found, but it can't make {codec} video, so the processor is used.":
        "Se encontró {card}, pero no puede crear vídeo {codec}, así que se usa el procesador.",
    "No compatible graphics card was found (only NVIDIA is supported), so the processor is used.":
        "No se encontró ninguna tarjeta gráfica compatible (solo se admite NVIDIA), así que se usa el procesador.",
    "Video format": "Formato de vídeo",
    "H.265 (recommended)": "H.265 (recomendado)",
    "AV1 files are usually smaller, but they play on fewer devices. Check that your TV or phone can play one first.":
        "Los archivos AV1 suelen ser más pequeños, pero se reproducen en menos dispositivos. Comprueba primero que tu televisor o tu teléfono puede reproducirlos.",
    "Largest size": "Tamaño máximo",
    "Keep the original resolution (recommended)": "Mantener la resolución original (recomendado)",
    "This permanently lowers the detail in the conversions, and videos are never enlarged. They are checked against a smaller copy of the original and labelled Resized. Keep the originals if you might want the full detail later.":
        "Esto reduce para siempre el detalle de las conversiones, y los vídeos nunca se amplían. Se comparan con una copia reducida del original y se marcan como Redimensionado. Conserva los originales si más adelante podrías querer todo el detalle.",
    "Show an Encoding column": "Mostrar una columna Codificación",
    "Format, quality setting, resolution and bitrate of each conversion.":
        "Formato, ajuste de calidad, resolución y tasa de bits de cada conversión.",
    "Show the Welcome screen when the app opens": "Mostrar la pantalla de bienvenida al abrir la aplicación",
    "Advanced": "Avanzado",
    "Only change these if you know what you are doing: they can lower the quality of your videos.":
        "Cambia estos valores solo si sabes lo que haces: pueden reducir la calidad de tus vídeos.",
    "Read what each one does": "Leer qué hace cada uno",
    "I've read this and understand what I'm doing": "Lo he leído y entiendo lo que hago",
    "Warn below": "Avisar por debajo de",
    "Also aim for these values when choosing quality": "Buscar también estos valores al elegir la calidad",
    "Ticked, lower values make smaller files with lower quality, and higher values make larger files. Not ticked, your files stay the same and only the warning moves.":
        "Si está marcado, los valores más bajos dan archivos más pequeños y de menor calidad, y los más altos, archivos más grandes. Si no, tus archivos no cambian y solo se mueve el aviso.",
    "Don't keep a conversion below a minimum": "No conservar una conversión por debajo de un mínimo",
    "Below the minimum, nothing is kept and your original stays. Off by default, so every result that is smaller and matches is kept, with a warning if needed.":
        "Por debajo del mínimo no se conserva nada y tu original se queda. Desactivado por defecto, así que se conserva todo resultado más pequeño y correcto, con un aviso si hace falta.",
    "Back to the defaults": "Volver a los valores por defecto",
    "Your target is {mean}.": "Tu objetivo es {mean}.",
    "How close this video looks to the original, from 0 to 100. VMAF is a score made by Netflix, based on how people see video. At 95 or above, most people can't see a difference.":
        "Cuánto se parece este vídeo al original, de 0 a 100. VMAF es una puntuación creada por Netflix, basada en cómo percibe la gente el vídeo. A partir de 95, la mayoría no ve ninguna diferencia.",
    "The score of the worst moments: 1% of the video's frames score lower than this. It catches a short bad patch that a good average would hide. The target is {p1} or above.":
        "La puntuación de los peores momentos: el 1 % de los fotogramas del vídeo puntúa por debajo. Detecta un tramo malo y corto que una buena media ocultaría. El objetivo es {p1} o más.",

    # --- Welcome
    "Welcome to {app}": "Bienvenido a {app}",
    "Shrink your videos, keep the quality.": "Reduce tus vídeos, conserva la calidad.",
    "Zero guesswork": "Sin conjeturas",
    "No bitrates or codecs to configure. ClipShrink automatically finds the right compression balance for every video.":
        "Sin tasas de bits ni códecs que configurar. ClipShrink encuentra automáticamente el equilibrio de compresión adecuado para cada vídeo.",
    "Measured frame-by-frame": "Medido fotograma a fotograma",
    "Every result is scored against the original using Netflix's VMAF visual quality metric, and any clip that misses the target is clearly flagged.":
        "Cada resultado se puntúa frente al original con VMAF, la métrica de calidad visual de Netflix, y cualquier vídeo que no alcance el objetivo se señala claramente.",
    "You stay in control": "Tú tienes el control",
    "Conversions are saved as new files alongside your originals. Compare both versions side by side before deciding what to send to the Recycle Bin.":
        "Las conversiones se guardan como archivos nuevos junto a tus originales. Compara ambas versiones lado a lado antes de decidir qué enviar a la Papelera de reciclaje.",
    "Don't show this again": "No volver a mostrar",

    # --- About
    "About {app}": "Acerca de {app}",
    "{app} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion against its original with VMAF and warns you about any below the quality target. Your originals are only read during conversion, and nothing is sent anywhere.":
        "{app} reduce vídeos H.264 a H.265 o AV1 para liberar espacio en disco. Mide cada conversión frente a su original con VMAF y te avisa de las que queden bajo el objetivo de calidad. Tus originales solo se leen durante la conversión, y no se envía nada a ningún sitio.",
    "Documentation:": "Documentación:",
    "Open in your browser": "Abrir en el navegador",
    "Copy the link": "Copiar el enlace",
    "Project:": "Proyecto:",
    "Reports:": "Informes:",
    "Each batch leaves a CSV report here. They're only for your information. Once a batch is finished and you exit or click Start Over, the app forgets those files.":
        "Cada lote deja aquí un informe CSV, solo a título informativo. Cuando un lote termina y sales o haces clic en Empezar de nuevo, la aplicación olvida esos archivos.",
    "Licence:": "Licencia:",
    "GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace.":
        "GPL-3.0. Se ofrece sin garantía, así que guarda una copia de seguridad de las grabaciones que no puedas reemplazar.",
    "Built with:": "Hecho con:",
    "FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in THIRD_PARTY_NOTICES.md in the install folder and on the project page.":
        "FFmpeg, x265, SVT-AV1, VMAF, mpv y Qt. Sus licencias y los enlaces a su código fuente están en THIRD_PARTY_NOTICES.md, en la carpeta de instalación y en la página del proyecto.",
    "What does \"no quality loss\" mean?": "¿Qué significa «sin pérdida de calidad»?",
    "Truly lossless H.265, where every pixel stays identical, usually makes files larger than the originals, so it would cost you space instead of saving it. This tool uses a measured definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure from Netflix of how a video looks to people, scored from 0 to 100. A conversion counts as recommended if the average score is at least 95 and the worst 1% of frames score at least 90, a level where differences are very hard to see. This is the quality target.\n\n"
    "If a file misses the target even at the best setting, it is still converted, and it gets a warning sign so you can decide for yourself. Use Select Recommended to leave those files out when cleaning up. If the result is not smaller, your original is simply kept and the file is listed in the report. Sound, any GoPro telemetry and capture dates are copied unchanged, and originals are never touched during conversion.\n\n"
    "If you choose a smaller resolution in Settings, the conversion is compared with a smaller copy of the original at the same size. So the score shows how clean the encoding is, not the detail lost by shrinking, and those files are labelled Resized rather than Verified.\n\n"
    "The advanced part of Settings can change these numbers. Files judged by other numbers show them in their label.":
        "Un H.265 realmente sin pérdidas, en el que cada píxel queda idéntico, suele dar archivos más grandes que los originales: te costaría espacio en lugar de ahorrarlo. Por eso este programa usa una definición medida.\n\n"
        "Después de cada conversión compara cada fotograma con el original mediante VMAF, una medida abierta de Netflix de cómo se ve un vídeo para las personas, con una puntuación de 0 a 100. Una conversión se considera recomendada si la puntuación media es de al menos 95 y el peor 1 % de los fotogramas obtiene al menos 90, un nivel en el que las diferencias son muy difíciles de ver. Ese es el objetivo de calidad.\n\n"
        "Si un archivo no alcanza el objetivo ni con el mejor ajuste, se convierte igualmente y recibe un signo de aviso para que decidas tú. Usa Marcar recomendados para dejar fuera esos archivos al limpiar. Si el resultado no es más pequeño, tu original simplemente se conserva y el archivo aparece en el informe. El sonido, la telemetría GoPro si la hay y las fechas de grabación se copian sin cambios, y los originales nunca se tocan durante la conversión.\n\n"
        "Si eliges una resolución menor en Ajustes, la conversión se compara con una copia reducida del original al mismo tamaño. Así la puntuación muestra lo limpia que es la codificación, no el detalle perdido al reducir, y esos archivos se marcan como Redimensionado en lugar de Verificado.\n\n"
        "La parte avanzada de Ajustes puede cambiar estas cifras. Los archivos juzgados con otras cifras las muestran en su etiqueta.",

    # --- Sizes and times
    "bytes": "bytes",
    "KB": "KB",
    "MB": "MB",
    "GB": "GB",
    "TB": "TB",
    "~{m}m left": "~{m} min restantes",
    "~{h}h {m}m left": "~{h} h {m} min restantes",
    "under a minute": "menos de un minuto",
    "about {h} h {m} min": "unas {h} h {m} min",
    "about {d} days": "unos {d} días",

    # --- Reasons
    "Could not convert, original kept: {error}": "No se pudo convertir, original conservado: {error}",
    "This is {codec}, not H.264, so it was left alone.": "Este archivo es {codec}, no H.264, así que no se ha tocado.",
    "the encoder stopped: {detail}": "el codificador se detuvo: {detail}",
    "the encoder failed: {detail}": "el codificador falló: {detail}",
    "could not write the file: {detail}": "no se pudo escribir el archivo: {detail}",
    "could not read a sample from the file: {detail}": "no se pudo leer un fragmento del archivo: {detail}",
    "the VMAF comparison could not run: {detail}": "no se pudo hacer la comparación VMAF: {detail}",
    "the VMAF comparison returned no frames": "la comparación VMAF no devolvió fotogramas",
    "the original changed while it was being converted": "el original cambió mientras se convertía",
    "Conversion is not smaller ({out} vs {src} bytes), original kept.": "La conversión no es más pequeña ({out} frente a {src} bytes), original conservado.",
    "Conversion did not match the original, original kept: {problems}": "La conversión no coincidía con el original, original conservado: {problems}",
    "video is {codec}": "el vídeo es {codec}",
    "resolution differs": "la resolución es distinta",
    "pixel format differs ({out} vs {src})": "el formato de píxel es distinto ({out} frente a {src})",
    "colour range differs": "el rango de color es distinto",
    "audio tracks differ": "las pistas de audio son distintas",
    "duration differs ({out}s vs {src}s)": "la duración es distinta ({out} s frente a {src} s)",
    "frame count differs ({out} vs {src})": "el número de fotogramas es distinto ({out} frente a {src})",
    "audio or telemetry tracks changed": "han cambiado pistas de audio o de telemetría",
    "camera info changed": "ha cambiado la información de la cámara",
    "VMAF compared {frames} frames out of {total}, original kept.": "VMAF comparó {frames} de {total} fotogramas, original conservado.",
    "VMAF short of what the search aims for.": "VMAF por debajo de lo que busca la búsqueda.",
    "VMAF below your minimum: average {mean} (minimum {min_mean}), worst 1% {p1} (minimum {min_p1}). Nothing was kept, and your original is untouched.":
        "VMAF por debajo de tu mínimo: media {mean} (mínimo {min_mean}), peor 1 % {p1} (mínimo {min_p1}). No se conservó nada y tu original está intacto.",
    "VMAF below the target: average {mean} (target {warn_mean}), worst 1% {p1} (target {warn_p1}). Compare it before removing the original.":
        "VMAF bajo el objetivo: media {mean} (objetivo {warn_mean}), peor 1 % {p1} (objetivo {warn_p1}). Compáralo antes de eliminar el original.",
    "this file was never converted by this tool": "este archivo nunca fue convertido por este programa",
    "its original has not been sent to the Recycle Bin": "su original no se ha enviado a la Papelera",
    "the converted file is missing": "falta el archivo convertido",
    "it already has the original's name": "ya tiene el nombre del original",
    "the converted file has changed since it was verified": "el archivo convertido ha cambiado desde que se verificó",
    "another file already has that name": "otro archivo ya tiene ese nombre",
    "renaming was not confirmed": "no se confirmó el cambio de nombre",
    "Windows refused the rename: {error}": "Windows rechazó el cambio de nombre: {error}",
    "it is not an LRV file": "no es un archivo LRV",
    "its full video is not beside it": "su vídeo completo no está al lado",
    "Windows did not move it to the Recycle Bin, so it was left in place": "Windows no lo movió a la Papelera, así que se quedó donde estaba",
    "its conversion is not verified (status: {status})": "su conversión no está verificada (estado: {status})",
    "the original has changed since it was verified": "el original ha cambiado desde que se verificó",
    "the converted file's content does not match what was verified": "el contenido del archivo convertido no coincide con lo verificado",
    "the converted file cannot be read: {error}": "no se puede leer el archivo convertido: {error}",
    "the converted file is not H.265 or AV1": "el archivo convertido no es H.265 ni AV1",
    "deletion was not confirmed": "no se confirmó la eliminación",
    "its conversion is below the default quality target, and that was not confirmed": "su conversión está bajo el objetivo de calidad por defecto, y eso no se confirmó",
    "its conversion has a lower resolution, and that was not confirmed": "su conversión tiene una resolución menor, y eso no se confirmó",

    # --- Report columns
    "Date": "Fecha",
    "Reason": "Motivo",
    "Before (bytes)": "Antes (bytes)",
    "After (bytes)": "Después (bytes)",
    "Saved %": "% ahorrado",
    "Encoder": "Codificador",
    "Quality setting": "Ajuste de calidad",
    "Conversion": "Conversión",
    "Codec": "Códec",
    "Output resolution": "Resolución de salida",
    "Output bitrate (Mbit/s)": "Tasa de bits de salida (Mbit/s)",
    "Target average": "Objetivo medio",
    "Target worst 1%": "Objetivo peor 1 %",
}

PLURALS = {
    "Found {n} GoPro LRV file ({size}).": ("Se encontró {n} archivo LRV de GoPro ({size}).", "Se encontraron {n} archivos LRV de GoPro ({size})."),
    "Measured on {n} file using your graphics card.": ("Medido en {n} archivo con tu tarjeta gráfica.", "Medido en {n} archivos con tu tarjeta gráfica."),
    "Measured on {n} file using your processor.": ("Medido en {n} archivo con tu procesador.", "Medido en {n} archivos con tu procesador."),
    "Remove the added tags from {n} name…": ("Quitar las etiquetas añadidas de {n} nombre…", "Quitar las etiquetas añadidas de {n} nombres…"),
    "Send it to the Recycle Bin?": ("¿Enviarlo a la Papelera de reciclaje?", "¿Enviarlos a la Papelera de reciclaje?"),
    "Send {n} ticked original to Recycle Bin…": ("Enviar {n} original marcado a la Papelera…", "Enviar {n} originales marcados a la Papelera…"),
    "about {n} minute": ("aproximadamente {n} minuto", "aproximadamente {n} minutos"),
    "{n} H.264 video, {size}.": ("{n} vídeo H.264, {size}.", "{n} vídeos H.264, {size}."),
    "{n} LRV file moved to the Recycle Bin.": ("{n} archivo LRV movido a la Papelera de reciclaje.", "{n} archivos LRV movidos a la Papelera de reciclaje."),
    "{n} conversion whose original is in the Recycle Bin will take the original's name, for example {name}.":
        ("{n} conversión cuyo original está en la Papelera tomará el nombre del original, por ejemplo {name}.",
         "{n} conversiones cuyo original está en la Papelera tomarán el nombre del original, por ejemplo {name}."),
    "{n} file renamed.": ("{n} archivo renombrado.", "{n} archivos renombrados."),
    "{n} original ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, and you can restore originals from the Recycle Bin.":
        ("{n} original ({size}) irá a la Papelera de reciclaje de Windows. Cada conversión se vuelve a comprobar antes, y puedes restaurar los originales desde la Papelera.",
         "{n} originales ({size}) irán a la Papelera de reciclaje de Windows. Cada conversión se vuelve a comprobar antes, y puedes restaurar los originales desde la Papelera."),
    "{n} original moved to the Recycle Bin.": ("{n} original movido a la Papelera de reciclaje.", "{n} originales movidos a la Papelera de reciclaje."),
    "{n} other LRV file will stay, because the original video isn't beside it.":
        ("{n} archivo LRV más se quedará, porque el vídeo original no está a su lado.",
         "{n} archivos LRV más se quedarán, porque el vídeo original no está a su lado."),
    "{n} video already in H.265, skipped.": ("{n} vídeo ya en H.265, omitido.", "{n} vídeos ya en H.265, omitidos."),
    "{n} video from your last batch is not finished. Files already verified will not be converted again. Continue now?":
        ("{n} vídeo de tu último lote no está terminado. Los archivos ya verificados no se volverán a convertir. ¿Continuar ahora?",
         "{n} vídeos de tu último lote no están terminados. Los archivos ya verificados no se volverán a convertir. ¿Continuar ahora?"),
    "{n} video in another format, skipped.": ("{n} vídeo en otro formato, omitido.", "{n} vídeos en otro formato, omitidos."),
    "{n} video, {size}.": ("{n} vídeo, {size}.", "{n} vídeos, {size}."),
    "⚠ {n} of these has a conversion at a lower resolution. Once the original is gone from the Recycle Bin, that detail is gone for good.":
        ("⚠ {n} de ellos tiene una conversión con menor resolución. Cuando el original salga de la Papelera, ese detalle se perderá para siempre.",
         "⚠ {n} de ellos tienen una conversión con menor resolución. Cuando el original salga de la Papelera, ese detalle se perderá para siempre."),
    "⚠ {n} of these has a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). Once the original is gone from the Recycle Bin, that lost quality can't be recovered.":
        ("⚠ {n} de ellos tiene una conversión por debajo de la calidad recomendada (VMAF medio {mean}, peor 1 % {p1}). Cuando el original salga de la Papelera, esa calidad perdida no se podrá recuperar.",
         "⚠ {n} de ellos tienen una conversión por debajo de la calidad recomendada (VMAF medio {mean}, peor 1 % {p1}). Cuando el original salga de la Papelera, esa calidad perdida no se podrá recuperar."),
}
