import os
import shutil
import subprocess
import argparse

def slice(output, origin):
    path = '/root/origin/' + origin
    os.system('python audio-slicer/slicer2.py ' + path + ' --out ' + output + ' --db_thresh -40  --min_length 5000  --min_interval 300  --hop_size 10  --max_sil_kept 1000')

def moveSampleToRaw(output):
    dataset_path = 'dataset_raw'
    path = dataset_path + '/' + output
    folder = os.path.exists(path)
    if folder:
        shutil.rmtree(path)
    print('移动样本到dataset_raw')
    shutil.move(output, dataset_path)

def prepareTrain():
    print('样本重采样至44100Hz单声道')
    os.system("python resample.py")
    print('自动划分训练集、验证集，以及自动生成配置文件')
    os.system("python preprocess_flist_config.py --speech_encoder vec768l12 --vol_aug")
    print('生成hubert与f0')
    os.system("python preprocess_hubert_f0.py --f0_predictor pm --use_diff")
    print('vec768l12带响度嵌入')
    os.system("cp pretrain/so-vits-svc/768l12-vol_D_0.pth logs/44k/D_0.pth") 
    os.system("cp pretrain/so-vits-svc/768l12-vol_G_0.pth logs/44k/G_0.pth")
    
def saveModel(output, step):
    saveFile = '/root/models/' + output + '/'
    print(saveFile)
    folder = os.path.exists(saveFile)
    if not folder:
        os.makedirs(saveFile)
        print('makedirs')
    shutil.copy('logs/44k/G_' + step +'.pth' , saveFile)
    shutil.copy('logs/44k/D_' + step +'.pth', saveFile)
    shutil.copy('logs/44k/config.json', saveFile)


if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Audio Train')
    parser.add_argument('--output', '-o', type = str, default = 'by', required = True, help = '训练的声音唯一标志')
    parser.add_argument('--origin', '-n', type = str, default = 'origin.wav', required = True, help = '待训练的人声的名称,放在 /root/origin 下')
    parser.add_argument('--step', '-s', type = str, default = '3000' , help = '训练步数，用字符串类型')
 
    args = parser.parse_args()
    print('训练名称:' + args.output)
    print('训练步数:' + args.step)
    print('训练文件名称:' + args.origin)

    # 训练的声音唯一标志
    output = args.output
    # 训练步数，用字符串类型
    step = args.step
    # 待训练的人声的名称,放在 /root/origin
    origin = args.origin

    print('-----音频切片-----')
    slice(output, origin)
    print('-----样本集移动到 dataset_raw 文件夹-----')
    moveSampleToRaw(output)
    print('-----训练前准备-----')
    prepareTrain()
    print('-----准备工作完成，开始训练-----')
    result = subprocess.run('python train.py -c configs/config.json -m 44k -step ' + step, shell=True, capture_output=False, text=True)
    if result.returncode == 0:
        print('-----开始保存模型-----')
        saveModel(output, step)
        print('-----完成-----')
    else:
        print("Python脚本执行失败！")


##### 测试
# python audio_train.py -o 'ade' -n 'ade.wav'
# python audio_train.py -o 'ade' -n 'ade.wav' -s '3000'