function toggleButton(button) {
    button.classList.toggle("selected");
}

// JavaScript code
const saveBtn = document.querySelector('.save-btn');
const options = document.querySelectorAll('.options li');

saveBtn.addEventListener('click', (e) => {
  e.preventDefault();
  const selectedOptions = document.querySelectorAll('.selected');
  const selectedSlots = Array.from(selectedOptions).map((option) => {
    return option.getAttribute('data-slot');
  });
  
  const slotsInput = document.querySelector('#slots');
  slotsInput.value = selectedSlots.join(',');
  document.querySelector('#myForm').submit();
});





   
  
  
