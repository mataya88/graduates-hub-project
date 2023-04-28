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


              const icons = timeSlot.querySelectorAll('i');
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
                    

                  if (occstart <= startTime && occend >= endTime) { // 
                    isOccupied = true;
                  }
                  
                });
                console.log(isOccupied)

          
                // Show or hide the icon based on the occupancy status
                if (isOccupied) {
                    
                  icon.style.display = 'none';
                } else {
                  icon.style.display = 'block';
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