# 笔记

+ 模拟(simulation): 从当前节点开始到终端节点的一个移动的序列，移动的动作使用Rollout策略来选择，通常是均匀随机分布

+ 节点扩展：在初始状态，我们位于游戏树的根节点，其他的节点都是未访问的。MCTS也是一样，节点分为访问过的和未访问过的。被访问过的节点意味着某个模拟过程是以它为起点的，即它至少被评估过一次。如果一个节点的所有子节点都被访问过了，那这个节点就称为是完全扩展的，否则就是未完全扩展的。
  在搜索的一开始，根节点的所有子节点都是未被访问的，如果选择了一个，开始向下rollout，第一次模拟就随之开始。模拟过程中由rollout策略函数选择的节点是不会被标记为已访问过的，只有从模拟开始的节点被标记为已访问过。

+ 反向传播：当完成对一个节点的模拟（rollout到了叶子节点或达到一定深度），其结果已准备好传播回当前游戏树的根节点，然后模拟开始的节点被标记为已访问。
  + 反向传播是从叶节点（模拟开始）到根节点的遍历。模拟结果被传送到根节点，并更新反向传播路径上每个节点的统计信息。反向传播保证每个节点的统计信息能够反映该节点所有后代的模拟结果
  + 每个节点有两个属性Q收益，N访问次数
  + Q(v)：总模拟收益是节点v的一个属性，最简单形式的就是所有考虑的节点的模拟结果之和
    N(v)：总访问次数是节点v的另一个属性，代表这个节点有多少次出现在反向传播路径上
  + 每个访问过的节点都需要维护这两个值。收益高的节点是接下来探索的优秀候选节点，但那些访问次数低的节点也同样值得关注（因为它没有被探索完全）。

+ UCT函数：
  + $UCT(v_i,v)=\frac{Q(v_i)}{N(v_i)}+c*(\frac{log(N(v))}{N(v_i)})^{1/2}$
  + UCT是关于节点$v$和其子节点$v_i$的函数，第一部分是exploitation component，为平均每次的收益，可看做节点$v_i$的胜率估计，第二项是exploration component，使得胜率较小、访问次数较小的节点也有可能被选到，从而充分探索，c为折中系数

```python
class MCTS:
    def UctSearch(s0):
        new a root node v0         // s0为初始状态，v0为根节点
        v0.state=s0,v0.action=null,v0.N=0,v0.Q=0
        while within computable budget:
            v=TreePolicy(v0)    //选择一个叶子节点
            r=DefaultPolicy(v.state)  //向下随机rollout
            Backup(v,r)  //将评估值反向传播
        return BestChild(v0,0).action   //选取在状态s0下的最优动作，只考虑Q/N
    def TreePolicy(v):
        while v.state is not terminal: //v不是终止节点
            if v is not fully expanded:
                return Expend(v)
            else
                v=BestChild(v,c)  //c为折中系数
        return v
    def Expend(v):
        choose action from A(state(v)) which has not been chosen
        v1.parent=v, v.child.append(v1)
        v1.state=f(v.state,action)  //v的状态执行动作action
        v1.action=action
        return v1
    def BestChild(v,c):    //选择uct值最大的孩子节点
        max_v=null,max_uct=-inf
        for v_ in v.children:
            uct=v_.Q/v_.N + c* math.sqrt(2*ln(v.N)/v_.N)
            if uct>max_uct:
                max_v=v_
                max_uct=uct
        return max_v    
    def DefaultPolicy(state):
        while state is not terminal:
            action=A(state)    //从当前状态的可执行动作中随机均匀选择一个
            state=f(state,action)
        return reward of state s
    def Backup(v,r):
        while v != null:
            v.N+=1
            v.Q+=r   //根据玩家来更新Q值
            r=-r
            v=v.parent
```




+ 对于一个棋盘，动作有N*N+1种，包括pass
+ coords.py是棋盘坐标模式的转换，如：
  + from_flat() 将一个一维的棋盘转换成二维的
  + to_flat() 将二维转为一维
+ 白子为-1，黑子为1，若要转换颜色则乘-1即可
+ komi是什么？
+ timestep: 存储了每一步的棋局的信息
   + observations: 一个字典，有两位玩家的信息
     + info_state：当前的棋盘状况，一个1x25的数组，0代表白子，1代表空位，2代表黑子，info_state[0]为黑子玩家，info_state[1]为白子玩家
     + legal_actions: 当前的合法落棋位置，一个数组 0~25， 25代表pass
     + current_player: 0为黑手，1为白手
   + rewards：黑手和白手的奖赏，一个列表，如[0,0]
   + discounts：黑手和白手的，一个列表
   + step_type：枚举量，三种：0：first；1：middle；2：last



























