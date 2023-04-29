
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
            const box = document.createElement('div');
            box.classList.add('box');
            const circle = document.createElement('div');
            circle.classList.add('red-circ');
      
            if (cellData[k]) {
              box.appendChild(circle);
              const text = document.createElement('span');
              text.textContent = cellData[k]; // set the span tag's value
              box.appendChild(text);
            }
            cell.appendChild(box);

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