# m3u8_To_mp4
将通过uc浏览器下载m3u8视频文件转化成mp4文件,具体方法如下：
通过连接手机，将uc下载目录下的视频缓存:videodata，完整的复制到PC端某个目录下，为了便于操作m3u8a.py也需要在该目录下。

特别强调，m3u8a.py必须和m3u8文件在同一个目录下面。
支持三种方式
1、m3u8文件：
使用方法：python m3u8a.py xxxx.m3u8
xxxx.m3u8为当前目录下的m3u8文件。
2、批量处理当前目录下所有m3u8文件
使用方法：python m3u8a.py .
"."表示为当前路径
3、指定m3u8目录
这种场景是m3u8文件丢失，只有缓存的文件目录
python m3u8a.py xxxx
xxxx为m3u8中ts的目录
