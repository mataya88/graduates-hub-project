        const today = new Date();
        let currentDate = today;

        function updateDays() {
        const daysContainer = document.querySelector(".days");
        daysContainer.innerHTML = "";
        
        for (let i = 0; i < 7; i++) {
            const day = new Date(currentDate.getTime() + i * 24 * 60 * 60 * 1000);
            const dayButton = document.createElement("button");
            dayButton.addEventListener("click", selectDay);
            dayButton.innerHTML = `
            <h3>${getMonthName(day.getMonth())}</h3>
            <h3>${day.getDate()}</h3>
            `;
            dayButton.setAttribute('data-day-of-week', day.getDay());
            dayButton.setAttribute('data-month', day.getMonth()+1);
            dayButton.setAttribute('data-date', day.getDate());
            if (day.toDateString() === today.toDateString()) {
            //dayButton.classList.add("today");
            dayButton.classList.add("selected")
            fetchData(dayButton.dataset.dayOfWeek)
            }
            daysContainer.appendChild(dayButton);
        }
        }

        function getMonthName(monthIndex) {
        const monthNames = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ];
        return monthNames[monthIndex];
        }
        
        function selectDay(event) {
        const selectedButton = event.currentTarget;
        const allButtons = document.querySelectorAll(".days button");
        
        // Remove the "today" class from all buttons
        //allButtons.forEach(button => button.classList.remove('today'));
        
        // Remove the "selected" class from all buttons
        allButtons.forEach(button => button.classList.remove('selected'));
        
        // Add the "selected" class only to the clicked button
        selectedButton.classList.add("selected");

        const dayOfWeek = selectedButton.dataset.dayOfWeek;
        fetchData(dayOfWeek)
        }


        function fetchData(dayOfWeek) {
        fetch(`/hub/fetch-occupancies/?dayOfWeek=${dayOfWeek}`)
        .then(response => response.json())
        .then(data => {

        processData(data);
        });
        }



        function nextDays() {
        currentDate = new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000);
        updateDays();
        }

        function previousDays() {
        const minimumDate = new Date();
        minimumDate.setHours(0, 0, 0, 0);
        minimumDate.setDate(minimumDate.getDate() - 6); // Set the minimum date to 6 days ago
        const previousDate = new Date(currentDate.getTime() - 7 * 24 * 60 * 60 * 1000);
        if (previousDate >= minimumDate) {
            currentDate = previousDate;
            updateDays();
        }
        }

        updateDays();


        
function processData(data) {
    const timeSlots = document.querySelectorAll('.time-slot');
    console.log('timeSlots:', timeSlots);


    // Iterate through each time slot
    timeSlots.forEach(timeSlot => {
        const startTime = parseInt(timeSlot.dataset.startTime.split(':').join('')+'00');
        const endTime = parseInt(timeSlot.dataset.endTime.split(':').join('')+'00');

        console.log(startTime);
        console.log(endTime);


        const icons = timeSlot.querySelectorAll('.icon');
        console.log('icons:', icons);

        // Iterate through each icon for this time slot
        icons.forEach((icon, index) => {
        // Assume that the member is not occupied
        let isOccupied = false;

        // Check if the member is occupied during this time slot
        const memberOccupancy = data[index];
        console.log('memberOccupancy:', memberOccupancy);
        
        memberOccupancy.forEach(occupancy => {
            const occstart = parseInt(occupancy["start"].split(':').join(''));
            const occend = parseInt(occupancy["end"].split(':').join(''));
            

            if (occstart < endTime && occend > startTime) { // 
            isOccupied = true;
            }
            
        });
        console.log(isOccupied)


        // Show or hide the icon based on the occupancy status
        if (isOccupied) {
            timeSlot.setAttribute(`data-member${index+1}`, 'no');
            icon.style.opacity = '0';
        } else {
            timeSlot.setAttribute(`data-member${index+1}`, 'yes');
            icon.style.opacity = '1';
        }
        });
    });
}

          

// get all the button elements
var btns = document.querySelectorAll('.time-slot .btn');

// add event listener to each button
btns.forEach(function(btn) {
btn.addEventListener('click', function() {
    // remove the 'active' class from all buttons
    btns.forEach(function(b) {
    b.classList.remove('active');
    });
    // add the 'active' class to the clicked button
    btn.classList.add('active');
});
});

const members = document.querySelectorAll('.member');
members.forEach(member => {
const name = member.querySelector('h4').textContent;
const initials = name.split(' ').map(word => word.charAt(0)).join('');
member.querySelector('h4').textContent = initials;
});

const available_members = document.querySelectorAll('.available-list');
available_members.forEach(list => {
// Select all the li elements in the available-list
const listItems = list.querySelectorAll('.available-list li');
    
// Loop through each li element
listItems.forEach((item) => {
    // Split the name into words
    const words = item.textContent.trim().split(' ');
    // Get the first letter of each word and combine them
    const initials = words.map((word) => word.charAt(0)).join('');
    // Set the content of the li element to the initials
    item.textContent = initials;
});
});

const icons = document.querySelectorAll('.icon');
icons.forEach(icon => {
// Select all the li elements in the available-list
    const name = icon.querySelector('h6');

    // Split the name into words
    const words = name.textContent.trim().split(' ');
    // Get the first letter of each word and combine them
    const initials = words.map((word) => word.charAt(0)).join('');
    // Set the content of the li element to the initials
    name.textContent = initials;

});



// Get a reference to the "Create Meeting" button
const createButton = document.querySelector('.finalsubmit');

// Attach a click event listener to the button
createButton.addEventListener('click', (event) => {
    event.preventDefault();
  // Find the selected button
  const selectedButton = document.querySelector('.active');
  const selectedDay  = document.querySelector('.selected')

  // Check if a selected button was found
  if (selectedButton) {
    // Get the parent div element of the selected button
    const parentDiv = selectedButton.closest('.time-slot');
    const meeting_name = document.getElementById("name").value;
    const meeting_desc = document.querySelector("textarea").value;

    // Extract the data attributes from the parent div element
    const dataAttributes = [
    meeting_name, meeting_desc,
    selectedDay.getAttribute('data-month'),
    selectedDay.getAttribute('data-date'),
    parentDiv.getAttribute('data-start-time'),
    parentDiv.getAttribute('data-end-time'),
    parentDiv.getAttribute('data-member1'),
    parentDiv.getAttribute('data-member2'),
    parentDiv.getAttribute('data-member3'),
    parentDiv.getAttribute('data-member4')
    ];

    console.log(dataAttributes)

    const formInput = document.querySelector('#meet_data');
    formInput.value = dataAttributes;

    document.querySelector('#myForm').submit();

  }
});


// Get the modal element
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myButton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    // Check if there is an element with class .active
    var active = document.querySelector(".active");
    if (active) {
      modal.style.display = "block";
    } else {
      // Display the "select a slot" message
      message.style.display = "flex";
      // Hide the message after 3 seconds
      setTimeout(function() {
        message.style.display = "none";
      }, 1800);
    }
  }
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
