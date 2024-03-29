import os
mp4=r"E:\lsp\番剧\ALL\懲罰指導（おしおき）～学園令嬢更性計画\3.mkv"
ass=os.path.splitext(mp4)[0]+'.ass'

newMP4=os.path.dirname(mp4)+'\\111'+os.path.splitext(mp4)[1]
os.system("ffmpeg -i \"%s\" -i \"%s\" -c copy \"%s\"" % (mp4,ass,newMP4))#ffmpeg -i 1.mp4 -i 1.ass -c copy 2.mp4



os.remove(mp4)
os.remove(ass)
os.rename(newMP4,mp4)