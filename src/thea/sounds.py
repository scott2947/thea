import os, math, struct, wave, subprocess


def play_morse_pattern(pattern, wpm=20, freq=750):

    pattern_slug = pattern.replace(".", "o").replace("-", "a").replace(" ", "s")
    filename = f"{pattern_slug}_{wpm}wpm_{freq}hz.wav"
    base_dir = "storage/sounds"
        
    path = os.path.join(base_dir, filename)

    if not os.path.exists(path):
        dot_duration = 1.2 / wpm
        sample_rate = 44100
        audio = []
        letters = pattern.split(" ")
        fade_len = int(sample_rate * 0.005)

        for i, letter in enumerate(letters):
            for char in letter:
                duration = dot_duration * 3 if char == "-" else dot_duration
                num_samples = int(duration * sample_rate)
                
                for s in range(num_samples):
                    val = math.sin(2 * math.pi * freq * s / sample_rate)
                    env = min(1.0, s / fade_len, (num_samples - s) / fade_len)
                    audio.append(struct.pack("<h", int(val * 16384 * env)))
                
                audio.append(struct.pack("<h", 0) * int(dot_duration * sample_rate))
            
            if i < len(letters) - 1:
                audio.append(struct.pack("<h", 0) * int(dot_duration * 2 * sample_rate))

        with wave.open(path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            f.writeframes(b"".join(audio))

    subprocess.run(["afplay", path])


def play_string_as_morse(string, **kwargs):
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '0': '-----', ' ': ' '
    }
    
    pattern = " ".join(morse_dict[char.upper()] for char in string)
    play_morse_pattern(pattern, **kwargs)


if __name__ == "__main__":
    pass
