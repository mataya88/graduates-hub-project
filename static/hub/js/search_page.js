		// Get the dropdown button and content
		const dropdownBtn = document.querySelector(".dropdown button");
		const dropdownContent = document.querySelector(".dropdown-content");

		
		// Add a click event listener to the dropdown button
		dropdownBtn.addEventListener("click", function() {
		// Toggle the display of the dropdown content
		dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
		});

		// Add a click event listener to the dropdown options
		const dropdownOptions = dropdownContent.querySelectorAll("a");
		dropdownOptions.forEach(function(option) {
		option.addEventListener("click", function(e) {
			e.preventDefault();
			// Change the button text to the selected option

			const btnText = dropdownBtn.querySelector(".btn-text");
    		btnText.textContent = option.textContent;
		});
		});

		// Add a click event listener to the document object
		document.addEventListener("click", function(e) {
			// Check if the target of the click event is inside the dropdown or not
			if (!dropdownBtn.contains(e.target) && !dropdownContent.contains(e.target)) {
				// If the target is outside the dropdown, hide the dropdown content
				dropdownContent.style.display = "none";
			}
			});
	
		const options = document.querySelectorAll(".filter a");
		const results = document.querySelectorAll(".result");

		
		//const filterInput = document.querySelector('input[name="filter"]');

		options.forEach(function(option) {
		option.addEventListener("click", function(e) {
			e.preventDefault();
			options.forEach(function(otherOption) {
			otherOption.classList.remove("active");
			});
			this.classList.add("active");

			const filterType = option.textContent.toLowerCase();
			results.forEach(function(result) {
				if (filterType === "all" || result.id === filterType) {
				  result.style.display = "block";
				} else {
				  result.style.display = "none";
				}
			  });
			


		});
		});

		
		// get search submit button
		const searchButton = document.querySelector(".submit-button");
		const searchForm = document.getElementById('search-form');

		searchButton.addEventListener("click", function(e){
			e.preventDefault();
			searchForm.submit();

		});
		