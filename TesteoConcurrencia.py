import pygame


def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x: x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


_cached_fonts = {}


def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font


_cached_text = {}


def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image


pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False

font_preferences = ['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 'consolas', 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 'georgia', 'impact', 'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 'lucidasans', 'malgungothic', 'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 'microsoftnewtailue', 'microsoftphagspa', 'microsoftsansserif', 'microsofttaile', 'microsoftyahei', 'microsoftyaheiui', 'microsoftyibaiti', 'mingliuextb', 'pmingliuextb', 'mingliuhkscsextb', 'mongolianbaiti', 'msgothic', 'msuigothic', 'mspgothic', 'mvboli', 'myanmartext', 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype', 'segoemdl2assets', 'segoeprint', 'segoescript', 'segoeui', 'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol', 'simsun', 'nsimsun', 'simsunextb', 'sitkasmall', 'sitkatext', 'sitkasubheading', 'sitkaheading', 'sitkadisplay', 'sitkabanner', 'sylfaen', 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 'verdana', 'webdings', 'wingdings', 'yugothic', 'yugothicuisemibold', 'yugothicui', 'yugothicmedium', 'yugothicuiregular', 'yugothicregular', 'yugothicuisemilight', 'holomdl2assets', 'museofordell', 'museofordellregular', 'agencyfb', 'algerian', 'bookantiqua', 'arialrounded', 'baskervilleoldface', 'bauhaus93', 'bell', 'bernardcondensed', 'bodoni', 'bodoniblack', 'bodonicondensed', 'bodonipostercompressed', 'bookmanoldstyle', 'bradleyhanditc', 'britannic', 'berlinsansfb', 'berlinsansfbdemi', 'broadway', 'brushscript', 'bookshelfsymbol7', 'californianfb', 'calisto', 'castellar', 'centuryschoolbook', 'centaur', 'century', 'chiller', 'colonna', 'cooperblack', 'copperplategothic', 'curlz', 'dubai', 'dubaimedium', 'dubairegular', 'elephant', 'engravers', 'erasitc', 'erasdemiitc', 'erasmediumitc', 'felixtitling', 'forte', 'franklingothicbook', 'franklingothicdemi', 'franklingothicdemicond', 'franklingothicheavy', 'franklingothicmediumcond', 'freestylescript', 'frenchscript', 'footlight', 'garamond', 'gigi', 'gillsans', 'gillsanscondensed', 'gillsansultracondensed', 'gillsansultra', 'gloucesterextracondensed', 'gillsansextcondensed', 'centurygothic', 'goudyoldstyle', 'goudystout', 'harlowsolid', 'harrington', 'haettenschweiler', 'hightowertext', 'imprintshadow', 'informalroman', 'blackadderitc', 'edwardianscriptitc', 'kristenitc', 'jokerman', 'juiceitc', 'kunstlerscript', 'widelatin', 'lucidabright', 'lucidacalligraphy', 'leelawadee', 'lucidafaxregular', 'lucidafax', 'lucidahandwriting', 'lucidasansregular', 'lucidasansroman', 'lucidasanstypewriterregular', 'lucidasanstypewriter', 'lucidasanstypewriteroblique', 'magneto', 'maiandragd', 'maturascriptcapitals', 'mistral', 'modernno20', 'microsoftuighur', 'monotypecorsiva', 'extra', 'niagaraengraved', 'niagarasolid', 'ocraextended', 'oldenglishtext', 'onyx', 'msoutlook', 'palacescript', 'papyrus', 'parchment', 'perpetua', 'perpetuatitling', 'playbill', 'poorrichard', 'pristina', 'rage', 'ravie', 'msreferencesansserif', 'msreferencespecialty', 'rockwellcondensed', 'rockwell', 'rockwellextra', 'script', 'showcardgothic', 'snapitc', 'stencil', 'twcen', 'twcencondensed', 'twcencondensedextra', 'tempussansitc', 'vinerhanditc', 'vivaldi', 'vladimirscript', 'wingdings2', 'wingdings3', 'teamviewer15', 'buxtonsketch', 'segoemarker', 'sketchflowprint']



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    text = create_text("Hello, World", 'impact', 72, (0, 128, 0))
    screen.fill((255, 255, 255))
    screen.blit(text,
                (320 - text.get_width() // 2, 240 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

# 'arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 'consolas',
# 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 'georgia', 'impact',
# 'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 'lucidasans', 'malgungothic',
# 'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 'microsoftnewtailue',
# 'microsoftphagspa', 'microsoftsansserif', 'microsofttaile', 'microsoftyahei', 'microsoftyaheiui', 'microsoftyibaiti',
# 'mingliuextb', 'pmingliuextb', 'mingliuhkscsextb', 'mongolianbaiti', 'msgothic', 'msuigothic', 'mspgothic', 'mvboli',
# 'myanmartext', 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype', 'segoemdl2assets', 'segoeprint', 'segoescript',
# 'segoeui', 'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol',
# 'simsun', 'nsimsun', 'simsunextb', 'sitkasmall', 'sitkatext', 'sitkasubheading', 'sitkaheading', 'sitkadisplay', 'sitkabanner',
# 'sylfaen', 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 'verdana', 'webdings', 'wingdings', 'yugothic',
# 'yugothicuisemibold', 'yugothicui', 'yugothicmedium', 'yugothicuiregular', 'yugothicregular', 'yugothicuisemilight',
# 'holomdl2assets', 'museofordell', 'museofordellregular', 'agencyfb', 'algerian', 'bookantiqua', 'arialrounded',
# 'baskervilleoldface', 'bauhaus93', 'bell', 'bernardcondensed', 'bodoni', 'bodoniblack', 'bodonicondensed',
# 'bodonipostercompressed', 'bookmanoldstyle', 'bradleyhanditc', 'britannic', 'berlinsansfb', 'berlinsansfbdemi',
# 'broadway', 'brushscript', 'bookshelfsymbol7', 'californianfb', 'calisto', 'castellar', 'centuryschoolbook',
# 'centaur', 'century', 'chiller', 'colonna', 'cooperblack', 'copperplategothic', 'curlz', 'dubai', 'dubaimedium',
# 'dubairegular', 'elephant', 'engravers', 'erasitc', 'erasdemiitc', 'erasmediumitc', 'felixtitling', 'forte',
# 'franklingothicbook', 'franklingothicdemi', 'franklingothicdemicond', 'franklingothicheavy', 'franklingothicmediumcond',
# 'freestylescript', 'frenchscript', 'footlight', 'garamond', 'gigi', 'gillsans', 'gillsanscondensed', 'gillsansultracondensed',
# 'gillsansultra', 'gloucesterextracondensed', 'gillsansextcondensed', 'centurygothic', 'goudyoldstyle', 'goudystout',
# 'harlowsolid', 'harrington', 'haettenschweiler', 'hightowertext', 'imprintshadow', 'informalroman', 'blackadderitc',
# 'edwardianscriptitc', 'kristenitc', 'jokerman', 'juiceitc', 'kunstlerscript', 'widelatin', 'lucidabright',
# 'lucidacalligraphy', 'leelawadee', 'lucidafaxregular', 'lucidafax', 'lucidahandwriting', 'lucidasansregular',
# 'lucidasansroman', 'lucidasanstypewriterregular', 'lucidasanstypewriter', 'lucidasanstypewriteroblique',
# 'magneto', 'maiandragd', 'maturascriptcapitals', 'mistral', 'modernno20', 'microsoftuighur', 'monotypecorsiva',
# 'extra', 'niagaraengraved', 'niagarasolid', 'ocraextended', 'oldenglishtext', 'onyx', 'msoutlook', 'palacescript',
# 'papyrus', 'parchment', 'perpetua', 'perpetuatitling', 'playbill', 'poorrichard', 'pristina', 'rage', 'ravie',
# 'msreferencesansserif', 'msreferencespecialty', 'rockwellcondensed', 'rockwell', 'rockwellextra', 'script',
# 'showcardgothic', 'snapitc', 'stencil', 'twcen', 'twcencondensed', 'twcencondensedextra', 'tempussansitc',
# 'vinerhanditc', 'vivaldi', 'vladimirscript', 'wingdings2', 'wingdings3', 'teamviewer15', 'buxtonsketch',
# 'segoemarker', 'sketchflowprint']