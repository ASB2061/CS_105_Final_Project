import pygame
import time
import random
import openCVhelper2 as ocv
# we import the necessary libraries + Julian's work on openCV for the game to actually function

# keystrokes are made as variables
from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_RETURN,
    K_ESCAPE,
    QUIT,
    KEYDOWN
)

# ["blue", "red", "yellow", "orange", "green", "purple", "white", "black", "gray", "brown"] colors2 = ["dark blue",
# "light blue", "dark red"," light red", "dark yellow", "light yellow", "dark orange", "light orange", "dark green",
# "light green", "dark purple", "light purple", "white", "black", "gray"] colors_advanced = [""]

"""NOTE : Much of the code here is an incorporation of Ben's Code, so I will do my best to explain the pygame aspects, 
# but avoid talking about the logical aspects since those will be explained by Ben in his portion of the Google Colab. 
Also note that any print statements were part of the gameLogic code, but do not actually appear in the pygame window
# useful colors for filling screen. """
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
origin = (0, 0)

# starts pygame
pygame.init()

# creates the display window
screen = pygame.display.set_mode((1800, 1012))
# sets the name of the display window
pygame.display.set_caption('Color Game!')

global leaderboard
leaderboard = {}

global colors
colors = ['black', 'blue', 'brown', 'gray', 'red', 'white', 'yellow']

global bgn
bgn = ['black', 'blue', 'brown', 'gray', 'red', 'white', 'yellow']

global colors1
colors1 = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'purple', 'red', 'white', 'yellow']

global avg
avg = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'purple', 'red', 'white', 'yellow']

global totalrow
totalrow = 0

global present
present = ["black", "blue", "green", "red"]
global colors2
colors2 = ["black", "blue", "green", "red"]


def insertionsort(l):
    for i in range(len(l)):  # checks all valuesin the full length of list l
        p = i  # sets up nested loop by assigning new value to check from i -> p
        while p > 0 and l[p - 1] > l[
            p]:  # ensures the loop keeps iterating while p is not the last value in the list and the value before it is greater than it
            inter = l[p - 1]  # switches indexes in the list with the spot before
            l[p - 1] = l[p]
            l[p] = inter
            p -= 1  # iterates down to continue checking previous values
    return l


def uusername():
    """
    The function that causes all of the other functions to run. This function requests a username by displaying a photo
    of a man waiting and asking the user to input a name. Below there is a white box that can be typed into and the user
    can press enter to mmove to the next page.
    :return:
    """

    global bgn
    global avg
    global colors
    global colors1
    global running
    running = True
    colors = ['black', 'blue', 'brown', 'gray', 'red', 'white', 'yellow']
    bgn = ['black', 'blue', 'brown', 'gray', 'red', 'white', 'yellow']
    avg = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'purple', 'red', 'white', 'yellow']
    colors1 = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'purple', 'red', 'white', 'yellow']
    print(bgn)
    print(avg)
    print(colors)
    print(colors1)
    waitingPage = pygame.image.load("waitingBackground.jpg")  # this incorporates the image background into the window
    waitingPage = pygame.transform.scale(waitingPage, (1800, 1012))  # reformats the image to fit in the window
    screen.blit(waitingPage, (10, 10))  # "draws" the image onto the screen, but isn't actually updating until

    # gives a prompt to the user at the top asking to input username
    userPrompt = pygame.font.SysFont("dejavuserif", 32)
    userPrompt = userPrompt.render("Please Input Your Username", True, black)
    userPromptRect = userPrompt.get_rect()
    userPromptRect.center = (900, 250)
    screen.blit(userPrompt, userPromptRect)

    pygame.display.flip()  # this line actually updates the window so the user can see the image and the statement at
    # the top
    base_font = pygame.font.Font(None, 32)  # this is used as the font of the input for the box
    global user_name
    user_name = ''  # user_name has to be global for it to be used in leaderboards

    # create rectangle
    input_rect = pygame.Rect(850, 570, 140, 32)

    while running:
        for event in pygame.event.get():
            # if there is a key press
            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_name = user_name[:-1]
                    # if backspace is pressed, the name displayed on screen will change as if we pressed backspace
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                elif event.key == pygame.K_RETURN:
                    running = False
                # Unicode standard is used for string formation with pygame
                else:
                    user_name += event.unicode
        pygame.draw.rect(screen, white, input_rect)
        # draw rectangle and argument passed which shouldbe on screen

        text_surface = base_font.render(user_name, True, black)
        # renders the font with text, bool and color

        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        # render at position stated in arguments

        input_rect.w = max(100, text_surface.get_width() + 10)
        # set width of textfield so that text cannot get outside of user's text input

        pygame.display.flip()

    if user_name not in leaderboard:  # if the user is new
        leaderboard[user_name] = 0  # adds the user name to the leaderboard dict
        startMenu()  # launches start menu
    else:  # this piece of code is meant to add 1 if the name inputted matches a name already in the function
        namenum = user_name[-1]
        print(namenum)
        try:
            int(namenum)
            namenum = str(int(namenum) + 1)
            print(namenum)
            user_name = user_name + namenum
        except ValueError:
            user_name += str(1)
        leaderboard[user_name] = 0
        startMenu()  # launches start menu
    print(leaderboard)


