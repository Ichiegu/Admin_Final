document.addEventListener('DOMContentLoaded', function () {
    // Edit Transaction
    const editButtons = document.querySelectorAll('.edit-transaction');
    editButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const transactionId = this.getAttribute('data-id');

            fetch(`/transactions/${transactionId}/edit/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('editTransactionId').value = data.id;
                    document.getElementById('editBookingId').value = data.booking_id;
                    document.getElementById('editUserId').value = data.user_id;
                    document.getElementById('editServiceId').value = data.service_id;
                    document.getElementById('editAmount').value = data.amount;
                    document.getElementById('editPaymentMethod').value = data.payment_method;
                    document.getElementById('editStatus').value = data.status;
                    document.getElementById('editTransactionType').value = data.transaction_type;

                    // Format date for datetime-local input
                    const date = new Date(data.transaction_date);
                    const formattedDate = date.toISOString().slice(0, 16);
                    document.getElementById('editTransactionDate').value = formattedDate;

                    document.getElementById('editReferenceCode').value = data.reference_code || '';
                    document.getElementById('editModal').style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching transaction:', error);
                    alert('Error loading transaction data');
                });
        });
    });

    // Delete Transaction
    const deleteButtons = document.querySelectorAll('.delete-transaction');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const transactionId = this.getAttribute('data-id');
            const row = this.closest('tr');

            document.getElementById('deleteTransactionId').textContent = row.cells[0].textContent;
            document.getElementById('deleteTransactionAmount').textContent = row.cells[4].textContent;
            document.getElementById('deleteModal').setAttribute('data-transaction-id', transactionId);
            document.getElementById('deleteModal').style.display = 'block';
        });
    });

    // Close Modals
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });

    // Save Transaction Changes
    document.getElementById('saveTransactionBtn').addEventListener('click', function() {
        const transactionId = document.getElementById('editTransactionId').value;
        const formData = new FormData();

        formData.append('booking_id', document.getElementById('editBookingId').value);
        formData.append('user_id', document.getElementById('editUserId').value);
        formData.append('service_id', document.getElementById('editServiceId').value);
        formData.append('amount', document.getElementById('editAmount').value);
        formData.append('payment_method', document.getElementById('editPaymentMethod').value);
        formData.append('status', document.getElementById('editStatus').value);
        formData.append('transaction_type', document.getElementById('editTransactionType').value);
        formData.append('transaction_date', document.getElementById('editTransactionDate').value);
        formData.append('reference_code', document.getElementById('editReferenceCode').value);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        fetch(`/transactions/${transactionId}/update/`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error updating transaction: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error updating transaction:', error);
            alert('Error updating transaction');
        });
    });

    // Confirm Delete
    document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
        const transactionId = document.getElementById('deleteModal').getAttribute('data-transaction-id');

        fetch(`/transactions/${transactionId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error deleting transaction: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting transaction:', error);
            alert('Error deleting transaction');
        });
    });

    // Search functionality
    document.querySelector('.search-btn').addEventListener('click', function() {
        const searchTerm = document.getElementById('transactionSearch').value.trim();
        if (searchTerm) {
            window.location.href = `/transactions/?search=${encodeURIComponent(searchTerm)}`;
        } else {
            window.location.href = '/transactions/';
        }
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
});