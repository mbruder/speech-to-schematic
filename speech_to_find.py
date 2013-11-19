import pyaudio
import wave
import os
import urllib2
import time


def find_by_voice():
    
    # Initial configuration
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 4

    # Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)

    frames = []

    # Save voice recording in frames
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	data = stream.read(CHUNK)
	frames.append(data)

    print "* done recording"

    # Save speech, send to Google and look for it in a PDF reader
    filename = save_speech(frames,p)
    component = stt_google(filename)    
    find_in_preview(component)

    # Close stream
    stream.close()
    p.terminate()


def save_speech(data, p):

    # Write speech to a .wav
    filename = 'output_'+str(int(time.time()))
    data = ''.join(data)
    wf = wave.open(filename+'.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(data)
    wf.close()

    # Convert .wav to .flac
    os.system('flac -f ' + filename + '.wav' + ' &> /dev/null')

    return filename


def stt_google(filename):

    # Open .flac speech
    f = open(filename+'.flac','rb')
    flac_cont = f.read()
    f.close()

    # Request STT to Google
    lang_code='es-AR'
    googl_speech_url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&pfilter=2&lang=%s&maxresults=6'%(lang_code)
    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",'Content-type': 'audio/x-flac; rate=16000'}
    req = urllib2.Request(googl_speech_url, data=flac_cont, headers=hrs)
    p = urllib2.urlopen(req)

    # Keep the best match
    res = eval(p.read())
    final_res = res['hypotheses'][0]['utterance']   # try print res['hypotheses'] to understand better 
    
    # Erase audio files from disk
    map(os.remove, (filename+'.flac', filename+'.wav'))
    
    return final_res

def find_in_preview(string):
    
    # Use Applescript to find string in Preview
    cmd = """
    osascript -e 'tell application "Preview" to activate
    set the clipboard to " """ + "\\\"" + string + "\\\"" + """ "
    tell application "System Events"
    	keystroke "f" using command down
    	keystroke "v" using command down
    end tell' 
    """
    os.system(cmd)
    
    return


if(__name__ == '__main__'):
    find_by_voice()
