var tblHistorialMedical;
var select_type_medicalhistory;
var select_mascot;

function getData() {
    var parameters = {
        'action': 'search',
        'type': select_type_medicalhistory.val(),
        'mascot': select_mascot.val(),
    };

    tblHistorialMedical = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: parameters,
            dataSrc: ""
        },
        columns: [
            {data: "date_joined"},
            {data: "mascot.name"},
            {data: "mascot.client.user.full_name"},
            {data: "employee.user.full_name"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a rel="historial" class="btn btn-success btn-xs"><i class="fas fa-file-medical-alt"></i> Ver Historial</a>';
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        }
    });
}

function formatHistorialMedical(data) {
    var html = '<p>';
    $.each(data, function (key, value) {
        html += '<b>' + value.medical_parameters.name + ':</b> ' + value.valor + '<br>';
    });
    html += '</p>';
    return html;
}

$(function () {

    select_type_medicalhistory = $('select[name="type_medicalhistory"]');
    select_mascot = $('select[name="mascots"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
        sorter: function (data) {
            return data.sort(function (a, b) {
                return a.text < b.text ? -1 : a.text > b.text ? 1 : 0;
            });
        }
    });

    select_type_medicalhistory.on('change.select2', function () {
        getData();
    });

    select_mascot
        .select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                url: pathname,
                data: function (params) {
                    var queryParameters = {
                        term: params.term,
                        action: 'search_mascot'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Ingrese una descripción',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            getData();
        })
        .on('select2:clear', function (e) {
            getData();
        });

    $('#data tbody')
        .on('click', 'a[rel="historial"]', function () {
            var cell = tblHistorialMedical.cell($(this).closest('td, li')).index();
            var data = tblHistorialMedical.row(cell.row).data();
            var tr = $(this).closest('tr');
            var row = tblHistorialMedical.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(formatHistorialMedical(data.historialmedical)).show();
                tr.addClass('shown');
            }
        });
});