import pygame # 用於建立遊戲視窗和處理遊戲中的圖形與音效
import random # 用於生成隨機數（決定障礙物的位置）
import sys  # 用於退出程式
import math # 用於數學運算（畫模式2中星星的頂點座標）
import numpy as np # 用於數組運算、數據處理
import ctypes # 用於設置鍵盤輸入為英文
from ai_bird import FlappyBirdEnv, load_model # 導入 AI 模型相關函數


# 初始化 Pygame
pygame.init()

# 設置遊戲視窗大小
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Flappy Bird')  # 設置遊戲視窗標題

FLOOR_HEIGHT_MODE_1 = 50  # 模式1的地板高度
FLOOR_HEIGHT_MODE_2 = 80  # 模式2的地板高度

# 定義顏色
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# 載入圖片並調整大小
bird_img = pygame.transform.scale(pygame.image.load('static/img/bird.png'), (50, 38))
background_img = pygame.transform.scale(pygame.image.load('static/img/background.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
background_night_img = pygame.transform.scale(pygame.image.load('static/img/background_night.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
homepage_img = pygame.transform.scale(pygame.image.load('static/img/homepage.png'), (WINDOW_WIDTH, WINDOW_HEIGHT)) 
gameover1_img = pygame.transform.scale(pygame.image.load('static/img/gameover1.png'), (WINDOW_WIDTH, WINDOW_HEIGHT)) 
gameover2_img = pygame.transform.scale(pygame.image.load('static/img/gameover2.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
rules_img = pygame.transform.scale(pygame.image.load('static/img/rules.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))  

# 載入音效
menu_music = pygame.mixer.Sound('static/sound/background_music.mp3')
game1_music = pygame.mixer.Sound('static/sound/background_music1.mp3')
game2_music = pygame.mixer.Sound('static/sound/background_music2.mp3')
death_sound = pygame.mixer.Sound('static/sound/death.wav')
shoot_sound = pygame.mixer.Sound('static/sound/shoot.wav')
jump_sound = pygame.mixer.Sound('static/sound/jump.wav')
hit_sound = pygame.mixer.Sound('static/sound/hit.wav')
gameover_sound = pygame.mixer.Sound('static/sound/gameover.mp3')
click_sound = pygame.mixer.Sound('static/sound/click.wav')
sounds = [menu_music, game1_music, game2_music, death_sound, shoot_sound, jump_sound, hit_sound, gameover_sound, click_sound]

# 定義設置音量的函數
for sound in sounds:
    sound.set_volume(0.01)

# 定義小鳥類別
class Bird:
    def __init__(self):
        self.x = 50  # 小鳥的初始橫坐標
        self.y = WINDOW_HEIGHT // 2  # 小鳥的初始縱坐標，在窗口高度的一半
        self.velocity = 0  # 初始速度
        self.gravity = 0.5  # 重力
        self.jump_strength = -8  # 跳躍力度
        self.width = bird_img.get_width()  # 小鳥的寬度
        self.height = bird_img.get_height()  # 小鳥的高度
        self.bullets = []  # 子彈列表，儲存小鳥發射的所有子彈

    def jump(self):
        self.velocity = self.jump_strength  # 設置跳躍速度
        jump_sound.play()  # 播放跳躍音效

    def move(self):
        self.velocity += self.gravity  # 速度增加，模擬重力效果
        self.y += self.velocity  # 更新小鳥的縱坐標

    def shoot(self):
        self.bullets.append(Bullet(self.x + self.width, self.y + self.height // 2))  # 添加一顆新子彈到子彈列表
        shoot_sound.play()  # 播放射擊音效

    def draw(self):
        WINDOW.blit(bird_img, (self.x, self.y))  # 繪製小鳥
        for bullet in self.bullets:  # 繪製所有子彈
            bullet.move()
            bullet.draw()
            if bullet.x > WINDOW_WIDTH:  # 如果子彈移出窗口，將其移除
                self.bullets.remove(bullet)

# 定義子彈類別
class Bullet:
    def __init__(self, x, y):
        self.x = x  # 子彈的初始橫坐標
        self.y = y  # 子彈的初始縱坐標
        self.speed = 10  # 子彈速度
        self.width = 10  # 子彈寬度
        self.height = 5  # 子彈高度

    def move(self):
        self.x += self.speed  # 更新子彈的橫坐標

    def draw(self):
        pygame.draw.rect(WINDOW, RED, (self.x, self.y, self.width, self.height))  # 繪製紅色矩形表示子彈

# 定義星星類別
class Star:
    def __init__(self, floor_height):
        self.x = WINDOW_WIDTH  #定義星星的初始橫坐標
        self.y = random.randint(50, WINDOW_HEIGHT - floor_height - 100)  #定義星星的初始縱坐標，隨機生成
        self.speed = 5  #定義星星速度
        self.width = 50  #定義星星寬度
        self.height = 50  #定義星星高度
        self.hit = False  # 是否被擊中
        self.hit_timer = 0  # 被擊中的計時器

    def move(self):
        self.x -= self.speed  # 更定義星星的橫坐標

    def draw_star(self, surface, color, x, y, size):
        points = []  # 星形的頂點列表
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2  # 外頂點角度
            outer_x = x + size * math.cos(angle)
            outer_y = y + size * math.sin(angle)
            points.append((outer_x, outer_y))
            angle = (i + 0.5) * 2 * math.pi / 5 - math.pi / 2  # 內頂點角度
            inner_x = x + size / 2 * math.cos(angle)
            inner_y = y + size / 2 * math.sin(angle)
            points.append((inner_x, inner_y))
        pygame.draw.polygon(surface, color, points)  # 繪製星形

    def draw(self):
        color = WHITE if self.hit else YELLOW  # 被擊中後變白色，否則為黃色
        self.draw_star(WINDOW, color, self.x + self.width // 2, self.y + self.height // 2, self.width // 2)  # 繪製星星
        
    def got_hit(self):
        self.hit = True  # 標記為被擊中
        self.hit_timer = pygame.time.get_ticks()  # 記錄擊中的時間
        hit_sound.play()  # 播放擊中音效
    def update(self):
        if self.hit and pygame.time.get_ticks() - self.hit_timer > 100:  # 如果被擊中後超過100毫秒
            return True  # 返回True，表示應該移定義星星
        return False  # 返回False，表示不應該移定義星星

# 定義管道類別
class Pipe:
    def __init__(self, is_moving=False, is_clamping=False):
        self.x = WINDOW_WIDTH  # 管道的初始橫坐標
        self.pipe_gap = 200  # 上下管道之間的間隙
        self.top_pipe_height = random.randint(50, WINDOW_HEIGHT - self.pipe_gap - FLOOR_HEIGHT_MODE_1 - 50)  # 上管道的高度
        self.bottom_pipe_height = WINDOW_HEIGHT - self.pipe_gap - self.top_pipe_height - FLOOR_HEIGHT_MODE_1  # 下管道的高度
        self.pipe_speed = 5  # 管道移動速度
        self.pipe_width = 50  # 管道寬度
        self.is_moving = is_moving  # 管道是否移動
        self.move_direction = 1  # 移動方向
        self.move_speed = 2  # 移動速度
        self.is_clamping = is_clamping  # 管道是否會夾動
        self.clamp_speed = 1  # 夾動速度

    def move(self):
        self.x -= self.pipe_speed  # 更新管道的橫坐標
        if self.is_moving:  # 如果管道會移動
            self.top_pipe_height += self.move_speed * self.move_direction  # 更新上管道的高度
            self.bottom_pipe_height = WINDOW_HEIGHT - self.pipe_gap - self.top_pipe_height - FLOOR_HEIGHT_MODE_1  # 更新下管道的高度
            if self.top_pipe_height < 50 or self.top_pipe_height > WINDOW_HEIGHT - self.pipe_gap - FLOOR_HEIGHT_MODE_1 - 50:  # 如果管道移動超出範圍
                self.move_direction *= -1  # 反向移動
        if self.is_clamping:  # 如果管道會夾動
            self.pipe_gap -= self.clamp_speed * self.move_direction  # 更新管道間隙
            if self.pipe_gap < 150 or self.pipe_gap > 200:  # 如果間隙超出範圍
                self.move_direction *= -1  # 反向夾動

    def draw(self):
        pygame.draw.rect(WINDOW, GREEN, (self.x, 0, self.pipe_width, self.top_pipe_height))  # 繪製上管道
        pygame.draw.rect(WINDOW, LIGHT_GREEN, (self.x, self.top_pipe_height - 10, self.pipe_width, 10))  # 繪製上管道邊緣
        pygame.draw.rect(WINDOW, GREEN, (self.x, WINDOW_HEIGHT - FLOOR_HEIGHT_MODE_1 - self.bottom_pipe_height, self.pipe_width, self.bottom_pipe_height))  # 繪製下管道
        pygame.draw.rect(WINDOW, LIGHT_GREEN, (self.x, WINDOW_HEIGHT - FLOOR_HEIGHT_MODE_1 - self.bottom_pipe_height, self.pipe_width, 10))  # 繪製下管道邊緣

# 停止所有音樂
def stop_all_music():
    pygame.mixer.Sound.stop(menu_music)  # 停止主選單音樂
    pygame.mixer.Sound.stop(game1_music)  # 停止遊戲模式1音樂
    pygame.mixer.Sound.stop(game2_music)  # 停止遊戲模式2音樂
    pygame.mixer.Sound.stop(gameover_sound)  # 停止遊戲結束音樂

# 主遊戲循環
def main():
    in_rules_page = False  # 是否在規則頁面
    mode = None  # 遊戲模式
    bird = Bird()  # 創建小鳥實例
    pipes = []  # 管道列表
    enemies = []  #定義星星列表
    game_over = False  # 遊戲是否結束
    game_started = False  # 遊戲是否開始
    score = 0  # 分數
    floor_height = 0  # 地板高度
    font = pygame.font.SysFont("monospace", 35)  # 設置字體
    death_display_time = 0  # 用於顯示死亡頁面的計時器
    ai_enabled = False  # 是否啟用 AI
    ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)  # 設置鍵盤輸入為英文
    model = load_model()  # 載入 AI 模型

    stop_all_music()  # 停止所有音樂
    pygame.mixer.Sound.play(menu_music, loops=-1)  # 播放主選單音樂，循環播放

    while True:  # 遊戲主循環
        for event in pygame.event.get():  # 處理所有事件
            if event.type == pygame.QUIT:  # 如果點擊關閉按鈕
                pygame.quit()  # 退出 Pygame
                sys.exit()  # 退出程式
                
            if event.type == pygame.KEYDOWN:  # 如果按下鍵盤按鍵
                if mode is None:  # 如果還未選擇模式
                    if event.key == pygame.K_1:
                        pygame.mixer.Sound.play(click_sound)  # 播放點擊音效
                        mode = "original"  # 經典模式
                        floor_height = FLOOR_HEIGHT_MODE_1  # 設置地板高度
                        stop_all_music()  # 停止所有音樂
                        pygame.mixer.Sound.play(game1_music, loops=-1)  # 播放模式1音樂，循環播放
                        
                    elif event.key == pygame.K_2:
                        pygame.mixer.Sound.play(click_sound)  # 播放點擊音效
                        mode = "shooting"  # 射擊模式
                        floor_height = FLOOR_HEIGHT_MODE_2  # 設置地板高度
                        stop_all_music()  # 停止所有音樂
                        pygame.mixer.Sound.play(game2_music, loops=-1)  # 播放模式2音樂，循環播放
                        
                    elif event.key == pygame.K_r:
                        pygame.mixer.Sound.play(click_sound)  # 播放點擊音效
                        in_rules_page = True  # 進入規則頁面
                        
                elif not game_over:  # 如果遊戲未結束
                    if event.key == pygame.K_SPACE:
                        if not game_started:
                            game_started = True  # 開始遊戲
                        bird.jump()  # 讓小鳥跳躍
                    if mode == "shooting" and event.key == pygame.K_s:
                        bird.shoot()  # 讓小鳥射擊
                        
                    if event.key == pygame.K_a:
                        ai_enabled = not ai_enabled  # 切換 AI 控制

                if game_over:  # 如果遊戲結束
                    if event.key == pygame.K_SPACE:
                        bird = Bird()  # 創建新小鳥
                        pipes = []  # 清空管道列表
                        enemies = []  # 清定義星星列表
                        game_over = False  # 重置遊戲結束狀態
                        game_started = False  # 重置遊戲開始狀態
                        score = 0  # 重置分數
                        death_display_time = 0  # 重置死亡顯示時間
                        stop_all_music()  # 停止所有音樂
                        
                        if mode == "original":
                            pygame.mixer.Sound.play(game1_music, loops=-1)  # 播放模式1音樂
                        elif mode == "shooting":
                            pygame.mixer.Sound.play(game2_music, loops=-1)  # 播放模式2音樂
                            
                    elif event.key == pygame.K_m:  # 按下 M 鍵返回主選單
                        mode = None  # 重置模式
                        bird = Bird()  # 創建新小鳥
                        pipes = []  # 清空管道列表
                        enemies = []  # 清定義星星列表
                        game_over = False  # 重置遊戲結束狀態
                        game_started = False  # 重置遊戲開始狀態
                        score = 0  # 重置分數
                        death_display_time = 0  # 重置死亡顯示時間
                        stop_all_music()  # 停止所有音樂
                        pygame.mixer.Sound.play(menu_music, loops=-1)  # 播放主選單音樂
                if in_rules_page and event.key == pygame.K_b:
                    in_rules_page = False  # 退出規則頁面

            if event.type == pygame.MOUSEBUTTONDOWN:  # 如果按下滑鼠按鍵
                pygame.mixer.Sound.play(click_sound)  # 播放點擊音效
                mouse_x, mouse_y = event.pos  # 獲取滑鼠點擊位置
                if mode is None and not in_rules_page:  # 在主畫面時
                    if 135 < mouse_x < 270 and 320 < mouse_y < 360:  # 如果點擊區域在 "Rules" 按鈕範圍內
                        in_rules_page = True  # 進入規則頁面
                        
                    elif 75 < mouse_x < 355 and 220 < mouse_y < 250:  # 如果點擊區域在 "Start" 按鈕範圍內
                        mode = "original"
                        floor_height = FLOOR_HEIGHT_MODE_1
                        stop_all_music()  # 停止所有音樂
                        pygame.mixer.Sound.play(game1_music, loops=-1)  # 播放模式1音樂
                        
                    elif 65 < mouse_x < 365 and 250 < mouse_y < 280:  # 如果點擊區域在 "Shooting" 按鈕範圍內
                        mode = "shooting"
                        floor_height = FLOOR_HEIGHT_MODE_2
                        stop_all_music()  # 停止所有音樂
                        pygame.mixer.Sound.play(game2_music, loops=-1)  # 播放模式2音樂
                        
                elif in_rules_page:  # 在規則頁面時
                    if 165 < mouse_x < 235 and 337 < mouse_y < 374:  # 如果點擊區域在 "Back" 按鈕範圍內
                        in_rules_page = False  # 返回主頁

        if mode is None and not in_rules_page:  # 如果未選擇模式且不在規則頁面
            WINDOW.blit(homepage_img, (0, 0))  # 顯示首頁圖片
        elif in_rules_page:  # 如果在規則頁面
            WINDOW.blit(rules_img, (0, 0))  # 顯示規則頁面圖片
        else:
            if not game_over:  # 如果遊戲未結束
                if game_started:  # 如果遊戲已開始
                    if ai_enabled:  # 如果啟用 AI
                        obs = np.array([bird.y, bird.velocity, pipes[0].x if pipes else 0, bird.y - pipes[0].top_pipe_height if pipes else 0, pipes[0].top_pipe_height if pipes else 0], dtype=np.float32)  # 獲取當前狀態
                        action, _ = model.predict(obs, deterministic=True)  # AI 做出行動決策
                        if action == 1:
                            bird.jump()  # AI 控制小鳥跳躍
                    bird.move()  # 更新小鳥位置

                    if mode == "original":
                        if len(pipes) == 0 or pipes[-1].x < WINDOW_WIDTH - 200:
                            is_moving_pipe = score >= 10  # 當分數達到10時，管道開始移動
                            is_clamping_pipe = score >= 20  # 當分數達到20時，管道開始夾動
                            pipes.append(Pipe(is_moving_pipe, is_clamping_pipe))  # 添加新管道
                    elif mode == "shooting":
                        if len(enemies) == 0 or enemies[-1].x < WINDOW_WIDTH - 200:
                            enemies.append(Star(floor_height))  # 添加定義星星

                if mode == "original":
                    WINDOW.blit(background_img, (0, 0))  # 顯示白天背景圖片
                elif mode == "shooting":
                    WINDOW.blit(background_night_img, (0, 0))  # 顯示夜晚背景圖片

                bird.draw()  # 繪製小鳥

                if game_started:
                    if mode == "original":
                        for pipe in pipes:
                            pipe.move()  # 移動管道
                            pipe.draw()  # 繪製管道

                        for pipe in pipes:
                            if bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.pipe_width:
                                if bird.y < pipe.top_pipe_height or bird.y + bird.height > WINDOW_HEIGHT - floor_height - pipe.bottom_pipe_height:
                                    game_over = True  # 遊戲結束
                                    stop_all_music()  # 停止所有音樂
                                    death_display_time = pygame.time.get_ticks()  # 設置死亡顯示時間
                                    death_sound.play()  # 播放死亡音效

                        if bird.y + bird.height >= WINDOW_HEIGHT - floor_height:
                            game_over = True  # 遊戲結束
                            stop_all_music()  # 停止所有音樂
                            death_display_time = pygame.time.get_ticks()  # 設置死亡顯示時間
                            death_sound.play()  # 播放死亡音效

                        if pipes and pipes[0].x < -pipes[0].pipe_width:
                            pipes.pop(0)  # 移除已經移出窗口的管道
                            score += 1  # 增加分數
                    elif mode == "shooting":
                        for enemy in enemies:
                            enemy.move()  # 移定義星星
                            if enemy.update():  # 如定義星星應該移除
                                enemies.remove(enemy)  # 移定義星星
                            else:
                                enemy.draw()  # 繪定義星星

                        for enemy in enemies:
                            if bird.x + bird.width > enemy.x and bird.x < enemy.x + enemy.width:
                                if bird.y < enemy.y + enemy.height and bird.y + bird.height > enemy.y:
                                    game_over = True  # 遊戲結束
                                    stop_all_music()  # 停止所有音樂
                                    death_display_time = pygame.time.get_ticks()  # 設置死亡顯示時間
                                    death_sound.play()  # 播放死亡音效
                            for bullet in bird.bullets:
                                if bullet.x + bullet.width > enemy.x and bullet.x < enemy.x + enemy.width:
                                    if bullet.y < enemy.y + enemy.height and bullet.y + bullet.height > enemy.y:
                                        bird.bullets.remove(bullet)  # 移除擊定義星星的子彈
                                        enemy.got_hit()  # 標定義星星被擊中
                                        score += 1  # 增加分數

                        if bird.y + bird.height >= WINDOW_HEIGHT - floor_height:
                            game_over = True  # 遊戲結束
                            stop_all_music()  # 停止所有音樂
                            death_display_time = pygame.time.get_ticks()  # 設置死亡顯示時間
                            death_sound.play()  # 播放死亡音效

                        if enemies and enemies[0].x < -enemies[0].width:
                            enemies.pop(0)  # 移除已經移出窗口定義星星

                    score_text = font.render("Score: {}".format(score), True, WHITE)
                    WINDOW.blit(score_text, [10, 10])  # 顯示分數

            if game_over:  # 如果遊戲結束
                ai_enabled = False  # 關閉 AI 控制
                current_time = pygame.time.get_ticks()
                if current_time - death_display_time > death_sound.get_length() * 1000:  # 檢查是否播放完死亡音效
                    pygame.mixer.Sound.play(gameover_sound, loops=-1)  # 播放遊戲結束音效
                    if mode == "original":
                        WINDOW.blit(gameover1_img, (0, 0))  # 顯示模式1死亡頁面
                    elif mode == "shooting":
                        WINDOW.blit(gameover2_img, (0, 0))  # 顯示模式2死亡頁面
                else:
                    # 保持黑屏，等待死亡音效播放完畢
                    font = pygame.font.Font(None, 60)
                    text1 = font.render("You're dead", True, WHITE)
                    text_rect1 = text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
                    WINDOW.blit(text1, text_rect1)  # 顯示死亡信息

            elif not game_started:  # 如果遊戲未開始
                font = pygame.font.Font(None, 36)
                text = font.render("Press SPACE to start", True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                WINDOW.blit(text, text_rect)  # 顯示開始提示

        pygame.display.update()  # 更新窗口顯示
        pygame.time.Clock().tick(60)  # 設置遊戲速度為每秒60幀

if __name__ == '__main__':
    main()  # 執行主函數
