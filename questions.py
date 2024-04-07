import random

trivia_questions = [
    ("The Great Wall of China is visible from space.", False),
    ("The Pacific Ocean is the largest ocean on Earth.", True),
    ("The Statue of Liberty was a gift from France to the United States.", True),
    ("The currency of Japan is the yuan.", False),
    ("The Nile River is the longest river in the world.", True),
    ("The capital of Canada is Montreal.", False),
    ("Mount Everest is the tallest mountain in the world.", True),
    ("The human body has four lungs.", False),
    ("The Earth orbits around the Moon.", False),
    ("Mozart was born in Germany.", False),
    ("Penguins are capable of flight.", False),
    ("The Mona Lisa was painted by Vincent van Gogh.", False),
    ("The first moon landing took place in 1969.", True),
    ("Australia is both a country and a continent.", True),
    ("The Eiffel Tower is taller than the Empire State Building.", False),
    ("Diamonds are made of compressed coal.", False),
    ("The Arctic Circle is located in the Northern Hemisphere.", True),
    ("The capital of Brazil is Rio de Janeiro.", False),
    ("Sharks are mammals.", False),
    ("The Amazon Rainforest is located primarily in Brazil.", True),
    ("The human brain stops developing after the age of 25.", False),
    ("Africa is the largest continent by land area.", True),
    ("The capital of Italy is Milan.", False),
    ("A decagon has ten sides.", True),
    ("J.K. Rowling is the author of the 'Twilight' book series.", False),
    ("The Celsius scale is used to measure temperature in the United States.", False),
    ("The primary ingredient in guacamole is avocado.", True),
    ("Marie Curie discovered the element radium.", True),
    ("The speed of light is approximately 300,000 kilometers per second.", True),
    ("The human body has more than 200 bones.", True),
    ("The 'Big Bang Theory' is a scientific explanation for the origin of the universe.", True),
    ("The capital of Spain is Barcelona.", False),
    ("The longest river in Europe is the Danube.", False),
    ("The Great Barrier Reef is located off the coast of Australia.", True),
    ("Canada has two official languages: English and French.", True),
    ("The Earth's inner core is composed of liquid iron.", False),
    ("The chemical symbol for water is H2O.", True),
    ("Leonardo da Vinci painted the Sistine Chapel ceiling.", False),
    ("The Sahara Desert is the largest hot desert in the world.", True),
    ("The capital of South Africa is Cape Town.", False),
    ("Venus is the hottest planet in the solar system.", True),
    ("The human body has more than 500 muscles.", False),
    ("Neil Armstrong was the first human to walk on the moon.", True),
    ("Canada has a Prime Minister, not a President.", True),
    ("The Amazon River is the longest river in South America.", True),
    ("Bees communicate with each other by dancing.", True),
    ("The speed of sound is faster in water than in air.", True),
    ("DNA stands for 'Deoxyribonucleic Acid'.", True),
    ("The North Pole is located on a continent.", False),
    ("Thomas Edison invented the light bulb.", True)
]


class bcolors:
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Additional colors
    ORANGE = '\033[38;5;202m'  # Orange
    PINK = '\033[38;5;213m'  # Pink
    PURPLE = '\033[38;5;141m'  # Purple
    TEAL = '\033[38;5;44m'  # Teal
    LIME = '\033[38;5;118m'  # Lime
    MAROON = '\033[38;5;52m'  # Maroon
    NAVY = '\033[38;5;17m'  # Navy
    OLIVE = '\033[38;5;58m'  # Olive
    GRAY = '\033[38;5;246m'  # Gray
    BROWN = '\033[38;5;94m'  # Brown

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Bright background colors
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'

    # Random color
    # Random color
    @staticmethod
    def random_color():
        colors = [
            bcolors.BLACK, bcolors.GREEN, bcolors.YELLOW,
            bcolors.BLUE, bcolors.MAGENTA, bcolors.CYAN, bcolors.WHITE,
            bcolors.BRIGHT_BLACK, bcolors.BRIGHT_RED, bcolors.BRIGHT_GREEN,
            bcolors.BRIGHT_YELLOW, bcolors.BRIGHT_BLUE, bcolors.BRIGHT_MAGENTA,
            bcolors.BRIGHT_CYAN, bcolors.BRIGHT_WHITE,
            bcolors.ORANGE, bcolors.PINK, bcolors.PURPLE, bcolors.TEAL,
            bcolors.LIME, bcolors.MAROON, bcolors.NAVY, bcolors.OLIVE,
            bcolors.GRAY, bcolors.BROWN
        ]
        return random.choice(colors)

    # Reset
    END = '\033[0m'
