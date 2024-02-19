





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
                    window.location.reload(true);
                } else {
                    console.error('Error updating status:', xhr.statusText);
                }
            };
            xhr.send('status=' + newStatus + '&task_id=' + taskId);
        });
    });





    // Get the popup
var btns = document.querySelectorAll(".form");

// Get the <a> element that opens the popu

// Get the <span> element that closes the popup
var span = document.getElementsByClassName("close")[0];

var popup = document.getElementById("popupForm");
// When the user clicks on <span> (x), close the popup
span.onclick = function() {
    popup.style.display = "none";
}

// When the user clicks anywhere outside of the popup, close it
window.onclick = function(event) {
    if (event.target == popup) {
        popup.style.display = "none";
    }
}

btns.forEach(function(btn) {
    btn.onclick = function() {
        popup.style.display = "block";
        var link_id = btn.getAttribute('name-task-id') ;
        var form = document.getElementById('updateForm')
        form.setAttribute("action", link_id);
    }
});

};

