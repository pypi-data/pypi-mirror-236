import swahilipro.swahilipro as swahilipro 
import time
def main():

    ascii_art = [
        [
            "   ____",
            " / ___|",
            "| |___ ",
            " \\___ \\",
            "  ___)|",
            " |____/"
        ],
        [
            "  _    _ ",
            " | |  | |",
            " | |  | |",
            " | |/\\| |",
            " \\  /\\  /",
            "  \\/  \\/ "
        ],
        [
            "   ____   ",
            "  / __ \\ ",
            " / / _` |",
            "| | (_| |",
            " \\ \\__,_|",
            "  \\____/ "
        ],
        [
        "_      ",
        "| |     ",
        "| |___  ",
        "|  __ | ",
        "| | | | ",
        "|_| |_| "
    ],
    [
        " _  ",
        "| | ",
        "| | ",
        "| | ",
        "| | ",
        "|_| "
    ],
    [
        " _    ",
        "| |   ",
        "| |   ",
        "| |   ",
        "| |__ ",
        "|____|"
    ],



    [
        " _  ",
        "| | ",
        "| | ",
        "| | ",
        "| | ",
        "|_| "
    ]
    ]

    def print_ascii_art(art):
        for i in range(len(art[0])):
            line = "".join([art[j][i] for j in range(len(art))])
            print(line)
            time.sleep(0.1)


    print_ascii_art(ascii_art)

    while True:
        text = input('Swahilipro > ')
        if text.strip() == "": continue
        result, error = swahilipro.run('<stdin>', text)

        if error:
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))

main()