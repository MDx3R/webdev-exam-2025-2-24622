function showDeleteModal(recipeTitle, url) {
  const modal = new bootstrap.Modal(document.getElementById("deleteModal"));
  const body = document.getElementById("deleteModalBody");
  const form = document.getElementById("deleteModalForm");

  body.textContent = `Вы уверены, что хотите удалить рецепт "${recipeTitle}"?`;
  form.action = url;

  modal.show();
}

window.addEventListener("DOMContentLoaded", () => {
  const gallery = document.getElementById("recipe-images");
  if (gallery) {
    new Viewer(gallery);
  }
  const reviewText = document.getElementById("review-text");
  if (reviewText) {
    new EasyMDE({
      element: reviewText,
      forceSync: true,
    });
  }
});