def autoBegin(inarow: int):
    """

    :param inarow:  how many colors has the user gotten correct in a row
    :return:
    this function reruns the beginner difficulty after the user has beat it
    """
    b = []
    colors = ['black', 'blue', 'brown', 'gray', 'red', 'white', 'yellow']
    # b and colors are reset
    print("Starting BEGINNER difficulty!")
    randomizer(colors, b, inarow)  # randomizer is called with the reset variables


def autoBasic(inarow: int):
    """
    This function reruns the advanced or average difficulty after the user has beat it
    :param inarow: how many colors has the user gotten correct in a row
    :return:
    """
    b = []
    colors1 = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'purple', 'red', 'white', 'yellow']
    print("Beginning AVERAGE difficulty!")
    randomizer(colors1, b, inarow)


def randomizer(l: list, b: list, inarow: int):  # this will be explained by ben since there was no modification done
    # to incorporate this function with pygame
    global colors
    global bgn
    global avg
    global colors1

    if len(l) == 0:
        print("You've gotten all the colors correct on your first try at least once! Decide what happens next")
        insertionsort(b)
        return AllDone(b, inarow)
    elif len(b) > 4 and inarow == 0:
        testold = random.random()
        if len(b) >= 2 and testold > 0.60:
            n = random.randint(0, len(b) - 1)
            checkCorrect(b[n], l, b, inarow)
        else:
            n = random.randint(0, len(l) - 1)
            checkCorrect(l[n], l, b, inarow)
    else:
        testold = random.random()
        if len(b) >= 3 and testold > 0.93:
            n = random.randint(0, len(l) - 1)
            checkCorrect(b[n], l, b, inarow)
        else:
            n = random.randint(0, len(l) - 1)
            checkCorrect(l[n], l, b, inarow)


# def identifierCode -- Julian


