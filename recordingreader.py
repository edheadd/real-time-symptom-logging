from audio_recorder import AudioToTextRecorder
def main():
    
    recorder = AudioToTextRecorder()
    recorder.start()
    while True:
        print(recorder.text())
        if recorder.text() == "Stop.":
            break
    recorder.stop()
    recorder.shutdown()

if __name__ == '__main__':
    main()