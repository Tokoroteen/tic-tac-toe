from flask import Flask, render_template, request

app = Flask(__name__,static_folder='./static')

#揃い判定
def aline_checker(n,s):
    if s.count('1')==n: #1が揃った時
        status=1
    elif s.count('2')==n: #2が揃った時
        status=2
    else:
        status=0
    return status

#勝ち判定
def winner_checker(n,status,board):
    diagonal_1='' #左上から右下のナナメのマス
    diagonal_2='' #右上から左下のナナメのマス
    for x in range(n): #列番号
        column = '' #タテのマス
        diagonal_1 += board[(n+1)*x]
        diagonal_2 += board[(n-1)*(x+1)]

        for y in range(0,n*n,n): #行番号
            column += board[x+y]

            if x==0:
                row = board[y:y+n] #ヨコのマス
                #ヨコが揃ったかどうか
                status = aline_checker(n,row)
                print('行',row)
                if status != 0: #勝敗がついたらbreak
                    break
        else:
            #タテが揃ったかどうか
            status = aline_checker(n,column)
            print('列',column)
            if status != 0: #勝敗がついたらbreak
                break
            continue
        break
    #ナナメが揃ったかどうか
    if status == 0:
        status = max(aline_checker(n,diagonal_1),aline_checker(n,diagonal_2))
        print('ななめ',diagonal_2)
    print('status',status)
    return status

#ホーム画面
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#ゲームが始まる画面
@app.route("/tic-tac-toe", methods=["POST"])
def tic_tac_toe():
    n = int(request.form["n_times_n"]) #n×nの丸バツゲーム
    count = 1 #ターン数
    status = 0 #勝者
    board = '0'*n*n #マス目の中身
    print(board)
    return render_template("tic-tac-toe.html", n=n, count=count, status=status, board=board)

@app.route("/tic-tac-toe?n=<int:n>", methods=["GET"])
def reset(n):
    n = int(n) #n×nの丸バツゲーム
    count = 1 #ターン数
    status = 0 #勝者
    board = '0'*n*n #マス目の中身
    print(board)
    return render_template("tic-tac-toe.html", n=n, count=count, status=status, board=board)

#ゲーム画面の更新
@app.route("/tic-tac-toe?n=<int:n>&count=<count>&status=<int:status>&x=<int:x>&y=<int:y>&board=<board>",methods=["GET"])
def update(n,count,status,x,y,board):
    n,count,status,x,y = int(n),int(count),int(status),int(x),int(y)
    if count%2 == 1: #先攻のとき
        board = board[:x+y] + '1' + board[x+y+1:] #該当マスを1に変更
    else: #後攻のとき
        board = board[:x+y] + '2' + board[x+y+1:] #該当マスを2に変更

    if status == 0: #勝敗が決していない時
        status = winner_checker(n,status,board)
    count += 1
    return render_template("tic-tac-toe.html", n=n, count=count, status=status, board=board)

if __name__ == "__main__":
    app.run()