def checkCorrect(check: str, l: list, b: list, inarow: int):
    """
    The UI's role in this function is to display strikes, what color needs to be found, how many are correct in a row,
    and when the user is right or wrong based on the color they have submitted.
    :param check:
    :param l:
    :param b:
    :param inarow:
    Again, these parameters will be explained by Ben, but the pygame aspect will display strikes, answers correct in a
    row and instruct the user on what color they need to find
    :return:
    """
    global totalrow
    global colors
    global bgn
    global avg
    global colors1
    print(len(l))
    print(len(b))
    print(len(colors))
    StrikeNum = 0
    # a bit complex with how long we run the checking software?

    while StrikeNum < 3:
        # these three if statements check what mode we are in before resetting the screen to their respective background
        # screens along with their info on strikes and answers correct in a row. This is done so that the text on the
        # screen does not write on top of itself
        if len(l) == len(colors):  # if l is equal to the list colors, then it must be the beginner background
            beginnerPageFunction()
        elif len(l) == len(colors1):  # if l is equal to the list colors1, then it must be the advanced background
            advancedPageBackground()
        elif len(l) == len(colors2):  # if l is equal to the list colors2, then it must be the demo background
            demoPageFunction()
        strikeCounting(StrikeNum)  # this displays the number of strikes on screen
        correctInARow(inarow)  # this displays the number of correct answers in a row on screen
        time.sleep(0.5)  # delays the screen before showing the object
        gameInstructions(
            f"Now Find a {check} Object and Show It to Your Computer's Camera")  # this gives a message to the user
        # about what color they need to find
        pygame.display.flip()  # updates screen
        textBlock("msgothic", 32, "Press the Spacebar twice if You are Happy with Your Image", black, (900, 275))
        # gives the user instructions on how to submit a capture from the webcam feed.
        pygame.display.flip()
        answer = ocv.color_check(check, ocv.camera(0))  # this is a boolean from the openCV that will give true or false
        # for the color requested.

        if not answer:
            inarow = 0
            StrikeNum += 1
        if check in b:
            if answer:
                # again, these three 'reset' the page temporarily to show whether the user is correct and new data based
                # on that
                if len(l) == len(colors):
                    beginnerPageFunction()
                elif len(l) == len(colors1):
                    advancedPageBackground()
                elif len(l) == len(colors2):
                    demoPageFunction()
                gameInstructions("Correct!!")  # displays that the user was correct
                correctInARow(inarow)  # displays the number of correct answers the user has in a row
                strikeCounting(StrikeNum)  # displays the number of strikes
                pygame.display.flip()
                time.sleep(1)  # delays the function for a second before returning to the while loop
                randomizer(l, b, inarow)  # recalls randomizer for a new color
                break
            elif not answer:
                if StrikeNum == 2:
                    # again, these three 'reset' the page temporarily to show whether the user is correct and new
                    # data based on that
                    if len(l) == len(colors):
                        beginnerPageFunction()
                    elif len(l) == len(colors1):
                        advancedPageBackground()
                    elif len(l) == len(colors2):
                        demoPageFunction()
                    strikeCounting(StrikeNum)  # displays strikes
                    correctInARow(inarow)  # displays number of correct answers in a row
                    gameInstructions(
                        "STRIKE 2! You've got 1 strike left. Try again")  # will display at the top that the user has
                    # 2 strikes
                    pygame.display.flip()
                    time.sleep(1)  # brief delay before returning to the top
                else:
                    # again, these three 'reset' the page temporarily to show whether the user is correct and new
                    # data based on that
                    if len(l) == len(colors):
                        beginnerPageFunction()
                    elif len(l) == len(colors1):
                        advancedPageBackground()
                    elif len(l) == len(colors2):
                        demoPageFunction()
                    strikeCounting(StrikeNum)  # display strikes
                    correctInARow(inarow)  # displays number of correct ansewrs in a row
                    gameInstructions("STRIKE " + str(StrikeNum) + "! You've got " + str(
                        (3 - StrikeNum)) + " strikes left. Try again!")  # displays number of strikes
                    pygame.display.flip()
                    time.sleep(1)

        elif answer:  # if the user is correct
            # again, these three 'reset' the page temporarily to show whether the user is correct and new
            # data based on that
            if len(l) == len(colors):
                beginnerPageFunction()
            elif len(l) == len(colors1):
                advancedPageBackground()
            elif len(l) == len(colors2):
                demoPageFunction()
            gameInstructions("YOU GOT IT! GOOD WORK")  # words of positive encouragement if the user is correct
            strikeCounting(StrikeNum)  # counts number of strikes
            if StrikeNum == 0:
                inarow = inarow + 1
                correctInARow(inarow)  # this displays the number of correct answers in a row on screen
                b.append(check)
                del l[l.index(check)]
                pygame.display.flip()  # updates screen
                randomizer(l, b, inarow)  # recalls randomizer
                break
            else:
                randomizer(l, b, inarow)
                break
        elif not answer:
            if StrikeNum == 2:
                # again, these three 'reset' the page temporarily to show whether the user is correct and new
                # data based on that
                if len(l) == len(colors):
                    beginnerPageFunction()
                elif len(l) == len(colors1):
                    advancedPageBackground()
                elif len(l) == len(colors2):
                    demoPageFunction()
                gameInstructions("STRIKE 2! You've got 1 strike left")
                correctInARow(0)  # this displays the number of correct answers in a row on screen
                pygame.display.flip()
                time.sleep(1)  # brief delay before returning to main page
            else:
                # again, these three 'reset' the page temporarily to show whether the user is correct and new
                # data based on that
                if len(l) == len(colors):
                    beginnerPageFunction()
                elif len(l) == len(colors1):
                    advancedPageBackground()
                elif len(l) == len(colors2):
                    demoPageFunction()
                gameInstructions("STRIKE " + str(StrikeNum) + "! You've got " + str((3 - StrikeNum)) + " strikes left")
                correctInARow(0)  # this displays the number of correct answers in a row on screen
                pygame.display.flip()  # updates the page
                time.sleep(1)  # brief delay before returning to main page
        if len(l) == 0:
            insertionsort(b)
            # print("You've gotten all the colors correct on your first try at least once! Now CHOOOOOSE!!!!!!!!")
            AllDone(b, inarow)
            break
    randomizer(l, b, inarow)


