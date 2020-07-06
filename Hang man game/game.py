import pygame, os, random, time, requests
from bs4 import BeautifulSoup

#getting random words from out sources
r = requests.get("https://www.hangmanwords.com/words")
soup = BeautifulSoup(r.text, "html.parser")
ul = soup.find("ul", {"class":"list-cols"})
lis = ul.findAll("li")
words = []
for li in lis:
    words.append(li.text)
print(words)

#intializing
pygame.init()
HEIGHT, WIDTH = 800, 500
lightgray = (101, 101, 101)
win = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Hangman game")

#Game Variables
FPS = 60
clock = pygame.time.Clock()
run = True
state = 0
word_font = pygame.font.SysFont("comicsansms", 72)
letter_font = pygame.font.SysFont("comicsansms", 36)


s_word = random.choice(words)
unknown_word = len(s_word) * "-"
letters = ["a", "b", 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', "o",
    "p", 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

right_letter = True
winner = False



#images
images = []
images_rect = []
for i in range(7):
    image = pygame.image.load(f"images\hangman{i}.png")
    images.append(image)
    image_rect = image.get_rect()
    image_rect.x = 60
    image_rect.y = 108
    images_rect.append(image_rect)



def check_in(chosen_letter):
    global unknown_word, state, right_letter
    if chosen_letter in s_word:
        letter_pos = [pos for pos, letter in enumerate(s_word) if letter == chosen_letter]
        lst = list(unknown_word)
        for pos in letter_pos:
            lst[pos] = chosen_letter
        unknown_word = "".join(lst)
        right_letter = True

    else:
        state += 1
        right_letter = False



#buttons
buttons = []
def draw_buttons():
    circle_x = 50
    row_1 = 389
    row_2 = 470
    clicked = False
    for i in range(26):
        if i <= 11:
            c = pygame.draw.circle(win, (180, 180, 180), (circle_x, row_1), 24)
            letter = letter_font.render(letters[i], True, (0, 0, 0))
            letter_rect = letter.get_rect()
            letter_rect.centerx = circle_x
            letter_rect.centery = row_1 - 5
            win.blit(letter, letter_rect)
            buttons.append(c)

        elif i == 12:
            c = pygame.draw.circle(win, (180, 180, 180), (circle_x, row_1), 24)
            letter = letter_font.render(letters[i], True, (0, 0, 0))
            letter_rect = letter.get_rect()
            letter_rect.centerx = circle_x
            letter_rect.centery = row_1 -5
            win.blit(letter, letter_rect)
            buttons.append(c)
            circle_x = -10

        else:
            c = pygame.draw.circle(win, (180, 180, 180), (circle_x, row_2), 24)
            letter = letter_font.render(letters[i], True, (0, 0, 0))
            letter_rect = letter.get_rect()
            letter_rect.centerx = circle_x
            letter_rect.centery = row_2 - 5
            win.blit(letter, letter_rect)
            buttons.append(c)
        circle_x += 60


def check_win():
    if unknown_word == s_word:
        run = False
        winner = True
        win.fill(lightgray)
        winnig_text = word_font.render("YOU  WON!!", True, (0, 255, 0))
        rect = winnig_text.get_rect()
        rect.centerx, rect.centery = WIDTH//2, HEIGHT//4
        win.blit(winnig_text, rect)
        ended()

def ended():
    global clicked, s_word, unknown_word
    clicked = False
    end = False
    while not end :
        b_again = pygame.draw.rect(win, (180, 180, 180), (int(WIDTH/2), int(HEIGHT/2), 160, 50))
        text = letter_font.render("play again", True, (0, 0, 0))
        rect = text.get_rect()
        rect.x, rect.y = int(WIDTH/2), int(HEIGHT/2)
        win.blit(text, rect)
        b_end = pygame.draw.rect(win, (180, 180, 180), (int(WIDTH/2) + 230, int(HEIGHT/2), 160, 50))
        text = letter_font.render("End", True, (0, 0, 0))
        rect = text.get_rect()
        rect.x, rect.y = int(WIDTH/2) + 230, int(HEIGHT/2)
        win.blit(text, rect)
        pos = pygame.mouse.get_pos()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if b_again.collidepoint(pos):
                    if not clicked:
                        s_word = random.choice(words)
                        unknown_word = len(s_word) * "-"
                        print("xxxxx")
                        print(s_word)
                        play()
                if b_end.collidepoint(pos):
                    if not clicked:
                        quit()

def play():
    global run, right_letter, state
    run = True
    state = 0
    win.fill(lightgray)
    draw_buttons()
    while run :
        clicked = False
        pos = pygame.mouse.get_pos()
        clock.tick(FPS)

        text = word_font.render(unknown_word, True, (0, 0, 0), lightgray)
        text_rect = text.get_rect()
        text_rect.x, text_rect.y = 431, 182
        win.blit(images[state], images_rect[state])
        win.blit(text, text_rect)

        if state == 6:
            run = False
            win.fill(lightgray)
            lose_text = word_font.render("YOU  LOST!!", True, (255, 0, 0))
            rect = lose_text.get_rect()
            rect.centerx, rect.centery = int(WIDTH/2), int(HEIGHT/4)
            win.blit(lose_text, rect)
            text = letter_font.render(f"the word was '{s_word}'.", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.centerx, text_rect.centery = int(WIDTH/2), int(HEIGHT/4) + 50
            win.blit(text, text_rect)
            ended()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                for b in buttons:
                    if b.x + b.width> pos[0] > b.x - 30 and  b.y+b.height> pos[1] > b.y - 30:
                        if not clicked:
                            clicked = True
                            chosen_letter = letters[buttons.index(b)]
                            check_in(chosen_letter)
                            pygame.draw.line(win, (0, 255, 0) if right_letter else (255, 0 ,0), (b.x, b.y), (b.x+b.width, b.y+b.height))
                            pygame.draw.line(win, (0, 255, 0) if right_letter else (255, 0 ,0), (b.x+b.width, b.y), (b.x, b.y+b.height))
                            print("clicked")

        check_win()
        pygame.display.update()

    #pygame.quit()
print(s_word)
play()
