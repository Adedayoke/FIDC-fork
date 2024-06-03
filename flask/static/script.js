document.addEventListener("DOMContentLoaded", function() {
    const dashboard = document.querySelector('.dashboard')
    const profileBtn = dashboard.querySelector('.profile');
    const profileSection = dashboard.querySelector('.profileSection');
    const updateBtn = dashboard.querySelector('.update');
    const updateSection = dashboard.querySelector('.updateSection');
    const tHistoryBtn = dashboard.querySelector('.tHistory');
    const thistorySection = dashboard.querySelector('.tHistorySection');
    
    profileBtn.addEventListener('click', function() {
      console.log("Profile button clicked");
      profileBtn.classList.add("activedash")
      updateBtn.classList.remove("activedash")
      tHistoryBtn.classList.remove("activedash")
      profileSection.classList.remove("sectNone")
      updateSection.classList.add("sectNone")
      thistorySection.classList.add("sectNone")
    });
  
    updateBtn.addEventListener('click', function() {
      console.log("Update button clicked");
      updateBtn.classList.add("activedash")
      profileBtn.classList.remove("activedash")
      tHistoryBtn.classList.remove("activedash")
      updateSection.classList.remove("sectNone")
      profileSection.classList.add("sectNone")
      thistorySection.classList.add("sectNone")
    });
  
    tHistoryBtn.addEventListener('click', function() {
      console.log("Transaction history button clicked");
      tHistoryBtn.classList.add("activedash")
      profileBtn.classList.remove("activedash")
      updateBtn.classList.remove("activedash")

      updateSection.classList.add("sectNone")
      profileSection.classList.add("sectNone")
      thistorySection.classList.remove("sectNone")
    }); 
  });