"""Português (do Brasil). Not yet checked by a native speaker: corrections are welcome on GitHub."""

MESSAGES = {
    # --- Steps, pages and buttons
    "Find videos": "Encontrar vídeos",
    "See the saving": "Ver a economia",
    "Convert": "Converter",
    "Compare and clean up": "Comparar e limpar",
    "Settings": "Configurações",
    "{app} {version}: shrink videos, keep the quality": "{app} {version}: reduza seus vídeos, mantenha a qualidade",
    "←  Back": "←  Voltar",
    "Choose folder…": "Escolher pasta…",
    "Choose the folder with your videos": "Escolha a pasta com seus vídeos",
    "No folder chosen": "Nenhuma pasta escolhida",
    "Find your videos": "Encontre seus vídeos",
    "Pick a folder. This tool looks through it and every folder inside it, and lists the H.264 videos it can shrink. Nothing is changed yet.":
        "Escolha uma pasta. O programa a percorre junto com todas as subpastas e lista os vídeos H.264 que pode reduzir. Nada é alterado ainda.",
    "Next: see the saving  →": "Próximo: ver a economia  →",
    "Reading your videos…": "Lendo seus vídeos…",
    "File": "Arquivo",
    "Folder": "Pasta",
    "Size": "Tamanho",
    "Picture": "Imagem",
    "Length": "Duração",
    "State": "Estado",
    "Ready": "Pronto",
    "Already has a conversion": "Já tem uma conversão",
    "GoPro low-res preview, off by default": "Prévia GoPro em baixa resolução, desmarcada por padrão",
    "Already {codec}, skipped": "Já em {codec}, ignorado",
    "(converted by this tool)": "(convertido por este programa)",
    "{n} could not be read and were skipped: {names}.": "{n} não puderam ser lidos e foram ignorados: {names}.",
    "No H.264 videos found in this folder or its subfolders.": "Nenhum vídeo H.264 encontrado nesta pasta ou nas subpastas.",
    "Delete GoPro LRV files?": "Excluir os arquivos LRV da GoPro?",
    "An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera and its phone app can show quick previews. You don't need it if you have the original video, which is beside each of these.":
        "Um arquivo LRV é uma pequena cópia em baixa resolução que a GoPro grava ao lado de cada vídeo, para que a câmera e o aplicativo do celular mostrem prévias rápidas. Você não precisa dele se tiver o vídeo original, que está ao lado de cada um deles.",
    "Done": "Concluído",
    "Left in place:": "Ficaram onde estavam:",
    "Left as they are:": "Ficaram como estavam:",

    # --- See the saving
    "See the saving before anything converts": "Veja a economia antes de converter qualquer coisa",
    "This makes short test encodes from a few of your own files and measures them. Your files are only read, and nothing appears in your folders.":
        "São feitas codificações de teste curtas com alguns dos seus arquivos, que depois são medidas. Seus arquivos são apenas lidos, e nada aparece nas suas pastas.",
    "Run the test encodes": "Fazer as codificações de teste",
    "Not measured yet": "Ainda não medido",
    "Click \"Run the test encodes\" to measure how much space you would save.":
        "Clique em \"Fazer as codificações de teste\" para medir quanto espaço você economizaria.",
    "Measuring…": "Medindo…",
    "Encoding samples of your files and comparing them with the originals.":
        "Codificando trechos dos seus arquivos e comparando com os originais.",
    "Could not measure": "Não foi possível medir",
    "The test encode stopped: {error}": "A codificação de teste parou: {error}",
    "About {size} saved ({pct}%)": "Cerca de {size} economizados ({pct}%)",
    "Likely between {low} and {high}, out of {total}.": "Provavelmente entre {low} e {high}, de {total}.",
    "Converting everything should take {time}.": "Converter tudo deve levar {time}.",
    "Sample from": "Trecho de",
    "At": "Em",
    "Original": "Original",
    "VMAF average": "VMAF médio",
    "VMAF worst 1%": "VMAF pior 1%",
    "Meets the quality target?": "Atinge a meta de qualidade?",
    "Yes": "Sim",
    "⚠ No, would get a warning": "⚠ Não, receberia um aviso",
    "Start converting  →": "Começar a converter  →",
    "Expected time: {time}. Your computer will not go to sleep while this runs.":
        "Tempo previsto: {time}. Seu computador não vai entrar em suspensão enquanto isso.",
    "The target: VMAF average at least {mean}, worst 1% of frames at least {p1}. Every full file is measured again after conversion.":
        "A meta: VMAF médio de pelo menos {mean} e pelo menos {p1} no pior 1% dos quadros. Cada arquivo completo é medido de novo após a conversão.",
    "{codec}. Change this in Settings.": "{codec}. Altere isso em Configurações.",
    "{codec}, at most {size}. Change this in Settings.": "{codec}, no máximo {size}. Altere isso em Configurações.",

    # --- Convert
    "Files Processed": "Arquivos processados",
    "Space Saved": "Espaço economizado",
    "Current Batch": "Lote atual",
    "Time Remaining": "Tempo restante",
    "Pause": "Pausar",
    "Resume": "Retomar",
    "Paused": "Pausado",
    "Calculating…": "Calculando…",
    "Overall Progress": "Progresso geral",
    "Overall Progress: {pct}% ({done} of {total} files)": "Progresso geral: {pct}% ({done} de {total} arquivos)",
    "Current File": "Arquivo atual",
    "Current File: {name}: {stage}": "Arquivo atual: {name}: {stage}",
    "Current File: none, the batch is finished": "Arquivo atual: nenhum, o lote terminou",
    "All": "Todos",
    "Completed": "Concluídos",
    "Active": "Em andamento",
    "Waiting": "Aguardando",
    "Before": "Antes",
    "After": "Depois",
    "% Saved": "% economizado",
    "Worst 1%": "Pior 1%",
    "Encoding": "Codificação",
    "Next: compare and clean up  →": "Próximo: comparar e limpar  →",
    "Finding the right quality": "Procurando a qualidade certa",
    "Measuring every frame": "Medindo cada quadro",
    "Finding quality": "Procurando qualidade",
    "Measuring": "Medindo",
    "Finished: {n} verified": "Concluído: {n} verificados",
    ", ⚠ {n} below target": ", ⚠ {n} abaixo da meta",
    ", {n} kept as original": ", {n} mantidos como original",
    "(see next page)": "(veja a próxima página)",
    "Nothing left to convert: every selected file is already finished.":
        "Não há mais nada para converter: todos os arquivos selecionados já estão concluídos.",
    "The batch stopped": "O lote parou",
    "Files already verified are safe. Reopen the app to continue.":
        "Os arquivos já verificados estão seguros. Abra o aplicativo de novo para continuar.",
    "Continue where you left off?": "Continuar de onde parou?",
    "Each conversion is saved beside its original with {suffix} added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Cada conversão é salva ao lado do original, com {suffix} acrescentado ao nome. Os originais são apenas lidos. Você pode pausar a qualquer momento e, se o PC travar, basta abrir o aplicativo de novo.",
    "Each conversion is saved beside its original with {suffix} ({shrunk} if it was shrunk) added to the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen this app.":
        "Cada conversão é salva ao lado do original, com {suffix} ({shrunk} se foi reduzida) acrescentado ao nome. Os originais são apenas lidos. Você pode pausar a qualquer momento e, se o PC travar, basta abrir o aplicativo de novo.",
    "Stop converting?": "Parar a conversão?",
    "The batch is still running. If you close now, the current file is restarted next time and finished files are kept. Close anyway?":
        "O lote ainda está em andamento. Se você fechar agora, o arquivo atual recomeça da próxima vez e os arquivos concluídos são mantidos. Fechar mesmo assim?",

    # --- Statuses
    "Working…": "Trabalhando…",
    "Verified": "Verificado",
    "⚠ Below target": "⚠ Abaixo da meta",
    "Resized": "Redimensionado",
    "Verified at {mean} / {p1}": "Verificado em {mean} / {p1}",
    "Resized at {mean} / {p1}": "Redimensionado em {mean} / {p1}",
    "Original kept": "Original mantido",
    "Failed, original kept": "Falhou, original mantido",
    "Original in Recycle Bin": "Original na Lixeira",
    "Done, has the original's name": "Concluído, tem o nome do original",
    "processor": "processador",

    # --- Compare and clean up
    "Play any original beside its conversion, in sync. When you are happy, you can send originals to the Recycle Bin. This step is optional. Click a column title to sort.":
        "Reproduza qualquer original ao lado da conversão, em sincronia. Quando estiver satisfeito, você pode enviar os originais para a Lixeira. Esta etapa é opcional. Clique no título de uma coluna para ordenar.",
    "Select All": "Marcar tudo",
    "Deselect All": "Desmarcar tudo",
    "Select Recommended": "Marcar recomendados",
    "Deselect Recommended": "Desmarcar recomendados",
    "Recommended means the conversion met the quality target, with no warning sign.":
        "Recomendado significa que a conversão atingiu a meta de qualidade, sem aviso.",
    "Tip: Ctrl+click a row to tick it, Shift+click to tick a range, Ctrl+A to tick all. Right-click a row to open its folder.":
        "Dica: Ctrl+clique marca uma linha, Shift+clique marca um intervalo, Ctrl+A marca tudo. Clique com o botão direito numa linha para abrir a pasta.",
    "Delete?": "Excluir?",
    "Result": "Resultado",
    "▶  Play selected side by side": "▶  Reproduzir a seleção lado a lado",
    "Remove the added tags from names": "Remover as etiquetas acrescentadas aos nomes",
    "Send ticked originals to Recycle Bin…": "Enviar os originais marcados para a Lixeira…",
    "Tick originals above to delete them": "Marque originais acima para excluí-los",
    "Needs your attention": "Precisa da sua atenção",
    "Needs your attention ({n})": "Precisa da sua atenção ({n})",
    "Needs your attention: nothing": "Precisa da sua atenção: nada",
    "Every conversion passed.": "Todas as conversões foram aprovadas.",
    "Nothing converted yet.": "Nada foi convertido ainda.",
    "{size} can be saved once originals are removed": "{size} podem ser economizados quando os originais forem removidos",
    "Available after an original has been sent to the Recycle Bin.": "Disponível depois que um original for enviado para a Lixeira.",
    "Start Over": "Recomeçar",
    "Forget these files and go back to step 1. Your videos and reports aren't touched.":
        "Esquecer estes arquivos e voltar à etapa 1. Seus vídeos e relatórios não são tocados.",
    "Open file location": "Abrir local do arquivo",
    "Pick a video": "Escolha um vídeo",
    "Click a row in the list first.": "Primeiro clique numa linha da lista.",
    "Cannot compare": "Não é possível comparar",
    "This row needs both an original and a verified conversion on disk.":
        "Esta linha precisa de um original e de uma conversão verificada no disco.",
    "Re-checking and removing": "Verificando de novo e removendo",
    "Renaming": "Renomeando",
    "finishing": "finalizando",
    "{action} {i} of {total}: {name}": "{action} {i} de {total}: {name}",
    "Remove the added tags from names?": "Remover as etiquetas acrescentadas aos nomes?",
    "Only the name changes. If you later restore an original from the Recycle Bin, Windows will ask what to do about the same name.":
        "Só o nome muda. Se depois você restaurar um original da Lixeira, o Windows vai perguntar o que fazer com o nome igual.",
    "Send originals to the Recycle Bin?": "Enviar os originais para a Lixeira?",
    "I understand. Send these originals to the Recycle Bin.": "Entendi. Enviar estes originais para a Lixeira.",
    "Send to Recycle Bin": "Enviar para a Lixeira",
    "Keep them": "Mantê-los",
    "Below the quality target. Compare it with the original before removing the original.":
        "Abaixo da meta de qualidade. Compare com o original antes de remover o original.",

    # --- Player
    "Side by side: {name}": "Lado a lado: {name}",
    "Original (H.264)": "Original (H.264)",
    "Original (H.264), shrunk to match": "Original (H.264), reduzido para combinar",
    "Conversion ({codec})": "Conversão ({codec})",
    "Play": "Reproduzir",
    "◀ Frame": "◀ Quadro",
    "Frame ▶": "Quadro ▶",
    "Whole picture": "Imagem inteira",
    "Drag the picture to look around": "Arraste a imagem para explorá-la",
    "VMAF average {mean}, worst 1% {p1}": "VMAF médio {mean}, pior 1% {p1}",
    "Could not play": "Não foi possível reproduzir",
    "Player": "Player",

    # --- Settings
    "Language": "Idioma",
    "The default settings suit most people, so you can leave this page alone. Change something only if you have a reason.":
        "As configurações padrão servem para a maioria das pessoas, então você pode deixar esta página como está. Só mude algo se tiver um motivo.",
    "Encode with": "Codificar com",
    "Graphics card (fast, recommended)": "Placa de vídeo (rápida, recomendada)",
    "Processor (slow, works on any PC)": "Processador (lento, funciona em qualquer PC)",
    "Graphics card (fast, recommended) ({card} detected)": "Placa de vídeo (rápida, recomendada) ({card} detectada)",
    "Graphics card ({card} can't make this format)": "Placa de vídeo ({card} não consegue criar este formato)",
    "Graphics card (no compatible graphics card detected)": "Placa de vídeo (nenhuma placa de vídeo compatível detectada)",
    "NVIDIA card": "placa NVIDIA",
    "In use: your graphics card, making {codec} video.": "Em uso: sua placa de vídeo, criando vídeo {codec}.",
    "In use: your processor, making {codec} video.": "Em uso: seu processador, criando vídeo {codec}.",
    "{card} was found, but it can't make {codec} video, so the processor is used.":
        "{card} foi encontrada, mas não consegue criar vídeo {codec}, então o processador é usado.",
    "No compatible graphics card was found (only NVIDIA is supported), so the processor is used.":
        "Nenhuma placa de vídeo compatível foi encontrada (só NVIDIA é suportada), então o processador é usado.",
    "Video format": "Formato de vídeo",
    "H.265 (recommended)": "H.265 (recomendado)",
    "AV1 files are usually smaller, but they play on fewer devices. Check that your TV or phone can play one first.":
        "Arquivos AV1 costumam ser menores, mas tocam em menos aparelhos. Confira antes se sua TV ou seu celular consegue reproduzi-los.",
    "Largest size": "Tamanho máximo",
    "Keep the original resolution (recommended)": "Manter a resolução original (recomendado)",
    "This permanently lowers the detail in the conversions, and videos are never enlarged. They are checked against a smaller copy of the original and labelled Resized. Keep the originals if you might want the full detail later.":
        "Isso reduz para sempre o detalhe das conversões, e os vídeos nunca são ampliados. Eles são comparados com uma cópia reduzida do original e marcados como Redimensionado. Guarde os originais se você puder querer todo o detalhe depois.",
    "Show an Encoding column": "Mostrar uma coluna Codificação",
    "Format, quality setting, resolution and bitrate of each conversion.":
        "Formato, ajuste de qualidade, resolução e taxa de bits de cada conversão.",
    "Show the Welcome screen when the app opens": "Mostrar a tela de boas-vindas ao abrir o aplicativo",
    "Advanced": "Avançado",
    "Only change these if you know what you are doing: they can lower the quality of your videos.":
        "Só mude estes valores se souber o que está fazendo: eles podem reduzir a qualidade dos seus vídeos.",
    "Read what each one does": "Leia o que cada um faz",
    "I've read this and understand what I'm doing": "Li isto e entendo o que estou fazendo",
    "Warn below": "Avisar abaixo de",
    "Also aim for these values when choosing quality": "Buscar também estes valores ao escolher a qualidade",
    "Ticked, lower values make smaller files with lower quality, and higher values make larger files. Not ticked, your files stay the same and only the warning moves.":
        "Marcado, valores mais baixos geram arquivos menores com qualidade mais baixa, e valores mais altos geram arquivos maiores. Desmarcado, seus arquivos continuam iguais e só o aviso muda.",
    "Don't keep a conversion below a minimum": "Não manter uma conversão abaixo de um mínimo",
    "Below the minimum, nothing is kept and your original stays. Off by default, so every result that is smaller and matches is kept, with a warning if needed.":
        "Abaixo do mínimo, nada é mantido e seu original fica. Desligado por padrão, então todo resultado menor e correto é mantido, com um aviso se necessário.",
    "Back to the defaults": "Voltar ao padrão",
    "Your target is {mean}.": "Sua meta é {mean}.",
    "How close this video looks to the original, from 0 to 100. VMAF is a score made by Netflix, based on how people see video. At 95 or above, most people can't see a difference.":
        "O quanto este vídeo se parece com o original, de 0 a 100. VMAF é uma pontuação criada pela Netflix, baseada em como as pessoas veem vídeo. A partir de 95, a maioria das pessoas não vê diferença.",
    "The score of the worst moments: 1% of the video's frames score lower than this. It catches a short bad patch that a good average would hide. The target is {p1} or above.":
        "A pontuação dos piores momentos: 1% dos quadros do vídeo pontua abaixo disso. Ela revela um trecho ruim e curto que uma boa média esconderia. A meta é {p1} ou mais.",

    # --- Welcome
    "Welcome to {app}": "Bem-vindo ao {app}",
    "Shrink your videos, keep the quality.": "Reduza seus vídeos, mantenha a qualidade.",
    "Zero guesswork": "Sem adivinhação",
    "No bitrates or codecs to configure. ClipShrink automatically finds the right compression balance for every video.":
        "Nenhuma taxa de bits ou codec para configurar. O ClipShrink encontra automaticamente o equilíbrio de compressão certo para cada vídeo.",
    "Measured frame-by-frame": "Medido quadro a quadro",
    "Every result is scored against the original using Netflix's VMAF visual quality metric, and any clip that misses the target is clearly flagged.":
        "Cada resultado é pontuado em relação ao original com o VMAF, a métrica de qualidade visual da Netflix, e todo vídeo que não atinge a meta é sinalizado com clareza.",
    "You stay in control": "Você continua no controle",
    "Conversions are saved as new files alongside your originals. Compare both versions side by side before deciding what to send to the Recycle Bin.":
        "As conversões são salvas como arquivos novos ao lado dos seus originais. Compare as duas versões lado a lado antes de decidir o que enviar para a Lixeira.",
    "Don't show this again": "Não mostrar de novo",

    # --- About
    "About {app}": "Sobre o {app}",
    "{app} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion against its original with VMAF and warns you about any below the quality target. Your originals are only read during conversion, and nothing is sent anywhere.":
        "O {app} reduz vídeos H.264 para H.265 ou AV1 para liberar espaço em disco. Ele mede cada conversão em relação ao original com o VMAF e avisa você sobre qualquer uma abaixo da meta de qualidade. Seus originais são apenas lidos durante a conversão, e nada é enviado para lugar nenhum.",
    "Documentation:": "Documentação:",
    "Open in your browser": "Abrir no navegador",
    "Copy the link": "Copiar o link",
    "Project:": "Projeto:",
    "Reports:": "Relatórios:",
    "Each batch leaves a CSV report here. They're only for your information. Once a batch is finished and you exit or click Start Over, the app forgets those files.":
        "Cada lote deixa aqui um relatório CSV, apenas para sua informação. Quando um lote termina e você sai ou clica em Recomeçar, o aplicativo esquece esses arquivos.",
    "Licence:": "Licença:",
    "GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace.":
        "GPL-3.0. Vem sem garantia, então guarde um backup das gravações que você não conseguiria substituir.",
    "Built with:": "Feito com:",
    "FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in THIRD_PARTY_NOTICES.md in the install folder and on the project page.":
        "FFmpeg, x265, SVT-AV1, VMAF, mpv e Qt. As licenças e os links para o código-fonte estão em THIRD_PARTY_NOTICES.md, na pasta de instalação e na página do projeto.",
    "What does \"no quality loss\" mean?": "O que significa \"sem perda de qualidade\"?",
    "Truly lossless H.265, where every pixel stays identical, usually makes files larger than the originals, so it would cost you space instead of saving it. This tool uses a measured definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure from Netflix of how a video looks to people, scored from 0 to 100. A conversion counts as recommended if the average score is at least 95 and the worst 1% of frames score at least 90, a level where differences are very hard to see. This is the quality target.\n\n"
    "If a file misses the target even at the best setting, it is still converted, and it gets a warning sign so you can decide for yourself. Use Select Recommended to leave those files out when cleaning up. If the result is not smaller, your original is simply kept and the file is listed in the report. Sound, any GoPro telemetry and capture dates are copied unchanged, and originals are never touched during conversion.\n\n"
    "If you choose a smaller resolution in Settings, the conversion is compared with a smaller copy of the original at the same size. So the score shows how clean the encoding is, not the detail lost by shrinking, and those files are labelled Resized rather than Verified.\n\n"
    "The advanced part of Settings can change these numbers. Files judged by other numbers show them in their label.":
        "Um H.265 realmente sem perdas, em que cada pixel fica idêntico, costuma gerar arquivos maiores que os originais: você perderia espaço em vez de economizar. Por isso este programa usa uma definição medida.\n\n"
        "Depois de cada conversão, ele compara cada quadro com o original usando o VMAF, uma medida aberta da Netflix de como um vídeo parece para as pessoas, com pontuação de 0 a 100. Uma conversão é considerada recomendada se a pontuação média for de pelo menos 95 e o pior 1% dos quadros tiver pelo menos 90, um nível em que as diferenças são muito difíceis de ver. Essa é a meta de qualidade.\n\n"
        "Se um arquivo não atingir a meta nem com o melhor ajuste, ele é convertido mesmo assim e recebe um sinal de aviso, para você decidir. Use Marcar recomendados para deixar esses arquivos de fora na limpeza. Se o resultado não for menor, seu original é simplesmente mantido e o arquivo aparece no relatório. O som, a telemetria GoPro se houver e as datas de gravação são copiados sem alterações, e os originais nunca são tocados durante a conversão.\n\n"
        "Se você escolher uma resolução menor em Configurações, a conversão é comparada com uma cópia reduzida do original no mesmo tamanho. Assim a pontuação mostra o quanto a codificação está limpa, não o detalhe perdido na redução, e esses arquivos são marcados como Redimensionado em vez de Verificado.\n\n"
        "A parte avançada das Configurações pode mudar esses números. Os arquivos avaliados por outros números os mostram no rótulo.",

    # --- Sizes and times
    "bytes": "bytes",
    "KB": "KB",
    "MB": "MB",
    "GB": "GB",
    "TB": "TB",
    "~{m}m left": "~{m} min restantes",
    "~{h}h {m}m left": "~{h} h {m} min restantes",
    "under a minute": "menos de um minuto",
    "about {h} h {m} min": "cerca de {h} h {m} min",
    "about {d} days": "cerca de {d} dias",

    # --- Reasons
    "Could not convert, original kept: {error}": "Não foi possível converter, original mantido: {error}",
    "This is {codec}, not H.264, so it was left alone.": "Este arquivo é {codec}, não H.264, então não foi tocado.",
    "the encoder stopped: {detail}": "o codificador parou: {detail}",
    "the encoder failed: {detail}": "o codificador falhou: {detail}",
    "could not write the file: {detail}": "não foi possível gravar o arquivo: {detail}",
    "could not read a sample from the file: {detail}": "não foi possível ler um trecho do arquivo: {detail}",
    "the VMAF comparison could not run: {detail}": "não foi possível fazer a comparação VMAF: {detail}",
    "the VMAF comparison returned no frames": "a comparação VMAF não retornou quadros",
    "the original changed while it was being converted": "o original mudou durante a conversão",
    "Conversion is not smaller ({out} vs {src} bytes), original kept.": "A conversão não é menor ({out} contra {src} bytes), original mantido.",
    "Conversion did not match the original, original kept: {problems}": "A conversão não correspondia ao original, original mantido: {problems}",
    "video is {codec}": "o vídeo é {codec}",
    "resolution differs": "a resolução é diferente",
    "pixel format differs ({out} vs {src})": "o formato de pixel é diferente ({out} contra {src})",
    "colour range differs": "a faixa de cores é diferente",
    "audio tracks differ": "as faixas de áudio são diferentes",
    "duration differs ({out}s vs {src}s)": "a duração é diferente ({out} s contra {src} s)",
    "frame count differs ({out} vs {src})": "o número de quadros é diferente ({out} contra {src})",
    "audio or telemetry tracks changed": "faixas de áudio ou de telemetria mudaram",
    "camera info changed": "as informações da câmera mudaram",
    "VMAF compared {frames} frames out of {total}, original kept.": "O VMAF comparou {frames} de {total} quadros, original mantido.",
    "VMAF short of what the search aims for.": "VMAF abaixo do que a busca procura.",
    "VMAF below your minimum: average {mean} (minimum {min_mean}), worst 1% {p1} (minimum {min_p1}). Nothing was kept, and your original is untouched.":
        "VMAF abaixo do seu mínimo: média {mean} (mínimo {min_mean}), pior 1% {p1} (mínimo {min_p1}). Nada foi mantido, e seu original está intacto.",
    "VMAF below the target: average {mean} (target {warn_mean}), worst 1% {p1} (target {warn_p1}). Compare it before removing the original.":
        "VMAF abaixo da meta: média {mean} (meta {warn_mean}), pior 1% {p1} (meta {warn_p1}). Compare antes de remover o original.",
    "this file was never converted by this tool": "este arquivo nunca foi convertido por este programa",
    "its original has not been sent to the Recycle Bin": "o original dele não foi enviado para a Lixeira",
    "the converted file is missing": "o arquivo convertido está faltando",
    "it already has the original's name": "ele já tem o nome do original",
    "the converted file has changed since it was verified": "o arquivo convertido mudou desde a verificação",
    "another file already has that name": "outro arquivo já tem esse nome",
    "renaming was not confirmed": "a renomeação não foi confirmada",
    "Windows refused the rename: {error}": "O Windows recusou a renomeação: {error}",
    "it is not an LRV file": "não é um arquivo LRV",
    "its full video is not beside it": "o vídeo completo não está ao lado",
    "Windows did not move it to the Recycle Bin, so it was left in place": "O Windows não o moveu para a Lixeira, então ele ficou onde estava",
    "its conversion is not verified (status: {status})": "a conversão dele não está verificada (estado: {status})",
    "the original has changed since it was verified": "o original mudou desde a verificação",
    "the converted file's content does not match what was verified": "o conteúdo do arquivo convertido não corresponde ao que foi verificado",
    "the converted file cannot be read: {error}": "não é possível ler o arquivo convertido: {error}",
    "the converted file is not H.265 or AV1": "o arquivo convertido não é H.265 nem AV1",
    "deletion was not confirmed": "a exclusão não foi confirmada",
    "its conversion is below the default quality target, and that was not confirmed": "a conversão dele está abaixo da meta de qualidade padrão, e isso não foi confirmado",
    "its conversion has a lower resolution, and that was not confirmed": "a conversão dele tem resolução menor, e isso não foi confirmado",

    # --- Report columns
    "Date": "Data",
    "Reason": "Motivo",
    "Before (bytes)": "Antes (bytes)",
    "After (bytes)": "Depois (bytes)",
    "Saved %": "% economizado",
    "Encoder": "Codificador",
    "Quality setting": "Ajuste de qualidade",
    "Conversion": "Conversão",
    "Codec": "Codec",
    "Output resolution": "Resolução de saída",
    "Output bitrate (Mbit/s)": "Taxa de bits de saída (Mbit/s)",
    "Target average": "Meta média",
    "Target worst 1%": "Meta pior 1%",
}

