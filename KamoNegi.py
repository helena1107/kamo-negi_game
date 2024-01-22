import pyxel

# 3種類のスクリーンにidを振る
TITLE_SCREEN = 0
MAIN_SCREEN = 1
END_SCREEN = 2

# オブジェクトの種類
KAMO = 0
NEGI = 1
NABE = 2

TIMER_MAX = 60

# プレイヤーの速さ
PLAYER_SPEED = 2
TRANSP_C = 14
PICT_ID = 0

Kamo_list = []
Negi_list = []
Nabe_list = []

# 存在するオブジェクトについて、.is_alive値がFalseであれば削除する
def check_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.is_alive:
            list.pop(i)
        else:
            i += 1

# キーにあわせて動くように設定する
class Player:
    def __init__(self, x, y):
        # 与えられた初期位置を反映する
        self.x = x
        self.y = 142
        # 幅と高さを決定する
        self.w = 26
        self.h = 10

        self.u = 3  # 切り出しの左側
        self.v = 38  # 切り出しの上側

    # 関数 : update ... キー入力にあわせて移動させる
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED
        # 端についていたら動きを止める
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)

    # プレイヤー表示
    def draw(self):
        pyxel.blt(self.x, self.y, PICT_ID, self.u, self.v, self.w, self.h, TRANSP_C)

# 落ちてくるオブジェクトをつかさどるクラス
class Object():
    def __init__(self, type, x, y):
        self.type = type
        # 与えられた位置で初期化
        self.x = x
        self.y = y
        self.u_kamo = 0
        self.v_kamo = 0
        self.u_negi = 32
        self.v_negi = 0
        self.u_nabe = 5
        self.v_nabe = 33
        self.w = 16
        self.h = 16
        self.c = pyxel.rndi(1,15)
        self.speed = pyxel.rndf(3,4.5)
        if self.type == NABE:
            self.speed += 3.5
        # オブジェクトリストに追加する
        if self.type == KAMO:
            Kamo_list.append(self)
        elif self.type == NEGI:
            Negi_list.append(self)
        elif self.type == NABE:
            Nabe_list.append(self)

        self.is_alive = True
    
    # 関数 : update ... 落とす
    def update(self):
        # 落とす
        self.y += self.speed
        # 範囲外なら消す
        if self.y > pyxel.height + 1:
            self.is_alive = False
    
    # 書く
    def draw(self):
        if self.type == KAMO:
            pyxel.blt(self.x, self.y, PICT_ID, self.u_kamo, self.v_kamo, self.w, self.h, TRANSP_C)
        elif self.type == NEGI:
            pyxel.blt(self.x, self.y, PICT_ID, self.u_negi, self.v_negi, self.w, self.h, TRANSP_C)
        elif self.type == NABE:
            pyxel.blt(self.x, self.y, PICT_ID, self.u_nabe, self.v_nabe, 22, 3, TRANSP_C)

