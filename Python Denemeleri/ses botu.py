from gtts import gTTS
import os

file_adi2="Yazi ciktisi"
 
cikti=gTTS(text="En iyi programlama dili Python'dir",lang="tr")
cikti.save(file_adi2+".mp3")
os.system(file_adi2+".mp3")