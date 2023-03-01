## 注意事项：

- 请及时修改server的端口号以免出错

- 每个server的调度权重目前被硬编码至启动函数中

  ```python
  # ip port weight
  asyncio.run(main("localhost", 50050, 3))
  ```

- 需要重新编译一下protobuf文件，如何编译请查阅：https://www.jianshu.com/p/43fdfeb105ff