document.addEventListener("DOMContentLoaded", function () {
  console.log("JS file is running");

  const searchForm = document.querySelector("[data-task-search-form]");
  const searchInput = document.querySelector("[data-task-search-input]");

  console.log("Search form:", searchForm);
  console.log("Search input:", searchInput);

  if (!searchForm || !searchInput) {
    console.log("STOP: form or input not found");
    return;
  }

  console.log("Event listener is being attached");
  searchForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const query = searchInput.value.trim();

    let apiUrl = "/api/tasks/";

    if (query) {
      apiUrl = `/api/tasks/?search=${encodeURIComponent(query)}`;
    }

    console.log("Submit event captured");
    console.log("Search query:", query);
    console.log("API URL:", apiUrl);
  });
});
