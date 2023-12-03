const deleteButtons = document.getElementsByClassName('delete-event-btn');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

for (let button of deleteButtons) {
    button.addEventListener('click', (e) => {
        let deleteEventId = e.target.getAttribute('data-event-id');
        confirmDeleteBtn.href = `events/delete-event/${deleteEventId}`;
    })
}