# copymanga_downloader

❤ 拷贝漫画下载器❤

## 特点

1. 采用多线程下载及多线程解析,让你快人一步![](README_md_files/102b9dc0-869f-11ee-838f-8740f019a9b0.jpeg?v=1&type=image)
2. 可以自定义章节下载,支持失败重连
3. 纯api接口访问,本地解密,运行速度快
4. 支持下载评论并绘制为图片查看
5. 无需登录配置什么的,没有限制,打开即下
6. 自动过滤尾页汉化组广告(准确度极高) ----可选
7. 代码工整好看,可读性高,不可替代性强(~~屎山~~)
8. 增加ai提升清晰度(吃cpu) 使用 [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)

## 截图展示

![](README_md_files/2bfd7ec0-48c3-11ee-8344-a91988da3ff6.jpeg?v=1&type=image)
![](README_md_files/376347e0-48c3-11ee-8344-a91988da3ff6.jpeg?v=1&type=image)
![](README_md_files/a6d17b70-4a11-11ee-b416-f5e0ee161af8.jpeg?v=1&type=image)
![](README_md_files/42439c10-6127-11ee-9130-ebfc613c0c36.jpeg?v=1&type=image)
![](README_md_files/7bead980-6774-11ee-98e6-535fc83230f7.jpeg?v=1&type=image)

## 食用说明

1. 右上角下载zip,解压打开,在当前窗口打开cmd
2. 输入 `pip install -r requirements.txt`
3. 按照需要自行修改 config.json 中的参数
4. 双击 .bat 程序 启动!!!

## 更新日志

### 0923

- 重构评论绘制算法，使用 `font.getbbox()` 函数定位文字宽高，更加准确
- 识别字幕组广告功能开关修改至配置文件 `config.json` 中

### 0912

- 下载从直接下载到指定目录改为下载至当前文件夹临时目录然后移动至指定目录
- ai超分图片选项人性化
- 增加下载输出格式（jpg|cbz） 从配置文件修改
