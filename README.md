# 拾见校园交互原型

本目录包含“校园失物招领小程序”的九页原型，供软件工程作业展示。页面中的物品和联系方式均为演示数据。

当前目录采用“校园线索卡”视觉方案。[在线体验新版原型](https://grim761.github.io/campus-lost-found-prototype/)。博客草稿仍为未发布状态。

- [交互展示页](index.html)与[样式文件](style.css)：无需安装依赖，直接在浏览器打开 `index.html`；可点击体验浏览、搜索、发布、查看详情和状态更新。
- [Slicerflow 原型源文件](拾见校园.slicerflow.yaml)：在 [Slicerflow Prototyping](https://slicerflow.live/prototype/) 的 Code 标签粘贴文件内容，即可查看九页画板和预设交互流程。
- [浏览与搜索页面](screens-discovery.png)、[发布与状态管理页面](screens-publishing.png)、[无连线九页总览](storyboard-clean.png)与[使用流程图](flowchart.png)。

展示图由 `render_storyboard.py` 根据 Slicerflow 源文件重新绘制，流程图由 `render_flowchart.py` 生成；两者已改为纸张底色、深蓝与陶土色。旧版工具画布导出保留在 `storyboard.png`，其中有工具的导航连线，本次展示请使用无连线图。

本项目仅为交互原型。新发布的信息和状态更新只保留在当前浏览页面，刷新后会清除；不会保存或提交真实失物信息。
