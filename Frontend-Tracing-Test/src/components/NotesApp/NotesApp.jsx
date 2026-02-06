import React, { useState, useEffect } from 'react';
import './NotesApp.css';

const NotesApp = () => {
    const [notes, setNotes] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [status, setStatus] = useState('Idle');
    const API_BASE = 'http://localhost:8000/api/notes';

    useEffect(() => {
        handleFetchNotes();
    }, []);

    const handleFetchNotes = async () => {
        setStatus('Fetching notes...');
        try {
            const response = await fetch(API_BASE + '/');
            const result = await response.json();
            if (result.status === 'success') {
                setNotes(result.data);
                setStatus('Notes loaded');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            setStatus('Error fetching notes');
        }
    };

    const handleAddNote = async (e) => {
        e.preventDefault();
        if (!title || !content) return;

        setStatus('Adding note...');
        try {
            const response = await fetch(`${API_BASE}/add?title=${encodeURIComponent(title)}&content=${encodeURIComponent(content)}`, {
                method: 'POST'
            });
            const result = await response.json();

            if (result.status === 'success') {
                setStatus('Note added successfully!');
                setTitle('');
                setContent('');
                handleFetchNotes(); // Refresh list
            } else {
                setStatus('Failed to add note: ' + (result.result?.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Add note error:', error);
            setStatus('Network error adding note');
        }
    };

    return (
        <div className="notes-container">
            <h3>Notes Manager (FastAPI Backend)</h3>
            <div className="status-badge">{status}</div>

            <form className="note-form" onSubmit={handleAddNote}>
                <input
                    type="text"
                    placeholder="Note Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <textarea
                    placeholder="Note Content"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                />
                <button type="submit" className="btn-add">Add Note</button>
            </form>

            <div className="notes-list">
                {notes.map(note => (
                    <div key={note.id} className="note-item">
                        <h4>{note.title}</h4>
                        <p>{note.content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default NotesApp;
