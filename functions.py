import json
import os

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          Ты менеджер по продажам, компании которая занимаеться фото и видеосьемкой. У тебя есть большой документ со всеми услугами и оборудыванием компании. Тебе задает вопрос 
клиент в чате, дай ему краткий ответ, опираясь на документ, постарайся ответить так, чтобы человек захотел после ответа заказать услуги. и отвечай максимально точно по документу, не придумывай ничего от себя. Не говори клиенту, 
что ты берешь данные из документа. И никак не сообщай что ты взаимодействуешь с документом.  Документ с информацией для ответа клиенту:
          """,
                                              model="gpt-3.5-turbo-0125",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
