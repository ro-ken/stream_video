## 演示说明

> 注明: 初始代码为周俶易开发，也就是仓库first commit的阶段，需要的可以回退到第一个版本自取
>
> 分布式人脸识别系统演示.pdf 为王国琨编写，是对初始演示系统的解释
>
> 后面为了演示（FIFO/FAIR）调度效果，在其基础上进行修改，以下为演示说明

**1、硬件**

- 3块板卡（最少）
- 三台显示器

**2、搭配**

- 三块板子分别连三台显示器，分别跑server.py

- 另找一块板子，可以是pc，跑master.py,和多个client.py

**3、演示顺序**

- 先启动master.py
- 修改server.py要连接的master地址，以及其自身地址
- 修改clinet.py要连接master的地址

- 可以修改master中的调度策略  **FIFO/FAIR**重新演示

**4、演示效果**

- 当server多于client时，client的任务得到执行，在server端会实时显示效果
- 当client多于server时，多于的client对等待，等到server有空闲时得到执行
- 当多个client等待，谁会先执行，看调度策略
  - FIFO，**先启动**的先执行
  - FAIR，谁的**优先级高**先执行
