var tblProducts;
var select_producttype;

function getData() {
    var parameters = {
        'action': 'search',
        'producttype': select_producttype.val(),
    };

    tblProducts = $('#data').DataTable({
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
            {data: "id"},
            {data: "name"},
            {data: "producttype.name"},
            {data: "image"},
            {data: "price"},
            {data: "stock"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.producttype.has_stock) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success">' + data + '</span>';
                        }
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                    return 'No necesita stock';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    buttons += '<a href="/clinic/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit" aria-hidden="true"></i></a> ';
                    buttons += '<a href="/clinic/product/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash" aria-hidden="true"></i></a>';
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

    select_producttype = $('select[name="product_type"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_producttype.on('change.select2', function () {
        getData();
    });

    getData();
});