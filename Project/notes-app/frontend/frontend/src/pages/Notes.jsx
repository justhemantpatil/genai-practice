import { useEffect, useState } from "react";
import api from "../api/axios";

function Notes() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const fetchNotes = async () => {
    const res = await api.get("/notes");
    setNotes(res.data);
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const addNote = async () => {
    if (!title || !content) return;

    await api.post("/notes", { title, content });
    setTitle("");
    setContent("");
    fetchNotes();
  };

  const deleteNote = async (id) => {
    await api.delete(`/notes/${id}`);
    fetchNotes();
  };

  return (
    <div>
      <h3>Add Note</h3>

      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <br /><br />

      <textarea
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <br /><br />

      <button onClick={addNote}>Add Note</button>

      <hr />

      <h3>My Notes</h3>

      {notes.map((note) => (
        <div key={note.id} style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}>
          <h4>{note.title}</h4>
          <p>{note.content}</p>
          <button onClick={() => deleteNote(note.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}

export default Notes;
