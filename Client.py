import xmlrpc.client
def server_connect():
    try:
        server = xmlrpc.client.ServerProxy("http://localhost:8000/")
        return server
    except ConnectionRefusedError:
        print("Unable to connect to server: Connection refused.")
    except xmlrpc.client.ProtocolError as e:
        print(e)
    except Exception as e:
        print(f"An unknown error occurred while trying to connect to the server:{e}")

    return None

def ask_input():
    topic = input("Enter topic: ")
    if check_exist_topic(topic):
        print("The topic already exists. ")
    else:
        print("The topic does not exists. A new topic will be created.")
    note = input("Enter note: ")
    text = input("Enter text: ")
    server = server_connect()
    print(server.add_note(topic, note, text))
    print("")
    return


def get_notes():
    server = server_connect()
    print("The following are all existing topics:")
    existing_topics = get_existing_topics()
    print('\n'.join(existing_topics))
    while True:
        topic = input("Enter topic to get notes: ")
        if topic in existing_topics:
            return print(server.get_notes(topic))
        else:
            print("The entered topic does not exist. Please enter a valid existing topic.")

def query():
    topic = input("Enter topic to query more information: ")
    print(query_notes(topic))
    print("The following are all existing topics:")
    existing_topics = get_existing_topics()
    print('\n'.join(existing_topics))
    while True:
        topic_add = input("Enter topic to add the information: ")
        if topic_add in existing_topics:
            note = input("Enter note: ")
            text = query_notes(topic)
            server = server_connect()
            print(server.add_wiki_info(topic_add, note, text))
            print("")
            return
        else:
            print("The entered topic does not exist. Please enter a valid existing topic.")

def query_notes(topic):
    server = server_connect()
    return server.query_notes(topic)

def get_existing_topics():
    server = server_connect()
    return server.get_existing_topics()

def check_exist_topic(topic_name):
    server = server_connect()
    return server.check_exist_topic(topic_name)

def main():
    while True:
        print("1. Add a topic")
        print("2. Get notes for a topic")
        print("3. Query the Wikipedia for more information")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            ask_input()
        elif choice == '2':
            get_notes()
        elif choice == '3':
            query()
        elif choice == '4':
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
