import os
import pandas as pd
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from student_outcomes import extract_student_outcomes_for_all_courses


def chat_with_gpt(client, messages: list[ChatCompletionMessageParam]):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {e}"


def main():
    api_key = os.getenv("OPENAI_API_KEY") or input("Please enter your OpenAI API key: ").strip()
    try:
        client = OpenAI(api_key=api_key)
        _ = client.models.list()
        print("✅ Successfully connected to OpenAI API.")
    except Exception as e:
        print(f"❌ Failed to connect to OpenAI API: {e}")
        return

    # 🔹 Load student outcomes but don't send yet
    student_outcomes = extract_student_outcomes_for_all_courses()
    print("📁 Student outcomes loaded. Type 'show student' anytime to insert it into the chat.")

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are an expert in assessing student learning capabilities based on a likert scale."}
    ]

    print("\n🔹 ChatGPT Terminal Chat (type 'exit' to quit)")

    while True:
        user_input = input("\n🧑 You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # ✅ Special trigger to show student outcomes
        if user_input.lower() in ["show student", "student", "send student"]:
            formatted = (
                f"Here is the Likert scale outcome dictionary for an anonymouse student:\n{student_outcomes}\n\n"
                f"Please Build a learner model of the students capability. Comment on the student's strengths and weaknesses."
            )
            messages.append({"role": "user", "content": formatted})
        else:
            messages.append({"role": "user", "content": user_input})

        response = chat_with_gpt(client, messages)
        print(f"\n🤖 ChatGPT: {response}")


if __name__ == "__main__":
    main()