def AllDone(b: list, inarow: int):
    """

    :param b:
    :param inarow:
    :return:
    Once the user has gotten all of the colors in the list correct, this function is called to ask the user if they
    would like to stop, replay the same level or 'level' up or down
    """
    global totalrow
    global colors1
    global colors
    global bgn
    global avg
    colors = ['black', 'blue', 'brown', 'gray', 'red', 'white', 'yellow']
    colors1 = avg
    colors2 = ["black", "blue", "green", "red"]

    print(b)
    print(bgn)
    print(colors)

    if b == colors:
        # resets screen for option page
        screen.fill(white)
        # reuses beginnerpage background as a waiting screen
        beginnerPage = pygame.image.load("beginnerGameBackground.jpg")
        beginnerPage = pygame.transform.scale(beginnerPage, (1800, 1012))
        screen.blit(beginnerPage, origin)
        pygame.display.flip()
        time.sleep(0.5)
        # displays prompt to the user
        gameInstructions("You have completed this level! Would you like to keep going?")
        # first option
        OptionOne = pygame.font.SysFont("sawasdee", 24)
        OptionOne = OptionOne.render("Select 1 for Done", True, white)
        OptionOneRect = OptionOne.get_rect()
        OptionOneRect.center = (750, 600)
        screen.blit(OptionOne, OptionOneRect)
        # second option
        OptionTwo = pygame.font.SysFont("sawasdee", 24)
        OptionTwo = OptionTwo.render("Select 2 for Repeat", True, white)
        OptionTwoRect = OptionTwo.get_rect()
        OptionTwoRect.center = (1050, 600)
        screen.blit(OptionTwo, OptionTwoRect)
        # third option
        thirdOption = pygame.font.SysFont("sawasdee", 24)
        thirdOption = thirdOption.render("Select 3 for Level Up", True, white)
        thirdOptionRect = thirdOption.get_rect()
        thirdOptionRect.center = (750, 700)
        screen.blit(thirdOption, thirdOptionRect)
        pygame.display.flip()
        running = True

        while running:
            for event in pygame.event.get():  # loop that runs until there is a keypress of 1 2 or 3
                if event.type == pygame.KEYDOWN:  # if there is a keypress
                    if event.key == K_1:  # if one the player stops
                        running = False
                        screen.fill(black)
                        textBlock("latinmodernmonolight", 32,
                                  f"Now that you are done, your longest winning streak was {totalrow}!", white,
                                  (900, 270))
                        time.sleep(1)
                        leaderboardTime()  # they get an option to see the leaderboard
                    elif event.key == K_2:  # they choose to replay the beginner event
                        running = False
                        b = []
                        autoBegin(inarow)
                        # replay beginner event
                    elif event.key == K_3:  # they choose to level up to advanced
                        running = False
                        b = []
                        autoBasic(inarow)
                        # level up to advanced.
        if b == colors1:  # does the same as above but for the average difficulty
            # resets screen for option page
            screen.fill(white)
            # reuses advanced page background as a waiting screen
            advancedPage = pygame.image.load("ColorsMainPage.jpg")
            advancedPage = pygame.transform.scale(advancedPage, (1800, 1012))
            screen.blit(advancedPage, origin)
            pygame.display.flip()
            time.sleep(0.5)

            # displays prompt to the user
            gameInstructions("You have completed this level! Would you like to keep going?")

            # displays first option
            OptionOne = pygame.font.SysFont("sawasdee", 24)
            OptionOne = OptionOne.render("Select 1 for Done", True, white)
            OptionOneRect = OptionOne.get_rect()
            OptionOneRect.center = (750, 600)
            screen.blit(OptionOne, OptionOneRect)

            # displays second option
            OptionTwo = pygame.font.SysFont("sawasdee", 24)
            OptionTwo = OptionTwo.render("Select 2 for Repeat", True, white)
            OptionTwoRect = OptionTwo.get_rect()
            OptionTwoRect.center = (1050, 600)
            screen.blit(OptionTwo, OptionTwoRect)

            # displays third option
            thirdOption = pygame.font.SysFont("sawasdee", 24)
            thirdOption = thirdOption.render("Select 3 for Level Down", True, white)
            thirdOptionRect = thirdOption.get_rect()
            thirdOptionRect.center = (750, 700)
            screen.blit(thirdOption, thirdOptionRect)
            pygame.display.flip()
            running = True

            while running:
                for event in pygame.event.get():  # loop that runs until there is a keypress
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_1:  # if key one is pressed, the player stops
                            running = False
                            screen.fill(black)
                            textBlock("latinmodernmonolight", 32,
                                      f"Now that you are done, your longest winning streak was {totalrow}!", white,
                                      (900, 270))
                            time.sleep(1)
                            leaderboardTime()
                        elif event.key == K_2:  # reruns advanced
                            running = False
                            b = []
                            autoBasic(inarow)
                            # replay advanced event
                        elif event.key == K_3:  # reruns beginner
                            running = False
                            b = []
                            autoBegin(inarow)
                            # level down to beginner
        if b == colors2:  # this is only for the presentation level of the 4 colors
            screen.fill(black)
            pygame.display.flip()
            textBlock("dejavuserif", 48, "You have completed the Demo", white, origin)
            time.sleep(1)
            AllDone(b, inarow)


