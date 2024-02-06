window.onload = function() {
    var radios = document.querySelectorAll('input[type="radio"]');
    radios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            var newStatus = this.value; // Get the new status
            var taskId = this.getAttribute('data-task-id'); // Get the task id

            // Send the updated status to the server
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/update_status', true); // Replace with your actual endpoint
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function() {
                if (xhr.status === 200) {
                    // Redirect to the /mytasks page after successful 
                    window.location.reload(true);;
                } else {
                    console.error('Error updating status:', xhr.statusText);
                }
            };
            xhr.send('status=' + newStatus + '&task_id=' + taskId);
        });
    });
};

