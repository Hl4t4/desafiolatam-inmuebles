
// function reloadPage() {
//     location.reload(true); // Force reload from server cache
// }

$(document).ready(function () {
    var myModal = $('#detailsModal');

    var modal = document.getElementById('loginErrorModal');
    $("#loginErrorModalClose").on('click', function() {
        modal.classList.remove('show');
        modal.classList.remove('d-block'); 
    });

    $(".detailsOpenModal").on('click', function() {
        let inmueble = $(this).data('value');
        inmueble = inmueble.replace(/\'/g, "\"");
        inmueble = inmueble.replace("O\"Higgins", "O'Higgins");
        inmueble = JSON.parse(inmueble);

        new_html = `
            <div class = "card-header text-center">
                <h3> ${ inmueble.nombre }</h3>
            <div class = "card-body overflow-y-scroll" >
                <p> Arrendatario: ${ inmueble.arrendatario }</p>
                <p> Arrendador: ${ inmueble.arrendador }</p>
                <p>${ inmueble.descripcion }</p>
                <p>Metros² Construidos: ${ inmueble.m2_construidos }[m²]</p>
                <p>Metros² Totales: ${ inmueble.m2_totales }[m²]</p>
                <p>N° Estacionamientos: ${ inmueble.estacionamientos }</p>
                <p>N° Habitaciones: ${ inmueble.habitaciones }</p>
                <p>N° Baños: ${ inmueble.restrooms }</p>
                <p>Dirección: ${ inmueble.direccion }</p>
                <p>Comuna: ${ inmueble.comuna }</p>
                <p>Región: ${ inmueble.region }</p>
                <p>Tipo de Inmueble: ${ inmueble.tipo_inmueble }</p>
                <p>Valor de Arriendo: ${ inmueble.arriendo }</p>
            </div>`
        myModal.find('.card').html(new_html)

        myModal.show();

    });
    $("#detailsModalCloseTop").on('click', function() {
        myModal.hide();
    });
    $("#detailsModalCloseBottom").on('click', function() {
        myModal.hide();
    });

    function formatRUT(value) {
        if(value) {
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
    }

    $('input[name="rut"]').val(formatRUT($('input[name="rut"]').val()));

    $('input[name="rut"]').on('input', function () {
        $(this).val(formatRUT($(this).val()));
    });

    
});