def leaderboardTime():
    global colors
    global bgn
    global colors1
    global avg
    global totalrow
    global colors2
    colors = ['black', 'blue', 'brown', 'gray', 'red', 'white', 'yellow']
    colors1 = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'purple', 'red', 'white', 'yellow']
    colors2 = ["black", "blue", "green", "red"]

    leaderboard[user_name] = totalrow

    screen.fill(black)
    pygame.display.flip()
    gameInstructions("Are You the Last Person Playing?")
    fontOptionOne = pygame.font.SysFont("sawasdee", 24)
    fontOptionOne = fontOptionOne.render("Select 1 for Yes", True, white)
    fontOptionOneRect = fontOptionOne.get_rect()
    fontOptionOneRect.center = (750, 600)

    fontOptionTwo = pygame.font.SysFont("sawasdee", 24)
    fontOptionTwo = fontOptionTwo.render("Select 2 for No", True, white)
    fontOptionTwoRect = fontOptionTwo.get_rect()
    fontOptionTwoRect.center = (1050, 600)
    screen.blit(fontOptionOne, fontOptionOneRect)
    screen.blit(fontOptionTwo, fontOptionTwoRect)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_1:
                    screen.fill(black)
                    pygame.display.flip()
                    gameInstructions("Would you like to see the leaderboard? Yes: 1 No: 2")
                    pygame.display.flip()
                    runningInside = True
                    while runningInside:
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                if event.key == K_1:
                                    runningInside = False
                                    leaderBoards()
                                else:
                                    textBlock("latinmodernmonolight", 32, "Thank You For Playing!", white, (900, 800))
                                    runningInside = False
                                    quit()
                if event.key == K_2:
                    colors = bgn
                    colors1 = avg
                    colors2 = present
                    totalrow = 0
                    uusername()


