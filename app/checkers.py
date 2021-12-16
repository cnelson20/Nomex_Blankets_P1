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

time_dict = dict();

def start_game():
    if (not 'username' in session) or user in games_dict:
        return false;
    else:
        session['game'] = dict();
        session['game']['board'] = generate_board();
        session['game']['turn'] = 1;
        # generate emojis
        return true;

def remove_game():
    ''' 
       delete a game 
    '''
    if 'game' in session:
        del session['game'];
        return true
    return false

def game_exists():
    return 'game' in session;

def move(oldx,oldy,movex,movey):
    '''
       move piece 
    '''
    if 'game' in session:
        print(session['game']);
        game_turn = session['game']['turn'];
        board = session['game']['board'];
        doublehop = False;
        
        if (board[oldy][oldx] != 0 and board[oldy][oldx] % 2 == game_turn):
            ''' correct player continue checking things '''
            if (board[movey][movex] != 0 and board[movey][movex] % 2 == game_turn):
                return false # if spot to move to is own team fail.
        else:
            return false
        
        if (not doublehop):
            user_game['turn'] = (game_turn % 2) + 1;
        return true
    else:
        return false  

    
if __name__ == "__main__":
    print(*generate_board(),sep='\n');
