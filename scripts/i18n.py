# -*- coding: utf-8 -*-
"""Teksty interfejsu strony Eve w 4 językach. Klucz kategorii bloga = nazwa polska (front matter)."""
LANGS = ['pl', 'en', 'es', 'pt']
HTML_LANG = {'pl': 'pl', 'en': 'en', 'es': 'es', 'pt': 'pt-BR'}
OG_LOCALE = {'pl': 'pl_PL', 'en': 'en_US', 'es': 'es_ES', 'pt': 'pt_BR'}
LANG_LABEL = {'pl': 'PL', 'en': 'EN', 'es': 'ES', 'pt': 'PT'}
LANG_NAME = {'pl': 'Polski', 'en': 'English', 'es': 'Español', 'pt': 'Português'}

CATEGORIES = {
    'Filmy':       {'pl': 'Filmy', 'en': 'Film', 'es': 'Cine', 'pt': 'Filmes'},
    'Gry':         {'pl': 'Gry', 'en': 'Games', 'es': 'Videojuegos', 'pt': 'Games'},
    'Książki':     {'pl': 'Książki', 'en': 'Books', 'es': 'Libros', 'pt': 'Livros'},
    'Komiksy':     {'pl': 'Komiksy', 'en': 'Comics', 'es': 'Cómics', 'pt': 'Quadrinhos'},
    'Alternatywa': {'pl': 'Alternatywa', 'en': 'Alt culture', 'es': 'Alternativa', 'pt': 'Alternativa'},
    'Popkultura':  {'pl': 'Popkultura', 'en': 'Pop culture', 'es': 'Cultura pop', 'pt': 'Cultura pop'},
}

MONTHS = {
    'pl': ['stycznia','lutego','marca','kwietnia','maja','czerwca','lipca','sierpnia','września','października','listopada','grudnia'],
    'en': ['January','February','March','April','May','June','July','August','September','October','November','December'],
    'es': ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'],
    'pt': ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'],
}
def fmt_date(d, lang):
    m = MONTHS[lang][d.month - 1]
    if lang == 'pl': return f'{d.day} {m} {d.year}'
    if lang == 'en': return f'{m} {d.day}, {d.year}'
    return f'{d.day} de {m} de {d.year}'

# Galeria: (plik, podpis) — kolejność = układ rozkładówki
GALLERY = ['portret','barista','londyn','biblioteka','park','gracz','usmiech','okulary','calus','spojrzenie','nie-nie','gest']
GAL_CAP = {
 'pl': ['Portret',"Baristka z Eve's Café",'Deszczowy Londyn','W bibliotece','Jesień w parku','Wieczór z grami','Uśmiech','Znad okularów','Spojrzenie','Szelmowski uśmiech','Gotycki styl','Nie, nie, nie'],
 'en': ['Portrait',"Barista at Eve's Café",'Rainy London','In the library','Autumn in the park','Game night','Smile','Over the sunglasses','The look','Mischievous smile','Gothic style','No, no, no'],
 'es': ['Retrato',"Barista en Eve's Café",'Londres bajo la lluvia','En la biblioteca','Otoño en el parque','Noche de juegos','Sonrisa','Por encima de las gafas','La mirada','Sonrisa pícara','Estilo gótico','No, no, no'],
 'pt': ['Retrato',"Barista no Eve's Café",'Londres chuvosa','Na biblioteca','Outono no parque','Noite de games','Sorriso','Por cima dos óculos','O olhar','Sorriso travesso','Estilo gótico','Não, não, não'],
}
VIDEOS = ['kiss', 'flirt', 'leave']

