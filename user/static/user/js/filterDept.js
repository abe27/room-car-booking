document.addEventListener('DOMContentLoaded', function () {
    const fccorpSelect = document.getElementById('id_fccorp');
    const fcdeptSelect = document.getElementById('id_fcdept');

    fccorpSelect.addEventListener('change', function () {
        const fccorpId = this.value;

        fetch(`/user/filter/dept/?fccorp=${fccorpId}`)
            .then(response => response.json())
            .then(data => {
                fcdeptSelect.innerHTML = '';
                data.forEach(department => {
                    const option = document.createElement('option');
                    option.value = department.id;
                    option.textContent = department.fcname;
                    fcdeptSelect.appendChild(option);
                });
            });
    });
});
