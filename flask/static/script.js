document.addEventListener("DOMContentLoaded", function() {
    const dashboard = document.querySelector('.dashboard')
    const profileBtn = document.querySelector('.profile');
    const profileSection = document.querySelector('.profileSection');
    const updateBtn = document.querySelector('.update');
    const updateSection = document.querySelector('.updateSection');
    const tHistoryBtn = document.querySelector('.tHistory');
    const thistorySection = document.querySelector('.tHistorySection');
    const alert = document.querySelectorAll('.alert');
    const ham = document.querySelector('.ham');
    const sidebar = document.querySelector('.sidebar');
    
    if (profileBtn){
      profileBtn.addEventListener('click', function() {
        profileBtn.classList.add("activedash")
        updateBtn.classList.remove("activedash")
        tHistoryBtn.classList.remove("activedash")
        profileSection.classList.remove("sectNone")
        updateSection.classList.add("sectNone")
        thistorySection.classList.add("sectNone")
      });
    }
  
    if(updateBtn){
      updateBtn.addEventListener('click', function() {
        updateBtn.classList.add("activedash")
        profileBtn.classList.remove("activedash")
        tHistoryBtn.classList.remove("activedash")
        updateSection.classList.remove("sectNone")
        profileSection.classList.add("sectNone")
        thistorySection.classList.add("sectNone")
      });
    }
  
    if (tHistoryBtn){
      tHistoryBtn.addEventListener('click', function() {
        tHistoryBtn.classList.add("activedash")
        profileBtn.classList.remove("activedash")
        updateBtn.classList.remove("activedash")
        updateSection.classList.add("sectNone")
        profileSection.classList.add("sectNone")
        thistorySection.classList.remove("sectNone")
      }); 
    }
    alert.forEach((alt)=>{
      setTimeout(()=>{
        alt.classList.add("altNone")
      }, 3000)
    })
    ham.addEventListener('click', function(){
      sidebar.classList.toggle("none")
      if(sidebar.classList.contains("none")){
        ham.innerHTML = '<img src="{{ url_for(\'static\', filename=\'images/hamburger-menu.png\') }}" />';

        }
      else{
        ham.innerHTML = "&times";
      }
    })
  });