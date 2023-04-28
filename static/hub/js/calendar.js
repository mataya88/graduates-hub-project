
/*const calendar = document.querySelector('.calendar');
const monthName = document.querySelector('.month-name');
const tbody = document.querySelector('tbody');

let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();
let day = date.getDate();

function getDaysInMonth(year, month) {
  return new Date(year, month + 1, 0).getDate();
}

function getFirstDayOfMonth(year, month) {
  return new Date(year, month, 1).getDay();
}

function getLastDayOfMonth(year, month) {
  return new Date(year, month + 1, 0).getDay();
}

// ...

function renderCalendar() {
    tbody.innerHTML = '';
  
    const daysInMonth = getDaysInMonth(year, month);
    const firstDayOfMonth = getFirstDayOfMonth(year, month);
    const lastDayOfMonth = getLastDayOfMonth(year, month);
  
    monthName.textContent = `${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}`;
  
    let dayCount = 1;
    let h4Count = 1; // initialize counter variable for h4 tags
    for (let i = 0; i < 6; i++) {
      const row = document.createElement('tr');
  
      for (let j = 0; j < 7; j++) {
        const cell = document.createElement('td');
        const dayNum = document.createElement('span'); // create span element
        dayNum.textContent = dayCount; // set the day number
  
        if (i === 0 && j < firstDayOfMonth) {
          dayNum.textContent = '';
        } else if (dayCount > daysInMonth) {
          dayNum.textContent = '';
        } else {
          if (dayCount === day && month === date.getMonth() && year === date.getFullYear()) {
            dayNum.classList.add('today');
          }
          dayCount++;
         

        }

        // add class to the span element for blue circle
        dayNum.classList.add('day-num');
  
        cell.appendChild(dayNum); // append the span element to the cell
        for (let k = 0; k < 4; k++) {
          const box = document.createElement('h5');
          box.classList.add('box');
          box.setAttribute('id', `box-${h4Count}`); // assign id to h4 tag
          cell.appendChild(box);
          h4Count++; // increment the counter variable
        }
        row.appendChild(cell);
      }
  
      tbody.appendChild(row);
  
      if (dayCount > daysInMonth) {
        break;
      }
    }
  
  }
  

calendar.querySelector('.prev').addEventListener('click', () => {
    month--;
    if (month < 0) {
      year--;
      month = 11;
    }
    renderCalendar();
  });

  calendar.querySelector('.next').addEventListener('click', () => {
    month++;
    if (month > 11) {
      year++;
      month = 0;
    }
    renderCalendar();
  });

  /*
function fillBoxesWithData(data) {
  const box1 = document.getElementById('box-1');
  const box2 = document.getElementById('box-2');
  const box3 = document.getElementById('box-3');
  const box4 = document.getElementById('box-4');

  box1.textContent = data.box1;
  box2.textContent = data.box2;
  box3.textContent = data.box3;
  box4.textContent = data.box4;
}

function getDataFromServer(year, month, day) {
  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        fillBoxesWithData(data);
      }
    }
  };
  xhr.open('GET', `/get_data?year=${year}&month=${month}&day=${day}`);
  xhr.send();
}

/*
  tbody.addEventListener('click', (event) => {
    const selectedCell = tbody.querySelector('.selected');
    if (selectedCell) {
      selectedCell.classList.remove('selected');
    }
    event.target.classList.add('selected');
    day = event.target.querySelector('.day-number').textContent;
  });*/
  /*
renderCalendar(); */

const calendar = document.querySelector('.calendar');
const monthName = document.querySelector('.month-name');
const tbody = document.querySelector('tbody');

let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();
let day = date.getDate();

function getDaysInMonth(year, month) {
  return new Date(year, month + 1, 0).getDate();
}

function getFirstDayOfMonth(year, month) {
  return new Date(year, month, 1).getDay();
}

function getLastDayOfMonth(year, month) {
  return new Date(year, month + 1, 0).getDay();
}

function renderCalendar(data) {
  tbody.innerHTML = '';

  const daysInMonth = getDaysInMonth(year, month);
  const firstDayOfMonth = getFirstDayOfMonth(year, month);
  const lastDayOfMonth = getLastDayOfMonth(year, month);

  monthName.textContent = `${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}`;

  let dayCount = 1;

  for (let i = 0; i < 6; i++) {
    const row = document.createElement('tr');

    for (let j = 0; j < 7; j++) {
      const cell = document.createElement('td');
      const dayNum = document.createElement('span');
      dayNum.textContent = dayCount;

      if (i === 0 && j < firstDayOfMonth) {
        dayNum.textContent = '';
      } else if (dayCount > daysInMonth) {
        dayNum.textContent = '';
      } else {
        if (dayCount === day && month === date.getMonth() && year === date.getFullYear()) {
          dayNum.classList.add('today');
        }
        dayCount++;

        dayNum.classList.add('day-num');
        cell.appendChild(dayNum);
        // find the corresponding data for this cell
        const cellData = data[dayCount - 2];
        if (cellData) {
          for (let k = 0; k < 4; k++) {
            const line = document.createElement('div');
            line.classList.add('box');
            const circle = document.createElement('div');
            circle.classList.add('red-circ');
      
            if (cellData[k]) {
              line.appendChild(circle);
              const text = document.createElement('span');
              text.textContent = cellData[k]; // set the h4 tag's value
              line.appendChild(text);
            }
            cell.appendChild(line);

          }
        }
      }

      
      row.appendChild(cell);
    }

    tbody.appendChild(row);

    if (dayCount > daysInMonth) {
      break;
    }
  }

}

// make an AJAX call to get the data
  fetch(`/hub/fetch-data/?year=${year}&month=${month}`)
  .then(response => response.json())
  .then(data => {
    renderCalendar(data);
  });

calendar.querySelector('.prev').addEventListener('click', () => {
  month--;
  if (month < 0) {
    year--;
    month = 11;
  }
  fetch(`/hub/fetch-data/?year=${year}&month=${month}`)
    .then(response => response.json())
    .then(data => {
      renderCalendar(data);
      
    });
});

calendar.querySelector('.next').addEventListener('click', () => {
  month++;
  if (month > 11) {
    year++;
    month = 0;
  }
  fetch(`/hub/fetch-data/?year=${year}&month=${month}`)
    .then(response => response.json())
    .then(data => {
      renderCalendar(data);
    });
 

});



