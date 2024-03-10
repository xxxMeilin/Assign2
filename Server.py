import xml.etree.ElementTree as ET
from xmlrpc.server import SimpleXMLRPCServer
import requests
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
from datetime import datetime

class ThreadedXMLRPCServer(threading.Thread, SimpleXMLRPCServer):
    def __init__(self, address, handler):
        threading.Thread.__init__(self)
        SimpleXMLRPCServer.__init__(self, address, requestHandler=handler)
class NotebookServer:
    def __init__(self):
        self.tree = ET.ElementTree(file='Notebook.xml')
        self.root = self.tree.getroot()

    def get_existing_topics(self):
        existing_topics = [topic.attrib['name'] for topic in self.root.findall('topic')]
        return existing_topics

    def check_exist_topic(self, topic_name):
        for t in self.root.findall('topic'):
            if t.attrib.get('name') == topic_name:
                return True
        return False

    def add_wiki_info(self, topic_name, note_name, note_text):
        for t in self.root.findall('topic'):
            if t.attrib.get('name') == topic_name:
                new_note = ET.SubElement(t, 'note', {'name': note_name})
                new_text = ET.SubElement(new_note, 'text')
                new_text.text = note_text
                timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
                new_timestamp = ET.SubElement(new_note, 'timestamp')
                new_timestamp.text = timestamp
                self.tree.write('Notebook.xml')
                return "New Note added successfully."


    def add_note(self, topic_name, note_name, note_text):
        if not self.check_exist_topic(topic_name):
            new_topic = ET.SubElement(self.root, 'topic', {'name': topic_name})
            new_note = ET.SubElement(new_topic, 'note', {'name': note_name})
            new_text = ET.SubElement(new_note, 'text')
            new_text.text = note_text
            timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
            new_timestamp = ET.SubElement(new_note, 'timestamp')
            new_timestamp.text = timestamp
            self.tree.write('Notebook.xml')
            return "New Topic added successfully."
        else:
            for t in self.root.findall('topic'):
                if t.attrib.get('name') == topic_name:
                    new_note = ET.SubElement(t, 'note', {'name': note_name})
                    new_text = ET.SubElement(new_note, 'text')
                    new_text.text = note_text
                    timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
                    new_timestamp = ET.SubElement(new_note, 'timestamp')
                    new_timestamp.text = timestamp
                    self.tree.write('Notebook.xml')
                    return "New Note added successfully."

    def get_notes(self, topic_name):
        notes_str = ""
        for topic in self.root.findall('topic'):
            if topic.attrib.get('name') == topic_name:
                for note in topic.findall('note'):
                    name = note.attrib.get('name')
                    text = note.find('text').text
                    timestamp = note.find('timestamp').text
                    notes_str += f"Note: {name}\nText: {text}\nTimestamp: {timestamp}\n\n"
        return notes_str

    def query_notes(self, topic_name):
        session = requests.Session()
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "namespace": "0",
            "search": topic_name,
            "limit": "5",
            "format": "json"
        }
        try:
            response = session.get(url=url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()
            search_url = data[3][0] if data[3] else "No search URL found"
            return search_url
        except requests.RequestException as e:
            print(f"Error occurred: {e}")
            return "Error occurred while querying Wikipedia"
        except (ValueError, IndexError) as e:
            print(f"Error occurred: {e}")
            return "Error occurred while parsing Wikipedia response"

def main():
    server = ThreadedXMLRPCServer(("localhost", 8000), SimpleXMLRPCRequestHandler)
    server.register_instance(NotebookServer())

    print("Listening on port 8000...")
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True  # Set the thread as daemon so it exits when the main program exits
    server_thread.start()
    while True:
        pass

if __name__ == "__main__":
    main()




