document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.querySelector("[data-task-search-form]");
  const searchInput = document.querySelector("[data-task-search-input]");
  const resultsContainer = document.querySelector("[data-task-results]");
  const searchStatus = document.querySelector("[data-search-status]");

  if (!searchForm || !searchInput || !resultsContainer) {
    return;
  }

  searchForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const query = searchInput.value.trim();

    loadTasks(query, resultsContainer, searchStatus);
  });

  const initialQuery = searchInput.value.trim();

  loadTasks(initialQuery, resultsContainer, searchStatus);
});

async function loadTasks(query, resultsContainer, searchStatus) {
  let apiUrl = "/api/tasks/";

  if (query) {
    apiUrl = `/api/tasks/?q=${encodeURIComponent(query)}`;
  }

  showLoading(resultsContainer);
  setStatus(searchStatus, "Loading tasks from API...");

  try {
    const response = await fetch(apiUrl, {
      method: "GET",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("API request failed.");
    }

    const data = await response.json();
    const tasks = Array.isArray(data) ? data : data.results || [];

    renderTasks(tasks, resultsContainer);

    if (query) {
      setStatus(searchStatus, `Found ${tasks.length} task(s) for "${query}".`);
    } else {
      setStatus(searchStatus, `Showing all tasks. Total: ${tasks.length}.`);
    }

    const pageUrl = query
      ? `/tasks/?q=${encodeURIComponent(query)}`
      : "/tasks/";

    window.history.replaceState(null, "", pageUrl);
  } catch (error) {
    resultsContainer.innerHTML = `
      <div class="alert alert-danger">
        Could not load tasks from the API.
      </div>
    `;

    setStatus(searchStatus, "");
  }
}

function showLoading(container) {
  container.innerHTML = `
    <div class="text-center py-4">
      <div class="spinner-border" role="status" aria-hidden="true"></div>
      <div class="mt-2 text-muted">
        Loading tasks...
      </div>
    </div>
  `;
}

function renderTasks(tasks, container) {
  container.innerHTML = "";

  if (tasks.length === 0) {
    container.innerHTML = `
      <div class="alert alert-info">
        No tasks found.
      </div>
    `;
    return;
  }

  const list = document.createElement("div");
  list.className = "list-group";

  tasks.forEach(function (task) {
    const link = document.createElement("a");
    link.href = `/tasks/${task.id}/`;
    link.className = "list-group-item list-group-item-action";

    const header = document.createElement("div");
    header.className = "d-flex justify-content-between align-items-center";

    const title = document.createElement("h5");
    title.className = "mb-1";
    title.textContent = task.title;

    const badge = document.createElement("span");
    badge.className = "badge bg-secondary";
    badge.textContent = task.status;

    const owner = document.createElement("small");
    owner.textContent = `Owner: ${task.owner_username || "unknown"}`;

    header.appendChild(title);
    header.appendChild(badge);

    link.appendChild(header);
    link.appendChild(owner);

    list.appendChild(link);
  });

  container.appendChild(list);
}

function setStatus(statusElement, message) {
  if (!statusElement) {
    return;
  }

  statusElement.textContent = message;
}