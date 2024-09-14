from audio_recorder import AudioToTextRecorder
def main():
    recorder = AudioToTextRecorder()
    recorder.start()
    print(recorder.text())
    recorder.stop()
    

if __name__ == '__main__':
    main()