# Data for the Home Page
def startMenu():
    """
    This function is the main page once the user has given the system their name.
    :return:
    """
    # gets an image for the mainPage
    mainPage = pygame.image.load("ColorsMainPageOption2.jpg")
    mainPage = pygame.transform.scale(mainPage, (1800, 1012))
    # Title text information
    fontTitle = pygame.font.SysFont("dejavuserif", 32)  # options for font and size
    textTitle = fontTitle.render(f'Welcome {user_name} to A Game of Colors', True,
                                 white)  # message, boolean and font color
    textTitleRect = textTitle.get_rect()
    textTitleRect.center = (870, 200)

    # subtitle text information
    fontSubTitle = pygame.font.SysFont("latinmodernmonolight", 24)
    textSubTitle = fontSubTitle.render("You Win or You Learn", True, white)
    textSubTitleRect = textSubTitle.get_rect()
    textSubTitleRect.center = (900, 275)

    # Beginner block text
    fontOptionOne = pygame.font.SysFont("sawasdee", 24)
    fontOptionOne = fontOptionOne.render("Select 1 for Beginner", True, white)
    fontOptionOneRect = fontOptionOne.get_rect()
    fontOptionOneRect.center = (750, 600)

    # Advanced block text
    fontOptionTwo = pygame.font.SysFont("sawasdee", 24)
    fontOptionTwo = fontOptionTwo.render("Select 2 for Advanced", True, white)
    fontOptionTwoRect = fontOptionTwo.get_rect()
    fontOptionTwoRect.center = (1050, 600)

    # Leaderboard block text
    leaderboardOption = pygame.font.SysFont("sawasdee", 24)
    leaderboardOption = leaderboardOption.render("Select 3 for Leaderboards", True, white)
    leaderboardOptionRect = leaderboardOption.get_rect()
    leaderboardOptionRect.center = (750, 700)

    # Demo block text
    fontOptionThree = pygame.font.SysFont("sawasdee", 24)
    fontOptionThree = fontOptionThree.render("Select 4 for Demo", True, white)
    fontOptionThreeRect = fontOptionThree.get_rect()
    fontOptionThreeRect.center = (1050, 700)

    # quit block text
    quitOption = pygame.font.SysFont("sawasdee", 18)
    quitOption = quitOption.render("Select ESC to Quit", True, white)
    quitOptionRect = quitOption.get_rect()
    quitOptionRect.center = (1400, 200)

    screen.fill(white)  # screen is filled with white, which clears the past screen.
    screen.blit(mainPage, (10, 10))  # each of the following screen.blit() lines 'draw' these features onto the canvas
    screen.blit(textTitle, textTitleRect)
    screen.blit(textSubTitle, textSubTitleRect)
    screen.blit(fontOptionOne, fontOptionOneRect)
    screen.blit(fontOptionTwo, fontOptionTwoRect)
    screen.blit(leaderboardOption, leaderboardOptionRect)
    screen.blit(quitOption, quitOptionRect)
    screen.blit(fontOptionThree, fontOptionThreeRect)
    pygame.display.flip()  # this line actually updates the screen to show each of these blocks + the image in the back
    running = True
    while running:  # this loop checks for keystrokes and runs until one of the five keys is selected.
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False  # ends the program
                elif event.key == K_1:
                    beginnerGameplay()  # navigates user to beginner gameplay
                elif event.key == K_2:
                    advancedGameplay()  # navigates user to advanced gameplay
                elif event.key == K_3:
                    leaderBoards()  # navigates user to leaderboards
                elif event.key == K_4:
                    demoGameplay()  # navigates user to demo gameplay


def loadingScreen():
    """
    serves as a brief loading screen between several pages in the game. Uses a delay to last onscreen for a set amount
    of time
    :return:
    """
    screen.fill(black)
    loadingMessage = pygame.font.SysFont("sawasdee", 24)
    loadingMessage = loadingMessage.render("Loading...", True, white)  # loading message in center of black screen
    loadingMessageRect = loadingMessage.get_rect()
    loadingMessageRect.center = (900, 506)
    screen.blit(loadingMessage, loadingMessageRect)
    pygame.display.flip()
    time.sleep(0.1)


def beginnerGameplay():
    """
    When 1 is selected in start menu, this function is launched. It will play the beginners level
    :return:
    """
    loadingScreen()  # uses loading screen inbewteen
    running = True
    beginnerPageFunction()  # replaces window with beginner image background
    while running:
        for event in pygame.event.get():  # if there is a key press for escape, we return to the start menu
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    startMenu()
        b = []
        pygame.display.flip()  # updates display
        randomizer(colors, b, 0)  # launches randomizer using b and colors variables for beginner game mode
    return None


def beginnerPageFunction():
    """
    Simply outputs the image of the beginnerGamebackground jpg
    :return:
    """
    screen.fill(black)
    beginnerPage = pygame.image.load("beginnerGameBackground.jpg")
    beginnerPage = pygame.transform.scale(beginnerPage, (1800, 1012))
    screen.blit(beginnerPage, origin)
    pygame.display.flip()


def demoPageFunction():
    """
    simply outputs the image of the demo game background jpg
    :return:
    """
    screen.fill(black)
    demoPage = pygame.image.load("BeginnersPage.jpg")
    demoPage = pygame.transform.scale(demoPage, (1800, 1012))
    screen.blit(demoPage, origin)
    pygame.display.flip()


def demoGameplay():
    """
        When 4 is selected in start menu, this function is launched. It will play the demo level
        :return:
        """
    loadingScreen()  # brief delay before level
    running = True
    demoPageFunction()
    while running:
        for event in pygame.event.get():  # if ESC is pressed, we return to the start menu
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    startMenu()
        b = []
        pygame.display.flip()
        randomizer(colors2, b, 0)  # launches randomizer with the colors2 and b variable meaning that we will use only
        # four colors
    return None