# アプリのメインの動きを決定するクラス
class App:
    def __init__(self):
        # 画面を作成
        pyxel.init(120, 160, title = "movement test")
        # 画像を読み込み
        pyxel.image(0).load(0,0,"Kamo.png")
        # 背景画像
        pyxel.image(1).load(0,0,"background.jpg")
        self.txtcolors = [3,7,11]
        # スコアを初期化
        self.score = 0
        self.kamo_score = 0
        self.negi_score = 0
        # 時間制限を初期化
        self.time_count = TIMER_MAX
        # 現在がどのスクリーンであるかを表示する関数
        # スクリーン初期設定をタイトルにする
        self.screen = TITLE_SCREEN
        # プレイヤーをインスタンス化(作成)
        self.player = Player(pyxel.width / 2, pyxel.height - 20)
        # 自動で実行される関数としてself.update,self.drawを指定する
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.screen == TITLE_SCREEN:
            self.update_title_screen()
        elif self.screen == MAIN_SCREEN:
            self.update_main_screen()
        elif self.screen == END_SCREEN:
            self.update_end_screen()
    
    # メインスクリーンのアップデート
    def update_main_screen(self):
        # タイマーの本体
        # pyxel.frame_countでスタートからいくつフレームが進んだかわかる
        # 30フレーム = 1秒　なので、time_countから1引く
        if pyxel.frame_count % 30 == 0:
            self.time_count -= 1
        if self.time_count == 0:
            self.screen = END_SCREEN

        # playerに関するupdateを実行(player Classに記述済み)
        self.player.update()
        # objに関するupdateを実行(中身は下に記述)
        self.update_obj(Kamo_list)
        self.update_obj(Negi_list)
        self.update_obj(Nabe_list)

    def update_obj(self, list):
        # 6フレームに1回、オブジェクトを作成する
        if pyxel.frame_count % 6 == 0:
            # ある確率でそれぞれのオブジェクトを生成する。
            obj_type = pyxel.rndi(0,120)
            if 0 <= obj_type and obj_type <= 5:
                Object(KAMO, pyxel.rndi(0, pyxel.width - 15), 0)
            elif 50 <= obj_type and obj_type <= 53:
                Object(NEGI, pyxel.rndi(0, pyxel.width - 15), 0)
            elif obj_type >= 118:
                Object(NABE, pyxel.rndi(0, pyxel.width - 15), 0)
        # 上でオブジェクトが生成された時点で、obj_listにインスタンス化されたオブジェクトがすべて入っているので
        # obj_listの中身について下の関数を実行する
        for obj in list:
            # playerと触れたとき
            if (self.player.x + self.player.w > obj.x
                and obj.x + obj.w > self.player.x
                and self.player.y + self.player.h > obj.y
                and obj.y + obj.h > self.player.y):

                # obj_typeによってスコアの追加方法とゲームオーバーか判定するかどうかを変更する。
                if obj.type == KAMO:
                    self.score += 1
                    self.kamo_score += 1
                elif obj.type == NEGI:
                    self.score += 2
                    self.negi_score += 2
                    if self.kamo_score < self.negi_score:
                        self.screen = END_SCREEN
                elif obj.type == NABE:
                    self.screen = END_SCREEN
                # オブジェクトを削除する(正確にはオブジェクトの.is_aliveパラメータをFalseにする)
                obj.is_alive = False
                # listの中で.is_aliveパラメータがFalseのものを削除する
                check_list(Kamo_list)
                check_list(Negi_list)
                check_list(Nabe_list)
            obj.update()
    
    def update_obj_pos(self,list):
        for obj in list:
            obj.update()
            check_list(list)

    def update_title_screen(self):        
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.screen = MAIN_SCREEN
            # パラメータの初期化
            self.time_count = TIMER_MAX
            self.score = 0
            self.kamo_score = 0
            self.negi_score = 0
        self.update_obj_pos(Kamo_list)
        self.update_obj_pos(Negi_list)
        self.update_obj_pos(Nabe_list)

    def update_end_screen(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.screen = TITLE_SCREEN
        self.update_obj_pos(Kamo_list)
        self.update_obj_pos(Negi_list)
        self.update_obj_pos(Nabe_list)

    # 表示系
    def draw(self):
        pyxel.cls(0)
        # pyxel.rect(0,0,120,160,6)
        # pyxel.blt(0,0,1,0,0,120,160,15)
        if self.screen == TITLE_SCREEN:
            self.draw_title_screen()
        elif self.screen == MAIN_SCREEN:
            self.draw_main_screen()
        elif self.screen == END_SCREEN:
            self.draw_end_screen()

    def draw_main_screen(self):
        # 残り時間を表示
        pyxel.text(pyxel.width - 15, 10, f"{self.time_count}", 7)
        # 現在のスコアを表示
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

        # playerの表示
        self.player.draw()
        # 場に存在するオブジェクトの表示
        self.draw_obj(Kamo_list)
        self.draw_obj(Negi_list)
        self.draw_obj(Nabe_list)

        # 残っているobjの表示(objの削除はupdateで既に行った)
    def draw_obj(self, list):
        for obj in list:
            obj.draw()

    def draw_title_screen(self):
        pyxel.text(35, 66, "KAMO-NEGI　GAME", self.txtcolors[pyxel.frame_count % 3])
        pyxel.text(31, 126, "- PRESS ENTER -", 13)
        self.draw_obj(Kamo_list)
        self.draw_obj(Negi_list)
        self.draw_obj(Nabe_list)

    def draw_end_screen(self):
        pyxel.text(41, 66, "GAME OVER", self.txtcolors[pyxel.frame_count % 3])
        pyxel.text(37, 75, f"SCORE {self.score:5}" , 7)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)
        self.draw_obj(Kamo_list)
        self.draw_obj(Negi_list)
        self.draw_obj(Nabe_list)

App()