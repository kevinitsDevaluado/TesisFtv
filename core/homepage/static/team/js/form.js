var tblSocialNet;
var team = {
    details: {
        socialnet: []
    },
    add: function (item) {
        this.details.socialnet.push(item);
        this.list();
    },
    list: function () {
        tblSocialNet = $('#tblSocialNet').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.socialnet,
            /*paging: false,
            ordering: false,
            info: false,*/
            columns: [
                {data: "name"},
                {data: "name"},
                {data: "icon"},
                {data: "url"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash" aria-hidden="true"></i></a>';
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm" placeholder="Ingrese un mombre" autocomplete="off" name="name" value="' + row.name + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm" placeholder="Ingrese un icono" autocomplete="off" name="icon" value="' + row.icon + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm" placeholder="Ingrese una dirección url" autocomplete="off" name="url" value="' + row.url + '">';
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {

            },
        });
    },
};

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
    const fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                names: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                job: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                desc: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                phrase: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
            },
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
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
           
            var inputFileImage = document.getElementById('id_image');
            var file = inputFileImage.files[0];
            var parameters = new FormData();
            parameters.append('image', file);
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('socialnet', JSON.stringify(team.details.socialnet));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = form.getAttribute('data-url');
                },
            );
        });
});

$(function () {

    $('.btnRemoveAll').on('click', function () {
        if (team.details.socialnet.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            team.details.socialnet = [];
            team.list();
        }, function () {

        });
    });

    $('.btnAdd').on('click', function () {
        team.add({
            'name': '',
            'icon': '',
            'url': '',
        });
    });

    $('#tblSocialNet tbody')
        .on('keyup', 'input[name="name"]', function () {
            var tr = tblSocialNet.cell($(this).closest('td, li')).index();
            team.details.socialnet[parseInt(tr.row)].name = $(this).val();
        })
        .on('keyup', 'input[name="url"]', function () {
           var tr = tblSocialNet.cell($(this).closest('td, li')).index();
            team.details.socialnet[parseInt(tr.row)].url = $(this).val();
        })
        .on('keyup', 'input[name="icon"]', function () {
           var tr = tblSocialNet.cell($(this).closest('td, li')).index();
            team.details.socialnet[parseInt(tr.row)].icon = $(this).val();
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblSocialNet.cell($(this).closest('td, li')).index();
            team.details.socialnet.splice(tr.row, 1);
            tblSocialNet.row(tr.row).remove().draw();
        });
});