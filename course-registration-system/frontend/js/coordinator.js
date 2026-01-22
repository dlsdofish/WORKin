const token = localStorage.getItem("token");

// Load colleges
async function loadColleges() {
    const res = await fetch("http://localhost:8000/admin/colleges", {
        headers: { Authorization: `Bearer ${token}` }
    });
    const colleges = await res.json();
    const collegeSelect = document.getElementById("collegeSelect");
    colleges.forEach(c => {
        const option = document.createElement("option");
        option.value = c.id;
        option.text = c.name;
        collegeSelect.add(option);
    });
}

// Load teachers
async function loadTeachers() {
    const res = await fetch("http://localhost:8000/admin/teachers", {
        headers: { Authorization: `Bearer ${token}` }
    });
    const teachers = await res.json();
    const teacherSelect = document.getElementById("teacherSelect");
    teachers.forEach(t => {
        const option = document.createElement("option");
        option.value = t.id;
        option.text = t.name;
        teacherSelect.add(option);
    });
}

// Create class
document.getElementById("createClassForm").addEventListener("submit", async e => {
    e.preventDefault();
    const name = document.getElementById("className").value;
    const college_id = document.getElementById("collegeSelect").value;
    const teacher_id = document.getElementById("teacherSelect").value;

    await fetch("http://localhost:8000/coordinator/classes", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ name, college_id, teacher_id })
    });
    alert("Class Created!");
    loadClasses();
});

// Load classes
async function loadClasses() {
    const res = await fetch("http://localhost:8000/coordinator/classes", {
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

// Load students (for selected college)
document.getElementById("collegeSelect").addEventListener("change", async () => {
    const collegeId = document.getElementById("collegeSelect").value;
    const res = await fetch(`http://localhost:8000/reports/college/${collegeId}/students`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    const students = await res.json();
    const studentSelect = document.getElementById("studentSelect");
    studentSelect.innerHTML = "";
    students.forEach(s => {
        const option = document.createElement("option");
        option.value = s.id;
        option.text = s.name;
        studentSelect.add(option);
    });
});

// Assign students to class
document.getElementById("assignStudentsBtn").addEventListener("click", async () => {
    const class_id = document.getElementById("classSelect").value;
    const student_ids = Array.from(document.getElementById("studentSelect").selectedOptions).map(o => o.value);

    await fetch(`http://localhost:8000/coordinator/classes/${class_id}/assign-students`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ student_ids })
    });
    alert("Students Assigned!");
});

loadColleges();
loadTeachers();
loadClasses();
