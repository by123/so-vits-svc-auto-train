import os 

for i in range(1,62):
    vocal = '{}.wav'.format(i)
    accomany = 'b{}.wav'.format(i)
    result = '{}'.format(i)
    os.system('python audio_inference.py -o ade -m G_3000.pth -v ' + vocal +' -a  ' + accomany + ' -r ' + result)