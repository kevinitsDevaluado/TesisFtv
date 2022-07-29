var tblSale;
var input_daterange;
var select_typesale;

function getData(all) {
    var parameters = {
        'action': 'search',
        'type_sale': select_typesale.val(),
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (all) {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
    }

    tblSale = $('#data').DataTable({
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
            {data: "pos"},
            {data: "mascot.client.user.full_name"},
            {data: "mascot.name"},
            {data: "date_joined"},
            {data: "hour"},
            {data: "subtotal"},
            {data: "total_iva"},
            {data: "total"},
            {data: "status.name"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-left',
                render: function (data, type, row) {
                    return '<span class="badge badge-secondary">' + data.toUpperCase() + '</span>'
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    var html = '';
                    switch (row.status.id) {
                        case 'activo':
                            html = '<span class="badge badge-info">' + data + '</span>'
                            break;
                        case 'cancelado':
                            html = '<span class="badge badge-warning">' + data + '</span>'
                            break;
                        case 'finalizado':
                            html = '<span class="badge badge-success">' + data + '</span>'
                            break;
                        case 'eliminado':
                            html = '<span class="badge badge-danger">' + data + '</span>'
                            break;
                    }
                    return html;
                }
            },
            {
                targets: [-3, -4, -5],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    buttons += '<a class="btn btn-info btn-xs btn-flat" rel="details"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<a href="/clinic/sale/print/voucher/' + row.id + '/" target="_blank" class="btn btn-success btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<a href="/clinic/sale/admin/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                    if (row.status.id === 'activo') {
                        buttons += '<a href="/clinic/sale/employee/attend/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-book-reader"></i></a> ';
                    }
                    return buttons;
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    select_typesale = $('select[name="type_sale"]');
    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data();
        var datemedical = [];
        datemedical.push({'id': 'Motivos', 'name': data.symptoms});
        datemedical.push({'id': 'Observación', 'name': data.observation});
        datemedical.push({'id': 'Diagnóstico', 'name': data.diagnosis});
        $('#tblDateMedical').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            data: datemedical,
            paging: false,
            ordering: false,
            info: true,
            columns: [
                {data: "id"},
                {data: "name"},
            ],
            scrollX: true,
            scrollCollapse: true,
            columnDefs: [
                // {
                //     targets: [0],
                //     class: 'text-center',
                //     render: function (data, type, row) {
                //         return data;
                //     }
                // },
            ]
        });
        $('#tblDetails').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_detproducts',
                    'id': data.id
                },
                dataSrc: ""
            },
            scrollX: true,
            scrollCollapse: true,
            paging: false,
            ordering: false,
            info: true,
            columns: [
                {data: "product.name"},
                {data: "product.producttype.name"},
                {data: "price"},
                {data: "cant"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-1, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ]
        });
        $('#tblMedicalParameters').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            paging: false,
            ordering: false,
            info: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_detmedicalparameters',
                    'id': data.id
                },
                dataSrc: ""
            },
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {data: "medical_parameters.name"},
                {data: "valor"},
                {data: "desc"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-left',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ]
        });
        $('.nav-tabs a[href="#home"]').tab('show');
        $('#myModalDetails').modal('show');
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
        sorter: function (data) {
            return data.sort(function (a, b) {
                return a.text < b.text ? -1 : a.text > b.text ? 1 : 0;
            });
        }
    });

    select_typesale.on('change.select2', function () {
        getData();
    });

    $('.drp-buttons').hide();

    getData(false);

    $('.btnSearch').on('click', function () {
        getData(false);
    });

    $('.btnSearchAll').on('click', function () {
        getData(true);
    });
});
