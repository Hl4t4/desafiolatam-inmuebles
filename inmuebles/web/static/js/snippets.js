$(document).ready(function () {
    var modal = document.getElementById('loginErrorModal');
    $("#loginErrorModalClose").on('click', function() {
        modal.classList.remove('show');
        modal.classList.remove('d-block'); 
    });

    function formatRUT(value) {
        // Remove all non-numeric characters except 'k' and 'K'
        value = value.replace(/[^0-9kK]/g, '');

        if (value.length > 1) {
            let body = value.slice(0, -1);
            body = body.replace(/[^0-9]/g, '');
            body = body.replace(/(\d)(?=(\d{3})+(?![0-9]))/g, '$1.');
            let verifier = value.slice(-1);
            return `${body}-${verifier}`;
        }
        return value;
    }

    $('input[name="rut"]').val(formatRUT($('input[name="rut"]').val()));

    $('input[name="rut"]').on('input', function () {
        $(this).val(formatRUT($(this).val()));
    });
});