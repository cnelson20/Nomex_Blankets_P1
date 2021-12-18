def invert10(i):
    if (i == 0):
        return 1;
    return 0;
def times2(i):
    return 2 * i;

def gen_list(iterable_thing):
    l = list();
    for i in iterable_thing:
        l.append(i);
    return l;
        
def generate_board():
    board = list();
    basic = [0,1,0,1,0,1,0,1];
    clear = [0,0,0,0,0,0,0,0];
    for i in range(8):
        board.append(clear);
    board[0] = basic;
    board[1] = gen_list(map(invert10,basic));
    board[2] = basic;

    board[5] = gen_list(map(times2,map(invert10,basic)));
    board[6] = gen_list(map(times2,basic));
    board[7] = gen_list(map(times2,map(invert10,basic)));

    return board;

def start_game(session):
    if (not 'username' in session) or 'game' in session:
        return False;
    else:
        session['game'] = dict();
        session['game']['board'] = generate_board();
        session['game']['turn'] = 0;
        session['game']['emojis'] = ["🐘","🐊"];
        # generate emojis
        return True;

def set_emojis(session,e1,e2):
    if 'game' in session:
        if (e1 != ""):
            session['game']['emojis'][0] = e1;
        if (e2 != ""):
            session['game']['emojis'][1] = e2;
        return True;
    return False;

def remove_game(session):
    ''' 
       delete a game 
    '''
    if 'game' in session:
        del session['game'];
        return True
    return False

def game_exists(session):
    return 'game' in session;

def turns(session,doublehop):
    if (not doublehop):
        session['game']['turn'] = invert10(session['game']['turn']);
    return True

def clear_unused(session):
    for y in range(8):
        for x in range(8):
            if (x + y) % 2 == 0:
                session['game']['board'][y][x] = 0;

def move(session,oldx,oldy,movex,movey):
    '''
       move piece 
    '''
    if 'game' in session:
        game_turn = session['game']['turn'];
        board = session['game']['board'];
        doublehop = False;

        if (movey < 0 or movey > 7 or movex < 0 or movex > 7 or oldy < 0 or oldy > 7 or oldx < 0 or oldy > 7):
            print("OOB")
            return False
        if (movey + movex) % 2 == 0:
            print("Wrong squares")
            return False
        if (board[oldy][oldx] != 0 and board[oldy][oldx] % 2 == game_turn):
            ''' correct player continue checking things '''
            if (board[movey][movex] != 0 and board[movey][movex] % 2 == game_turn):
                print("Move onto teammate")
                return False # if spot to move to is own team fail.
        else:
            print("Not your piece!")
            return False        

        if (game_turn == 0 or board[oldy][oldx] >= 3):
            if ((movex == oldx - 1 and movey == oldy - 1) or (movex == oldx + 1 and movey == oldy - 1)) and board[movey][movex] == 0:
                board[movey][movex] = board[oldy][oldx];
                if (movey == 0 and board[movey][movex] <= 2):
                    board[movey][movex] += 2
                board[oldy][oldx] = 0;
                return turns(doublehop);
        if (game_turn == 1 or board[oldy][oldx] >= 3):
            if ((movex == oldx - 1 and movey == oldy + 1) or (movex == oldx + 1 and movey == oldy + 1)) and board[movey][movex] == 0:
                board[movey][movex] = board[oldy][oldx];
                if (movey == 0 and board[movey][movex] <= 2):
                    board[movey][movex] += 2
                board[oldy][oldx] = 0;
                return turns(session,doublehop);
    else:
        print("game not in session")
        # print(session)
        return False  

if __name__ == "__main__":
    session['user'] = 'username';
    session['game'] = dict();
    session['game']['board'] = generate_board()
    session['game']['turn'] = 0;
    while True:
        print(*session['game']['board'],sep="\n");
        print("Turn: " + str(1 + invert10(session['game']['turn'])))
        first = True
        inp = [0,0,0,0]
        while first or not move(int(inp[0]),int(inp[1]),int(inp[2]),int(inp[3])):
            first = False
            inp = input(": ");
            inp = inp.split(" ");
        # clear_unused();
    
