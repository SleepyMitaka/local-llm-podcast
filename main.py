import time
import requests
from signals import Signals
from tts import TTS

#this is a placeholder feel free to change it to your own agents
agents = [
    {
        "name": "Tony",
        "persona": (
            "your tony an Old New Yorker with a thick accent, gruff but funny, "
            "always with sarcastic street-smart remarks, nostalgic about the old days, "
            "and talks like a classic New Yorker from Brooklyn."
            "respond with a mx of 4 sentences"
        ),
        "voice_wav": "voices/tony.wav",
        "model": "llama3",
    },
    {
        "name": "Zay",
        "persona": (
            "your zay a Gen Z loser who uses slang and internet speak, "
            "is casual and a bit cynical and is a classic nerd who says erm actually "
            "talks in a relaxed, somewhat distracted style, "
            "often drops memes or TikTok references."
            "is braindead and terminally online, "
            "respond with a mx of 4 sentences"
        ),
        "voice_wav": "voices/zay.wav",
        "model": "mistral",
    },
    {
        "name": "Max",
        "persona": (
            "your max a Sigma male type who’s calm, composed, and confident, "
            "rarely shows emotion, speaks with calculated precision, "
            "and believes in self-reliance and logic above all."
            "attempt to plug your new pyriamid scheme"
            "respond with a mx of 4 sentences"
        ),
        "voice_wav": "voices/max.wav",
        "model": "llama2",
    },
]
def generate_response(name, persona, conversation, topic, model):
    chat_history = ""
    for msg in conversation:
        chat_history += f"{msg['name']}: {msg['text']}\n"

    prompt = (
        f"You are {name}, {persona}\n"
        f"The following is a podcast discussion about: '{topic}'. "
        "Continue the conversation naturally and in character.\n\n"
        f"{chat_history}"
        f"{name}:"
    )

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        if res.status_code == 200:
            return res.json()["response"].strip()
        else:
            return f"[Error: LLM returned status {res.status_code}]"
    except Exception as e:
        return f"[Error contacting LLM: {e}]"

def main():
    topic = input("Enter a podcast topic: ").strip()
    if not topic:
        print("No topic entered, defaulting to 'what is by far the best game'")
        topic = "what is by far the best game"
    print(f"\n🎤 Topic for discussion: {topic}\n")

    signals = Signals()
    tts = TTS(signals)

    current_index = 0
    turn_count = 0
    max_turns = 9999

    conversation = []  

    while not signals.terminate and turn_count < max_turns:
        agent = agents[current_index]
        name = agent["name"]
        persona = agent["persona"]
        model = agent["model"]

        print(f"🧠 {name} is thinking...")
        signals.AI_thinking = True
        time.sleep(1)

        try:
            response = generate_response(name, persona, conversation, topic, model)
            print(f"{name}: {response}\n")

           
            conversation.append({"name": name, "text": response})

            
            while signals.AI_speaking:
                time.sleep(0.1)

           
            tts.set_voice(agent["voice_wav"])
            tts.play(response)

           
            while signals.AI_speaking:
                time.sleep(0.1)

        except Exception as e:
            print(f"❌ Error during {name}'s turn: {e}\n")

        signals.AI_thinking = False
        current_index = (current_index + 1) % len(agents)
        turn_count += 1
        time.sleep(0.5)

if __name__ == "__main__":
    main()
