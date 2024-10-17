// router.js

function navigateTo(page) {
  const contentArea = document.getElementById("right-container");

  fetch(page + ".html")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.text();
    })
    .then((data) => {
      contentArea.innerHTML = data;
      // Update the URL with the hash
      window.location.hash = page; // Changes the URL to include the hash
    })
    .catch((error) => console.log("Error loading page: ", error));
}

// Load content based on the current URL hash
function loadContentFromHash() {
  const hash = window.location.hash.substring(1); // Remove the '#'
  if (hash) {
    navigateTo(hash);
  } else {
    navigateTo("circular"); // Default to Circular tab
  }
}

// Handle back/forward navigation
window.addEventListener("popstate", loadContentFromHash);

// Load content on initial page load
document.addEventListener("DOMContentLoaded", loadContentFromHash);
