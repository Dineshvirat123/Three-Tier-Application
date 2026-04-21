// ===== DevOps Portfolio JS =====

// Show alert messages
function showMessage(msg, type="success") {
    const box = document.createElement("div");
    box.innerText = msg;
    box.style.padding = "10px";
    box.style.margin = "10px";
    box.style.color = "white";
    box.style.backgroundColor = type === "success" ? "green" : "red";

    document.body.prepend(box);

    setTimeout(() => box.remove(), 3000);
}


// ===== Add Project without reload =====
const projectForm = document.querySelector("form[action='/add_project']");

if (projectForm) {
    projectForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const formData = new FormData(projectForm);

        fetch("/add_project", {
            method: "POST",
            body: formData
        })
        .then(res => {
            if (res.ok) {
                showMessage("Project added successfully 🚀");
                projectForm.reset();
                setTimeout(() => location.reload(), 1000);
            } else {
                showMessage("Error adding project ❌", "error");
            }
        })
        .catch(() => showMessage("Server error ❌", "error"));
    });
}


// ===== Highlight active menu =====
const links = document.querySelectorAll("a");

links.forEach(link => {
    if (link.href === window.location.href) {
        link.style.fontWeight = "bold";
    }
});


// ===== Confirm delete (future use) =====
function confirmDelete() {
    return confirm("Are you sure you want to delete?");
}


// ===== Show current time (optional DevOps touch) =====
function showTime() {
    const el = document.getElementById("time");
    if (el) {
        const now = new Date();
        el.innerText = "Time: " + now.toLocaleTimeString();
    }
}

setInterval(showTime, 1000);