T = {
'pl': dict(
  title='Eve — gotycka bohaterka multiwersum gier',
  desc='Eve — wirtualna, wygenerowana przez AI gotycka bohaterka darmowych gier z multiwersum Eve. Galeria, filmiki, gry i blog.',
  nav=['O Eve','Galeria','Filmiki','Gry','Blog'], menu='Menu', langs_label='Język',
  kicker='Multiwersum Eve · Wydanie specjalne',
  deck='Gotycka bohaterka darmowych gier. Elegancja w czerni, spojrzenie spod grzywki i świat, do którego wchodzisz jednym kliknięciem.',
  cta_play='Zagraj teraz', cta_gallery='Sesja zdjęciowa', issue='Numer', season='Jesień 2026',
  cover_alt='Eve w płaszczu z parasolem na deszczowej londyńskiej ulicy',
  about_h='O Eve',
  about='Eve to <strong>wirtualna bohaterka gier</strong> — dorosła, gotycka postać wygenerowana przez AI. Nie jest prawdziwą osobą. Jest twarzą <strong>multiwersum Eve</strong>: serii darmowych gier HTML5, w które zagrasz prosto w przeglądarce, bez instalowania czegokolwiek.',
  quote='„Czerń nigdy nie wychodzi z mody. Ja też nie.”',
  traits=['czarny bob','brązowe oczy i ostry eyeliner','septum i dwa kolczyki pod wargą','złote koła w uszach','czarny choker'],
  about_alt='Eve w golfie czyta książkę w bibliotece przy świecach',
  gal_h='Galeria', zoom='Powiększ', videos_h='Filmiki', frame='Kadr',
  video_titles=['Buziak na powitanie','Znad okularów','Nie, nie, nie!'],
  video_hint='Krótkie, ciche scenki z gier. Najedź lub dotknij, by odtworzyć.', novideo='Twoja przeglądarka nie obsługuje wideo.',
  games_h='Gry', available='Dostępna teraz',
  cafe_desc='Prowadź kawiarnię razem z Eve — parz kawę, obsługuj gości i rozwijaj lokal.',
  tama_title='Eve — tamagotchi',
  tama_desc='Opiekuj się Eve, rozmawiaj z nią i odkrywaj jej humory. Gra na telefon i w przeglądarce — dla wszystkich.',
  run='▶ Uruchom grę tutaj', newtab='Zagraj w nowej karcie ↗', notshowing='Gra się nie wyświetla?',
  blog_h='Blog Eve', blog_lead='Filmy, gry, książki, komiksy i alternatywa — popkultura oczami gotyckiej bohaterki.',
  read_more='Czytaj dalej', all_posts='Wszystkie wpisy', back_blog='← Wszystkie wpisy', back_home='← Strona główna',
  blog_title='Blog Eve — popkultura oczami gotyckiej bohaterki', rss='Kanał RSS', no_posts='Pierwszy wpis już wkrótce.',
  ai_note='Eve jest fikcyjną postacią wygenerowaną przez AI, a wpisy na blogu są pisane przez AI na podstawie podanych źródeł.',
  foot='Eve jest fikcyjną postacią wygenerowaną przez AI. Wszelkie podobieństwo do prawdziwych osób jest przypadkowe.',
  variants='Warianty projektu', sources='Źródła',
),
'en': dict(
  title='Eve — the gothic heroine of a game multiverse',
  desc='Eve is a virtual, AI-generated gothic heroine of the free Eve multiverse games. Gallery, clips, games and blog.',
  nav=['About Eve','Gallery','Clips','Games','Blog'], menu='Menu', langs_label='Language',
  kicker='The Eve Multiverse · Special edition',
  deck='The gothic heroine of free browser games. Elegance in black, a glance from under the fringe, and a world you enter with a single click.',
  cta_play='Play now', cta_gallery='Photo shoot', issue='Issue', season='Autumn 2026',
  cover_alt='Eve in a coat with an umbrella on a rainy London street',
  about_h='About Eve',
  about='Eve is a <strong>virtual game heroine</strong> — an adult, AI-generated gothic character. She is not a real person. She is the face of the <strong>Eve multiverse</strong>: a series of free HTML5 games you can play right in your browser, with nothing to install.',
  quote='“Black never goes out of style. Neither do I.”',
  traits=['black bob','brown eyes and sharp eyeliner','septum and two piercings below the lip','gold hoop earrings','black choker'],
  about_alt='Eve in a turtleneck reading a book in a candlelit library',
  gal_h='Gallery', zoom='Enlarge', videos_h='Clips', frame='Frame',
  video_titles=['A hello kiss','Over the sunglasses','No, no, no!'],
  video_hint='Short, silent scenes from the games. Hover or tap to play.', novideo='Your browser does not support video.',
  games_h='Games', available='Available now',
  cafe_desc='Run a café with Eve — brew coffee, serve guests and grow the place.',
  tama_title='Eve — tamagotchi',
  tama_desc='Look after Eve, talk to her and discover her moods. A game for your phone and browser — for everyone.',
  run='▶ Start the game here', newtab='Play in a new tab ↗', notshowing='Game not showing?',
  blog_h='Eve’s Blog', blog_lead='Films, games, books, comics and alt culture — pop culture through the eyes of a gothic heroine.',
  read_more='Read more', all_posts='All posts', back_blog='← All posts', back_home='← Home',
  blog_title='Eve’s Blog — pop culture through gothic eyes', rss='RSS feed', no_posts='The first post is coming soon.',
  ai_note='Eve is a fictional, AI-generated character, and the blog posts are written by AI based on the sources listed.',
  foot='Eve is a fictional, AI-generated character. Any resemblance to real people is coincidental.',
  variants='Design variants', sources='Sources',
),
'es': dict(
  title='Eve — la heroína gótica de un multiverso de juegos',
  desc='Eve es una heroína gótica virtual generada por IA, protagonista de los juegos gratuitos del multiverso Eve. Galería, vídeos, juegos y blog.',
  nav=['Sobre Eve','Galería','Vídeos','Juegos','Blog'], menu='Menú', langs_label='Idioma',
  kicker='Multiverso Eve · Edición especial',
  deck='La heroína gótica de juegos gratuitos para el navegador. Elegancia en negro, una mirada bajo el flequillo y un mundo al que entras con un solo clic.',
  cta_play='Jugar ahora', cta_gallery='Sesión de fotos', issue='Número', season='Otoño 2026',
  cover_alt='Eve con abrigo y paraguas en una calle lluviosa de Londres',
  about_h='Sobre Eve',
  about='Eve es una <strong>heroína virtual de videojuegos</strong>: un personaje gótico adulto generado por IA. No es una persona real. Es la cara del <strong>multiverso Eve</strong>, una serie de juegos HTML5 gratuitos que puedes jugar directamente en el navegador, sin instalar nada.',
  quote='«El negro nunca pasa de moda. Yo tampoco».',
  traits=['melena bob negra','ojos marrones y delineado marcado','septum y dos piercings bajo el labio','aros dorados','gargantilla negra'],
  about_alt='Eve con jersey de cuello alto leyendo un libro en una biblioteca a la luz de las velas',
  gal_h='Galería', zoom='Ampliar', videos_h='Vídeos', frame='Toma',
  video_titles=['Un beso de bienvenida','Por encima de las gafas','¡No, no, no!'],
  video_hint='Escenas breves y sin sonido de los juegos. Pasa el cursor o toca para reproducir.', novideo='Tu navegador no admite vídeo.',
  games_h='Juegos', available='Disponible ahora',
  cafe_desc='Lleva una cafetería con Eve: prepara café, atiende a los clientes y haz crecer el local.',
  tama_title='Eve — tamagotchi',
  tama_desc='Cuida de Eve, habla con ella y descubre sus estados de ánimo. Un juego para el móvil y el navegador, para todos los públicos.',
  run='▶ Iniciar el juego aquí', newtab='Jugar en una pestaña nueva ↗', notshowing='¿No se ve el juego?',
  blog_h='El blog de Eve', blog_lead='Cine, videojuegos, libros, cómics y cultura alternativa: la cultura pop vista por una heroína gótica.',
  read_more='Seguir leyendo', all_posts='Todas las entradas', back_blog='← Todas las entradas', back_home='← Inicio',
  blog_title='El blog de Eve — la cultura pop con mirada gótica', rss='Canal RSS', no_posts='La primera entrada llegará pronto.',
  ai_note='Eve es un personaje ficticio generado por IA, y las entradas del blog están escritas por IA a partir de las fuentes indicadas.',
  foot='Eve es un personaje ficticio generado por IA. Cualquier parecido con personas reales es pura coincidencia.',
  variants='Variantes de diseño', sources='Fuentes',
),
'pt': dict(
  title='Eve — a heroína gótica de um multiverso de jogos',
  desc='Eve é uma heroína gótica virtual gerada por IA, protagonista dos jogos gratuitos do multiverso Eve. Galeria, vídeos, jogos e blog.',
  nav=['Sobre a Eve','Galeria','Vídeos','Jogos','Blog'], menu='Menu', langs_label='Idioma',
  kicker='Multiverso Eve · Edição especial',
  deck='A heroína gótica de jogos gratuitos no navegador. Elegância em preto, um olhar por baixo da franja e um mundo em que você entra com um só clique.',
  cta_play='Jogar agora', cta_gallery='Ensaio de fotos', issue='Edição', season='Outono 2026',
  cover_alt='Eve de casaco e guarda-chuva numa rua chuvosa de Londres',
  about_h='Sobre a Eve',
  about='Eve é uma <strong>heroína virtual de jogos</strong> — uma personagem gótica adulta gerada por IA. Ela não é uma pessoa real. É o rosto do <strong>multiverso Eve</strong>: uma série de jogos HTML5 gratuitos que você joga direto no navegador, sem instalar nada.',
  quote='“O preto nunca sai de moda. Eu também não.”',
  traits=['chanel preto','olhos castanhos e delineado marcado','septo e dois piercings abaixo do lábio','argolas douradas','gargantilha preta'],
  about_alt='Eve de gola alta lendo um livro numa biblioteca à luz de velas',
  gal_h='Galeria', zoom='Ampliar', videos_h='Vídeos', frame='Cena',
  video_titles=['Um beijo de oi','Por cima dos óculos','Não, não, não!'],
  video_hint='Cenas curtas e sem som dos jogos. Passe o mouse ou toque para reproduzir.', novideo='Seu navegador não suporta vídeo.',
  games_h='Jogos', available='Disponível agora',
  cafe_desc='Administre um café com a Eve — prepare cafés, atenda os clientes e faça o lugar crescer.',
  tama_title='Eve — tamagotchi',
  tama_desc='Cuide da Eve, converse com ela e descubra os humores dela. Um jogo para celular e navegador — para todas as idades.',
  run='▶ Iniciar o jogo aqui', newtab='Jogar em uma nova aba ↗', notshowing='O jogo não aparece?',
  blog_h='Blog da Eve', blog_lead='Filmes, games, livros, quadrinhos e cultura alternativa — a cultura pop pelos olhos de uma heroína gótica.',
  read_more='Continuar lendo', all_posts='Todos os posts', back_blog='← Todos os posts', back_home='← Início',
  blog_title='Blog da Eve — cultura pop com olhar gótico', rss='Feed RSS', no_posts='O primeiro post chega em breve.',
  ai_note='Eve é uma personagem fictícia gerada por IA, e os posts do blog são escritos por IA com base nas fontes indicadas.',
  foot='Eve é uma personagem fictícia gerada por IA. Qualquer semelhança com pessoas reais é mera coincidência.',
  variants='Variantes de design', sources='Fontes',
),
}
