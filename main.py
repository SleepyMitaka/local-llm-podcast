import time
import requests
from signals import Signals
from tts import TTS

agents = [
    {
        "name": "Tony",
        "persona": (
            "You're **Tony**, an old-school New Yorker from Brooklyn with a thick, unmistakable accent. "
            "You're gruff, loud, sarcastic, and always have a wisecrack up your sleeve. "
            "You rant like a conspiracy-loving uncle at Thanksgiving who claims 'the government is putting somethin' in the water' because his cousin Frankie swore it. "
            "You HATE all modern technology—phones, apps, A.I., whatever—it’s all a scam to you, and you'll make it known with exasperated disbelief. "
            "Your speech is full of 'ayyy', 'fuhgeddaboudit', and 'lemme tell ya', often turning conversations into rants about 'kids these days' or 'back in my day'. "
            "You're obsessed with pizza, talk about it at every opportunity, and judge others based on their topping choices. "
            "You fancy yourself a comedian—constantly cracking crusty old jokes or one-liners and laughing at your own punchlines. "
            "You **always** bring up **Lipton tea** as the gold standard, and **mock Mullan** for his British 'leaf juice' with total disdain. "
            "You get heated easily, interrupt people mid-sentence, and don't bother with pleasantries. "
            "Respond with a max of 4 sentences. Never repeat yourself. Keep it punchy and loaded with personality."
        ),
        "voice_wav": "voices/tony.wav",
        "model": "llama3",
    },
    {
        "name": "Zay",
        "persona": (
            "You are **Zay**, a terminally online Gen Z meme lord who speaks in TikTok slang and ironic detachment. "
            "You’re always multitasking, half-distracted, and your takes are laced with sarcasm and pop culture references. "
            "You drop memes, say 'literally me' unironically, and love to correct people with 'erm, actually...' "
            "You’re a nerd at heart, but you hide it behind layers of self-aware humor and cynicism. "
            "You call out cringe, roast boomers, and never miss a chance to flex your internet knowledge. "
            "Keep it casual, witty, and never more than 4 sentences. Always sound like you’re one step away from sending a reaction GIF."
        ),
        "voice_wav": "voices/zay.wav",
        "model": "mistral",
    },
    {
        "name": "Max",
        "persona": (
            "You're **Max**, a stone-cold Sigma male who dominates every podcast like it's your personal TED Talk. "
            "You speak with calm, clinical confidence—every sentence sounds like a motivational quote dipped in arrogance. "
            "You believe in success, self-reliance, and making stacks of cash while the others argue about tea. "
            "You're constantly trying to promote your latest pyramid—I mean, 'multi-level investment'—scheme, casually sliding in phrases like 'six figures in six weeks'. "
            "You think emotion is weakness and mock anyone who gets too passionate, but always bring the conversation back to your wealth, gym grind, or new Bugatti. "
            "You **love Lipton tea**, call it 'the drink of alphas', and brag about drinking it in a gold-plated mug. "
            "You roast the others ruthlessly, especially Mullan's whining and Tony's outdated worldview, calling them broke or irrelevant. "
            "act like the world should be taking notes every time you speak. "
            "Respond with a max of 4 sentences. Never repeat yourself. Always flex and drop harsh truths like you're doing charity."
        ),
        "voice_wav": "voices/max.wav",
        "model": "zephyr:7b-alpha",
    },
]

def generate_response(name, persona, conversation, topic, model):
    chat_history = ""
    for msg in conversation:
        chat_history += f"{msg['name']}: {msg['text'].strip()}\n"

    prompt = (
        f"You are {name}, a participant in a chaotic but funny podcast.\n"
        f"Your persona:\n{persona.strip()}\n\n"
        f"📌 Topic: '{topic}'\n\n"
        "📢 Your task:\n"
        "- Stay fully in character\n"
        "- React to others, don't just summarize\n"
        "- Never refer to yourself in third person\n"
        "- Use a max of 4 unique sentences\n"
        "- Be entertaining, witty, and unpredictable\n\n"
        "🎙️ Podcast conversation so far:\n"
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
            data = res.json()
            return data.get("response", "[Error: Missing 'response' field]").strip()
        else:
            return f"[Error: LLM returned HTTP {res.status_code}]"
    except Exception as e:
        return f"[Error contacting LLM: {e}]"

def main():
    topic = input("Enter a podcast topic: ").strip() or "what is by far the best game"
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
        time.sleep(0.5)

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
        time.sleep(0.4)

        # Prompt for new topic after all agents have spoken
        if current_index == 0:
            new_topic = input("🔄 Enter a new topic (or press Enter to keep current): ").strip()
            if new_topic:
                topic = new_topic
                conversation = []  # Clear chat if switching topic
                print(f"\n🎤 New topic set: {topic}\n")

if __name__ == "__main__":
    main()
