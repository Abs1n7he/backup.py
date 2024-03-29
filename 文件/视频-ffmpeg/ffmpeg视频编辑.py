import os
mp4=r"E:\lsp\番剧\●彼女\僕だけのヘンタイカノジョ 2もっと.mp4"


newMP4=os.path.dirname(mp4)+'\\temp'+os.path.splitext(mp4)[1]
print(newMP4)

#os.system('ffmpeg -hwaccel cuvid -c:v h264_cuvid -i "%s" -c:v h264_nvenc "%s" -r 40 -b:v 3M -ss 00:03 -to 00:08  ' % (mp4,newMP4))#40帧 3000比特率

os.system('ffmpeg -hwaccel cuvid -c:v h264_cuvid -i "%s" -c:v h264_nvenc -ss 00:17 -to 15:45 "%s"' % (mp4,newMP4))#-ss 00:03 -to 00:08 裁剪		 

os.remove(mp4)
os.rename(newMP4,mp4)