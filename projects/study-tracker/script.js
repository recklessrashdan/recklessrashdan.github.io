const taskForm = document.getElementById("taskForm");
const taskInput = document.getElementById("taskInput");
const taskList = document.getElementById("taskList");
const clearDone = document.getElementById("clearDone");
const storageKey = "study-tracker-tasks";

let tasks = JSON.parse(localStorage.getItem(storageKey) || "[]");

function saveTasks() {
  localStorage.setItem(storageKey, JSON.stringify(tasks));
}

function renderTasks() {
  taskList.innerHTML = "";

  tasks.forEach((task) => {
    const li = document.createElement("li");
    if (task.done) {
      li.classList.add("done");
    }

    const label = document.createElement("span");
    label.textContent = task.text;

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.textContent = task.done ? "Undo" : "Done";
    toggleBtn.addEventListener("click", () => {
      task.done = !task.done;
      saveTasks();
      renderTasks();
    });

    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.textContent = "Delete";
    deleteBtn.addEventListener("click", () => {
      tasks = tasks.filter((t) => t.id !== task.id);
      saveTasks();
      renderTasks();
    });

    actions.append(toggleBtn, deleteBtn);
    li.append(label, actions);
    taskList.append(li);
  });
}

taskForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = taskInput.value.trim();
  if (!text) {
    return;
  }

  tasks.push({ id: Date.now(), text, done: false });
  saveTasks();
  renderTasks();
  taskInput.value = "";
  taskInput.focus();
});

clearDone.addEventListener("click", () => {
  tasks = tasks.filter((task) => !task.done);
  saveTasks();
  renderTasks();
});

renderTasks();
