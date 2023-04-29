function toggleButton(button) {
    button.classList.toggle("selected");
}

// Send data when user clicks "Save"
const saveBtn = document.querySelector('.save-btn');
const options = document.querySelectorAll('.options li');

saveBtn.addEventListener('click', (e) => {
  e.preventDefault();
  const selectedOptions = document.querySelectorAll('.selected');
  
  const selectedSlots = Array.from(selectedOptions).map((option) => {
    const parentUl = option.closest('.options');
    const day = parentUl.getAttribute('data-day');
    const start = option.getAttribute('data-start');
    const end = option.getAttribute('data-end');
    return { day, start, end };
  });
  
  const slotsInput = document.querySelector('#slots');
  slotsInput.value = JSON.stringify(selectedSlots);

  document.querySelector('#myForm').submit();
});







   
  
  
