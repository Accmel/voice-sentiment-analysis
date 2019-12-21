import librosa
from tqdm import tqdm
import numpy as np
import glob

def get_power(filenames):
    print("start get_power ...")
    dim = 771
    power_list = np.zeros((len(filenames), dim))
    for i, filename in tqdm(enumerate(filenames)):
        y, sr = librosa.load(filename,res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.4)
        S = np.abs(librosa.stft(y, n_fft=512))
        power = librosa.power_to_db(S**2, ref=np.max)
        mean = np.mean(power, axis=1)
        mx = np.max(power, axis=1)
        mn = np.min(power, axis=1)
        power = np.hstack((mean, mx, mn))
        power_list[i] = power
    print(f"power size : {power_list.shape}")
    return power_list

if __name__ == '__main__':

    # Dataset1
    filenames = [ f"./dataset1/{i}.wav" for i in range(1, 101) ]

    # Dataset1 augument
    #filenames = [ f"./dataset1/{i}.wav" for i in range(1, 101) ] \
    #            + [ f"./dataset1/white_noise/{i}.wav" for i in range(1, 101) ] \
    #            + [ f"./dataset1/stretch/{i}.wav" for i in range(1, 101) ] \
    #            + [ f"./dataset1/shift/{i}.wav" for i in range(1, 101) ]

    # Dataset2
    #filenames = glob.glob("./ravdess-emotional-speech-audio/*/*")

    power_list = get_power(filenames)
    np.savez_compressed('power-aver.npz', power_list)
    
