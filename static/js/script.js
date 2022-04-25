const getNotes = () => {
    getData('/api/notes')
        .then((data) => {
            drawNotes(data)
        });
}

getNotes();

const drawNotes = (notes) => {
    const allNotes = document.getElementsByClassName('section_container')[0];
    allNotes.innerHTML = '';
    notes.map(note => {
        console.log(note);
        allNotes.innerHTML += `
        <div class="note">
            <div class="title_container">
                <h4 class="note_title">${note.title}</h4>
            </div>
            <div class="text_container">
                <p>${note.text}</p>
        </div>
        <button class="edit" onclick="editNote(${note.id})">Edit</button>
        <button class="delete" onclick="deleteNote(${note.id})">Delete</button>
        </div>`
    });
}

const deleteNote = (id) => {
    deleteData('/api/notes/' + id)
        .then((data) => {
            if (data.status === 200) return getNotes();
        });
}

const createNote = () => {
    const title = document.getElementById('new_note_title').value;
    const text = tinyMCE.get('mytextarea').getContent();
    if (!title) return alert('Please, enter Title');
    const data = {
        title: title,
        text: text
    }
    postData('api/notes', data)
        .then((data) => {
            if (data) return getNotes()
        })
}

const editNote = (id) => {
    getData('api/note/' + id)
        .then((data) => {
            const saveButton = document.getElementsByClassName('submit_button')[0];
            saveButton.onclick = () => {
                const data = {
                    title: title_input.value,
                    text: tinyMCE.get('mytextarea').getContent()
                }
                putData('/api/notes/' + id, data)
                    .then((data) => {
                        if (data) return getNotes()
                })
            }
            const title_input = document.getElementById('new_note_title');
            title_input.value = data.title;
            tinyMCE.get('mytextarea').setContent(data.text);
        })
}


