var tblProducts;
var tblSearchProducts;
var tblMedicalParameters = null;

var client = {'id': ''};
var fvSale;
var fvMascot;

var input_datejoined;
var select_mascot;
var select_type;
var input_searchproducts;
var textarea_symptoms;

var fgrpmedical;

var vents = {
    details: {
        products: [],
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.details.products, function (i, item) {
            item.cant = parseInt(item.cant);
            item.subtotal = item.cant * parseFloat(item.price);
            subtotal += item.subtotal;
        });
        vents.details.iva = parseFloat(iva);
        vents.details.subtotal = subtotal;
        vents.details.total_iva = subtotal * (vents.details.iva / 100);
        vents.details.total = subtotal + vents.details.total_iva;
        $('input[name="subtotal"]').val(vents.details.subtotal.toFixed(2));
        $('input[name="iva"]').val(vents.details.iva.toFixed(2));
        $('input[name="total_iva"]').val(vents.details.total_iva.toFixed(2));
        $('input[name="total"]').val(vents.details.total.toFixed(2));
    },
    list_products: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "producttype.name"},
                {data: "stock"},
                {data: "cant"},
                {data: "price"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.producttype.has_stock) {
                            return '---';
                        }
                        return data;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" style="width: 100px;" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                var stock = data.producttype.has_stock ? parseInt(data.stock) : 1000;
                tr.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: stock,
                        verticalbuttons: true,
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {

            },
        });
    },
    get_products_ids: function () {
        var ids = [];
        $.each(this.details.products, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
    add_product: function (item) {
        this.details.products.push(item);
        this.list_products();
    },
};


document.addEventListener('DOMContentLoaded', function (e) {
    const frmSale = document.getElementById('frmSale');
    fvSale = FormValidation.formValidation(frmSale, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                // excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                mascot: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una mascota/cliente'
                        },
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                symptoms: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                diagnosis: {
                    validators: {
                        notEmpty: {},
                    }
                },
                observation: {
                    validators: {
                        // notEmpty: {},
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de venta'
                        },
                    }
                },
            },
        }
    )
        .on('core.form.invalid', function () {
            $('a[href="#home"][data-toggle="tab"]').parent().find('i').removeClass().addClass('fas fa-times');
        })
        .on('core.element.validated', function (e) {
            var tab = e.element.closest('.tab-pane'),
                tabId = tab.getAttribute('id');
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
                $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass();
            } else {
                $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass().addClass('fas fa-times');
            }
            const iconPlugin = fvSale.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            var tab = e.element.closest('.tab-pane'),
                tabId = tab.getAttribute('id');
            if (!e.result.valid) {
                // Query all messages
                const messages = [].slice.call(frmSale.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
                $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass();
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData($(fvSale.form)[0]);
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('medical_parameters', JSON.stringify(tblMedicalParameters.rows().data().toArray()));
            parameters.append('products', JSON.stringify(vents.details.products));
            parameters.append('iva', vents.details.iva);
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function (request) {
                    var urlrefresh = fvSale.form.getAttribute('data-url');
                    dialog_action('Notificación', '¿Desea imprimir la boleta de venta?', function () {
                        window.open('/clinic/sale/print/voucher/' + request.id + '/', '_blank');
                        location.href = urlrefresh;
                    }, function () {
                        location.href = urlrefresh;
                    });
                },
            );
        });
});

document.addEventListener('DOMContentLoaded', function (event) {
    const frmMascot = document.getElementById('frmMascot');
    const submitButton = frmMascot.querySelector('[type="submit"]');
    fvMascot = FormValidation.formValidation(frmMascot, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                // defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                /* client */
                first_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        regexp: {
                            regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                            message: 'Debe ingresar sus dos nombres y solo utilizando caracteres alfabéticos'
                        },
                    }
                },
                last_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        regexp: {
                            regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                            message: 'Debe ingresar sus dos apellidos y solo utilizando caracteres alfabéticos'
                        },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10,
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: frmMascot.querySelector('[name="dni"]').value,
                                    type: 'dni',
                                    id: client.id,
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de cedula ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: frmMascot.querySelector('[name="email"]').value,
                                    id: client.id,
                                    type: 'email',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: frmMascot.querySelector('[name="mobile_phone"]').value,
                                    id: client.id,
                                    type: 'mobile_phone',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de teléfono ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                address: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                /* mascot */
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                breed: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una raza'
                        },
                    }
                },
                color: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un color'
                        },
                    }
                },
                gender: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un genero'
                        },
                    }
                },
            }
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvMascot.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmMascot.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData($(fvMascot.form)[0]);
            parameters.append('action', 'create_mascot');
            parameters.append('id_client', client.id);
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de crear el siguiente cliente/mascota', pathname, parameters, function (response) {
                var newOption = new Option(response.text, response.id, false, true);
                select_mascot.append(newOption).trigger('change');
                $('#myModalMascot').modal('hide');
            });
        });
});

