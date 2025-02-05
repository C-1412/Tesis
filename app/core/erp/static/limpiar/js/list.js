$(function () {
    let isAllSelected = false; // Variable para rastrear el estado de selección

    function loadTable(area_id = '') {
        let table = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'searchdata',
                    'area_id': area_id
                },
                dataSrc: ""
            },
            columns: [
                {"data": "username"},
                {"data": "area"},
                {
                    "data": function (row) {
                        return `<div style="text-align: center;">
                                    <input type="checkbox" class="user-checkbox" value="${row.id}">
                                </div>`;
                    }, 
                    "orderable": false, 
                    "searchable": false
                }
            ],
            drawCallback: function () {
                // Si el botón "Seleccionar Todos" está activo, marcar checkboxes
                if (isAllSelected) {
                    $('.user-checkbox').prop('checked', true);
                }
            }
        });

        return table;
    }

    let dataTable = loadTable();

    $('#filter-area').change(function () {
        let area_id = $(this).val();
        dataTable = loadTable(area_id);
    });

    $('#clear-responses').click(function (e) {
        e.preventDefault();
        let selectedUsers = [];
        $('.user-checkbox:checked').each(function () {
            selectedUsers.push($(this).val());
        });

        if (selectedUsers.length === 0) {
            Swal.fire({
                title: 'Error!',
                text: 'Seleccione al menos un usuario.',
                icon: 'error',
            });
            return;
        }

        $.post(window.location.pathname, {
            'action': 'delete_answers',
            'user_ids': selectedUsers
        }, function (response) {
            if (response.success) {
                Swal.fire({
                    title: '¡Éxito!',
                    text: 'Respuestas eliminadas.',
                    icon: 'success',
                });
                dataTable.ajax.reload(); // Recargar sin perder filtrado
            } else {
                Swal.fire({
                    title: 'Error!',
                    text: 'Error al eliminar respuestas.',
                    icon: 'error',
                });
            }
        }, 'json');
    });

    // Evento para seleccionar/deseleccionar todos los checkboxes visibles
    $('#select-all').click(function () {
        isAllSelected = !isAllSelected; // Alternar estado de selección
        $('.user-checkbox').prop('checked', isAllSelected);
    });

    // Asegurar que la tabla se recargue correctamente con la selección
    $('#data').on('draw.dt', function () {
        if (isAllSelected) {
            $('.user-checkbox').prop('checked', true);
        }
    });

});
