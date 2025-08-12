document.addEventListener('DOMContentLoaded', () => {
    const editBtn = document.getElementById('edit-btn');
    const formDiv = document.querySelector('.profile-edit-form');
    const profileInfo = document.querySelector('.profile-info');
    
    formDiv.style.display = 'none';
    
    if (editBtn && formDiv) {
        editBtn.addEventListener('click', () => {
            formDiv.style.display = 'block';
            editBtn.style.display = 'none';
            profileInfo.style.display = 'none';
        });
    }
});