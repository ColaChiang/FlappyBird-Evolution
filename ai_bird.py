import gym  # OpenAI 的 gym 庫，用於建立和訓練強化學習環境
import numpy as np  # 用於數組運算和數據處理
from stable_baselines3 import PPO  # 從 stable_baselines3 庫中導入 PPO 演算法
from stable_baselines3.common.env_util import make_vec_env  # 用於創建向量化環境
import os  # 用於處理文件路徑和文件操作

# 定義 Flappy Bird 環境類別，繼承自 gym.Env
class FlappyBirdEnv(gym.Env):
    def __init__(self):
        super(FlappyBirdEnv, self).__init__()
        # 定義觀察空間，這裡的觀察空間是 5 維的浮點數數組
        self.observation_space = gym.spaces.Box(low=-float('inf'), high=float('inf'), shape=(5,), dtype=np.float32)
        # 定義行動空間，這裡有兩個離散動作：0 和 1
        self.action_space = gym.spaces.Discrete(2)
        self.seed()  # 設置隨機數種子
        self.reset()  # 重置環境狀態

    def seed(self, seed=None):
        # 設置隨機數種子，保證結果的可重現性
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self):
        # 重置小鳥和管道的初始位置
        self.bird_y = 250  # 小鳥的初始高度
        self.bird_velocity = 0  # 小鳥的初始速度
        self.pipe_x = 400  # 管道的初始橫坐標
        self.pipe_y = self.np_random.integers(100, 300)  # 隨機設置管道的初始縱坐標
        self.done = False  # 標記遊戲是否結束
        # 返回初始狀態，包含小鳥的高度、速度、管道的位置和縱坐標差
        return np.array([self.bird_y, self.bird_velocity, self.pipe_x, self.bird_y - self.pipe_y, self.pipe_y], dtype=np.float32)

    def step(self, action):
        # 根據行動更新小鳥的速度和位置
        if action == 1:
            self.bird_velocity = -8  # 如果動作為 1，讓小鳥跳躍
        self.bird_velocity += 0.5  # 模擬重力效果
        self.bird_y += self.bird_velocity  # 更新小鳥的縱坐標
        self.pipe_x -= 5  # 更新管道的橫坐標

        if self.pipe_x < 0:
            # 如果管道移出屏幕，重置管道位置
            self.pipe_x = 400
            self.pipe_y = self.np_random.integers(100, 300)  # 隨機設置新的管道縱坐標

        reward = 1  # 每一步的基礎獎勵為 1
        if self.bird_y < 0 or self.bird_y > 600 or (self.pipe_x < 50 and abs(self.bird_y - self.pipe_y) > 50):
            # 如果小鳥撞到地面或飛出屏幕，或者撞到管道，遊戲結束
            self.done = True
            reward = -100  # 獎勵設為 -100 表示懲罰

        # 返回新的狀態、獎勵、遊戲是否結束和額外信息（此處為空字典）
        state = np.array([self.bird_y, self.bird_velocity, self.pipe_x, self.bird_y - self.pipe_y, self.pipe_y], dtype=np.float32)
        return state, reward, self.done, {}

    def render(self, mode='human'):
        pass  # 渲染環境，此處為空實現

# 評估模型性能的函數
def evaluate_model(env, model, num_episodes=10):
    all_rewards = []  # 儲存每次評估的總獎勵
    for _ in range(num_episodes):
        obs = env.reset()  # 重置環境
        total_reward = 0  # 初始化總獎勵
        done = False  # 標記遊戲是否結束
        while not done:
            action, _ = model.predict(obs, deterministic=True)  # 使用模型預測動作
            obs, reward, done, _ = env.step(action)  # 執行動作，更新狀態和獲得獎勵
            total_reward += reward  # 累計獎勵
        all_rewards.append(total_reward)  # 將此次回合的總獎勵加入列表
    mean_reward = np.mean(all_rewards)  # 計算平均獎勵
    return mean_reward

# 加載或訓練新模型的函數
def load_model():
    model_path = "best_ppo_flappybird.zip"  # 模型保存的路徑
    if os.path.exists(model_path):
        model = PPO.load(model_path)  # 如果模型文件存在，則加載模型
        print("Model loaded successfully")
    else:
        print("Model not found, training new model")
        env = make_vec_env(FlappyBirdEnv, n_envs=4)  # 創建向量化環境，包含 4 個環境實例
        model = PPO("MlpPolicy", env, verbose=1)  # 使用 PPO 演算法和 MlpPolicy 訓練模型
        model.learn(total_timesteps=100000)  # 訓練模型 100,000 個時間步
        model.save(model_path)  # 保存訓練好的模型
    return model

# 主程序部分
if __name__ == "__main__":
    env = make_vec_env(FlappyBirdEnv, n_envs=4)  # 創建向量化環境，包含 4 個環境實例
    model = PPO("MlpPolicy", env, verbose=1)  # 使用 PPO 演算法和 MlpPolicy 訓練模型
    total_timesteps = 500000  # 設定總訓練步數
    num_eval_episodes = 10  # 設定每次評估的回合數
    eval_interval = 50000  # 設定評估間隔
    early_stopping_patience = 3  # 設定早停耐心次數
    no_improvement_steps = 0  # 初始化無改進步數計數
    best_mean_reward = -np.inf  # 設定最佳平均獎勵初始值

    for i in range(total_timesteps // eval_interval):
        model.learn(total_timesteps=eval_interval)  # 訓練模型指定步數
        mean_reward = evaluate_model(env, model, num_eval_episodes)  # 評估模型性能
        print(f"Evaluation after {eval_interval * (i+1)} timesteps: Mean Reward = {mean_reward}")

        if mean_reward > best_mean_reward:
            best_mean_reward = mean_reward  # 更新最佳平均獎勵
            no_improvement_steps = 0  # 重置無改進步數計數
            print("New best model found")
            model.save("best_ppo_flappybird")  # 保存新的最佳模型
        else:
            no_improvement_steps += 1  # 增加無改進步數計數
            if no_improvement_steps >= early_stopping_patience:
                print("Early stopping triggered")
                break

    print("Training completed")
    model.save("ppo_flappybird")  # 保存最終訓練好的模型