+ 模拟(simulation): 从当前节点开始到终端节点的一个移动的序列，移动的动作使用Rollout策略来选择，通常是均匀随机分布

+ 节点扩展：在初始状态，我们位于游戏树的根节点，其他的节点都是未访问的。MCTS也是一样，节点分为访问过的和未访问过的。被访问过的节点意味着某个模拟过程是以它为起点的，即它至少被评估过一次。如果一个节点的所有子节点都被访问过了，那这个节点就称为是完全扩展的，否则就是未完全扩展的。
  在搜索的一开始，根节点的所有子节点都是未被访问的，如果选择了一个，开始向下rollout，第一次模拟就随之开始。模拟过程中由rollout策略函数选择的节点是不会被标记为已访问过的，只有从模拟开始的节点被标记为已访问过。

+ 反向传播：当完成对一个节点的模拟（rollout到了叶子节点或达到一定深度），其结果已准备好传播回当前游戏树的根节点，然后模拟开始的节点被标记为已访问。
  + 反向传播是从叶节点（模拟开始）到根节点的遍历。模拟结果被传送到根节点，并更新反向传播路径上每个节点的统计信息。反向传播保证每个节点的统计信息能够反映该节点所有后代的模拟结果
  + 每个节点有两个属性Q收益，N访问次数
  + Q(v)：总模拟收益是节点v的一个属性，最简单形式的就是所有考虑的节点的模拟结果之和
    N(v)：总访问次数是节点v的另一个属性，代表这个节点有多少次出现在反向传播路径上
  + 每个访问过的节点都需要维护这两个值。收益高的节点是接下来探索的优秀候选节点，但那些访问次数低的节点也同样值得关注（因为它没有被探索完全）。

+ UCT函数：
  + $UCT(v_i,v)=\frac{Q(v_i)}{N(v_i)}+c*(\frac{log(N(v))}{N(v_i)})^{1/2}$
  + UCT是关于节点$v$和其子节点$v_i$的函数，第一部分是exploitation component，为平均每次的收益，可看做节点$v_i$的胜率估计，第二项是exploration component，使得胜率较小、访问次数较小的节点也有可能被选到，从而充分探索，c为折中系数

```python
class MCTS:
    def UctSearch(s0):
        new a root node v0         // s0为初始状态，v0为根节点
        v0.state=s0,v0.action=null,v0.N=0,v0.Q=0
        while within computable budget:
            v=TreePolicy(v0)    //选择一个叶子节点
            r=DefaultPolicy(v.state)  //向下随机rollout
            Backup(v,r)  //将评估值反向传播
        return BestChild(v0,0).action   //选取在状态s0下的最优动作，只考虑Q/N
    def TreePolicy(v):
        while v.state is not terminal: //v不是终止节点
            if v is not fully expanded:
                return Expend(v)
            else
                v=BestChild(v,c)  //c为折中系数
        return v
    def Expend(v):
        choose action from A(state(v)) which has not been chosen
        v1.parent=v, v.child.append(v1)
        v1.state=f(v.state,action)  //v的状态执行动作action
        v1.action=action
        return v1
    def BestChild(v,c):    //选择uct值最大的孩子节点
        max_v=null,max_uct=-inf
        for v_ in v.children:
            uct=v_.Q/v_.N + c* math.sqrt(2*ln(v.N)/v_.N)
            if uct>max_uct:
                max_v=v_
                max_uct=uct
        return max_v    
    def DefaultPolicy(state):
        while state is not terminal:
            action=A(state)    //从当前状态的可执行动作中随机均匀选择一个
            state=f(state,action)
        return reward of state s
    def Backup(v,r):
        while v != null:
            v.N+=1
            v.Q+=r   //根据玩家来更新Q值
            r=-r
            v=v.parent
```

## 围棋环境中的mcts

+ 第一次模拟：从根节点到叶节点；第二次模拟：叶节点扩展，rollout直到游戏结束
+ select: 从根节点开始选择 Q+u值最大的节点直到叶节点，u依赖于节点的先验概率p，从策略/估值网络中可获得
+ expand: 