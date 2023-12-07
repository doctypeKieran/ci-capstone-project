const deleteButtons = document.getElementsByClassName('delete-event-btn');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

for (let button of deleteButtons) {
    button.addEventListener('click', (e) => {
        let deleteEventId = e.target.getAttribute('data-event-id');
        confirmDeleteBtn.href = `events/delete-event/${deleteEventId}`;
    })
}

const navMenuIcon = document.getElementById('nav-menu-icon');

navMenuIcon.addEventListener('click', () => {
    navMenuIcon.innerHTML = navMenuIcon.innerHTML === `<i class="hamburger-icon fa-solid fa-bars" aria-hidden="true"></i>` ? `<i class="hamburger-icon fa-solid fa-xmark"></i>` : `<i class="hamburger-icon fa-solid fa-bars" aria-hidden="true"></i>`;
})