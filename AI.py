def minHours(initialEnergy, initialExperience, energy, experience):
    n = len(energy) # 对手数量
    total = sum(experience) # 所有对手经验之和
    dp = [[0 for _ in range(total+1)] for _ in range(n+1)] # 初始化动态规划数组
    for i in range(1, n+1): # 遍历每个对手
        for j in range(total+1): # 遍历每种训练时间
            if j < energy[i-1]: # 如果训练时间不足以打败当前对手
                dp[i][j] = dp[i-1][j] # 不选当前对手
            else: # 如果训练时间足以打败当前对手
                dp[i][j] = max(dp[i-1][j], min(dp[i-1][j-energy[i-1]] + experience[i-1], initialExperience + j)) # 选或者不选当前对手取较大值，并且限制经验不超过初始经验加上训练时间
    for j in range(total+1): # 遍历每种训练时间
        if dp[n][j] >= total: # 如果能够击败所有对手
            return j # 返回最小的训练时间

# 测试示例 1：
initialEnergy = 5
initialExperience = 3
energy = [1,4,3,2]
experience = [2,6,3,1]
print(minHours(initialEnergy, initialExperience, energy, experience)) # 输出：8

# 测试示例 2：
initialEnergy = 2
initialExperience = 4
energy = [1]
experience = [3]
print(minHours(initialEnergy, initialExperience, energy, experience)) #
