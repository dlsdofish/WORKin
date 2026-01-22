const token = localStorage.getItem("token");

// Load colleges into select
async function loadColleges() {
    const res = await fetch("http://localhost:8000/admin/colleges", {
        headers: {Authorization: `Bearer ${token}`}
    });
    const colleges = await res.json();
    const select = document.getElementById("collegeSelect");
    colleges.forEach(c => {
        const option = document.createElement("option");
        option.value = c.id;
        option.text = c.name;
        select.add(option);
    });
}
loadColleges();

// Add college
document.getElementById("addCollegeForm").addEventListener("submit", async (e)=>{
    e.preventDefault();
    const name = document.getElementById("collegeName").value;
    await fetch("http://localhost:8000/admin/college", {
        method: "POST",
        headers: {"Content-Type":"application/json", Authorization:`Bearer ${token}`},
        body: JSON.stringify({name})
    });
    alert("College Added!");
    loadColleges();
});

// View students
document.getElementById("viewStudentsBtn").addEventListener("click", async ()=>{
    const collegeId = document.getElementById("collegeSelect").value;
    const res = await fetch(`http://localhost:8000/reports/college/${collegeId}/students`, {
        headers: {Authorization: `Bearer ${token}`}
    });
    const students = await res.json();
    const ul = document.getElementById("studentsList");
    ul.innerHTML = "";
    students.forEach(s => {
        const li = document.createElement("li");
        li.textContent = `${s.id} - ${s.name}`;
        ul.appendChild(li);
    });
});
