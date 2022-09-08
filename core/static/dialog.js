
document.addEventListener('DOMContentLoaded', () => {
  
  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  (document.querySelectorAll('.modal-background, .modal-close') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });
});

;(function () {
    const modal = document.getElementById("modal")
  
    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "dialog") {
        modal.classList.add('is-active')
      }
    })
  
    htmx.on("htmx:beforeSwap", (e) => {
      // Empty response targeting #dialog => hide the modal
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        modal.classList.remove('is-active')
        e.detail.shouldSwap = false
      }
    })
    
  })()