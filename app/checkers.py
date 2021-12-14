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
    basic = [1,0,1,0,1,0,1,0];
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

games_dict = dict();

def new_game(user):
    if user in games_dict:
        return false;
    else:
        games_dict[user] = generate_board();
        return true;

def move(user,x1,y1,x2,y2):
    if user in games_dict:
        return true
    else:
        return false
    

if __name__ == "__main__":
    print(*generate_board(),sep='\n');
