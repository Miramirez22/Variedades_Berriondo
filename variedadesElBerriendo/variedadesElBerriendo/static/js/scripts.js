
// mostrar popup window para confirmar eliminación de producto en carrito
document.addEventListener('DOMContentLoaded', function () {

    const myModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'), {
        keyboard: true, //cerrar modal con tecla ESC
    });

    // selección de todos los botones de eliminar producto
    document.querySelectorAll('.btn-eliminar-producto').forEach((btn) => {
        btn.addEventListener('click', function (event) {
            event.preventDefault(); // evitar que el botón envíe el formulario

            // obtener el id del producto
            const productId = this.getAttribute('data-product-id');
            // obtener la url de eliminar producto
            const deleteUrl = '/remove_from_cart/' + productId + '/';

            document.getElementById('deleteForm').action = deleteUrl;

            // mostrar Modal
            const myModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
            myModal.show();
        });
    });
    
    // Cerrar modal con botón cancelar
    document.querySelector('.btn-secondary').addEventListener('click', function () {
        myModal.hide();
        document.querySelector('.modal-backdrop').remove();
    });

});