PLURALS = {
    "Found {n} GoPro LRV file ({size}).": ("{n} arquivo LRV da GoPro encontrado ({size}).", "{n} arquivos LRV da GoPro encontrados ({size})."),
    "Measured on {n} file using your graphics card.": ("Medido em {n} arquivo com sua placa de vídeo.", "Medido em {n} arquivos com sua placa de vídeo."),
    "Measured on {n} file using your processor.": ("Medido em {n} arquivo com seu processador.", "Medido em {n} arquivos com seu processador."),
    "Remove the added tags from {n} name…": ("Remover as etiquetas acrescentadas de {n} nome…", "Remover as etiquetas acrescentadas de {n} nomes…"),
    "Send it to the Recycle Bin?": ("Enviá-lo para a Lixeira?", "Enviá-los para a Lixeira?"),
    "Send {n} ticked original to Recycle Bin…": ("Enviar {n} original marcado para a Lixeira…", "Enviar {n} originais marcados para a Lixeira…"),
    "about {n} minute": ("cerca de {n} minuto", "cerca de {n} minutos"),
    "{n} H.264 video, {size}.": ("{n} vídeo H.264, {size}.", "{n} vídeos H.264, {size}."),
    "{n} LRV file moved to the Recycle Bin.": ("{n} arquivo LRV movido para a Lixeira.", "{n} arquivos LRV movidos para a Lixeira."),
    "{n} conversion whose original is in the Recycle Bin will take the original's name, for example {name}.":
        ("{n} conversão cujo original está na Lixeira vai receber o nome do original, por exemplo {name}.",
         "{n} conversões cujo original está na Lixeira vão receber o nome do original, por exemplo {name}."),
    "{n} file renamed.": ("{n} arquivo renomeado.", "{n} arquivos renomeados."),
    "{n} original ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, and you can restore originals from the Recycle Bin.":
        ("{n} original ({size}) vai para a Lixeira do Windows. Cada conversão é verificada de novo antes, e você pode restaurar os originais da Lixeira.",
         "{n} originais ({size}) vão para a Lixeira do Windows. Cada conversão é verificada de novo antes, e você pode restaurar os originais da Lixeira."),
    "{n} original moved to the Recycle Bin.": ("{n} original movido para a Lixeira.", "{n} originais movidos para a Lixeira."),
    "{n} other LRV file will stay, because the original video isn't beside it.":
        ("{n} outro arquivo LRV vai ficar, porque o vídeo original não está ao lado.",
         "{n} outros arquivos LRV vão ficar, porque o vídeo original não está ao lado."),
    "{n} video already in H.265, skipped.": ("{n} vídeo já em H.265, ignorado.", "{n} vídeos já em H.265, ignorados."),
    "{n} video from your last batch is not finished. Files already verified will not be converted again. Continue now?":
        ("{n} vídeo do seu último lote não terminou. Os arquivos já verificados não serão convertidos de novo. Continuar agora?",
         "{n} vídeos do seu último lote não terminaram. Os arquivos já verificados não serão convertidos de novo. Continuar agora?"),
    "{n} video in another format, skipped.": ("{n} vídeo em outro formato, ignorado.", "{n} vídeos em outro formato, ignorados."),
    "{n} video, {size}.": ("{n} vídeo, {size}.", "{n} vídeos, {size}."),
    "⚠ {n} of these has a conversion at a lower resolution. Once the original is gone from the Recycle Bin, that detail is gone for good.":
        ("⚠ {n} deles tem uma conversão com resolução menor. Quando o original sair da Lixeira, esse detalhe estará perdido para sempre.",
         "⚠ {n} deles têm uma conversão com resolução menor. Quando o original sair da Lixeira, esse detalhe estará perdido para sempre."),
    "⚠ {n} of these has a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). Once the original is gone from the Recycle Bin, that lost quality can't be recovered.":
        ("⚠ {n} deles tem uma conversão abaixo da qualidade recomendada (VMAF médio {mean}, pior 1% {p1}). Quando o original sair da Lixeira, essa qualidade perdida não poderá ser recuperada.",
         "⚠ {n} deles têm uma conversão abaixo da qualidade recomendada (VMAF médio {mean}, pior 1% {p1}). Quando o original sair da Lixeira, essa qualidade perdida não poderá ser recuperada."),
}
