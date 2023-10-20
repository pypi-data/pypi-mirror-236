from scipy.signal import resample
from sys import argv, stderr
import soundfile as sf

bold = lambda s: f"\x1b[1m{s}\x1b[0m"

USAGE = f"""{bold('Usage:')} {argv[0]} <audio_file> <multiplier> [file_ext]
	audio_file:
		the file containing audio to speed up
	multiplier:
		the speed multiplier, aka multiply the audio's speed by <multiplier>
	file_ext:
		must be one of ('mp3', 'wav')
		default: 'wav'"""

def main():
	if len(argv) < 2:
		print(USAGE, file=stderr)
		exit(1)

	input_file = argv[1]
	multiplier = float(argv[2])
	try:
		file_ext = argv[3]
	except IndexError:
		file_ext = "mp3"

	if file_ext != "wav" and file_ext != "mp3":
		print(f"{bold('file_ext')} is not one of ('{bold('wav')}', '{bold('mp3')}').\n", file=stderr)
		print(USAGE, file=stderr)
		exit(1)

	input_filename = input_file[:input_file.index('.')]
	output_filename = f"{input_filename}-spedup-{multiplier}x.{file_ext}"

	audio, samplerate = sf.read(input_file)
	spedup_audio = resample(audio, int(len(audio) * (1 / multiplier)))
	sf.write(output_filename, spedup_audio, samplerate)

if __name__ == '__main__':
	main()