def advancedGameplay():
    """
        When 2 is selected in start menu, this function is launched. It will play the advanced level
        :return:
        """
    loadingScreen()  # brief delay before gameplay
    running = True
    advancedPageBackground()
    while running:
        for event in pygame.event.get():  # if the ESC key is pressed the function will return to the start menu
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    startMenu()
        b = []
        pygame.display.flip()
        randomizer(colors1, b, 0)  # calls randomizer using colors1 and b indicating an advanced gamemode
    return None


def advancedPageBackground():
    """
    simply displays the background for the advanced gamemode
    :return:
    """
    advancedPage = pygame.image.load("ColorsMainPage.jpg")
    advancedPage = pygame.transform.scale(advancedPage, (1800, 1012))
    pygame.display.flip()

    screen.fill(black)
    screen.blit(advancedPage, origin)
    pygame.display.flip()


def strikeCounting(StrikeNum: int):
    """Displays the number of strikes by the user. Called by checkCorrect"""
    strikeCounter = pygame.font.SysFont("calibri", 24)
    strikeCounter = strikeCounter.render(f"Strikes: {StrikeNum}", True, black)
    strikeCounterRect = strikeCounter.get_rect()
    strikeCounterRect.center = (500, 300)
    screen.blit(strikeCounter, strikeCounterRect)
    pygame.display.flip()


def gameInstructions(title: str):
    """Used as a title for instructions. Called frequently by checkCorrect"""
    instructionTitle = pygame.font.SysFont("msgothic", 32)
    instructionTitle = instructionTitle.render(title, True, black)
    instructionTitleRect = instructionTitle.get_rect()
    instructionTitleRect.center = (900, 225)
    screen.blit(instructionTitle, instructionTitleRect)
    pygame.display.flip()


def correctInARow(inarow):
    """ Displays the number of correct answers in a row by the user. Called by checkCorrect"""
    inarowCounter = pygame.font.SysFont("calibri", 24)
    inarowCounter = inarowCounter.render(f"Answers in a Row: {inarow}", True, black)
    inarowCounterRect = inarowCounter.get_rect()
    inarowCounterRect.center = (500, 350)
    screen.blit(inarowCounter, inarowCounterRect)
    pygame.display.flip()


def leaderBoards():
    """
    Displays the leaderboard
    :return:
    """
    screen.fill(black)  # makes screen black
    pygame.display.flip()
    lineX = 900
    lineY = 200
    i = 0
    leaderBoardText = pygame.font.SysFont("dejavuserif", 32)
    leaderBoardText = leaderBoardText.render("Leaderboard", True, white)  # shows the title leaderboard at the top
    leaderBoardTextRect = leaderBoardText.get_rect()
    leaderBoardTextRect.center = (lineX, lineY)
    screen.blit(leaderBoardText, leaderBoardTextRect)
    pygame.display.flip()
    sorted(leaderboard)
    for userName, score in leaderboard.items():  # this for loop goes through each key value pair in the dictionary
        # and displays them in the pygame window
        i += 1
        lineY += 75
        userNamePlusScore = pygame.font.SysFont("latinmodernmonolight", 24)
        userNamePlusScore = userNamePlusScore.render(f"{i}. {userName}                             {score}", True,
                                                     white)
        userNamePlusScoreRect = userNamePlusScore.get_rect()
        userNamePlusScoreRect.center = (lineX, lineY)
        screen.blit(userNamePlusScore, userNamePlusScoreRect)
        pygame.display.flip()

    textBlock("latinmodernmonolight", 32, "Thank You For Playing!", white, (900, 800))  # thanks the user for playing
    time.sleep(5)
    quit()  # exits the game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    startMenu()
                    running = False


def textBlock(font: str, fontSize: int, text: str, color: tuple, center: tuple):
    """Used as a basic version of the text block in pygame to make displaying new text a little more efficient"""
    textLine = pygame.font.SysFont(font, fontSize)
    textLine = textLine.render(text, True, color)
    textLineRect = textLine.get_rect()
    textLineRect.center = center
    screen.blit(textLine, textLineRect)
    pygame.display.flip()


if __name__ == "__main__":
    uusername()

pygame.quit()  # ends the game once the loop finishes
