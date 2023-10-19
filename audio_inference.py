import os
from pydub import AudioSegment
import soundfile
import argparse

def inference(output, model, vocal, vocal_path):
    model_path = '/root/models/' + output + '/' + model
    model_config = '/root/models/' + output + '/config.json'
    vocal_path = '/root/vocal/' + vocal
    os.system('python inference_main.py -m ' + model_path + ' -c ' + model_config + ' -n ' + vocal_path + ' -t 0 -s ' + output + ' -f0p crepe -r ' + vocal_path)

    
def mergeAudio(vocal_path, accompany, res_path):
    vocalSeg = AudioSegment.from_wav(vocal_path)
    # 增加/减少音量
    vocal = vocal[:] + 8
    accompanySeg = AudioSegment.from_wav('/root/accompany/' + accompany)
    # accompany = accompany[:] - 10

    outout = AudioSegment.overlay(vocalSeg, accompanySeg)
    outout.export(res_path, format = "wav")


if __name__=="__main__":

    parser = argparse.ArgumentParser(description='AI Audio')
    parser.add_argument('--output', '-o', type = str, default = 'by', required = True, help = '训练的声音唯一标志')
    parser.add_argument('--model', '-m', type = str, default = 'G_3000.pth' , required = True, help = '模型名称, 模型在 /root/models/#output#/xxx')
    parser.add_argument('--vocal','-v', type=str, default = 'vocal.wav', required = True, help = '目标音频人声,放在 /root/vocal 下')
    parser.add_argument('--accompany','-a', type=str, help = '目标音频人声,放在 /root/accompany 下')
    parser.add_argument('--result','-r', type=str, default = 'result.wav', required = True, help = '保存结果, 语音替换的结果，放在 /root/temp_result 下，和伴奏合成的结果，放在 /root/result 下')


    args = parser.parse_args()
    output = args.output
    print('训练名称:' + output)

    model = args.model
    print('模型名称:' + model)

    vocal = args.vocal
    print('目标音频人声名称:' + vocal)

    vocal_path = '/root/temp_result/' + args.result
    
    if args.accompany:
        accompany = args.accompany
        res_path = '/root/result/' + args.result
        print('目标音频伴奏名称:' + args.accompany)

    
    print('保存目录:' + result)
    print('-----开始预测-----')
    inference(output, model, vocal, vocal_path)

    if args.accompany:
        print('-----开始合并人声和伴奏-----')
        mergeAudio(vocal_path, accompany, res_path)
        print('合并完成，输出 /root/results/xxx.wav')
    
    
#### python 用于人声替换人声，tts转语音
# audio_inference.py -o 'ade' -m 'G_3000.pth' -v 'vocal.wav'

#### python 用于人声和伴奏的合成
# audio_inference.py -o 'ade' -m 'G_3000.pth' -v 'vocal.wav' -a 'accompany.wav'