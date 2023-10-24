import openai
openai.api_key = "Insert key here"

def generate_response(prompt):
    MyMessage = [{"role": "system", "content": "You are a helpful assistant."},
                 {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=MyMessage,
        max_tokens=8092,
        n=1,
        stop=None,
        temperature=0.01,
    )
    return response.choices[0]["message"]["content"]


if __name__ == '__main__':
    
    Question = "Hoe moet ik in python load_qa_chain uit de module langChain.chains.question_answering gebruiken met het gpt-4 model?"
    Answer = generate_response(Question)
    print(Answer)
