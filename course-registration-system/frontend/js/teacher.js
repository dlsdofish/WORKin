const token = localStorage.getItem("token");
let studentsData = [];

// Load teacher classes
async function loadClasses() {
    const res = await fetch("http://localhost:8000/teacher/classes", {
        headers: { Authorization: `Bearer ${token}` }
    });
    const classes = await res.json();
    const classSelect = document.getElementById("classSelect");
    classSelect.innerHTML = "";
    classes.forEach(c => {
        const option = document.createElement("option");
        option.value = c.id;
        option.text = c.name;
        classSelect.add(option);
    });
}

document.getElementById("loadStudentsBtn").addEventListener("click", async () => {
    const class_id = document.getElementById("classSelect").value;
    const res = await fetch(`http://localhost:8000/teacher/classes/${class_id}/students`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    studentsData = await res.json();
    const ul = document.getElementById("studentsList");
    ul.innerHTML = "";
    studentsData.forEach(s => {
        const li = document.createElement("li");
        li.innerHTML = `<input type="checkbox" value="${s.id}"> ${s.name}`;
        ul.appendChild(li);
    });
});

// Submit attendance
document.getElementById("submitAttendanceBtn").addEventListener("click", async () => {
    const class_id = document.getElementById("classSelect").value;
    const student_ids_present = Array.from(document.querySelectorAll("#studentsList input:checked")).map(cb => cb.value);

    await fetch(`http://localhost:8000/teacher/classes/${class_id}/attendance`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify(student_ids_present)
    });
    alert("Attendance Submitted!");
});

loadClasses();