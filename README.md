# AI Audio 配置说明

---
#### 准备工作

 * 将 audio_slicer 整个文件夹放在 so-vits-svc 目录下
 * 安装必要的 python 库
   * pip install pytest-shutil
   * pip install numpy
   * pip install librosa
   * pip install soundfile
   * pip install TTS

---
#### 目录说明
根目录
* <strong>models</strong> 
训练出模型的存放位置，一共有3个文件
    * config.json 模型的配置信息
    * G_3000.pth 主推理模型，用于推理
    * D_3000.pth 临时记录推理模型，用于再训练
* <strong>origin</strong> 
用于存放待训练的音频
* <strong>vocal</strong> 
用于存放替换目标的音频人声
* <strong>accompany</strong> 
用于存放目标的音频伴奏
* <strong>temp_result</strong> 
用于存放已经替换目标音频的人声，如果是 tts 文字转声音 + 声音替换声音，则此结果为最终结果
* <strong>result</strong> 
用于存放已经替换目标音频的人声与伴奏合成的结果
* <strong>so-vits-svc</strong> 
主训练预测模块，自动化脚本存放在此目录下


---
#### 脚本说明
* <strong>audio_train.py</strong> 
包含声音切片，声音训练模型的脚本
    * -o 训练的声音唯一标志
    * -n 待训练的人声的名称，放在 /root/origin 
    * -s 训练步数，用字符串类型

> 不带最大训练步数(默认3000步)
> <strong>python audio_train.py -o 'ade' -n 'ade.wav'</strong>
> 带最大训练步数
> <strong>python audio_train.py -o 'ade' -n 'ade.wav' -s '3000'</strong>
* <strong>audio_inference.py</strong> 
包含声音预测，人声和伴奏合成的脚本
    * -o 训练的声音唯一标志
    * -m 模型名称，模型在 /root/models/#output#/xxx
    * -v 目标音频人声，放在 /root/vocal 
    * -a 目标音频伴奏,放在 /root/accompany 
    * -r 保存结果
    语音替换的结果，放在 /root/temp_result 下
    与伴奏合成的结果，放在 /root/result 下

> 用于人声替换人声，tts转语音
> <strong>audio_inference.py -o 'ade' -m 'G_3000.pth' -v 'vocal.wav'</strong>
> 用于人声和伴奏的合成
> <strong>paudio_inference.py -o 'ade' -m 'G_3000.pth' -v 'vocal.wav' -a 'accompany.wav'</strong>
* <strong>train.py</strong> 
svc 的训练脚本，直接替换即可
* <strong>inference_main.py</strong> 
svc 的预测脚本，直接替换即可

