

寻找柱子的导航机器人

![map](https://github.com/user-attachments/assets/4548cdfa-fbea-47af-87e7-cf186edc299e)



机器人（turtlebot）在已知静态地图的情况寻找柱子。柱子的位置未知。机器人依次寻找柱子，每次找到柱子就在柱子前 15 厘米的范围内完全停止两秒钟，表示找到柱子。



https://github.com/user-attachments/assets/db8ab7be-58ca-48dc-801d-c226bba164f6

### 功能实现
我将该任务划分为两个部分
1.导航：机器人在静态地图内导航到航点
2.识别柱子:机器人识别的到柱子，从航点出发向它靠近。在距离柱子15s时候，机器人停留3s。
两个任务之间使用smatch状态机进行切换
