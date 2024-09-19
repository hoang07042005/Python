document.getElementById('image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const previewImage = document.getElementById('preview-image');
        const noImageMessage = document.getElementById('no-image-message');
        previewImage.src = e.target.result;
        previewImage.style.display = 'block'; 
        noImageMessage.style.display = 'none'; 
    }
    
    if (file) {
        reader.readAsDataURL(file);
    } else {
        const previewImage = document.getElementById('preview-image');
        const noImageMessage = document.getElementById('no-image-message');
        previewImage.src = '';
        previewImage.style.display = 'none'; 
        noImageMessage.style.display = 'block'; 
    }
});