function loadMedicalParameters() {
    var parameters = {
        'action': 'search_medicalparameters',
        'mascot': select_mascot.val()
    };

    tblMedicalParameters = $('#tblMedicalParameters').DataTable({
        // responsive: true,
        // autoWidth: false,
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
        scrollX: true,
        scrollCollapse: true,
        columns: [
            {data: "name"},
            {data: "last_valor"},
            {data: "valor"},
            {data: "desc"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    if (data.length === 0) {
                        return 'Sin registro';
                    }
                    return data;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input class="form-control" autocomplete="off" name="desc" placeholder="Ingrese una descripción" value="' + data + '" maxlength="500">';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input class="form-control" autocomplete="off" name="valor" style="width: 100px;" placeholder="Ingrese un valor" value="' + data + '">';
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

    input_datejoined = $('input[name="date_joined"]');
    input_searchproducts = $('input[name="searchproducts"]');
    select_mascot = $('select[name="mascot"]');
    select_type = $('select[name="type"]');
    fgrpmedical = $('.fgrpmedical');
    textarea_symptoms = $('textarea[name="symptoms"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    /* Products */

    $('.btnRemoveAllProducts').on('click', function () {
        if (vents.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            vents.details.products = [];
            vents.list_products();
        });
    });

    input_searchproducts.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(vents.get_products_ids()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            console.log(ui.item);
            if (ui.item.stock === 0 && ui.item.producttype.has_stock) {
                message_error('El stock de este producto esta en 0');
                return false;
            }
            ui.item.cant = 1;
            vents.add_product(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_searchproducts.val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            // responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_products',
                    'term': input_searchproducts.val(),
                    'ids': JSON.stringify(vents.get_products_ids()),
                },
                dataSrc: ""
            },
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {data: "name"},
                {data: "producttype.name"},
                {data: "price"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
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
                        if (!row.producttype.has_stock) {
                            return '---';
                        }
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-cart-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody').on('click', 'a[rel="add"]', function () {
        var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
        var row = tblSearchProducts.row(tr.row).data();
        row.cant = 1;
        vents.add_product(row);
        tblSearchProducts.row(tr.row).remove().draw();
    });

    $('#tblProducts tbody')
        .on('change', 'input[name="cant"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.details.products[tr.row].cant = parseInt($(this).val());
            vents.calculate_invoice();
            $('td:eq(6)', tblProducts.row(tr.row).node()).html('$' + vents.details.products[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.details.products.splice(tr.row, 1);
            tblProducts.row(tr.row).remove().draw();
        });

    /* MedicalParameters */

    $('#tblMedicalParameters tbody')
        .on('change', 'input[name="valor"]', function () {
            var tr = tblMedicalParameters.cell($(this).closest('td, li')).index();
            row = tblMedicalParameters.row(tr.row).data();
            row.valor = $(this).val();
        })
        .on('keyup', 'input[name="desc"]', function () {
            var tr = tblMedicalParameters.cell($(this).closest('td, li')).index();
            row = tblMedicalParameters.row(tr.row).data();
            row.desc = $(this).val();
        });

    /* Form */

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
            fvSale.revalidateField('mascot');
            loadMedicalParameters();
        })
        .on('select2:clear', function (e) {
            fvSale.revalidateField('mascot');
        });

    select_type.on('change', function () {
        var id = $(this).val();
        fgrpmedical.hide();
        fvSale.disableValidator('symptoms');
        fvSale.disableValidator('diagnosis');
        var navlink = $('.nav-tabs a[href="#menu2"]'); // $('[href="#tab2"]').closest('li').hide();
        navlink.closest('li').hide();
        if (id === 'cita_medica' || id === 'control_vacuna' || id === 'control_antiparasitario') {
            navlink.closest('li').show();
            if (id === 'cita_medica') {
                fvSale.enableValidator('symptoms');
                fvSale.enableValidator('diagnosis');
                $(fgrpmedical).show();
            }
        } else {
            $('.nav-tabs a[href="#home"]').tab('show');
        }
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_datejoined.on('change.datetimepicker', function (e) {
        fvSale.revalidateField('date_joined');
    });

    fgrpmedical.hide();

    loadMedicalParameters();

    select_type.trigger('change');

    /* Add Mascot */

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
            fvSale.revalidateField('mascot');
            loadMedicalParameters();
        })
        .on('select2:clear', function (e) {
            fvSale.revalidateField('mascot');
        });

    $('.btnAddMascot').on('click', function () {
        fvMascot.revalidateField('dni')
            .then(function (status) {
                fvMascot.resetForm(true);
            });
        client = {'id': ''};
        $('#myModalMascot').modal('show');
    });

    $('#myModalMascot').on('hidden.bs.modal', function (e) {
        fvMascot.resetForm(true);
    });

    $('input[name="first_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="last_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('select[name="color"]').on('change', function () {
        fvMascot.revalidateField('color');
    });

    $('select[name="breed"]').on('change', function () {
        fvMascot.revalidateField('breed');
    });

    $('select[name="gender"]').on('change', function () {
        fvMascot.revalidateField('gender');
    });

    $('input[name="name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="dni"]')
        .autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: pathname,
                    data: {
                        'action': 'search_client',
                        'term': request.term
                    },
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    dataType: 'json',
                    success: function (request) {
                        response(request);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        message_error(errorThrown + ' ' + textStatus);
                    }
                });
            },
            delay: 500,
            minLength: 1,
            select: function (event, ui) {
                fvMascot.revalidateField('dni');
                $(fvMascot.form).find('input[name="first_name"]').val(ui.item.user.first_name);
                $(fvMascot.form).find('input[name="last_name"]').val(ui.item.user.last_name);
                $(fvMascot.form).find('input[name="email"]').val(ui.item.user.email);
                $(fvMascot.form).find('input[name="mobile"]').val(ui.item.mobile);
                $(fvMascot.form).find('input[name="address"]').val(ui.item.address);
                client = ui.item;
            }
        }).keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('.btnClearClient').on('click', function () {
        client = {'id': ''};
        $(fvMascot.form).find('input[name="dni"]').val('');
        $(fvMascot.form).find('input[name="first_name"]').val('');
        $(fvMascot.form).find('input[name="last_name"]').val('');
        $(fvMascot.form).find('input[name="email"]').val('');
        $(fvMascot.form).find('input[name="mobile_phone"]').val('');
        $(fvMascot.form).find('input[name="address"]').val('');
    });
});