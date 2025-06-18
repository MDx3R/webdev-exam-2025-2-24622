function confirmDelete(recipeId, recipeTitle) {
  const modal = document.createElement("div");
  modal.className = "modal";
  modal.innerHTML = `
        <div class="modal-content">
            <h2>Delete Recipe</h2>
            <p>Are you sure you want to delete "${recipeTitle}"?</p>
            <button onclick="submitDelete(${recipeId})">Yes</button>
            <button onclick="closeModal()">No</button>
        </div>
    `;
  document.body.appendChild(modal);
}

function submitDelete(recipeId) {
  const form = document.querySelector(
    `form[action="/recipe/delete/${recipeId}"]`
  );
  form.submit();
}

function closeModal() {
  const modal = document.querySelector(".modal");
  if (modal) modal.remove();
}
